"""Compile variant-level GPCR mutational scanning data into one long table.

One row = one variant scored in one condition. Scores are kept as published
(units differ by study; see score_type). Reads only the authors' files in <study_id>/source/.
Run through build.py; `python3 build_master.py [loader ...]` prints per-loader counts without writing.
"""
import re, sys
from pathlib import Path
import numpy as np
import pandas as pd

from paths import src

COLS = ["study_id", "receptor", "gene", "uniprot", "study", "year", "journal", "doi", "scan_type",
        "assay", "condition", "ligand", "ligand_conc_M", "variant", "pos", "wt_aa", "mut_aa", "mut_class",
        "score", "score_se", "score_type", "ec50_log", "ec50_log_se", "emax", "emax_se", "in_mavedb", "source_file"]

AA3 = {"Ala": "A", "Arg": "R", "Asn": "N", "Asp": "D", "Cys": "C", "Gln": "Q", "Glu": "E", "Gly": "G",
       "His": "H", "Ile": "I", "Leu": "L", "Lys": "K", "Met": "M", "Phe": "F", "Pro": "P", "Ser": "S",
       "Thr": "T", "Trp": "W", "Tyr": "Y", "Val": "V", "Ter": "*", "Sec": "U"}
AAS = set("ACDEFGHIKLMNPQRSTVWY")


def mclass(wt, mut):
    """missense / synonymous / nonsense / deletion / insertion / other from wt and mut strings."""
    wt, mut = str(wt), str(mut)
    if mut in ("*", "X", "Ter", "stop"): return "nonsense"
    if mut.lower().startswith("del") or mut.startswith("D_") or mut == "-": return "deletion"
    if mut.lower().startswith("ins"): return "insertion"
    if mut == "fs": return "frameshift"
    if mut == wt and mut in AAS: return "synonymous"
    if mut in AAS and wt in AAS: return "missense"
    return "other"


def finish(df, meta):
    df = df.reset_index(drop=True)
    for k, v in meta.items():
        df[k] = v
    if "mut_class" not in df:
        df["mut_class"] = np.nan
    df["mut_class"] = df["mut_class"].astype(object)
    miss = df["mut_class"].isna()
    df.loc[miss, "mut_class"] = [mclass(w, m) for w, m in zip(df.wt_aa[miss], df.mut_aa[miss])]
    if "variant" not in df or df["variant"].isna().all():
        df["variant"] = [f"p.{w}{int(p)}{m}" if pd.notna(p) else None for w, p, m in zip(df.wt_aa, df.pos, df.mut_aa)]
    for c in COLS:
        if c not in df:
            df[c] = np.nan
    df = df[COLS].copy()
    df["pos"] = pd.to_numeric(df.pos, errors="coerce").astype("Int64")
    return df


# ---------------------------------------------------------------- studies from GitHub
def mor_howard_2026():
    v = pd.read_csv(src("OPRM1_Howard2026", "01_variant_scores.csv"))
    base = v[["hgvs", "type", "position", "wildtype", "mutation"]]
    out = []
    ligs = ["surface", "Naltrexone", "Naloxone", "Nalbuphine", "Buprenorphine", "Butorphanol", "MP", "TRV130",
            "PZM21", "Methadone", "C6guano", "Morphine", "SR17018", "Fentanyl", "Carfentanil", "DAMGO", "NoLigand"]
    for L in ligs:
        x = base.copy()
        x["score"], x["score_se"] = v[f"{L}_effect"], v[f"{L}_effect_se"]
        if L == "surface":
            x["assay"], x["condition"], x["ligand"], x["conc"] = "surface expression (HaloTag/JF635i)", "surface", None, np.nan
        elif L == "NoLigand":
            x["assay"], x["condition"], x["ligand"], x["conc"] = "cAMP reporter (Gi)", "forskolin only (15-ligand panel)", None, np.nan
        else:
            x["assay"], x["condition"], x["ligand"], x["conc"] = "cAMP reporter (Gi)", f"{L} 10 µM", L, 1e-5
        x["score_type"] = "Lilace posterior effect, synonymous = 0, negative = loss"
        x["src"] = "01_variant_scores.csv"
        out.append(x)
    r = pd.read_csv(src("OPRM1_Howard2026", "02_dose_response_scores.csv"))
    rb = r[["hgvs", "type", "position", "wildtype", "mutation"]]
    for c in [c for c in r.columns if "_score_logM" in c]:
        L, lc = c.split("_score_logM")
        x = rb.copy()
        x["score"], x["score_se"] = r[c], r[c.replace("_score_", "_sd_")]
        x["assay"], x["ligand"], x["conc"] = "cAMP reporter (Gi)", L, 10 ** float(lc)
        x["condition"] = f"{L} 10^{lc} M (dose series)"
        x["score_type"] = "Lilace rescaled score (dose series), synonymous-normalised; SE column = SD"
        x["src"] = "02_dose_response_scores.csv"
        out.append(x)
    x = rb.copy()
    x["score"], x["score_se"] = r["NoLigand_DAMGOscreen_score"], r["NoLigand_DAMGOscreen_sd"]
    x["assay"], x["ligand"], x["conc"], x["condition"] = "cAMP reporter (Gi)", None, np.nan, "forskolin only (DAMGO dose series)"
    x["score_type"], x["src"] = "Lilace rescaled score (dose series); SE column = SD", "02_dose_response_scores.csv"
    out.append(x)
    df = pd.concat(out)
    df = df.rename(columns={"hgvs": "variant", "position": "pos", "wildtype": "wt_aa", "mutation": "mut_aa",
                            "conc": "ligand_conc_M", "src": "source_file"})
    df["mut_class"] = df.pop("type").replace({"insertion": "insertion", "deletion": "deletion"})
    df = df[df.score.notna()]
    return finish(df, dict(study_id="OPRM1_Howard2026", receptor="µOR", gene="OPRM1", uniprot="P35372",
                           study="M. Howard 2026", year=2026, journal="bioRxiv", doi="10.64898/2026.10.12.758633",
                           scan_type="DMS", in_mavedb="yes (urn:mavedb:00001326)"))


