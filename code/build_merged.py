"""The merged long table: every study in one file, one row per variant x condition, on GPCRdb numbering.

Writes merged/gpcr_dms_long.parquet, merged/gpcr_dms_long.csv.gz and merged/conditions.csv.

Published scores are kept untouched in `score`. Two derived columns make conditions comparable:
  score_norm  WT-like = 0, null-like = -1. Only where both anchors exist and are well separated (see anchors()).
  score_rank  percentile of `score` within the condition (0-1). Defined for every scored row.
"""
import re
import numpy as np
import pandas as pd
from licenses import L
from paths import GPCRDB_TABLE

MIN_NULL = 5        # nonsense (or frameshift) variants needed to place the null anchor
MIN_SYN = 5         # synonymous variants needed to use their median as the WT anchor
MIN_SEP = 1.0       # (WT anchor - null anchor) in units of the null variants' robust SD

ASSAY_CLASS = {
    "expression": ["surface expression", "surface elisa", "surface trafficking", "membrane proximity", "abundance",
                   "surface immunostaining (individual variants)"],
    "expression ratio": ["retinal sensitivity", "temperature sensitivity"],
    "signaling": ["camp", "cre ", "reporter", "nb80", "arrestin", "bret", "trupath", "validation,"],
    "binding": ["binding"],
    "self-association": ["bific", "bifc"],
    "cell phenotype": ["migration", "proliferation"],
}
GROUP = ["study_id", "assay", "condition"]


def assay_class(a):
    a = a.lower()
    for cls in ("expression ratio", "binding", "self-association", "cell phenotype", "signaling", "expression"):
        if any(k in a for k in ASSAY_CLASS[cls]):
            return cls
    raise ValueError(f"no assay_class for {a!r}")


def short_license(s):
    """'CC BY 4.0 (repository data licence); MaveDB ...' -> 'CC BY 4.0'."""
    return re.split(r"\s*\(|;|\.\s|,\s", s)[0].strip()


def robust_sd(x):
    x = x.dropna()
    return 1.4826 * (x - x.median()).abs().median() if len(x) else np.nan


def anchors(g):
    """WT-like and null-like reference values for one study x assay x condition."""
    s = g.score
    syn = s[g.mut_class.eq("synonymous")]
    wtref = s[g.mut_class.eq("wt_reference") | g.variant.eq("p.=")]
    st = g.score_type.iloc[0]
    if len(wtref):
        wt, wt_from = wtref.median(), f"WT reference row (n={len(wtref)})"
    elif len(syn) >= MIN_SYN:
        wt, wt_from = syn.median(), f"synonymous median (n={len(syn)})"
    elif st.startswith("log2 fold change vs WT"):
        wt, wt_from = 0.0, "0 (score is log2 fold change vs WT)"
    else:
        wt, wt_from = np.nan, "none"
    for cls in ("nonsense", "frameshift"):
        nul = s[g.mut_class.eq(cls)]
        if len(nul) >= MIN_NULL:
            null, null_from, null_sd = nul.median(), f"{cls} median (n={len(nul)})", robust_sd(nul)
            break
    else:
        null, null_from, null_sd = np.nan, "none", np.nan
    sep = abs(wt - null) / null_sd if null_sd and null_sd > 0 else np.nan
    if np.isnan(wt) or np.isnan(null):
        method = "not normalised: no " + ("WT" if np.isnan(wt) else "null") + " anchor"
    elif null >= wt:
        method = "not normalised: null anchor is not below WT (readout does not depend on the receptor)"
    elif not sep >= MIN_SEP:
        method = f"not normalised: WT and null anchors not separated ({sep:.1f} SD < {MIN_SEP:g})"
    else:
        method = "WT = 0, null = -1"
    return pd.Series(dict(rows=len(g), n_synonymous=len(syn), n_null=int(g.mut_class.isin(["nonsense", "frameshift"]).sum()),
                          wt_anchor=wt, wt_anchor_from=wt_from, null_anchor=null, null_anchor_from=null_from,
                          separation_sd=sep, norm_method=method, score_type=st))


