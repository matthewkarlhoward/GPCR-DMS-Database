"""Study- and assay-level annotations for the GPCR master table.

Everything here is taken from the source papers, repositories and data files (see `source_url`). Fields left as
"see paper" were not stated in the material we read; nothing is filled in by guess.
"""
import re

# ---------------------------------------------------------------- per-study facts
STUDY = {
    "OPRM1_Howard2026": dict(
        cell_system="HEK293T landing-pad line, one variant per cell (pooled)",
        library="DIMPLE site-saturation library: missense, synonymous, 1–3-codon deletions and insertions",
        method="FACS sort-seq into bins; scores fitted with Lilace (Bayesian, sort-seq)",
        score_definition="Lilace posterior mean effect relative to synonymous variants (synonymous = 0). The cAMP reporter is "
                         "signal-down (Gi activation lowers cAMP and eGFP); signs are flipped in the source so negative = loss "
                         "of signalling or loss of surface expression. Dose-series columns are Lilace rescaled scores that the "
                         "Hill fits were fit to.",
        se_definition="score_se = Lilace posterior SD (saturating panel); dose series give a rescaled SD",
        source_url="https://github.com/matthewkarlhoward/HaloTag-MOR_DMS_analysis (supplementary_table/csv); MaveDB urn:mavedb:00001326"),
    "GPR68_Howard2025": dict(
        cell_system="HEK293T landing-pad line, one variant per cell (pooled)",
        library="DIMPLE site-saturation library: missense, synonymous, single deletions and insertions",
        method="FACS sort-seq; Enrich2-format output (score, SE, epsilon)",
        score_definition="Enrich2 score relative to wild type; synonymous ≈ 0, negative = less signalling or surface expression",
        se_definition="score_se = Enrich2 standard error",
        source_url="https://github.com/matthewkarlhoward/GPR68_DMS_Analysis (GPR68_DMS/figures/gpr68_scores_processed.csv); MaveDB urn:mavedb:00001207"),
    "GPR161_Howard2026": dict(
        cell_system="HEK293T landing-pad line, one variant per cell (pooled)",
        library="DIMPLE library: 10,032 missense, 503 synonymous, 508 single deletions",
        method="Three FACS assays: anti-FLAG surface stain; split-mNeonGreen2 whole-cell abundance; CRE-eGFP basal cAMP. Lilace scoring",
        score_definition="Lilace posterior mean effect, synonymous = 0, negative = less readout",
        se_definition="score_se = Lilace posterior SD",
        source_url="https://github.com/matthewkarlhoward/2026_GPR161_mutational_scan (data/scores); MaveDB urn:mavedb:00001323; Zenodo 23755947"),
    "MC4R_Howard2025": dict(
        cell_system="HEK293-derived reporter cells (Octant platform), barcoded variants (pooled)",
        library="Site-saturation library: 19 missense + stop at 332 positions (no synonymous)",
        method="Barcoded transcriptional reporters: CRE for Gs (DMS5, DMS11), UAS/Gq reporter (DMS8); negative-binomial GLMM per condition",
        score_definition="log2 fold change of reporter output, variant vs wild type, within each condition (model coefficient). "
                         "0 = WT-like; negative = less reporter output",
        se_definition="score_se = standard error of the log2 fold change",
        source_url="https://github.com/octantbio/mc4r-dms (sumstats/*unnormalized.tsv, sumstats/pipeline-outputs/dms11-combined.sumstats.tsv)"),
    "ADRB2_Jones2020": dict(
        cell_system="HEK293T, barcoded variants integrated (pooled)",
        library="Single amino-acid substitutions (7,800 of 7,828), no synonymous or stop",
        method="Barcoded CRE transcriptional reporter (RNA-seq of barcodes), normalised to forskolin-stimulated expression",
        score_definition="Reporter output normalised to the mean of frameshift (null) controls in the same condition, averaged over "
                         "2 repeats (paper.Rmd 'Norm'). 1 = frameshift-like; the WT-like value is the synonymous scalar in output/scalars.csv",
        se_definition="score_se = paper.Rmd 'Uncert' = 0.5·sqrt(Σ SD²/scale²) over repeats",
        source_url="https://github.com/KosuriLab/b2-dms (output/lib-med.csv.gz, output/scalars.csv)"),
    "ADRB2_Mighell2026": dict(
        cell_system="HEK293T Bxb1 landing pad (attB), one variant per cell (pooled)",
        library="Site-saturation library incl. synonymous, stop and deletions",
        method="GPCR-MAPS: HA-tag surface stain; TEV-protease transcriptional recruitment reporter (Gal4-UAS-Citrine) for Nb80 and β-arrestin",
        score_definition="Normalised score with replicates combined (source *_reps_comb / *_norm_comb_score); per-replicate scores, "
                         "read and barcode counts are in the same table",
        se_definition="score_se = SEM across replicates where given; dose-series points have no SE",
        source_url="https://zenodo.org/records/15363336 (b2AR_all_data_annot.csv.gz)"),
    "ADRB2_Heydenreich2023": dict(
        cell_system="see paper (individually transfected mutants)",
        library="Alanine scan (412 mutants; native Ala → Gly)",
        method="Surface ELISA; Gs-activation BRET concentration–response with adrenaline",
        score_definition="Surface expression in % WT; Gs CRC amplitude (BRET units) with log10 EC50 in ec50_log",
        se_definition="SEM",
        source_url="Science Table S1 as mirrored in Zenodo 15363336 (Heydenreich_* columns)"),
    "AVPR2_Mighell2025": dict(
        cell_system="HEK293T Bxb1 landing pad (attB), one variant per cell (pooled)",
        library="Site-saturation library incl. synonymous and stop",
        method="HA-tag surface-abundance sort-seq at 37 °C (DMSO), 27 °C, tolvaptan and compound 34",
        score_definition="Normalised surface score, replicates combined (source *_comb)",
        se_definition="score_se = SEM across replicates (*_sem)",
        source_url="https://zenodo.org/records/14216036 (v2R_all_exp_all_reps_com_and_norm.xlsx)"),
    "TAS1R2_Park2019": dict(
        cell_system="Expi293F (pooled transfection)",
        library="Single amino-acid substitution library incl. stop",
        method="FACS sort for T1R2 surface (anti-FLAG) or partner T1R3 co-surface (anti-myc); Enrich deep-sequencing pipeline",
        score_definition="log2 enrichment ratio (sorted vs naive library) with WT subtracted (WT = 0); floor −4",
        se_definition="score_se = |rep1 − rep2| / 2 (SEM, n = 2)",
        source_url="GEO GSE115751 (GSE115751_enrichment_ratios_T1R2.xlsx)"),
    "CXCR4_Gill2023": dict(
        cell_system="Expi293F (pooled transfection)",
        library="Single amino-acid substitution library incl. stop",
        method="FACS sort for myc surface stain or BiFC (Venus complementation with FLAG-WT-VN)",
        score_definition="log2 enrichment ratio (sorted vs naive) with WT subtracted (WT = 0); floor −3",
        se_definition="score_se = |rep1 − rep2| / 2 (SEM, n = 2)",
        source_url="GEO GSE125426 (GSE125426_X4R5_BiFC_enrichment_ratios.xlsx)"),
    "CCR5_Gill2023": dict(
        cell_system="Expi293F (pooled transfection)",
        library="Single amino-acid substitution library incl. stop",
        method="FACS sort for myc surface stain or BiFC (Venus complementation with FLAG-WT-VN)",
        score_definition="log2 enrichment ratio (sorted vs naive) with WT subtracted (WT = 0); floor −3",
        se_definition="score_se = |rep1 − rep2| / 2 (SEM, n = 2)",
        source_url="GEO GSE125426 (GSE125426_X4R5_BiFC_enrichment_ratios.xlsx)"),
    "CCR5_Heredia2018": dict(
        cell_system="Expi293F (pooled transfection)",
        library="Single amino-acid substitution library incl. stop",
        method="FACS sort for surface (anti-myc), antibody 2D7 binding, HIV gp120 binding",
        score_definition="MaveDB score as deposited: log2 enrichment ratio, WT = 0",
        se_definition="none deposited",
        source_url="MaveDB urn:mavedb:00000047"),
    "CXCR4_Heredia2018": dict(
        cell_system="Expi293F (pooled transfection)",
        library="Single amino-acid substitution library incl. stop",
        method="FACS sort for surface (anti-myc), CXCL12 binding, antibody 12G5 binding",
        score_definition="MaveDB score as deposited: log2 enrichment ratio, WT = 0",
        se_definition="none deposited",
        source_url="MaveDB urn:mavedb:00000048"),
    "RHO_Wan2019": dict(
        cell_system="see paper (pooled flow assay without barcodes)",
        library="210 curated rhodopsin variants (literature + diagnostic VUS) plus WT",
        method="Pooled flow-cytometry surface-expression sort, NGS readout",
        score_definition="MaveDB score as deposited (surface expression)",
        se_definition="none deposited (CI in source file)",
        source_url="MaveDB urn:mavedb:00000099"),
    "RHO_Manian2025": dict(
        cell_system="see paper",
        library="All 6,612 missense variants plus synonymous and stop",
        method="Surface-abundance immunoassay (method 1) and membrane-proximity assay (method 2)",
        score_definition="MaveDB score as deposited (trafficking score)",
        se_definition="score_se as deposited",
        source_url="MaveDB urn:mavedb:00001275"),
    "RHO_Chen2026": dict(
        cell_system="see paper (cell-based multiphenotype assay)",
        library="~2,000 single-residue substitutions incl. stop",
        method="Simultaneous basal activity, light-dependent signalling and receptor abundance",
        score_definition="Scaled scores as published in Dataset S2 (dark, light, abundance)",
        se_definition="none published",
        source_url="PNAS Dataset S2 (pnas.2624087123.sd02.xlsx)"),
    "RHO_McKee2021": dict(
        cell_system="HEK293T",
        library="700 variants in TM2 and TM7",
        method="DMS of plasma-membrane immunostaining at 27 °C vs 37 °C",
        score_definition="Ratio of surface-immunostaining intensity, 27 °C / 37 °C (1 = no temperature sensitivity)",
        se_definition="none published",
        source_url="JBC 2021 Table S1 (PMC8649220 mmc1.pdf)"),
    "RHO_Penn2020": dict(
        cell_system="HEK293T",
        library="808 variants in TM2 and TM7",
        method="DMS of plasma-membrane immunostaining ± 9-cis-retinal",
        score_definition="Ratio of surface-immunostaining intensity, +9-cis-retinal / −retinal (from McKee 2021 Table S1). Penn's "
                         "absolute −/+ scores were not released",
        se_definition="none published",
        source_url="JBC 2021 Table S1 (PMC8649220 mmc1.pdf); Penn SI has read counts only"),
    "RHO_Roushar2022": dict(
        cell_system="HEK293T",
        library="123 known pathogenic variants",
        method="Plasma-membrane immunostaining, apo and +9-cis-retinal",
        score_definition="Surface-immunostaining intensity (a.u.), mean",
        se_definition="score_se = SE as published",
        source_url="JBC 2022 Table S1 (PMC9399271 mmc1.pdf)"),
    "P2RY8_LaFlam2025": dict(
        cell_system="see paper",
        library="Near-saturation library (7,045 variants) incl. synonymous",
        method="Surface expression, migration and proliferation selections; Enrich2",
        score_definition="Enrich2 overall score (combined transductions), relative to WT",
        se_definition="score_se = Enrich2 overall SE",
        source_url="Cell Genomics Table S2 (mmc3.xlsx, PMC12648108)"),
    "AGTR1_Cao2023": dict(
        cell_system="see paper (individually transfected mutants)",
        library="Alanine scan of the full receptor (native Ala → Gly)",
        method="Surface ELISA; Gαq activation (PKC-C1b BRET) and β-arrestin2 recruitment (BRET) AngII CRCs; Gαq/Gβγ BRET validation",
        score_definition="Signalling: log(Emax/EC50) activity (ec50_log = log10 EC50 in M, emax = % WT). Expression: % WT",
        se_definition="SE as published (n = 3 unless noted)",
        source_url="Sci Signal Data files S1 and S4"),
    "AGTR1_Boora2026": dict(
        cell_system="see paper (individually transfected mutants; validation in Gq/11 or G12/13 KO cells)",
        library="Alanine scan of the full receptor",
        method="Gαq/11 and Gα12/13 activation biosensor CRCs with AngII",
        score_definition="log(Emax/EC50) activity; ec50_log = log10 EC50 (M); emax = % WT",
        se_definition="SE as published",
        source_url="bioRxiv 10.64898/2026.08.28.747882 Data S2 and S4"),
    "PTGFR_Boora2026": dict(
        cell_system="see paper (individually transfected mutants)",
        library="Alanine scan of the full receptor",
        method="Surface ELISA; Gαq/11 and Gα12/13 activation biosensor CRCs with PGF2α",
        score_definition="Signalling: log(Emax/EC50) activity (ec50_log, emax = % WT). Expression: % WT",
        se_definition="SE as published",
        source_url="bioRxiv 10.64898/2026.08.28.747882 Data S1 and S3"),
}