def gpr68_howard_2025():
    g = pd.read_csv(src("GPR68_Howard2025", "gpr68_scores_processed.csv"))
    out = []
    for key, assay, cond in [("ph55", "cAMP reporter (Gs)", "pH 5.5"), ("ph65", "cAMP reporter (Gs)", "pH 6.5"),
                             ("surface", "surface expression", "surface")]:
        x = pd.DataFrame({"variant": g.hgvs, "pos": g.pos, "score": g[f"score_{key}"], "score_se": g[f"SE_{key}"]})
        m = g.hgvs.str.extract(r"p\.\(([A-Z])(\d+)([A-Z*]|del|ins.*|=)?.*\)")
        x["wt_aa"] = m[0]
        x["mut_aa"] = np.where(g.mutation_type.eq("S"), m[0], g.variants)
        x["mut_class"] = g.mutation_type.map({"S": "synonymous", "M": "missense", "N": "nonsense", "D": "deletion",
                                              "I": "insertion"}).fillna("other")
        x.loc[x.mut_aa.isin(["*", "X"]), "mut_class"] = "nonsense"
        x["assay"], x["condition"] = assay, cond
        x["score_type"] = "Rosace score, synonymous-centred"
        x["source_file"] = "gpr68_scores_processed.csv"
        out.append(x)
    return finish(pd.concat(out), dict(study_id="GPR68_Howard2025", receptor="GPR68", gene="GPR68", uniprot="Q15743",
                                       study="M. Howard 2025", year=2025, journal="Cell", doi="10.1016/j.cell.2024.11.036",
                                       scan_type="DMS", in_mavedb="yes (urn:mavedb:00001207)"))


def gpr161_howard_2026():
    out = []
    for key, assay in [("cre", "cAMP reporter, basal (constitutive)"), ("surface", "surface expression"),
                       ("abundance", "whole-cell abundance")]:
        s = pd.read_csv(src("GPR161_Howard2026", f"{key}_variant_scores.tsv"), sep="\t")
        x = pd.DataFrame({"variant": s.hgvs, "pos": s.position, "wt_aa": s.wildtype, "mut_aa": s.mutation,
                          "mut_class": s["type"], "score": s.effect, "score_se": s.effect_se})
        x["assay"], x["condition"] = assay, key
        x["score_type"] = "Lilace posterior effect, synonymous = 0, negative = less readout"
        x["source_file"] = f"{key}_variant_scores.tsv"
        out.append(x)
    return finish(pd.concat(out), dict(study_id="GPR161_Howard2026", receptor="GPR161", gene="GPR161", uniprot="Q8N6U8",
                                       study="M. Howard 2026", year=2026, journal="bioRxiv", doi="10.64898/2026.10.30.762644",
                                       scan_type="DMS", in_mavedb="yes (urn:mavedb:00001323)"))


def mc4r_howard_2025():
    out = []
    for f, rep, path in [("MC4R-DMS5-Gs-unnormalized.tsv", "CRE reporter (Gs)", "Gs"),
                         ("MC4R-DMS8-Gq-unnormalized.tsv", "UAS/NFAT reporter (Gq)", "Gq")]:
        s = pd.read_csv(src("MC4R_Howard2025", f), sep="\t")
        c = s.contrast.str.replace("_unnormalized", "")
        lig = c.str.split("_").str[0]
        conc = pd.to_numeric(c.str.split("_").str[1], errors="coerce")
        x = pd.DataFrame({"pos": s.pos, "mut_aa": s.aa, "score": s.log2FoldChange, "score_se": s.log2StdError})
        x["ligand"] = lig.replace({"None": None, "Forsk": "forskolin"})
        x["ligand_conc_M"] = conc.where(conc > 0)
        x["condition"] = [("untreated" if l == "None" else f"{'forskolin' if l == 'Forsk' else l} {v:g} M")
                          for l, v in zip(lig, conc)]
        x["assay"] = rep
        x["score_type"] = "log2 fold change vs WT within condition (unnormalized model coefficient)"
        x["source_file"] = f
        out.append(x)
    s = pd.read_csv(src("MC4R_Howard2025", "MC4R-DMS11-DefectSumstats.tsv"), sep="\t")
    x = pd.DataFrame({"pos": s.pos, "mut_aa": s.aa, "score": s.log2FoldChange, "score_se": s["std.error"]})
    x["ligand"] = np.where(s.chaperone.eq("Ipsen"), "Ipsen 17", None)
    x["condition"] = np.where(s.chaperone.eq("Ipsen"), "expression defect + Ipsen 17 (chaperone)", "expression defect, no chaperone")
    x["assay"] = "CRE reporter (Gs), marginal defect across forskolin/untreated/aMSH"
    x["score_type"] = "log2 fold change vs WT (marginal defect model)"
    x["source_file"] = "MC4R-DMS11-DefectSumstats.tsv"
    out.append(x)
    df = pd.concat(out)
    df = df[df.mut_aa.ne("WT")]                        # WT reference rows (fixed at 0)
    wt = pd.read_csv(src("MC4R_Howard2025", "mc4r-wt.tsv"), sep="\t")
    df = add_wt(df, wt)
    return finish(df, dict(study_id="MC4R_Howard2025", receptor="MC4R", gene="MC4R", uniprot="P32245",
                           study="C. Howard 2025 (Octant)", year=2025, journal="eLife", doi="10.7554/eLife.104725",
                           scan_type="DMS", in_mavedb="no"))


def add_wt(df, wt):
    """Attach wt_aa from a per-position WT table (any layout with a position and residue column)."""
    cols = {c.lower(): c for c in wt.columns}
    pc = next(cols[c] for c in cols if c in ("pos", "position"))
    ac = next(cols[c] for c in cols if c in ("aa", "wt", "wt_aa", "wildtype", "residue", "ref"))
    m = dict(zip(wt[pc], wt[ac]))
    m = {k: (AA3.get(str(v), v)) for k, v in m.items()}
    df["wt_aa"] = df.pos.map(m)
    return df


