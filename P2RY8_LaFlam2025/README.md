# P2RY8_LaFlam2025

**LaFlam 2025**, *Cell Genom* 2025. DOI: [10.1016/j.xgen.2025.100981](https://doi.org/10.1016/j.xgen.2025.100981)
P2Y8 (P2RY8, UniProt Q86VZ1). DMS. MaveDB: no.

- Cells: see paper
- Library: Near-saturation library (7,045 variants) incl. synonymous
- Method: Surface expression, migration and proliferation selections; Enrich2
- Main score: Enrich2 overall score (combined transductions), relative to WT
- Uncertainty: score_se = Enrich2 overall SE
- Source: Cell Genomics Table S2 (mmc3.xlsx, PMC12648108)

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
| `tables/TableS2_1_CodonCounts.csv.gz` | 13,962 | 69 | 71% | codon-level read counts per sample; one row per sample x position |
| `tables/TableS2_2_Enrich2_Expression.csv.gz` | 7,046 | 12 | 71% | Enrich2 per-transduction and overall scores and SE |
| `tables/TableS2_3_Enrich2_Migration.csv.gz` | 7,046 | 12 | 71% | Enrich2 per-transduction and overall scores and SE |
| `tables/TableS2_4_Enrich2_Proliferation.csv.gz` | 7,046 | 12 | 71% | Enrich2 per-transduction and overall scores and SE |
| `tables/TableS2_5_DMS_Variant.csv.gz` | 7,045 | 9 | 71% | z-scores and expression-adjusted scores per variant |
| `tables/TableS2_6_DMS_Position.csv.gz` | 353 | 10 | 71% | position-level summaries |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `supp_p2y8_PMC12648108_mmc2.xlsx`, `supp_p2y8_PMC12648108_mmc3.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> LaFlam TN, Billesbølle CB, Dinh T, Wolfreys FD, Lu E, Matteson T, An J, Xu Y, Singhal A, Brandes N, Ntranos V, Manglik A, et al. Phenotypic pleiotropy of missense variants in human B cell confinement receptor P2RY8. Cell Genomics. 2025;5(11):100981. doi:10.1016/j.xgen.2025.100981

| | |
|---|---|
| Paper DOI | https://doi.org/10.1016/j.xgen.2025.100981 |
| Article license | CC BY 4.0 (Cell Genomics) |
| Data obtained from | Cell Genomics supplementary Tables S1–S2 (mmc2.xlsx, mmc3.xlsx) |
| Data location | https://doi.org/10.1016/j.xgen.2025.100981 |
| **License on the data in this folder** | **CC BY 4.0, as part of the open-access article** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
