# RHO_Roushar2022

**Roushar 2022 (Schlebach)**, *J Biol Chem* 2022. DOI: [10.1016/j.jbc.2022.102266](https://doi.org/10.1016/j.jbc.2022.102266)
Rho (RHO, UniProt P08100). targeted panel. MaveDB: no.

- Cells: HEK293T
- Library: 123 known pathogenic variants
- Method: Plasma-membrane immunostaining, apo and +9-cis-retinal
- Main score: Surface-immunostaining intensity (a.u.), mean
- Uncertainty: score_se = SE as published
- Source: JBC 2022 Table S1 (PMC9399271 mmc1.pdf)

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
| `tables/Roushar2022_TableS1.csv.gz` | 123 | 7 | 65% | all columns of Table S1 |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `supp_roushar_PMC9399271_mmc1.pdf`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Roushar FJ, McKee AG, Kuntz CP, Ortega JT, Penn WD, Woods H, Chamness LM, Most V, Meiler J, Jastrzebska B, Schlebach JP. Molecular basis for variations in the sensitivity of pathogenic rhodopsin variants to 9-cis-retinal. Journal of Biological Chemistry. 2022;298(8):102266. doi:10.1016/j.jbc.2022.102266

| | |
|---|---|
| Paper DOI | https://doi.org/10.1016/j.jbc.2022.102266 |
| Article license | CC BY 4.0 (JBC; ASBMB open access) |
| Data obtained from | JBC supplementary Table S1 (PMC9399271 mmc1.pdf), parsed from the PDF table |
| Data location | https://doi.org/10.1016/j.jbc.2022.102266 |
| **License on the data in this folder** | **CC BY 4.0, as part of the open-access article** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