def adrb2_jones_2020():
    lib = pd.read_csv(src("ADRB2_Jones2020", "lib-med.csv.gz"))
    sc = pd.read_csv(src("ADRB2_Jones2020", "scalars.csv"))
    sc = sc[sc.Variant.eq("Indel")][["Condition", "Repeat", "Scale_Mean"]]
    x = lib.merge(sc, on=["Condition", "Repeat"])
    x["Norm"] = x.Mean / x.Scale_Mean
    x["u2"] = x.SD ** 2 / x.Scale_Mean ** 2
    g = x.groupby(["Condition", "Pos", "AA"]).agg(score=("Norm", "mean"), u2=("u2", "sum"), n=("Norm", "size")).reset_index()
    g["score_se"] = 0.5 * np.sqrt(g.u2)                 # 'Uncert' as defined in paper.Rmd
    df = pd.DataFrame({"pos": g.Pos, "mut_aa": g.AA.replace({"Stop": "*", "X": "*"}), "score": g.score, "score_se": g.score_se})
    df["ligand"], df["ligand_conc_M"] = np.where(g.Condition > 0, "isoproterenol", None), np.where(g.Condition > 0, g.Condition * 1e-6, np.nan)
    df["condition"] = [f"isoproterenol {c:g} µM" if c > 0 else "untreated" for c in g.Condition]
    df["assay"] = "CRE transcriptional reporter (Gs)"
    df["score_type"] = "reporter expression / mean frameshift control, mean of 2 repeats (paper.Rmd 'Norm'); SE = paper 'Uncert'"
    df["source_file"] = "output/lib-med.csv.gz + output/scalars.csv"
    return df


def jones_wt():
    """WT residue per position for the Jones construct.

    First the one amino acid absent at a position whose other 19 were scored (the library has no synonymous
    codons). Positions that rule cannot resolve fall back to GPCRdb's human ADRB2 sequence (the same residues as
    the b2-gpcrdb.csv table in the Kosuri repo, which is not redistributed here), then to the GPCR-MAPS
    annotation. Jones' construct carries the common G16 / E27 haplotype, which GPCRdb also has.
    """
    df = adrb2_jones_2020()
    present = df.groupby("pos").mut_aa.apply(set)
    wt = {p: next(iter(AAS - s)) for p, s in present.items() if len(AAS - s) == 1}
    from paths import GPCRDB_TABLE
    g = pd.read_csv(GPCRDB_TABLE)
    g = g[g.uniprot.eq("P07550") & g.gpcrdb_generic.notna()]
    for p, a in zip(g.pos, g.gpcrdb_aa):
        wt.setdefault(int(p), a)
    b, w2, p2, _ = _maps()
    for p, a in zip(p2, w2):
        if p is not None and a is not None:
            wt.setdefault(int(p), a)
    return wt


def adrb2_jones_2020_final():
    df = adrb2_jones_2020()
    df["wt_aa"] = df.pos.map(jones_wt())
    return finish(df, dict(study_id="ADRB2_Jones2020", receptor="β2AR", gene="ADRB2", uniprot="P07550",
                           study="Jones 2020 (Kosuri)", year=2020, journal="eLife", doi="10.7554/eLife.54895",
                           scan_type="DMS", in_mavedb="no"))


# ---------------------------------------------------------------- shared helpers for downloaded tables
VAR = re.compile(r"^\s*([A-Z])\s*(\d+)\s*([A-Z*]|del|Del)\s*$")


def split_var(v):
    m = VAR.match(str(v))
    if not m:
        return None, None, None
    mut = m.group(3)
    return m.group(1), int(m.group(2)), ("del" if mut.lower() == "del" else mut)


def from_names(names):
    p = [split_var(v) for v in names]
    return [a[0] for a in p], [a[1] for a in p], [a[2] for a in p]


def procko_sheet(raw, r0, cols, cond_names):
    """Procko-lab GEO tables: Residue (first row of each position only), Substitution, Frequency, then replicate
    pairs per sort. 'WT' marks the wild-type residue. Score = mean of replicates, SE = SEM (n = 2)."""
    d = raw.iloc[r0:, cols].copy()
    d.columns = ["res", "sub", "freq"] + [f"{c}|{r}" for c in cond_names for r in (1, 2)]
    d["res"] = d.res.ffill()
    d = d[d["sub"].notna()]
    d["pos"] = d.res.astype(str).str.extract(r"(\d+)")[0].astype(int)
    out = []
    for c in cond_names:
        r = d[[f"{c}|1", f"{c}|2"]]
        wt = r.eq("WT").any(axis=1)
        num = r.apply(pd.to_numeric, errors="coerce")
        x = pd.DataFrame({"pos": d.pos, "mut_aa": d["sub"].astype(str), "score": num.mean(axis=1),
                          "score_se": (num.iloc[:, 0] - num.iloc[:, 1]).abs() / 2, "condition": c, "_wt": wt})
        out.append(x)
    x = pd.concat(out)
    wtmap = x[x._wt].groupby("pos").mut_aa.first()
    x["wt_aa"] = x.pos.map(wtmap)
    return x[~x._wt].drop(columns="_wt")


def hdr(raw, rows, ncol=None):
    """Join multi-row headers (forward-filled across columns) into 'a|b|c' labels."""
    parts = []
    for r in rows:
        v = raw.iloc[r, :ncol].copy()
        v = v.where(v.notna(), None)
        parts.append(pd.Series(v.values).ffill() if r != rows[-1] else pd.Series(v.values))
    labs = []
    for j in range(len(parts[0])):
        labs.append("|".join(str(p[j]).strip() for p in parts if p[j] is not None and str(p[j]).strip() not in ("", "nan")))
    return labs


