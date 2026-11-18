# AGTR1_Cao2023

**Cao 2023 (Heydenreich)**, *Sci Signal* 2023. DOI: [10.1126/scisignal.adf2173](https://doi.org/10.1126/scisignal.adf2173)
AT1R (AGTR1, UniProt P30556). alanine scan. MaveDB: no.

- Cells: see paper (individually transfected mutants)
- Library: Alanine scan of the full receptor (native Ala → Gly)
- Method: Surface ELISA; Gαq activation (PKC-C1b BRET) and β-arrestin2 recruitment (BRET) AngII CRCs; Gαq/Gβγ BRET validation
- Main score: Signalling: log(Emax/EC50) activity (ec50_log = log10 EC50 in M, emax = % WT). Expression: % WT
- Uncertainty: SE as published (n = 3 unless noted)
- Source: Sci Signal Data files S1 and S4

## tables/
Each table is one source table with all of the authors' columns, unchanged. Multi-row Excel headers are joined with ` | `. At the front, added:

- `receptor`, then `variant`, `pos`, `wt_aa`, `mut_aa`: the variant, parsed from the source identifier.
- GPCRdb numbering for `pos`:
  - `gpcrdb_generic`: GPCRdb display number, e.g. `3.50x50`.
  - `gpcrdb_x`: class-independent number for comparing receptors, e.g. `3x50`.
  - `bw`: Ballesteros–Weinstein number.
  - `segment`.
  - `gpcrdb_aa`: GPCRdb residue at that position.
  - `wt_matches_gpcrdb`: whether the study's WT residue agrees with GPCRdb.

Positions in termini and long loops have no generic number.

| table | rows | source columns | rows with generic number | contents |
|---|---|---|---|---|
| `tables/Data_file_S1_A_LogEC50_Emax_Table.csv.gz` | 360 | 17 | 74% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S1_B_Relative_Activity_and_bias.csv.gz` | 360 | 16 | 74% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S2_Fig1A_dLogEC50_Emax_RA.csv.gz` | 346 | 16 | 74% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S2_Fig1B_Bias.csv.gz` | 327 | 9 | 74% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2a_Gq_EC50.csv.gz` | 99 | 7 | 90% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2b_Gq_Emax.csv.gz` | 95 | 8 | 81% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2c_Gq_RA.csv.gz` | 99 | 7 | 90% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2d_barr_EC50.csv.gz` | 40 | 7 | 82% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2e_barr_Emax.csv.gz` | 79 | 7 | 82% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S3_Fig2f_barr_RA.csv.gz` | 56 | 7 | 82% | all columns; '*' after a mutant name is the authors' footnote marker |
| `tables/Data_file_S4_Gaq_Gbetagamma_sensor_fig_S8.csv.gz` | 321 | 8 | 74% | all columns; '*' after a mutant name is the authors' footnote marker |

WT residues that differ from GPCRdb: `tables/Data_file_S1_A_LogEC50_Emax_Table.csv.gz`: G160 (GPCRdb S); `tables/Data_file_S1_B_Relative_Activity_and_bias.csv.gz`: G160 (GPCRdb S)

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `adf2173_Data_file_S1.xlsx`, `adf2173_Data_file_S2.xlsx`, `adf2173_Data_file_S3.xlsx`, `adf2173_Data_file_S4.xlsx`, `adf2173_Data_file_S5.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Cao Y, van der Velden WJC, Namkung Y, Nivedha AK, Cho A, Sedki D, Holleran B, Lee N, Leduc R, Muk S, Le K, Bhattacharya S, et al. Unraveling allostery within the angiotensin II type 1 receptor for Gαq and β-arrestin coupling. Science Signaling. 2023;16(797):eadf2173. doi:10.1126/scisignal.adf2173

| | |
|---|---|
| Paper DOI | https://doi.org/10.1126/scisignal.adf2173 |
| Article license | No reuse licence declared; the article is not open access (AAAS / Science Signaling). © 2023 AAAS |
| Data obtained from | Science Signaling supplementary Data files S1–S5 |
| Data location | https://doi.org/10.1126/scisignal.adf2173 |
| **License on the data in this folder** | **Publisher copyright; no explicit data-reuse licence. Included here as the authors' published supplementary data, cited in full. AAAS permits reuse of supplementary data for non-commercial research; anything beyond that needs permission from AAAS** |
| License text | https://www.science.org/content/page/reuse-and-republication-permissions |
| Redistribution status | `cite-only` — No explicit data-reuse licence. Redistributed here as the authors' published supplementary data, fully cited; see the note below before reusing. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
