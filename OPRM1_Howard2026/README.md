# OPRM1_Howard2026

**M. Howard 2026**, *bioRxiv* 2026. DOI: [10.64898/2026.10.12.758633](https://doi.org/10.64898/2026.10.12.758633)
µOR (OPRM1, UniProt P35372). DMS. MaveDB: yes (urn:mavedb:00001326).

- Cells: HEK293T landing-pad line, one variant per cell (pooled)
- Library: DIMPLE site-saturation library: missense, synonymous, 1–3-codon deletions and insertions
- Method: FACS sort-seq into bins; scores fitted with Lilace (Bayesian, sort-seq)
- Main score: Lilace posterior mean effect relative to synonymous variants (synonymous = 0). The cAMP reporter is signal-down (Gi activation lowers cAMP and eGFP); signs are flipped in the source so negative = loss of signalling or loss of surface expression. Dose-series columns are Lilace rescaled scores that the Hill fits were fit to.
- Uncertainty: score_se = Lilace posterior SD (saturating panel); dose series give a rescaled SD
- Source: https://github.com/matthewkarlhoward/HaloTag-MOR_DMS_analysis (supplementary_table/csv); MaveDB urn:mavedb:00001326

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
| `tables/01_variant_scores.csv.gz` | 10,178 | 106 | 66% | released supplementary table: saturating-dose scores, surface, Hill and operational fits, PCA |
| `tables/02_dose_response_scores.csv.gz` | 10,178 | 49 | 66% | released supplementary table: dose-series scores and SDs |
| `tables/DAMGO_drc.csv.gz` | 9,749 | 26 | 66% | DAMGO dose-series per-variant scores and curve classes |
| `tables/Fentanyl_wide_hill_ordinal_df.csv.gz` | 10,096 | 42 | 66% | fentanyl dose-series scores and Hill fits |
| `tables/Morphine_wide_hill_ordinal_df.csv.gz` | 10,106 | 42 | 66% | morphine dose-series scores and Hill fits |
| `tables/all_drug_scores_mapped_normalized.csv.gz` | 504,838 | 15 | 66% | 15-ligand Lilace output in raw, normalized and mapped forms (incl. MCAM) |
| `tables/composite_dms_scores.csv.gz` | 10,178 | 210 | 66% | analysis master table (211 columns), see COMPOSITE_SCORES_README.md |
| `tables/damgo_operational_fits.csv.gz` | 10,178 | 12 | 66% | operational-model fits |
| `tables/fentanyl_operational_fits.csv.gz` | 10,178 | 12 | 66% | operational-model fits |
| `tables/morphine_operational_fits.csv.gz` | 10,106 | 28 | 66% | operational-model fits |
| `tables/refit_3param_robust_damgo.csv.gz` | 10,178 | 19 | 66% | robust 3-parameter refits |
| `tables/refit_3param_robust_fentanyl.csv.gz` | 10,178 | 19 | 66% | robust 3-parameter refits |
| `tables/refit_3param_robust_morphine.csv.gz` | 10,178 | 19 | 66% | robust 3-parameter refits |
| `tables/surface_expression_scores.csv.gz` | 10,104 | 12 | 66% | surface Lilace output incl. position effects and discovery calls |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `01_variant_scores.csv`, `02_dose_response_scores.csv`, `DAMGO_drc.csv`, `Fentanyl_wide_hill_ordinal_df.csv`, `Morphine_wide_hill_ordinal_df.csv`, `all_drug_scores_mapped_normalized.tsv.gz`, `composite_dms_scores.csv`, `damgo_operational_fits.csv`, `fentanyl_operational_fits.csv`, `morphine_operational_fits.csv`, `refit_3param_robust_damgo.csv`, `refit_3param_robust_fentanyl.csv`, `refit_3param_robust_morphine.csv`, `supplementary_table_README.md`, `surface_expression_scores.tsv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Howard MK, Fine EJ, Srinivasan K, Richman DD, Freudenberg J, Weinberg Z, Rao J, Zou Z, Macdonald C, Grimes PR, Varga BR, Fraser JS, et al. Distinct activation mechanisms underlie ligand efficacy at a GPCR. bioRxiv. 2026. doi:10.64898/2026.10.12.758633

| | |
|---|---|
| Paper DOI | https://doi.org/10.64898/2026.10.12.758633 |
| Article license | CC BY 4.0 (bioRxiv preprint) |
| Data obtained from | Author GitHub repository matthewkarlhoward/HaloTag-MOR_DMS_analysis (supplementary_table/); also MaveDB urn:mavedb:00001326 |
| Data location | https://github.com/matthewkarlhoward/HaloTag-MOR_DMS_analysis |
| **License on the data in this folder** | **CC BY 4.0 (repository data licence); MaveDB score sets are CC0 1.0** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