def crc_rows(tab, mutcol, blocks, base):
    """blocks: list of (condition, {'act': (mean_col, se_col), 'ec50': (...), 'emax': (...)})"""
    out = []
    for cond, cols in blocks:
        x = base.copy()
        g = lambda k, i: pd.to_numeric(tab[cols[k][i]], errors="coerce") if k in cols and cols[k][i] is not None else np.nan
        x["score"], x["score_se"] = g("act", 0), g("act", 1)
        x["ec50_log"], x["ec50_log_se"], x["emax"], x["emax_se"] = g("ec50", 0), g("ec50", 1), g("emax", 0), g("emax", 1)
        x["condition"] = cond
        out.append(x)
    return pd.concat(out)


# ---------------------------------------------------------------- MaveDB score CSVs (user-downloaded)
HGVS = re.compile(r"p\.\(?([A-Z][a-z]{2})(\d+)([A-Z][a-z]{2}fs|fs|[A-Z][a-z]{2}|=|del|Ter|\*|ins[A-Za-z]*|_.*)?\)?$")


def parse_hgvs_pro(h):
    m = HGVS.match(str(h))
    if not m:
        return None, None, None
    wt, pos, mut = AA3.get(m.group(1), m.group(1)), int(m.group(2)), m.group(3) or ""
    if mut.endswith("fs"):
        mut = "fs"
    elif mut == "=":
        mut = wt
    elif mut.startswith("del") or mut.startswith("_"):
        mut = "del"
    elif mut.startswith("ins"):
        mut = "ins"
    else:
        mut = AA3.get(mut, mut)
    return wt, pos, mut


MAVEDB_SETS = {  # urn: (study_id, assay, condition)
    "00000047-a-1": ("CCR5_Heredia2018", "surface expression (anti-myc)", "surface"),
    "00000047-b-1": ("CCR5_Heredia2018", "antibody 2D7 binding", "2D7 binding"),
    "00000047-c-1": ("CCR5_Heredia2018", "HIV gp120 binding", "gp120 binding"),
    "00000048-a-1": ("CXCR4_Heredia2018", "surface expression (anti-myc)", "surface"),
    "00000048-b-1": ("CXCR4_Heredia2018", "CXCL12 binding", "CXCL12 binding"),
    "00000048-c-1": ("CXCR4_Heredia2018", "antibody 12G5 binding", "12G5 binding"),
    "00000099-a-1": ("RHO_Wan2019", "surface expression (pooled flow)", "surface"),
    "00001275-a-1": ("RHO_Manian2025", "surface trafficking", "surface trafficking"),
    "00001275-a-2": ("RHO_Manian2025", "membrane proximity", "membrane proximity"),
}
STUDY_META = {
    "CCR5_Heredia2018": dict(receptor="CCR5", gene="CCR5", uniprot="P51681", study="Heredia 2018 (Procko)", year=2018,
                             journal="J Immunol", doi="10.4049/jimmunol.1800343", scan_type="DMS"),
    "CXCR4_Heredia2018": dict(receptor="CXCR4", gene="CXCR4", uniprot="P61073", study="Heredia 2018 (Procko)", year=2018,
                              journal="J Immunol", doi="10.4049/jimmunol.1800343", scan_type="DMS"),
    "RHO_Wan2019": dict(receptor="Rho", gene="RHO", uniprot="P08100", study="Wan 2019 (Comander)", year=2019,
                        journal="Hum Mutat", doi="10.1002/humu.23762", scan_type="targeted panel"),
    "RHO_Manian2025": dict(receptor="Rho", gene="RHO", uniprot="P08100", study="Manian 2026 (Comander)", year=2026,
                           journal="Sci Adv", doi="10.1126/sciadv.aef3518", scan_type="DMS"),
}


def mavedb_sets():
    out = []
    for urn, (sid, assay, cond) in MAVEDB_SETS.items():
        s = pd.read_csv(src(sid, f"mavedb_{urn}.csv"))
        p = [parse_hgvs_pro(h) for h in s.hgvs_pro]
        x = pd.DataFrame({"variant": s.hgvs_pro, "wt_aa": [a[0] for a in p], "pos": [a[1] for a in p],
                          "mut_aa": [a[2] for a in p], "score": s.score,
                          "score_se": s["score_se"] if "score_se" in s else np.nan})
        x["mut_class"] = [mclass(w, m) for w, m in zip(x.wt_aa, x.mut_aa)]
        x.loc[x.variant.eq("p.="), "mut_class"] = "synonymous"
        x["assay"], x["condition"] = assay, cond
        x["score_type"] = "MaveDB score as deposited"
        x["source_file"] = f"urn:mavedb:{urn}"
        x = x[x.score.notna()]
        out.append(finish(x, dict(study_id=sid, in_mavedb=f"yes (urn:mavedb:{urn})", **STUDY_META[sid])))
    return pd.concat(out)


# ---------------------------------------------------------------- GEO / Zenodo / journal supplements
def t1r2_park_2019():
    raw = pd.read_excel(src("TAS1R2_Park2019", "GSE115751_enrichment_ratios_T1R2.xlsx"), header=None)
    x = procko_sheet(raw, 7, list(range(7)), ["T1R2 surface (anti-FLAG)", "T1R3 co-surface (anti-myc)"])
    x["assay"] = np.where(x.condition.str.startswith("T1R2"), "surface expression of T1R2", "surface expression of partner T1R3")
    x["score_type"] = "log2 enrichment ratio (sorted vs naive), mean of 2 replicates; floor -4"
    x["source_file"] = "GEO GSE115751_enrichment_ratios_T1R2.xlsx"
    return finish(x, dict(study_id="TAS1R2_Park2019", receptor="T1R2", gene="TAS1R2", uniprot="Q8TE23",
                          study="Park 2019 (Procko)", year=2019, journal="J Biol Chem", doi="10.1074/jbc.RA118.006173",
                          scan_type="DMS", in_mavedb="no"))