def build(master):
    m = master.copy()
    # ---- GPCRdb numbering, joined on UniProt + position
    g = pd.read_csv(GPCRDB_TABLE, dtype={"bw": str, "gpcrdb_generic": str, "gpcrdb_x": str})
    g = g[["uniprot", "pos", "gpcrdb_generic", "gpcrdb_x", "bw", "segment", "gpcrdb_aa"]]
    m = m.merge(g, on=["uniprot", "pos"], how="left", validate="many_to_one")
    wt = m.wt_aa.astype("string")
    m["wt_matches_gpcrdb"] = (wt == m.gpcrdb_aa.astype("string")).where(wt.notna() & m.gpcrdb_aa.notna())
    # ---- assay class
    m["assay_class"] = m.assay.map({a: assay_class(a) for a in m.assay.unique()})
    # ---- normalisation anchors per condition
    cond = m.groupby(GROUP, sort=False).apply(anchors, include_groups=False).reset_index()
    m = m.merge(cond[GROUP + ["wt_anchor", "null_anchor", "norm_method"]], on=GROUP, how="left", validate="many_to_one")
    ok = m.norm_method.eq("WT = 0, null = -1")
    m["score_norm"] = np.where(ok, (m.score - m.wt_anchor) / (m.wt_anchor - m.null_anchor), np.nan)
    scored = m.score.notna() & m.mut_class.ne("wt_reference")
    m["score_rank"] = m.score.where(scored).groupby([m[c] for c in GROUP]).rank(pct=True)
    m = m.drop(columns=["wt_anchor", "null_anchor"])
    # ---- license, so non-commercial data can be filtered out in one step (full text: licenses.csv)
    m["data_license"] = m.study_id.map({k: short_license(v["data_license"]) for k, v in L.items()})
    m["redistribution_status"] = m.study_id.map({k: v["status"] for k, v in L.items()})
    assert m.data_license.notna().all()
    # no-derivatives licences: carry the published score, but share no rescaled version of it
    nd = m.data_license.str.contains("-ND", regex=False)
    m.loc[nd, ["score_norm", "score_rank"]] = np.nan
    m.loc[nd, "norm_method"] = "not normalised: data license (CC BY-NC-ND) does not allow sharing adapted values"
    cond = cond.merge(m[GROUP + ["norm_method"]].drop_duplicates(GROUP), on=GROUP, suffixes=("_anchors", ""))
    cond = cond.drop(columns="norm_method_anchors")
    order = ["study_id", "receptor", "gene", "uniprot", "study", "year", "journal", "doi", "scan_type",
             "assay_class", "assay", "condition", "ligand", "ligand_conc_M",
             "variant", "pos", "wt_aa", "mut_aa", "mut_class",
             "gpcrdb_generic", "gpcrdb_x", "bw", "segment", "gpcrdb_aa", "wt_matches_gpcrdb",
             "score", "score_se", "score_type", "score_norm", "score_rank", "norm_method",
             "ec50_log", "ec50_log_se", "emax", "emax_se",
             "in_mavedb", "data_license", "redistribution_status", "source_file"]
    assert sorted(order) == sorted(m.columns), set(order) ^ set(m.columns)
    cond = cond.merge(m.groupby(GROUP).agg(assay_class=("assay_class", "first"),
                                           n_score_norm=("score_norm", lambda x: int(x.notna().sum()))).reset_index(), on=GROUP)
    return m[order], cond


