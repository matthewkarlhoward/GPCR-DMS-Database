# ADRB2_Heydenreich2023

**Heydenreich 2023 (Babu)**, *Science* 2023. DOI: [10.1126/science.adh1859](https://doi.org/10.1126/science.adh1859)
β2AR (ADRB2, UniProt P07550). alanine scan. MaveDB: no.

- Cells: see paper (individually transfected mutants)
- Library: Alanine scan (412 mutants; native Ala → Gly)
- Method: Surface ELISA; Gs-activation BRET concentration–response with adrenaline
- Main score: Surface expression in % WT; Gs CRC amplitude (BRET units) with log10 EC50 in ec50_log
- Uncertainty: SEM
- Source: Science Table S1 as mirrored in Zenodo 15363336 (Heydenreich_* columns)

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
| `tables/heydenreich_columns_from_b2AR_all_data_annot.csv.gz` | 412 | 9 | 65% | Heydenreich Table S1 values mirrored by the GPCR-MAPS authors |

WT residues that differ from GPCRdb: `tables/heydenreich_columns_from_b2AR_all_data_annot.csv.gz`: R16 (GPCRdb G), Q27 (GPCRdb E)

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `b2AR_all_data_annot.csv.gz`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Heydenreich FM, Marti-Solano M, Sandhu M, Kobilka BK, Bouvier M, Babu MM. Molecular determinants of ligand efficacy and potency in GPCR signaling. Science. 2023;382(6677):eadh1859. doi:10.1126/science.adh1859

| | |
|---|---|
| Paper DOI | https://doi.org/10.1126/science.adh1859 |
| Article license | No reuse licence declared by the publisher (AAAS / Science) |
| Data obtained from | Science Table S1 values, taken from the columns prefixed Heydenreich_ in the Zenodo 15363336 deposit of Mighell et al. |
| Data location | https://zenodo.org/records/15363336 |
| **License on the data in this folder** | **CC BY 4.0 (the Zenodo deposit these columns were taken from)** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