def cxcr4_ccr5_gill_2023():
    raw = pd.read_excel(src("CXCR4_Gill2023", "GSE125426_X4R5_BiFC_enrichment_ratios.xlsx"), header=None)
    out = []
    for cols, rec, gene, uni in [(list(range(7)), "CXCR4", "CXCR4", "P61073"), (list(range(8, 15)), "CCR5", "CCR5", "P51681")]:
        x = procko_sheet(raw, 7, cols, ["surface expression (myc)", "BiFC self-association"])
        x["assay"] = x.condition
        x["score_type"] = "log2 enrichment ratio (sorted vs naive), mean of 2 replicates; floor -3"
        x["source_file"] = "GEO GSE125426_X4R5_BiFC_enrichment_ratios.xlsx"
        out.append(finish(x, dict(study_id=f"{gene}_Gill2023", receptor=rec, gene=gene, uniprot=uni, study="Gill 2023 (Procko)",
                                  year=2023, journal="J Biol Chem", doi="10.1016/j.jbc.2023.105229", scan_type="DMS",
                                  in_mavedb="no")))
    return pd.concat(out)


def v2r_mighell_2025():
    v = pd.read_excel(src("AVPR2_Mighell2025", "v2R_all_exp.xlsx"))
    name = v.iloc[:, 0]
    wt, pos, mut = from_names(name)
    out = []
    for key, cond, lig in [("ctrls", "DMSO, 37 °C", None), ("27", "27 °C", None), ("Tol", "tolvaptan", "tolvaptan"),
                           ("cmpd34", "compound 34", "compound 34")]:
        x = pd.DataFrame({"variant": name, "wt_aa": wt, "pos": pos, "mut_aa": mut, "score": v[f"{key}_comb"],
                          "score_se": v[f"{key}_sem"]})
        x["condition"], x["ligand"] = cond, lig
        x["assay"] = "surface expression (abundancePCA-style sort)"
        x["score_type"] = "normalised surface score, replicates combined (Zenodo *_comb); SE = *_sem"
        x["source_file"] = "Zenodo 14216036 v2R_all_exp_all_reps_com_and_norm.xlsx"
        out.append(x)
    df = pd.concat(out)
    df = df[df.score.notna() & df.pos.notna()]
    return finish(df, dict(study_id="AVPR2_Mighell2025", receptor="V2R", gene="AVPR2", uniprot="P30518",
                           study="Mighell 2025 (Lehner)", year=2025, journal="Nat Struct Mol Biol",
                           doi="10.1038/s41594-025-01659-6", scan_type="DMS", in_mavedb="no"))


def _maps():
    b = pd.read_csv(src("ADRB2_Mighell2026", "b2AR_all_data_annot.csv.gz"), low_memory=False)
    b = b[b.iloc[:, 0].ne("WT")]
    wt, pos, mut = from_names(b.iloc[:, 0])
    return b, wt, pos, mut


def adrb2_mighell_maps_2025():
    b, wt, pos, mut = _maps()
    base = pd.DataFrame({"variant": b.iloc[:, 0].values, "wt_aa": wt, "pos": pos, "mut_aa": mut})
    out = []
    for col, se, cond, assay, lig, conc in [
            ("surfexp_reps_comb", "surfexp_reps_comb_SEM", "surface", "surface expression", None, np.nan),
            ("Nb80_isoP_reps_comb", "Nb80_isoP_reps_comb_SEM", "Nb80 recruitment, isoproterenol 10 µM",
             "Nb80 (active-state) recruitment, TEV-transcriptional", "isoproterenol", 1e-5),
            ("BArr_isoP_reps_comb", "BArr_isoP_reps_comb_SEM", "β-arrestin recruitment, isoproterenol 10 µM",
             "β-arrestin recruitment, TEV-transcriptional", "isoproterenol", 1e-5)]:
        x = base.copy(); x["score"], x["score_se"] = b[col].values, b[se].values
        x["condition"], x["assay"], x["ligand"], x["ligand_conc_M"] = cond, assay, lig, conc
        x["score_type"] = "normalised score, replicates combined (Zenodo *_reps_comb); SE = SEM"
        out.append(x)
    units = {"uM": 1e-6, "nM": 1e-9, "pM": 1e-12}
    for c in [c for c in b.columns if re.fullmatch(r"Nb80_[\d.]+[unp]M_norm_comb_score", c)]:
        lab = c.split("_")[1]
        conc = float(lab[:-2]) * units[lab[-2:]]
        x = base.copy(); x["score"], x["score_se"] = b[c].values, np.nan
        x["condition"] = f"Nb80 recruitment, isoproterenol {lab} (dose series)"
        x["assay"], x["ligand"], x["ligand_conc_M"] = "Nb80 (active-state) recruitment, TEV-transcriptional", "isoproterenol", conc
        x["score_type"] = "normalised score, replicates combined (Zenodo Nb80_<conc>_norm_comb_score)"
        out.append(x)
    df = pd.concat(out)
    df = df[df.score.notna()]
    df["source_file"] = "Zenodo 15363336 b2AR_all_data_annot.csv.gz"
    return finish(df, dict(study_id="ADRB2_Mighell2026", receptor="β2AR", gene="ADRB2", uniprot="P07550",
                           study="Mighell 2026 GPCR-MAPS (Lehner)", year=2026, journal="Nat Struct Mol Biol",
                           doi="10.1038/s41594-026-01907-3", scan_type="DMS", in_mavedb="no"))


def adrb2_heydenreich_2023():
    b, wt, pos, mut = _maps()
    k = b.Heydenreich_expression.notna().values
    base = pd.DataFrame({"variant": b.iloc[:, 0].values, "wt_aa": wt, "pos": pos, "mut_aa": mut})[k]
    e = base.copy(); e["score"], e["score_se"] = b.Heydenreich_expression.values[k], b.Heydenreich_expression_SEM.values[k]
    e["condition"], e["assay"] = "surface expression", "surface ELISA"
    e["score_type"] = "surface expression, % WT"
    g = base.copy()
    g["score"], g["score_se"] = b.Heydenreich_amplitude.values[k], b.Heydenreich_amplitude_SEM.values[k]
    g["emax"], g["emax_se"] = g.score, g.score_se
    g["ec50_log"], g["ec50_log_se"] = b.Heydenreich_EC50.values[k], b.Heydenreich_EC50_SEM.values[k]
    g["condition"], g["assay"], g["ligand"] = "Gs activation, adrenaline CRC", "Gs BRET concentration-response", "adrenaline"
    g["score_type"] = "CRC amplitude (BRET units); ec50_log = log10 EC50 (M)"
    df = pd.concat([e, g])
    df["source_file"] = "Heydenreich Table S1 as mirrored in Zenodo 15363336 (Heydenreich_* columns)"
    return finish(df, dict(study_id="ADRB2_Heydenreich2023", receptor="β2AR", gene="ADRB2", uniprot="P07550",
                           study="Heydenreich 2023 (Veprintsev)", year=2023, journal="Science", doi="10.1126/science.adh1859",
                           scan_type="alanine scan", in_mavedb="no"))