COLUMN_DOC = [
    ("study_id", "`GENE_FirstauthorYear`, the study folder this row comes from"),
    ("receptor, gene, uniprot", "receptor name, HGNC gene, human UniProt accession"),
    ("study, year, journal, doi, scan_type", "source paper; scan_type is DMS / DMS (TM2 + TM7) / alanine scan / targeted panel"),
    ("assay_class", "expression, expression ratio, signaling, binding, self-association or cell phenotype"),
    ("assay", "what was read out (surface expression, cAMP reporter, Nb80 recruitment, BRET CRC, ...)"),
    ("condition", "the specific sort or treatment; a dose series has one condition per concentration. "
                  "Names repeat across assays (MC4R `untreated` is in both the Gs and Gq screens), so group on assay + condition"),
    ("ligand, ligand_conc_M", "ligand and molar concentration, where there is one"),
    ("variant", "identifier as given in the source (HGVS where the source used it); joins to `<study>/tables/`"),
    ("pos, wt_aa, mut_aa", "position in the human receptor, WT residue, substituted residue (`*` stop, `del`, `ins`, `fs`)"),
    ("mut_class", "missense / synonymous / nonsense / deletion / insertion / frameshift / wt_reference"),
    ("gpcrdb_generic, gpcrdb_x, bw, segment, gpcrdb_aa", "GPCRdb numbering for `pos`. Match on `gpcrdb_x` (e.g. `3x50`) to compare receptors"),
    ("wt_matches_gpcrdb", "whether the study's WT residue agrees with GPCRdb (empty where either is missing)"),
    ("score, score_se", "the published score and its uncertainty, unchanged (SE, SEM or SD; see score_type)"),
    ("score_type", "units and normalisation of `score` in that study"),
    ("score_norm", "`score` rescaled so the condition's WT-like anchor = 0 and null-like anchor = -1. Empty where the condition has no usable anchors"),
    ("score_rank", "percentile of `score` among all scored variants in the same study, assay and condition (0 to 1)"),
    ("norm_method", "how `score_norm` was set for this condition, or why it was not"),
    ("ec50_log, ec50_log_se, emax, emax_se", "concentration-response fit parameters (alanine scans); `score` holds log(Emax/EC50) there"),
    ("in_mavedb", "whether the data are in MaveDB, with URN"),
    ("data_license, redistribution_status", "the data's own license (full statement in `../licenses.csv`) and its status in `../LICENSE.md`"),
    ("source_file", "the file the numbers came from (in `<study>/source/`)"),
]


