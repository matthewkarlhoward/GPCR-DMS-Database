# RHO_McKee2021

**McKee 2021 (Schlebach)**, *J Biol Chem* 2021. DOI: [10.1016/j.jbc.2021.101359](https://doi.org/10.1016/j.jbc.2021.101359)
Rho (RHO, UniProt P08100). DMS (TM2 + TM7). MaveDB: no.

- Cells: HEK293T
- Library: 700 variants in TM2 and TM7
- Method: DMS of plasma-membrane immunostaining at 27 °C vs 37 °C
- Main score: Ratio of surface-immunostaining intensity, 27 °C / 37 °C (1 = no temperature sensitivity)
- Uncertainty: none published
- Source: JBC 2021 Table S1 (PMC8649220 mmc1.pdf)

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
| `tables/McKee2021_TableS1.csv.gz` | 700 | 10 | 100% | all columns of Table S1; the +Ret/−Ret ratio is Penn 2020's data |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `supp_mckee_PMC8649220_mmc1.pdf`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> McKee AG, Kuntz CP, Ortega JT, Woods H, Most V, Roushar FJ, Meiler J, Jastrzebska B, Schlebach JP. Systematic profiling of temperature- and retinal-sensitive rhodopsin variants by deep mutational scanning. Journal of Biological Chemistry. 2021;297(6):101359. doi:10.1016/j.jbc.2021.101359

| | |
|---|---|
| Paper DOI | https://doi.org/10.1016/j.jbc.2021.101359 |
| Article license | CC BY 4.0 (JBC; ASBMB open access) |
| Data obtained from | JBC supplementary Table S1 (PMC8649220 mmc1.pdf), parsed from the PDF table |
| Data location | https://doi.org/10.1016/j.jbc.2021.101359 |
| **License on the data in this folder** | **CC BY 4.0, as part of the open-access article** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