def p2ry8_laflam_2025():
    f = src("P2RY8_LaFlam2025", "supp_p2y8_PMC12648108_mmc3.xlsx")
    out = []
    for sheet, cond, assay in [("2_Enrich2_Expression", "surface expression", "surface expression"),
                               ("3_Enrich2_Migration", "migration (S1P-gradient chemotaxis)", "transwell migration"),
                               ("4_Enrich2_Proliferation", "proliferation", "cell proliferation")]:
        raw = pd.read_excel(f, sheet_name=sheet, header=None)
        d = raw.iloc[2:]
        wt, pos, mut = from_names(d[0])
        x = pd.DataFrame({"variant": d[0].values, "wt_aa": wt, "pos": pos, "mut_aa": mut,
                          "score": pd.to_numeric(d[10], errors="coerce").values,
                          "score_se": pd.to_numeric(d[9], errors="coerce").values})
        x["condition"], x["assay"] = cond, assay
        x["mut_class"] = np.where(x.variant.eq("_wt"), "wt_reference", None)
        x["score_type"] = "Enrich2 overall score (combined transductions); SE = Enrich2 overall SE"
        x["source_file"] = f"Cell Genomics Table S2 (mmc3.xlsx) sheet {sheet}"
        out.append(x)
    df = pd.concat(out)
    df = df[df.score.notna()]
    return finish(df, dict(study_id="P2RY8_LaFlam2025", receptor="P2Y8", gene="P2RY8", uniprot="Q86VZ1",
                           study="LaFlam 2025", year=2025, journal="Cell Genom", doi="10.1016/j.xgen.2025.100981",
                           scan_type="DMS", in_mavedb="no"))


def rho_chen_2026():
    d = pd.read_excel(src("RHO_Chen2026", "chen_sd02.xlsx"))
    d.columns = [str(c).strip() for c in d.columns]
    wt, pos, mut = from_names(d.Variant)
    out = []
    for col, cond, assay in [("Scaled_dark_activity_scores", "dark (basal)", "yeast signaling reporter, dark"),
                             ("Scaled_light_activity_scores", "light", "yeast signaling reporter, light-activated"),
                             ("Scaled_Abundance_scores", "abundance", "receptor abundance")]:
        x = pd.DataFrame({"variant": d.Variant, "wt_aa": wt, "pos": d.Position, "mut_aa": mut, "score": d[col]})
        x["condition"], x["assay"] = cond, assay
        x["score_type"] = "scaled score as published (Dataset S2); light/dark ratio omitted as derived"
        x["source_file"] = "PNAS Dataset S2 (pnas.2624087123.sd02.xlsx)"
        out.append(x)
    df = pd.concat(out)
    df = df[df.score.notna()]
    return finish(df, dict(study_id="RHO_Chen2026", receptor="Rho", gene="RHO", uniprot="P08100", study="Chen 2026",
                           year=2026, journal="PNAS", doi="10.1073/pnas.2624087123", scan_type="DMS", in_mavedb="no"))


def _pdftext(path):
    import subprocess
    return subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True).stdout


