"""Extract every per-variant table from every source file into clean CSVs, keeping all columns.

Output: raw_by_study/<study_id>/source_tables/<name>.csv.gz plus source_tables/INDEX.csv
Each table keeps the authors' columns verbatim (multi-row Excel headers are joined with ' | ') and gains four key
columns at the front, built the same way as in the master table:
  variant (identifier as in the master table), pos, wt_aa, mut_aa
Join to harmonized/gpcr_harmonized_variants on study_id + variant (or study_id + pos + wt_aa + mut_aa for substitutions).
"""
import re, subprocess
import numpy as np
import pandas as pd
from pathlib import Path
from build_master import split_var, parse_hgvs_pro, GH, UP, AA3

ROOT = Path(__file__).parent
OUT = ROOT / "raw_by_study"
INDEX = []


def uniq(cols):
    seen, out = {}, []
    for c in cols:
        c = str(c).strip() or "unnamed"
        n = seen.get(c, 0)
        out.append(c if n == 0 else f"{c} ({n + 1})")
        seen[c] = n + 1
    return out


def flat_xlsx(path, sheet, hdr_rows, data_row):
    raw = pd.read_excel(path, sheet_name=sheet, header=None)
    labs = []
    for j in range(raw.shape[1]):
        parts = []
        for r in hdr_rows:
            v = raw.iloc[r, :j + 1].ffill().iloc[-1] if r != hdr_rows[-1] else raw.iloc[r, j]
            if pd.notna(v) and str(v).strip() and str(v).strip() not in parts:
                parts.append(str(v).strip())
        labs.append(" | ".join(parts) if parts else f"col{j}")
    d = raw.iloc[data_row:].copy()
    d.columns = uniq(labs)
    d = d.dropna(how="all")
    return d.loc[:, d.notna().any()]


def keys_from_names(names):
    p = [split_var(str(v).strip().rstrip("*") if re.fullmatch(r"[A-Z]\d+[A-Z]\*+", str(v).strip()) else v) for v in names]
    return [a[1] for a in p], [a[0] for a in p], [a[2] for a in p]


def keys_from_hgvs_paren(h):
    """'p.(D2A)', 'p.(D2del)', 'p.(D2_S3insG)' -> pos, wt, mut (substitutions only; indels keep pos and wt)."""
    m = pd.Series(h).astype(str).str.extract(r"p\.\(?([A-Z])(\d+)(.*?)\)?$")
    mut = m[2].where(m[2].str.fullmatch(r"[A-Z*=]"), m[2].str.extract(r"(del|ins)", expand=False))
    mut = np.where(mut.eq("="), m[0], mut)
    return pd.to_numeric(m[1]).values, m[0].values, mut


def emit(sid, name, df, variant, pos, wt, mut, src, note=""):
    df = df.reset_index(drop=True).copy()
    front = pd.DataFrame({"variant": list(variant), "pos": list(pos), "wt_aa": list(wt), "mut_aa": list(mut)})
    df = pd.concat([front, df.drop(columns=[c for c in front.columns if c in df.columns])], axis=1)
    d = OUT / sid / "source_tables"
    d.mkdir(parents=True, exist_ok=True)
    df.to_csv(d / f"{name}.csv.gz", index=False)
    INDEX.append(dict(study_id=sid, table=f"source_tables/{name}.csv.gz", rows=len(df), columns=df.shape[1] - 4,
                      from_file=src, note=note, column_names=" ; ".join(map(str, df.columns[4:]))))


def mavedb(sid, urn):
    f = UP / f"mavedb_{urn}.csv"
    d = pd.read_csv(f)
    p = [parse_hgvs_pro(h) for h in d.hgvs_pro]
    emit(sid, f"mavedb_{urn}", d, d.hgvs_pro, [a[1] for a in p], [a[0] for a in p], [a[2] for a in p], f"MaveDB urn:mavedb:{urn} scores CSV")