# ---------------------------------------------------------------- readout class from assay / condition text
RULES = [
    (r"whole-cell abundance|abundance$|^abundance|receptor abundance", "abundance (total)"),
    (r"surface|ELISA|immunostain|trafficking|membrane proximity|expression", "surface expression"),
    (r"binding", "ligand / antibody binding"),
    (r"BiFC|self-association", "self-association"),
    (r"migration|proliferation", "cell phenotype"),
    (r"cAMP|CRE|reporter|BRET|Gαq|Gq|Gs |Gs\)|G12|G13|Nb80|arrestin|signal|activation|light|dark", "signalling"),
]


def readout_class(assay, condition):
    s = f"{assay} | {condition}"
    if re.search(r"27 °C / 37 °C|retinal \(ratio\)", s):
        return "surface expression (ratio)"
    for pat, lab in RULES:
        if re.search(pat, s, re.I):
            return lab
    return "other"


DIRECTION = {
    "surface expression": "higher = more receptor at the cell surface",
    "surface expression (ratio)": "higher = larger gain in surface expression under the treatment (ratio > 1)",
    "abundance (total)": "higher = more total receptor",
    "signalling": "higher = more signalling output",
    "ligand / antibody binding": "higher = more binding",
    "self-association": "higher = more self-association (BiFC)",
    "cell phenotype": "higher = more of the phenotype (migration or proliferation)",
    "other": "see score_definition",
}