def rho_mckee_penn():
    txt = _pdftext(src("RHO_McKee2021", "supp_mckee_PMC8649220_mmc1.pdf"))
    rows = re.findall(r"^\s*([A-Z])\s+(\d+)\s+([A-Z*])\s+(-?[\d.]+|N/A)\s+(-?[\d.]+|N/A)\s", txt, re.M)
    d = pd.DataFrame(rows, columns=["wt_aa", "pos", "mut_aa", "ret", "temp"]).drop_duplicates(["pos", "mut_aa"])
    for c in ("ret", "temp"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["pos"] = d.pos.astype(int)
    seg = lambda p: "TM2 + TM7"
    mk = d.copy(); mk["score"] = mk.temp
    mk["condition"], mk["assay"] = "surface expression 27 °C / 37 °C", "surface immunostaining (DMS), temperature sensitivity"
    mk["score_type"] = "ratio of DMS surface-immunostaining intensity, 27 °C over 37 °C (McKee Table S1)"
    mk["source_file"] = "JBC 2021 Table S1 (mmc1.pdf)"
    pn = d.copy(); pn["score"] = pn.ret
    pn["condition"], pn["ligand"], pn["assay"] = "surface expression +/− 9-cis-retinal (ratio)", "9-cis-retinal", "surface immunostaining (DMS), retinal sensitivity"
    pn["score_type"] = "ratio of DMS surface-immunostaining intensity, +9-cis-retinal over −retinal (Penn 2020 data, tabulated in McKee 2021 Table S1)"
    pn["source_file"] = "JBC 2021 Table S1 (mmc1.pdf); Penn 2020 SI gives only read counts"
    a = finish(mk[mk.score.notna()], dict(study_id="RHO_McKee2021", receptor="Rho", gene="RHO", uniprot="P08100",
               study="McKee 2021 (Schlebach)", year=2021, journal="J Biol Chem", doi="10.1016/j.jbc.2021.101359",
               scan_type="DMS (TM2 + TM7)", in_mavedb="no"))
    b = finish(pn[pn.score.notna()], dict(study_id="RHO_Penn2020", receptor="Rho", gene="RHO", uniprot="P08100",
               study="Penn 2020 (Schlebach)", year=2020, journal="Sci Adv", doi="10.1126/sciadv.aay7505",
               scan_type="DMS (TM2 + TM7)", in_mavedb="no"))
    return pd.concat([a, b])


def rho_roushar_2022():
    txt = _pdftext(src("RHO_Roushar2022", "supp_roushar_PMC9399271_mmc1.pdf"))
    rows = re.findall(r"^\s*((?:del\s+)?[A-Z]\d+[A-Z*]?)\s+.*?(\d+)\s*±\s*(\d+)\s+(\d+)\s*±\s*(\d+)\s*$", txt, re.M)
    d = pd.DataFrame(rows, columns=["v", "apo", "apo_se", "ret", "ret_se"]).drop_duplicates("v")
    out = []
    for c, cond, lig in [("apo", "surface expression, apo", None), ("ret", "surface expression, +9-cis-retinal", "9-cis-retinal")]:
        x = pd.DataFrame({"variant": d.v, "score": pd.to_numeric(d[c]), "score_se": pd.to_numeric(d[c + "_se"])})
        m = d.v.str.extract(r"(del\s+)?([A-Z])(\d+)([A-Z*])?")
        x["wt_aa"], x["pos"] = m[1], m[2].astype(int)
        x["mut_aa"] = np.where(m[0].notna(), "del", m[3])
        x["condition"], x["ligand"], x["assay"] = cond, lig, "surface immunostaining (individual variants)"
        x["score_type"] = "plasma-membrane immunostaining intensity (a.u.), mean ± SE"
        out.append(x)
    df = pd.concat(out)
    df["source_file"] = "JBC 2022 Table S1 (mmc1.pdf)"
    return finish(df, dict(study_id="RHO_Roushar2022", receptor="Rho", gene="RHO", uniprot="P08100",
                           study="Roushar 2022 (Schlebach)", year=2022, journal="J Biol Chem", doi="10.1016/j.jbc.2022.102266",
                           scan_type="targeted panel", in_mavedb="no"))


def _crc_sheet(path, sheet, hdr_rows, data_row, mutcol):
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    labs = hdr(raw, hdr_rows)
    tab = raw.iloc[data_row:].reset_index(drop=True)
    tab = tab[tab[mutcol].notna()]
    return raw, labs, tab


def _find(labs, *keys, start=0):
    for j, l in enumerate(labs):
        if j >= start and all(k.lower() in l.lower() for k in keys):
            return j
    return None


def at1r_cao_2023():
    f = src("AGTR1_Cao2023", "adf2173_Data_file_S1.xlsx")
    rawA, la, ta = _crc_sheet(f, 0, [1, 2, 3], 4, 4)
    rawB, lb, tb = _crc_sheet(f, 1, [1, 2, 3], 4, 4)
    tb = tb.set_index(4).reindex(ta[4]).reset_index()
    names = ta[4].astype(str).str.strip().str.replace(r"^([A-Z]\d+[A-Z])\*+$", r"\1", regex=True)
    wt, pos, mut = from_names(names)
    base = pd.DataFrame({"variant": names.values, "wt_aa": wt, "pos": pos, "mut_aa": mut})
    base.loc[names.eq("WT").values, "mut_class"] = "wt_reference"
    out = []
    for path, cond, assay in [("Gq", "Gq activation, AngII CRC", "Gαq activation (PKC-C1b BRET), CRC"),
                              ("b-arr", "β-arrestin recruitment, AngII CRC", "β-arrestin2 recruitment BRET, CRC")]:
        bk = "Gq" if path == "Gq" else "Barr"
        x = base.copy()
        jb = _find(lb, bk, "Log (Emax/EC50)|", "Mean") or _find(lb, bk, "Mean")
        x["score"] = pd.to_numeric(tb.iloc[:, jb], errors="coerce").values
        x["score_se"] = pd.to_numeric(tb.iloc[:, jb + 1], errors="coerce").values
        je = _find(la, path, "LogEC50", "Mean"); jm = _find(la, path, "Emax", "Mean")
        x["ec50_log"], x["ec50_log_se"] = pd.to_numeric(ta.iloc[:, je], errors="coerce").values, pd.to_numeric(ta.iloc[:, je + 1], errors="coerce").values
        x["emax"], x["emax_se"] = pd.to_numeric(ta.iloc[:, jm], errors="coerce").values, pd.to_numeric(ta.iloc[:, jm + 1], errors="coerce").values
        x["condition"], x["assay"], x["ligand"] = cond, assay, "angiotensin II"
        x["score_type"] = "log(Emax/EC50) activity; ec50_log = log10 EC50 (M); emax = % WT"
        out.append(x)
    e = base.copy()
    e["score"] = pd.to_numeric(ta[2], errors="coerce").values
    e["condition"], e["assay"], e["score_type"] = "surface expression", "surface ELISA", "surface expression, % WT"
    out.append(e)
    df = pd.concat(out)
    df = df[df.score.notna() | df.ec50_log.notna()]
    df["source_file"] = "Sci Signal Data file S1"
    return finish(df, dict(study_id="AGTR1_Cao2023", receptor="AT1R", gene="AGTR1", uniprot="P30556",
                           study="Cao 2023 (Heydenreich)", year=2023, journal="Sci Signal", doi="10.1126/scisignal.adf2173",
                           scan_type="alanine scan", in_mavedb="no"))


def boora_2026():
    out = []
    specs = [("boora_media-1.xlsx", "FP", "PTGFR", "P43088", True, "Data S1", "PGF2α"),
             ("boora_media-2.xlsx", "AT1R", "AGTR1", "P30556", False, "Data S2", "angiotensin II")]
    for fn, rec, gene, uni, keep_expr, label, lig in specs:
        raw, labs, tab = _crc_sheet(src(f"{gene}_Boora2026", fn), 0, [0, 1, 2], 3, 4)
        names = tab[4].astype(str).str.strip().str.replace(r"^([A-Z]\d+[A-Z])\*+$", r"\1", regex=True)
        wt, pos, mut = from_names(names)
        base = pd.DataFrame({"variant": names.values, "wt_aa": wt, "pos": pos, "mut_aa": mut})
        base.loc[names.eq("WT").values, "mut_class"] = "wt_reference"
        parts = []
        for pw, cond in [("Gq/11 Pathway", "Gq/11 activation"), ("G12/13 Pathway", "G12/13 activation")]:
            j0 = _find(labs, pw)
            blk = {"ec50": (_find(labs, pw, "LogEC50", "Mean"), _find(labs, pw, "LogEC50", "SE")),
                   "emax": (_find(labs, pw, "Emax (Efficacy)", "Mean"), _find(labs, pw, "Emax (Efficacy)", "SE")),
                   "act": (_find(labs, pw, "Activity", "Mean"), _find(labs, pw, "Activity", "SE"))}
            x = crc_rows(tab, 4, [(f"{cond}, {lig} CRC", blk)], base)
            x["assay"] = f"{cond.split()[0]} TRUPATH-style BRET sensor, CRC"
            parts.append(x)
        if keep_expr:
            e = base.copy(); e["score"] = pd.to_numeric(tab[2], errors="coerce").values
            e["condition"], e["assay"], e["score_type"] = "surface expression", "surface ELISA", "surface expression, % WT"
            parts.append(e)
        x = pd.concat(parts)
        x["ligand"] = np.where(x.condition.eq("surface expression"), None, lig)
        if "score_type" not in x:
            x["score_type"] = np.nan
        x = x.reset_index(drop=True)
        x["score_type"] = x["score_type"].astype(object)
        x.loc[x.score_type.isna(), "score_type"] = "log(Emax/EC50) activity; ec50_log = log10 EC50 (M); emax = % WT"
        x["source_file"] = f"bioRxiv {label} ({fn.replace('boora_', '')})"
        out.append(finish(x, dict(study_id=f"{gene}_Boora2026", receptor=rec, gene=gene, uniprot=uni, study="Boora 2026 (Heydenreich / Vaidehi)",
                                  year=2026, journal="bioRxiv", doi="10.64898/2026.08.28.747882", scan_type="alanine scan", in_mavedb="no")))
    # validation tables S3 (FP, Gaq-Gbg sensor + G13) and S4 (AT1R, KO cells)
    for fn, rec, gene, uni, label, lig in [("boora_media-3.xlsx", "FP", "PTGFR", "P43088", "Data S3", "PGF2α"),
                                           ("boora_media-4.xlsx", "AT1R", "AGTR1", "P30556", "Data S4", "angiotensin II")]:
        raw, labs, tab = _crc_sheet(src(f"{gene}_Boora2026", fn), 0, [1, 2, 3], 4, 3)
        sensors = [l.split("|")[0] for l in labs if "LogEC50" in l and "Mean" in l]
        parts = []
        for k, col in enumerate(labs):
            if not ("LogEC50" in col and "Mean" in col):
                continue
            j = labs.index(col)
            sensor = col.split("|")[0]
            mcol = 3 if k < 10 else next((i for i in range(j - 1, -1, -1) if str(raw.iloc[3, i]).strip() == "Mutant"), 3)
            names = tab[mcol].astype(str).str.strip().str.replace(r"^([A-Z]\d+[A-Z])\*+$", r"\1", regex=True)
            keep = names.ne("nan").values
            wt, pos, mut = from_names(names)
            base = pd.DataFrame({"variant": names.values, "wt_aa": wt, "pos": pos, "mut_aa": mut})
            base.loc[names.eq("WT").values, "mut_class"] = "wt_reference"
            ja = _find(labs, "Log(Emax/EC50)", "Mean", start=j)
            jm = _find(labs, "Emax", "Mean", start=j)
            blk = {"ec50": (j, j + 1), "emax": (jm, jm + 1) if jm else (None, None), "act": (ja, ja + 1) if ja else (None, None)}
            x = crc_rows(tab, mcol, [(f"validation: {sensor}, {lig} CRC", blk)], base)[keep]
            x["assay"] = f"validation, {sensor}"
            parts.append(x)
        if not parts:
            continue
        x = pd.concat(parts)
        x = x[x.ec50_log.notna() | x.score.notna()]
        x["ligand"] = lig
        x["score_type"] = "log(Emax/EC50) activity; ec50_log = log10 EC50 (M); emax = % WT"
        x["source_file"] = f"bioRxiv {label} ({fn.replace('boora_', '')})"
        out.append(finish(x, dict(study_id=f"{gene}_Boora2026", receptor=rec, gene=gene, uniprot=uni, study="Boora 2026 (Heydenreich / Vaidehi)",
                                  year=2026, journal="bioRxiv", doi="10.64898/2026.08.28.747882", scan_type="alanine scan", in_mavedb="no")))
    return pd.concat(out)


LOADERS = [mor_howard_2026, gpr68_howard_2025, gpr161_howard_2026, mc4r_howard_2025, adrb2_jones_2020_final,
           mavedb_sets, t1r2_park_2019, cxcr4_ccr5_gill_2023, v2r_mighell_2025, adrb2_mighell_maps_2025,
           adrb2_heydenreich_2023, p2ry8_laflam_2025, rho_chen_2026, rho_mckee_penn, rho_roushar_2022,
           at1r_cao_2023, boora_2026]

def build(only=(), verbose=True):
    """Run every loader (or only the named ones) and return the long table. A missing source file is an error."""
    parts = []
    for f in LOADERS:
        if only and f.__name__ not in only:
            continue
        d = f()
        parts.append(d)
        if verbose:
            print(f"  {f.__name__:28s} {len(d):>8,} rows  {d.condition.nunique():>3} conditions  "
                  f"{d.groupby(['pos','mut_aa']).ngroups:>6,} variants")
    m = pd.concat(parts, ignore_index=True)
    if verbose:
        print("  total", f"{len(m):,}")
    return m


if __name__ == "__main__":
    build(sys.argv[1:])