def run():
    # ---------------- µOR
    S = GH / "HaloTag-MOR_DMS_analysis"
    for rel, note in [("supplementary_table/csv/01_variant_scores.csv", "released supplementary table: saturating-dose scores, surface, Hill and operational fits, PCA"),
                      ("supplementary_table/csv/02_dose_response_scores.csv", "released supplementary table: dose-series scores and SDs"),
                      ("data/dms_scores/composite_dms_scores.csv", "analysis master table (211 columns), see COMPOSITE_SCORES_README.md"),
                      ("data/dms_scores/surface/surface_expression_scores.tsv", "surface Lilace output incl. position effects and discovery calls"),
                      ("data/dms_scores/multidrug/all_drug_scores_mapped_normalized.tsv.gz", "15-ligand Lilace output in raw, normalized and mapped forms (incl. MCAM)"),
                      ("data/dms_scores/drc/DAMGO_drc.csv", "DAMGO dose-series per-variant scores and curve classes"),
                      ("data/dms_scores/drc/Fentanyl_wide_hill_ordinal_df.csv", "fentanyl dose-series scores and Hill fits"),
                      ("data/dms_scores/drc/Morphine_wide_hill_ordinal_df.csv", "morphine dose-series scores and Hill fits"),
                      ("data/curve_fits/refit_3param_robust_damgo.csv", "robust 3-parameter refits"),
                      ("data/curve_fits/refit_3param_robust_fentanyl.csv", "robust 3-parameter refits"),
                      ("data/curve_fits/refit_3param_robust_morphine.csv", "robust 3-parameter refits"),
                      ("data/operational_model/damgo_operational_fits.csv", "operational-model fits"),
                      ("data/operational_model/fentanyl_operational_fits.csv", "operational-model fits"),
                      ("data/operational_model/morphine_operational_fits.csv", "operational-model fits")]:
        d = pd.read_csv(S / rel, sep=None, engine="python")
        h = d["hgvs"] if "hgvs" in d else d["variant"]
        if "multidrug" in rel:
            h = d["hgvs"]
        pos, wt, mut = keys_from_hgvs_paren(h)
        emit("OPRM1_Howard2026", Path(rel).name.split(".")[0], d, h, pos, wt, mut, f"github HaloTag-MOR_DMS_analysis/{rel}", note)
    # ---------------- GPR68
    S = GH / "GPR68_DMS_Analysis/GPR68_DMS/figures"
    for fn in ["ph55_GOF.tsv", "ph55_LOF.tsv", "ph65_GOF.tsv", "ph65_LOF.tsv"]:
        d = pd.read_csv(S / fn, sep="\t", header=None, names=["position", "value"])
        emit("GPR68_Howard2025", fn.split(".")[0], d, [None] * len(d), d.position, [None] * len(d), [None] * len(d),
             f"github GPR68_DMS_Analysis/GPR68_DMS/figures/{fn}", "position-level summary used for structure colouring (no header in source)")
    for fn, note in [("gpr68_scores_processed.csv", "Enrich2 score, SE and epsilon per condition"),
                     ("GPR68_replicate_scores.tsv", "per-replicate scores (3 replicates x 3 conditions)")]:
        d = pd.read_csv(S / fn, sep=None, engine="python")
        pos, wt, mut = keys_from_hgvs_paren(d.hgvs)
        emit("GPR68_Howard2025", fn.split(".")[0], d, d.hgvs, pos, wt, mut, f"github GPR68_DMS_Analysis/GPR68_DMS/figures/{fn}", note)
    # ---------------- GPR161
    S = GH / "2026_GPR161_mutational_scan/data"
    for rel, note in [("scores/cre_variant_scores.tsv", "Lilace output, basal cAMP"), ("scores/surface_variant_scores.tsv", "Lilace output, surface"),
                      ("scores/abundance_variant_scores.tsv", "Lilace output, abundance"),
                      ("processed/merged_variant_scores.tsv", "all three assays merged, with position effects, z-scores and phenotype class")]:
        d = pd.read_csv(S / rel, sep="\t")
        if "hgvs" in d:
            pos, wt, mut = d.position, d.wildtype, d.mutation
            v = d.hgvs
        else:
            pos, wt, mut = d.position, d.wildtype, d.mutation
            v = [f"p.({w}{p}{m})" for w, p, m in zip(wt, pos, mut)]
        emit("GPR161_Howard2026", Path(rel).stem, d, v, pos, wt, mut, f"github 2026_GPR161_mutational_scan/data/{rel}", note)
    # ---------------- MC4R
    S = GH / "mc4r-dms"
    wtmap = pd.read_csv(S / "data/mc4r-wt.tsv", sep="\t").set_index("Pos").WT_AA_Short.to_dict()
    files = [("sumstats/MC4R-DMS5-Gs-unnormalized.tsv", "per-condition log2FC vs WT (Gs)"), ("sumstats/MC4R-DMS8-Gq-unnormalized.tsv", "per-condition log2FC vs WT (Gq)"),
             ("sumstats/MC4R-DMS5-Gs.tsv", "contrasts vs forskolin (Gs)"), ("sumstats/MC4R-DMS8-Gq.tsv", "contrasts vs untreated (Gq)"),
             ("sumstats/MC4R-DMS11-DefectSumstats.tsv", "DMS11 marginal defect ± Ipsen 17"), ("sumstats/MC4R-DMS11-RescueSumstats.tsv", "DMS11 chaperone rescue"),
             ("sumstats/pipeline-outputs/dms5-combined.sumstats.tsv", "full GLMM coefficient table, DMS5"),
             ("sumstats/pipeline-outputs/dms8-combined.sumstats.tsv", "full GLMM coefficient table, DMS8"),
             ("sumstats/pipeline-outputs/dms11-combined.sumstats.tsv", "full GLMM coefficient table, DMS11"),
             ("sumstats/pipeline-outputs/dms5-combined.marginals.tsv", "marginal means, DMS5"), ("sumstats/pipeline-outputs/dms8-combined.marginals.tsv", "marginal means, DMS8"),
             ("sumstats/pipeline-outputs/dms11-combined.marginals.tsv", "marginal means, DMS11"),
             ("sumstats/supp_table_2/Supplementary-Table-S2-variant-classifications.tsv", "Supplementary Table S2: variant classifications"),
             ("paper/mc4r-dms.tsv", "processed aMSH/THIQ x Gs/Gq table used in the paper")]
    for rel, note in files:
        d = pd.read_csv(S / rel, sep="\t")
        if "aa" in d:
            mut = d.aa.replace({"X": "*"})
        elif "mut_aa" in d:
            mut = d.mut_aa.replace({"X": "*"})
        elif "term" in d:
            mut = d.term.str.extract(r"mut_aa(.+)$")[0].replace({"X": "*"})
        else:
            mut = pd.Series([None] * len(d))
        pos = d["pos"] if "pos" in d else d.get("position", pd.Series([None] * len(d)))
        wt = pos.map(wtmap)
        v = [f"p.{w}{int(p)}{m}" if pd.notna(p) and isinstance(m, str) else None for w, p, m in zip(wt, pos, mut)]
        emit("MC4R_Howard2025", Path(rel).name.split(".")[0].replace("-combined", "_combined"), d, v, pos, wt, mut, f"github octantbio/mc4r-dms/{rel}", note)
    # ---------------- Jones β2AR
    S = GH / "b2-dms/output"
    jw = pd.read_parquet(ROOT / "gpcr_mutational_master.parquet", columns=["study_id", "pos", "wt_aa"])
    jw = jw[jw.study_id.eq("ADRB2_Jones2020")].dropna().drop_duplicates("pos").set_index("pos").wt_aa.to_dict()
    for fn, note in [("lib-med.csv.gz", "per condition x repeat x variant: median, MAD, mean, SD, CV, N of barcodes (pre-normalisation)"),
                     ("class-norm-int.csv.gz", "per condition x repeat x position x residue class"), ("negs-med.csv.gz", "frameshift / negative-control barcodes"),
                     ("scalars.csv", "per condition x repeat normalisation scalars (synonymous and frameshift)")]:
        d = pd.read_csv(S / fn)
        pos = d["Pos"] if "Pos" in d else pd.Series([None] * len(d))
        mut = d["AA"] if "AA" in d else pd.Series([None] * len(d))
        wt = pos.map(jw)
        v = [f"p.{w}{int(p)}{m}" if pd.notna(p) and isinstance(m, str) else None for w, p, m in zip(wt, pos, mut)]
        emit("ADRB2_Jones2020", fn.split(".")[0], d, v, pos, wt, mut, f"github KosuriLab/b2-dms/output/{fn}", note)
    # ---------------- MaveDB
    for sid, urns in [("CCR5_Heredia2018", ["00000047-a-1", "00000047-b-1", "00000047-c-1"]),
                      ("CXCR4_Heredia2018", ["00000048-a-1", "00000048-b-1", "00000048-c-1"]),
                      ("RHO_Wan2019", ["00000099-a-1"]), ("RHO_Manian2025", ["00001275-a-1", "00001275-a-2"])]:
        for u in urns:
            mavedb(sid, u)
    # ---------------- Procko GEO tables (Residue filled down; 'WT' marks the wild-type residue)
    def procko(sid, path, cols, name, note):
        raw = pd.read_excel(path, header=None)
        d = flat_xlsx(path, 0, [5, 6], 7).iloc[:, [c for c in range(len(cols))]] if False else None
        sub = raw.iloc[7:, cols].copy()
        hdr = [" | ".join(str(x) for x in raw.iloc[[5, 6], c].ffill().dropna()) or f"col{c}" for c in cols]
        sec = raw.iloc[5, cols].ffill().fillna("")
        hdr = [(f"{s} | {raw.iloc[6, c]}" if s else str(raw.iloc[6, c])) for s, c in zip(sec, cols)]
        sub.columns = uniq(hdr)
        sub = sub[sub.iloc[:, 1].notna()]
        res = sub.iloc[:, 0].ffill().astype(str)
        pos = res.str.extract(r"(\d+)")[0].astype(int)
        mut = sub.iloc[:, 1].astype(str)
        iswt = sub.iloc[:, 2].astype(str).eq("WT")
        wtm = pd.Series(mut[iswt].values, index=pos[iswt].values).groupby(level=0).first()
        wt = pos.map(wtm)
        v = [f"p.{w}{p}{m}" for w, p, m in zip(wt, pos, mut)]
        emit(sid, name, sub, v, pos, wt, mut, path.name, note)
    procko("TAS1R2_Park2019", UP / "GSE115751_enrichment_ratios_T1R2.xlsx", list(range(7)), "GSE115751_enrichment_ratios_T1R2",
           "naive-library frequency and per-replicate log2 enrichment ratios for both sorts")
    procko("CXCR4_Gill2023", UP / "GSE125426_X4R5_BiFC_enrichment_ratios.xlsx", list(range(7)), "GSE125426_CXCR4",
           "naive-library frequency and per-replicate log2 enrichment ratios (surface, BiFC)")
    procko("CCR5_Gill2023", UP / "GSE125426_X4R5_BiFC_enrichment_ratios.xlsx", list(range(8, 15)), "GSE125426_CCR5",
           "naive-library frequency and per-replicate log2 enrichment ratios (surface, BiFC)")
    # ---------------- Lehner lab
    v2 = pd.read_excel(UP / "v2R_all_exp.xlsx")
    v2 = v2.rename(columns={v2.columns[0]: "variant_id"})
    pos, wt, mut = keys_from_names(v2.variant_id)
    emit("AVPR2_Mighell2025", "v2R_all_exp_all_reps_com_and_norm", v2, v2.variant_id, pos, wt, mut,
         "Zenodo 14216036 v2R_all_exp_all_reps_com_and_norm.xlsx", "per-replicate normalised scores, cell and barcode counts, combined scores, annotations")
    b = pd.read_csv(UP / "b2AR_all_data_annot.csv.gz", low_memory=False)
    b = b.rename(columns={b.columns[0]: "variant_id"})
    pos, wt, mut = keys_from_names(b.variant_id)
    emit("ADRB2_Mighell2026", "b2AR_all_data_annot", b, b.variant_id, pos, wt, mut, "Zenodo 15363336 b2AR_all_data_annot.csv.gz",
         "per-replicate scores, reads, barcode counts, combined scores, dose series, Emax/EC50 fits, annotations")
    hcols = ["variant_id", "pos", "WT_aa", "mut_aa"] + [c for c in b.columns if c.startswith("Heydenreich")]
    hb = b.loc[b.Heydenreich_expression.notna(), hcols]
    pos, wt, mut = keys_from_names(hb.variant_id)
    emit("ADRB2_Heydenreich2023", "heydenreich_columns_from_b2AR_all_data_annot", hb, hb.variant_id, pos, wt, mut,
         "Zenodo 15363336 (Heydenreich_* columns)", "Heydenreich Table S1 values mirrored by the GPCR-MAPS authors")
    # ---------------- P2Y8
    f = next(UP.glob("supp_p2y8_*/mmc3.xlsx"))
    for sheet, hr, dr, note in [("2_Enrich2_Expression", [0, 1], 2, "Enrich2 per-transduction and overall scores and SE"),
                                ("3_Enrich2_Migration", [0, 1], 2, "Enrich2 per-transduction and overall scores and SE"),
                                ("4_Enrich2_Proliferation", [0, 1], 2, "Enrich2 per-transduction and overall scores and SE"),
                                ("5_DMS_Variant", [0], 1, "z-scores and expression-adjusted scores per variant"),
                                ("1_CodonCounts", [0, 1], 2, "codon-level read counts per sample (position x codon)")]:
        d = flat_xlsx(f, sheet, hr, dr)
        if sheet == "1_CodonCounts":
            raw = pd.read_excel(f, sheet_name=sheet, header=None)
            blocks, cur = [], None
            for i in range(len(raw)):
                v0 = raw.iat[i, 0]
                if isinstance(v0, str) and not str(v0).isdigit() and v0 != "Pos":
                    cur = v0
                elif v0 == "Pos":
                    hdrrow = raw.iloc[i].tolist()
                elif pd.notna(v0) and str(v0).isdigit():
                    rec = dict(zip(["Pos"] + hdrrow[1:], raw.iloc[i].tolist()))
                    rec["sample"] = cur
                    blocks.append(rec)
            d = pd.DataFrame(blocks)
            d = d[["sample"] + [c for c in d.columns if c != "sample"]]
            d = d.loc[:, d.columns.notna()]
            emit("P2RY8_LaFlam2025", "TableS2_1_CodonCounts", d, [None] * len(d), d.Pos, [None] * len(d), [None] * len(d),
                 f"Cell Genomics Table S2 (mmc3.xlsx) sheet {sheet}", "codon-level read counts per sample; one row per sample x position")
            continue
        name_col = d.columns[0]
        pos, wt, mut = keys_from_names(d[name_col] if sheet != "5_DMS_Variant" else d["full_var"])
        v = d[name_col] if sheet != "5_DMS_Variant" else d["full_var"]
        emit("P2RY8_LaFlam2025", f"TableS2_{sheet}", d, v, pos, wt, mut, f"Cell Genomics Table S2 (mmc3.xlsx) sheet {sheet}", note)
    d = flat_xlsx(f, "6_DMS_Position", [0], 1)
    emit("P2RY8_LaFlam2025", "TableS2_6_DMS_Position", d, [None] * len(d), d["pos"], d["wt_aa"], [None] * len(d),
         "Cell Genomics Table S2 (mmc3.xlsx) sheet 6_DMS_Position", "position-level summaries")
    # ---------------- Chen Rho
    d = pd.read_excel(UP / "chen_sd02.xlsx")
    d.columns = [str(c).strip() for c in d.columns]
    pos, wt, mut = keys_from_names(d.Variant)
    emit("RHO_Chen2026", "Dataset_S2", d, d.Variant, d.Position, wt, mut, "PNAS Dataset S2", "all published columns incl. light/dark ratio")
    d = flat_xlsx(UP / "chen_sd01.xlsx", 0, [1], 2)
    emit("RHO_Chen2026", "Dataset_S1", d, [None] * len(d), [None] * len(d), [None] * len(d), [None] * len(d), "PNAS Dataset S1",
         "Sanger validation of library colonies")
    # ---------------- McKee / Penn (PDF Table S1, all columns)
    txt = subprocess.run(["pdftotext", "-layout", str(next(UP.glob("supp_mckee_*/mmc1.pdf"))), "-"], capture_output=True, text=True).stdout
    rows = re.findall(r"^\s*([A-Z])\s+(\d+)\s+([A-Z*])\s+(-?[\d.]+|N/A|nan)\s+(-?[\d.]+|N/A|nan)\s+(-?[\d.]+|N/A|nan)\s+(-?[\d.]+|N/A|nan)\s+(-?[\d.]+|N/A|nan)\s+([+-])\s+([+-])", txt, re.M)
    d = pd.DataFrame(rows, columns=["WT", "Position", "Mutant", "Intensity (+Ret)/Intensity (-Ret)", "Intensity (27°C)/Intensity (37°C)",
                                    "Rosetta ΔΔG (REU)", "Cα distance to retinal centroid (Å)", "Biological hydrophobicity ΔΔG (kcal/mol)",
                                    "9-cis-retinal sensitivity", "Temperature sensitivity"]).drop_duplicates(["Position", "Mutant"])
    v = [f"p.{w}{p}{m}" for w, p, m in zip(d.WT, d.Position, d.Mutant)]
    for sid in ("RHO_McKee2021", "RHO_Penn2020"):
        emit(sid, "McKee2021_TableS1", d, v, d.Position.astype(int), d.WT, d.Mutant, "JBC 2021 Table S1 (mmc1.pdf), parsed with pdftotext",
             "all columns of Table S1; the +Ret/−Ret ratio is Penn 2020's data")
    # ---------------- Roushar (PDF Table S1)
    txt = subprocess.run(["pdftotext", "-layout", str(next(UP.glob("supp_roushar_*/mmc1.pdf"))), "-"], capture_output=True, text=True).stdout
    rows = re.findall(r"^\s*((?:del\s+)?[A-Z]\d+[A-Z*]?)\s{2,}(.+?)\s{2,}(\S.*?Class 2)\s+(\d+)\s*±\s*(\d+)\s+(\d+)\s*±\s*(\d+)\s*$", txt, re.M)
    d = pd.DataFrame(rows, columns=["Mutation", "Prior classification", "DMS classification", "Surface immunostaining intensity (apo)",
                                    "SE (apo)", "Surface immunostaining intensity (+Ret)", "SE (+Ret)"]).drop_duplicates("Mutation")
    m = d.Mutation.str.extract(r"(del\s+)?([A-Z])(\d+)([A-Z*])?")
    mut = np.where(m[0].notna(), "del", m[3])
    emit("RHO_Roushar2022", "Roushar2022_TableS1", d, d.Mutation, m[2].astype(int), m[1], mut, "JBC 2022 Table S1 (mmc1.pdf), parsed with pdftotext",
         "all columns of Table S1")
    # ---------------- Cao (all sheets of Data files S1–S4)
    for f in sorted(UP.glob("cao/*Data_file_S[1-4].xlsx")):
        x = pd.ExcelFile(f)
        for sh in x.sheet_names:
            raw = pd.read_excel(f, sheet_name=sh, header=None)
            # header block = rows before the first row whose mutant cell looks like a variant or 'WT'
            mcol = next(j for j in range(raw.shape[1]) if raw.iloc[:, j].astype(str).str.fullmatch(r"[A-Z]\d+[A-Z]\*?").sum() > 10)
            first = raw.index[raw.iloc[:, mcol].astype(str).str.fullmatch(r"(WT|[A-Z]\d+[A-Z]\*?)")][0]
            d = flat_xlsx(f, sh, list(range(0, first)), first)
            mname = d.columns[mcol] if mcol < len(d.columns) else d.columns[0]
            names = raw.iloc[first:, mcol].reindex(d.index).astype(str).str.strip()
            keep = names.ne("nan")
            d, names = d[keep], names[keep]
            pos, wt, mut = keys_from_names(names.str.replace(r"\*+$", "", regex=True))
            emit("AGTR1_Cao2023", f"{f.stem.split('_', 1)[1]}_{re.sub(r'[^A-Za-z0-9]+', '_', sh).strip('_')}", d, names, pos, wt, mut,
                 f"Sci Signal {f.name} sheet '{sh}'", "all columns; '*' after a mutant name is the authors' footnote marker")
    # ---------------- Boora (Data S1–S4)
    for fn, sid, hr, dr, mcol, label in [("boora_media-1.xlsx", "PTGFR_Boora2026", [0, 1, 2], 3, 4, "Data S1"),
                                         ("boora_media-2.xlsx", "AGTR1_Boora2026", [0, 1, 2], 3, 4, "Data S2"),
                                         ("boora_media-3.xlsx", "PTGFR_Boora2026", [0, 1, 2, 3], 4, 3, "Data S3"),
                                         ("boora_media-4.xlsx", "AGTR1_Boora2026", [0, 1, 2, 3], 4, 3, "Data S4")]:
        d = flat_xlsx(UP / fn, 0, hr, dr)
        names = d.iloc[:, mcol].astype(str).str.strip()
        d = d[names.ne("nan")]
        names = names[names.ne("nan")]
        pos, wt, mut = keys_from_names(names.str.replace(r"\*+$", "", regex=True))
        emit(sid, f"Boora2026_{label.replace(' ', '')}", d, names, pos, wt, mut, f"bioRxiv {label} ({fn.replace('boora_', '')})", "all columns incl. FDR tests and effect classes")
    idx = pd.DataFrame(INDEX)
    for sid, g in idx.groupby("study_id"):
        g.drop(columns="study_id").to_csv(OUT / sid / "source_tables" / "INDEX.csv", index=False)
    idx.to_csv(ROOT / "source_tables_index.csv", index=False)
    print(idx.groupby("study_id").agg(tables=("table", "size"), rows=("rows", "sum"), cols=("columns", "sum")).to_string())


if __name__ == "__main__":
    run()
