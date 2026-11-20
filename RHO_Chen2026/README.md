# RHO_Chen2026

**Chen 2026 (Chang)**, *PNAS* 2026. DOI: [10.1073/pnas.2624087123](https://doi.org/10.1073/pnas.2624087123)
Rho (RHO, UniProt P08100). DMS. MaveDB: no.

- Cells: see paper (cell-based multiphenotype assay)
- Library: ~2,000 single-residue substitutions incl. stop
- Method: Simultaneous basal activity, light-dependent signalling and receptor abundance
- Main score: Scaled scores as published in Dataset S2 (dark, light, abundance)
- Uncertainty: none published
- Source: PNAS Dataset S2 (pnas.2624087123.sd02.xlsx)

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
| `tables/Dataset_S1.csv.gz` | 105 | 8 | no positions | Sanger validation of library colonies |
| `tables/Dataset_S2.csv.gz` | 2,121 | 9 | 78% | all published columns incl. light/dark ratio |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `chen_sd01.xlsx`, `chen_sd02.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Chen SK, Liu J, Chang BSW. Deep mutational scanning of the GPCR rhodopsin reveals pleiotropic mutational effects and their roles in modulating receptor signaling. Proceedings of the National Academy of Sciences. 2026;123(44):e2624087123. doi:10.1073/pnas.2624087123

| | |
|---|---|
| Paper DOI | https://doi.org/10.1073/pnas.2624087123 |
| Article license | CC BY-NC-ND 4.0 (PNAS) — https://creativecommons.org/licenses/by-nc-nd/4.0/ |
| Data obtained from | PNAS supplementary Datasets S1 and S2 (pnas.2624087123.sd01.xlsx, sd02.xlsx) |
| Data location | https://doi.org/10.1073/pnas.2624087123 |
| **License on the data in this folder** | **CC BY-NC-ND 4.0. Non-commercial use only; no derivatives of the article. The files in source/ are unmodified; the tables/ versions add columns and are therefore adapted — a commercial user, or anyone needing a derivative, should obtain permission from PNAS or use source/ directly** |
| License text | https://creativecommons.org/licenses/by-nc-nd/4.0/ |
| Redistribution status | `permissive-with-conditions` — An open licence permits redistribution, with conditions a reuser must respect (see below). |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
