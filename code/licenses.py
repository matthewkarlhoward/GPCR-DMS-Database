"""Per-study citation + licensing, stated individually. Checked 2026-11-18."""

# Crossref metadata lives in reference/crossref_citations.json; DOI per study:
DOI = {
    "OPRM1_Howard2026": "10.64898/2026.10.12.758633",
    "GPR68_Howard2025": "10.1016/j.cell.2024.11.036",
    "GPR161_Howard2026": "10.64898/2026.10.30.762644",
    "MC4R_Howard2025": "10.7554/eLife.104725",
    "ADRB2_Jones2020": "10.7554/eLife.54895",
    "ADRB2_Mighell2026": "10.1038/s41594-026-01907-3",
    "ADRB2_Heydenreich2023": "10.1126/science.adh1859",
    "AVPR2_Mighell2025": "10.1038/s41594-025-01659-6",
    "TAS1R2_Park2019": "10.1074/jbc.RA118.006173",
    "CCR5_Gill2023": "10.1016/j.jbc.2023.105229",
    "CXCR4_Gill2023": "10.1016/j.jbc.2023.105229",
    "CCR5_Heredia2018": "10.4049/jimmunol.1800343",
    "CXCR4_Heredia2018": "10.4049/jimmunol.1800343",
    "P2RY8_LaFlam2025": "10.1016/j.xgen.2025.100981",
    "RHO_Manian2025": "10.1126/sciadv.aef3518",
    "RHO_Chen2026": "10.1073/pnas.2624087123",
    "CNR2_MoralesPastor2025": "10.1038/s41467-025-60003-0",
    "RHO_McKee2021": "10.1016/j.jbc.2021.101359",
    "RHO_Penn2020": "10.1126/sciadv.aay7505",
    "RHO_Roushar2022": "10.1016/j.jbc.2022.102266",
    "RHO_Wan2019": "10.1002/humu.23762",
    "AGTR1_Cao2023": "10.1126/scisignal.adf2173",
    "AGTR1_Boora2026": "10.64898/2026.08.28.747882",
    "PTGFR_Boora2026": "10.64898/2026.08.28.747882",
}

