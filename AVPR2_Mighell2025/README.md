# AVPR2_Mighell2025

**Mighell 2025 (Lehner)**, *Nat Struct Mol Biol* 2025. DOI: [10.1038/s41594-025-01659-6](https://doi.org/10.1038/s41594-025-01659-6)
V2R (AVPR2, UniProt P30518). DMS. MaveDB: no.

- Cells: HEK293T Bxb1 landing pad (attB), one variant per cell (pooled)
- Library: Site-saturation library incl. synonymous and stop
- Method: HA-tag surface-abundance sort-seq at 37 °C (DMSO), 27 °C, tolvaptan and compound 34
- Main score: Normalised surface score, replicates combined (source *_comb)
- Uncertainty: score_se = SEM across replicates (*_sem)
- Source: https://zenodo.org/records/14216036 (v2R_all_exp_all_reps_com_and_norm.xlsx)

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
| `tables/v2R_all_exp_all_reps_com_and_norm.csv.gz` | 7,791 | 70 | 73% | per-replicate normalised scores, cell and barcode counts, combined scores, annotations |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `v2R_all_exp.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Mighell TL, Lehner B. A small molecule stabilizer rescues the surface expression of nearly all missense variants in a GPCR. Nature Structural & Molecular Biology. 2025;32(12):2429-2440. doi:10.1038/s41594-025-01659-6

| | |
|---|---|
| Paper DOI | https://doi.org/10.1038/s41594-025-01659-6 |
| Article license | CC BY 4.0 (Nature Structural & Molecular Biology) |
| Data obtained from | Zenodo record 14216036 (v2R_all_exp_all_reps_com_and_norm.xlsx) |
| Data location | https://zenodo.org/records/14216036 |
| **License on the data in this folder** | **CC BY 4.0** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