def readme(m, cond):
    ok = cond.norm_method.eq("WT = 0, null = -1")
    per = m.groupby("study_id").agg(receptor=("receptor", "first"), rows=("score", "size"))
    per = per.join(cond.assign(ok=ok).groupby("study_id").agg(conditions=("ok", "size"), normed=("ok", "sum")))
    why = (cond[~ok].groupby("study_id").norm_method
           .agg(lambda x: "; ".join(sorted({s.replace("not normalised: ", "").split(" (")[0] for s in x}))))
    rows = "\n".join(f"| `{sid}` | {r.receptor} | {r.rows:,} | {r.normed} of {r.conditions} | {why.get(sid, '')} |"
                     for sid, r in per.iterrows())
    cols = "\n".join(f"| `{'`, `'.join(c.split(', '))}` | {d} |" for c, d in COLUMN_DOC)
    return f"""# Merged long table

`gpcr_dms_long.parquet` and `gpcr_dms_long.csv.gz` hold the same table: **{len(m):,} rows from {m.study_id.nunique()} study
folders, {m.uniprot.nunique()} receptors, {len(cond)} conditions**. One row is one variant scored in one condition. Every
row carries GPCRdb numbering, so positions can be lined up across receptors on `gpcrdb_x`.

Generated by `code/build.py` from the files in each `<study>/source/`. Do not edit by hand.

```python
import pandas as pd
d = pd.read_parquet("merged/gpcr_dms_long.parquet")        # or read_csv("merged/gpcr_dms_long.csv.gz")
d = d[d.redistribution_status.eq("clear")]                 # drop the non-commercial and cite-only datasets
tm3 = d[d.gpcrdb_x.eq("3x50") & d.assay_class.eq("expression")]
```

## Columns

| column | meaning |
|---|---|
{cols}

## Scores are not on a common scale

`score` is the number as published, in the study's own units: Lilace and Rosace posterior effects, Enrich2 scores,
log2 enrichment ratios, log2 fold change vs WT, immunostaining ratios, CRC parameters. Two derived columns help put
conditions side by side:

- **`score_norm`** sets the WT-like anchor to 0 and the null-like anchor to -1, within each study x assay x condition.
  - WT anchor, first available of: a WT reference row; the synonymous median (at least {MIN_SYN} synonymous variants);
    0 where the score is a log2 fold change vs WT.
  - Null anchor: the nonsense median (at least {MIN_NULL}), or else the frameshift median.
  - The two anchors must be at least {MIN_SEP:g} robust SD apart (SD of the null variants), with null below WT. Conditions
    where the readout does not depend on the receptor (MC4R forskolin, untreated) or that sit below the response
    (low doses of a dose series) fail this check and are left empty.
- **`score_rank`** is the percentile within the condition. It is defined for every scored row, but it says nothing
  about effect size: a condition where every variant is WT-like still spans 0 to 1.

`score_norm` covers {ok.sum()} of {len(cond)} conditions and {m.score_norm.notna().mean():.0%} of rows. The DIMPLE libraries
(µOR, GPR68, GPR161) and P2Y8 have no stop codons, the Procko-lab GEO tables have no synonymous variants, and the alanine
scans have neither, so those are not normalised. Their published scores are already centred on synonymous
(DIMPLE, P2Y8) or expressed relative to WT (alanine scans). `conditions.csv` lists every condition with its anchors,
anchor counts, separation and outcome.

`RHO_Chen2026` is CC BY-NC-ND 4.0. Its published scores are included as in `tables/`, but no rescaled version of
them is distributed (`score_norm` and `score_rank` are empty).

| study | receptor | rows | conditions with `score_norm` | why not, for the rest |
|---|---|---|---|---|
{rows}

## Things to know

- `RHO_McKee2021` and `RHO_Penn2020` come from the same McKee 2021 Table S1, but different columns of it: the
  27 °C / 37 °C ratio (McKee) and the +/- 9-cis-retinal ratio (Penn's data). They are not duplicates.
- Heredia CCR5/CXCR4 and Manian Rho MaveDB rows with no score are dropped. Cao AT1R mutants marked n.d. have
  no CRC values.
- β2AR (Jones 2020) WT residues follow the construct, which carries the common G16 / E27 haplotype.
- AT1R position 160 is G in Cao 2023 and S in Boora 2026; both are kept as published.
- Not compiled, because no per-variant numbers were released: Tate-lab thermostability alanine scans (β1AR,
  A2AR, NTS1), Okuta 2016 ETB, Scott 2024 Rho.

## License

The rows keep their study's license (`data_license`, and `../LICENSE.md`). `score_norm`, `score_rank`,
`assay_class` and the GPCRdb columns are adaptations; see `../NOTICE.md`. Cite the original paper for every
dataset you use (`../REFERENCES.md`), and GPCRdb.
"""


def write(master, out):
    out.mkdir(parents=True, exist_ok=True)
    m, cond = build(master)
    m.to_parquet(out / "gpcr_dms_long.parquet", index=False, compression="zstd")
    m.to_csv(out / "gpcr_dms_long.csv.gz", index=False, compression={"method": "gzip", "mtime": 0})
    cond.to_csv(out / "conditions.csv", index=False, float_format="%.6g")
    (out / "README.md").write_text(readme(m, cond))
    n = cond.norm_method.eq("WT = 0, null = -1")
    print(f"  merged: {len(m):,} rows, {m.study_id.nunique()} studies, {len(cond)} conditions; "
          f"score_norm in {n.sum()} conditions ({m.score_norm.notna().mean():.0%} of rows)")
    return m, cond