# article_license: the reuse licence Crossref/the publisher states for the paper itself.
# data: where the numbers in this folder came from.
# data_license: the licence that governs those numbers, and what it requires of a redistributor.
# status: "clear" = an open licence explicitly permits redistribution;
#         "permissive-with-conditions" = open licence with a restriction a reuser must respect (NC / ND);
#         "cite-only" = no reuse licence declared; included as published supplementary data, cited in full.
L = {
    "OPRM1_Howard2026": dict(
        article_license="CC BY 4.0 (bioRxiv preprint)",
        data="Author GitHub repository matthewkarlhoward/HaloTag-MOR_DMS_analysis (supplementary_table/); also MaveDB urn:mavedb:00001326",
        data_url="https://github.com/matthewkarlhoward/HaloTag-MOR_DMS_analysis",
        data_license="CC BY 4.0 (repository data licence); MaveDB score sets are CC0 1.0",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "GPR68_Howard2025": dict(
        article_license="Elsevier open-access user licence (CC BY-NC-ND-equivalent terms for the article text)",
        article_license_url="http://www.elsevier.com/open-access/userlicense/1.0/",
        data="Author GitHub repository matthewkarlhoward/GPR68_DMS_Analysis; also MaveDB urn:mavedb:00001207",
        data_url="https://github.com/matthewkarlhoward/GPR68_DMS_Analysis",
        data_license="MIT (repository); MaveDB score set CC0 1.0",
        data_license_url="https://opensource.org/licenses/MIT",
        status="clear"),
    "GPR161_Howard2026": dict(
        article_license="CC BY 4.0 (bioRxiv preprint)",
        data="Author GitHub repository matthewkarlhoward/2026_GPR161_mutational_scan (data/scores); also MaveDB urn:mavedb:00001323 and Zenodo 23755947",
        data_url="https://github.com/matthewkarlhoward/2026_GPR161_mutational_scan",
        data_license="CC BY 4.0 (repository LICENSE-DATA); repository code MIT; MaveDB score sets CC0 1.0",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "MC4R_Howard2025": dict(
        article_license="CC BY 4.0 (eLife)",
        data="Octant GitHub repository octantbio/mc4r-dms (sumstats/)",
        data_url="https://github.com/octantbio/mc4r-dms",
        data_license="MIT",
        data_license_url="https://opensource.org/licenses/MIT",
        status="clear"),
    "ADRB2_Jones2020": dict(
        article_license="CC BY 4.0 (eLife)",
        data="Kosuri lab GitHub repository KosuriLab/b2-dms (output/)",
        data_url="https://github.com/KosuriLab/b2-dms",
        data_license="MIT",
        data_license_url="https://opensource.org/licenses/MIT",
        status="clear"),
    "ADRB2_Mighell2026": dict(
        article_license="CC BY 4.0 (Nature Structural & Molecular Biology)",
        data="Zenodo record 15363336 (b2AR_all_data_annot.csv.gz)",
        data_url="https://zenodo.org/records/15363336",
        data_license="CC BY 4.0",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "ADRB2_Heydenreich2023": dict(
        article_license="No reuse licence declared by the publisher (AAAS / Science)",
        data="Science Table S1 values, taken from the columns prefixed Heydenreich_ in the Zenodo 15363336 deposit of Mighell et al.",
        data_url="https://zenodo.org/records/15363336",
        data_license="CC BY 4.0 (the Zenodo deposit these columns were taken from)",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "AVPR2_Mighell2025": dict(
        article_license="CC BY 4.0 (Nature Structural & Molecular Biology)",
        data="Zenodo record 14216036 (v2R_all_exp_all_reps_com_and_norm.xlsx)",
        data_url="https://zenodo.org/records/14216036",
        data_license="CC BY 4.0",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "TAS1R2_Park2019": dict(
        article_license="CC BY 4.0 (JBC; ASBMB open access)",
        data="GEO series GSE115751 (GSE115751_enrichment_ratios_T1R2.xlsx)",
        data_url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115751",
        data_license="NCBI GEO: no restrictions on use or redistribution of the data; cite the source",
        data_license_url="https://www.ncbi.nlm.nih.gov/home/about/policies/",
        status="clear"),
    "CCR5_Gill2023": dict(
        article_license="CC BY 4.0 (JBC; ASBMB open access)",
        data="GEO series GSE125426 (GSE125426_X4R5_BiFC_enrichment_ratios.xlsx)",
        data_url="https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125426",
        data_license="NCBI GEO: no restrictions on use or redistribution of the data; cite the source",
        data_license_url="https://www.ncbi.nlm.nih.gov/home/about/policies/",
        status="clear"),
    "CCR5_Heredia2018": dict(
        article_license="Oxford University Press standard publication reuse rights (The Journal of Immunology)",
        article_license_url="https://academic.oup.com/pages/standard-publication-reuse-rights",
        data="MaveDB score sets urn:mavedb:00000047-a/-b/-c",
        data_url="https://www.mavedb.org/experiment-sets/urn:mavedb:00000047",
        data_license="CC0 1.0 (public domain dedication)",
        data_license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        status="clear"),
    "P2RY8_LaFlam2025": dict(
        article_license="CC BY 4.0 (Cell Genomics)",
        data="Cell Genomics supplementary Tables S1–S2 (mmc2.xlsx, mmc3.xlsx)",
        data_url="https://doi.org/10.1016/j.xgen.2025.100981",
        data_license="CC BY 4.0, as part of the open-access article",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "RHO_Manian2025": dict(
        article_license="No reuse licence declared in Crossref (AAAS / Science Advances; the article is open access and Europe PMC records it as CC BY)",
        data="MaveDB score sets urn:mavedb:00001275-a-1 and -a-2",
        data_url="https://www.mavedb.org/experiment-sets/urn:mavedb:00001275",
        data_license="CC0 1.0 (public domain dedication)",
        data_license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        status="clear"),
    "CNR2_MoralesPastor2025": dict(
        article_license="CC BY-NC-ND 4.0 (Nature Communications)",
        article_license_url="https://creativecommons.org/licenses/by-nc-nd/4.0/",
        data="Nat Commun Supplementary Data 1 (41467_2025_60003_MOESM3_ESM.xlsx)",
        data_url="https://doi.org/10.1038/s41467-025-60003-0",
        data_license="CC BY-NC-ND 4.0. Non-commercial use only; no derivatives of the article. The file in source/ is unmodified; the tables/ version adds columns and is therefore adapted — a commercial user, or anyone needing a derivative, should obtain permission from the authors / Springer Nature or use source/ directly",
        data_license_url="https://creativecommons.org/licenses/by-nc-nd/4.0/",
        status="permissive-with-conditions"),
    "RHO_Chen2026": dict(
        article_license="CC BY-NC-ND 4.0 (PNAS)",
        article_license_url="https://creativecommons.org/licenses/by-nc-nd/4.0/",
        data="PNAS supplementary Datasets S1 and S2 (pnas.2624087123.sd01.xlsx, sd02.xlsx)",
        data_url="https://doi.org/10.1073/pnas.2624087123",
        data_license="CC BY-NC-ND 4.0. Non-commercial use only; no derivatives of the article. The files in source/ are unmodified; the tables/ versions add columns and are therefore adapted — a commercial user, or anyone needing a derivative, should obtain permission from PNAS or use source/ directly",
        data_license_url="https://creativecommons.org/licenses/by-nc-nd/4.0/",
        status="permissive-with-conditions"),
    "RHO_McKee2021": dict(
        article_license="CC BY 4.0 (JBC; ASBMB open access)",
        data="JBC supplementary Table S1 (PMC8649220 mmc1.pdf), parsed from the PDF table",
        data_url="https://doi.org/10.1016/j.jbc.2021.101359",
        data_license="CC BY 4.0, as part of the open-access article",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "RHO_Penn2020": dict(
        article_license="No reuse licence declared in Crossref (AAAS / Science Advances; Europe PMC records the article as CC BY)",
        data="The ±9-cis-retinal ratios reported for Penn et al. variants in McKee et al. 2021 JBC Table S1 (CC BY 4.0). The Penn 2020 supplement itself releases sequencing counts only, which are out of scope here",
        data_url="https://doi.org/10.1016/j.jbc.2021.101359",
        data_license="CC BY 4.0 (via the McKee 2021 open-access supplement that carries these values)",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "RHO_Roushar2022": dict(
        article_license="CC BY 4.0 (JBC; ASBMB open access)",
        data="JBC supplementary Table S1 (PMC9399271 mmc1.pdf), parsed from the PDF table",
        data_url="https://doi.org/10.1016/j.jbc.2022.102266",
        data_license="CC BY 4.0, as part of the open-access article",
        data_license_url="https://creativecommons.org/licenses/by/4.0/",
        status="clear"),
    "RHO_Wan2019": dict(
        article_license="CC BY-NC-ND 4.0 (Human Mutation, Wiley)",
        article_license_url="http://creativecommons.org/licenses/by-nc-nd/4.0/",
        data="MaveDB score set urn:mavedb:00000099-a-1",
        data_url="https://www.mavedb.org/experiment-sets/urn:mavedb:00000099",
        data_license="CC0 1.0 (public domain dedication). The authors' own MaveDB deposit carries CC0, so redistribution of the scores is unrestricted even though the article is ND",
        data_license_url="https://creativecommons.org/publicdomain/zero/1.0/",
        status="clear"),
    "AGTR1_Cao2023": dict(
        article_license="No reuse licence declared; the article is not open access (AAAS / Science Signaling). © 2023 AAAS",
        data="Science Signaling supplementary Data files S1–S5",
        data_url="https://doi.org/10.1126/scisignal.adf2173",
        data_license="Publisher copyright; no explicit data-reuse licence. Included here as the authors' published supplementary data, cited in full. AAAS permits reuse of supplementary data for non-commercial research; anything beyond that needs permission from AAAS",
        data_license_url="https://www.science.org/content/page/reuse-and-republication-permissions",
        status="cite-only"),
    "AGTR1_Boora2026": dict(
        article_license="CC BY-NC 4.0 (bioRxiv preprint)",
        article_license_url="http://creativecommons.org/licenses/by-nc/4.0/",
        data="bioRxiv supplementary Data S2 and S4",
        data_url="https://doi.org/10.64898/2026.08.28.747882",
        data_license="CC BY-NC 4.0. Non-commercial use only; adaptation allowed with credit",
        data_license_url="http://creativecommons.org/licenses/by-nc/4.0/",
        status="permissive-with-conditions"),
}
L["CXCR4_Gill2023"] = dict(L["CCR5_Gill2023"])
L["CXCR4_Heredia2018"] = dict(L["CCR5_Heredia2018"],
                              data="MaveDB score sets urn:mavedb:00000048-a/-b/-c",
                              data_url="https://www.mavedb.org/experiment-sets/urn:mavedb:00000048")
L["PTGFR_Boora2026"] = dict(L["AGTR1_Boora2026"], data="bioRxiv supplementary Data S1 and S3")

STATUS_NOTE = {
    "clear": "An open licence explicitly permits redistribution of these numbers.",
    "permissive-with-conditions": "An open licence permits redistribution, with conditions a reuser must respect (see below).",
    "cite-only": "No explicit data-reuse licence. Redistributed here as the authors' published supplementary data, fully cited; see the note below before reusing.",
}

GPCRDB = dict(
    name="GPCRdb",
    url="https://gpcrdb.org",
    license="CC BY 4.0",
    license_url="https://creativecommons.org/licenses/by/4.0/",
    cite=["Pándy-Szekeres G, Caroli J, Mamyrbekov A, Kermani AA, Keserű GM, Kooistra AJ, Gloriam DE. "
          "GPCRdb in 2023: state-specific structure models using AlphaFold2 and new ligand resources. "
          "Nucleic Acids Res. 2023;51(D1):D395–D402. doi:10.1093/nar/gkac1013",
          "Isberg V, de Graaf C, Bortolato A, Cherezov V, Katritch V, Marshall FH, Mordalski S, Pin J-P, "
          "Stevens RC, Vriend G, Gloriam DE. Generic GPCR residue numbers – aligning topology maps while "
          "minding the gaps. Trends Pharmacol Sci. 2015;36(1):22–31. doi:10.1016/j.tips.2014.11.001"],
    ack="We acknowledge the use of the GPCRdb database (https://www.gpcrdb.org).")

MAVEDB_CITE = ("Rubin AF, Stone J, Bianchi AH, Capodanno BJ, Da EY, Dias M, Esposito D, Frazer J, Fu Y, "
               "Grosse SM, et al. MaveDB 2024: a curated community database with over seven million "
               "variant effects from multiplexed functional assays. Genome Biol. 2025;26:13. "
               "doi:10.1186/s13059-025-03476-y")
