# RHO_Penn2020

**Penn 2020 (Schlebach)**, *Sci Adv* 2020. DOI: [10.1126/sciadv.aay7505](https://doi.org/10.1126/sciadv.aay7505)
Rho (RHO, UniProt P08100). DMS (TM2 + TM7). MaveDB: no.

- Cells: HEK293T
- Library: 808 variants in TM2 and TM7
- Method: DMS of plasma-membrane immunostaining ± 9-cis-retinal
- Main score: Ratio of surface-immunostaining intensity, +9-cis-retinal / −retinal (from McKee 2021 Table S1). Penn's absolute −/+ scores were not released
- Uncertainty: none published
- Source: JBC 2021 Table S1 (PMC8649220 mmc1.pdf); Penn SI has read counts only

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
Original files, unmodified: `aay7505_SM.pdf`, `supp_mckee_PMC8649220_mmc1.pdf`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Penn WD, McKee AG, Kuntz CP, Woods H, Nash V, Gruenhagen TC, Roushar FJ, Chandak M, Hemmerich C, Rusch DB, Meiler J, Schlebach JP. Probing biophysical sequence constraints within the transmembrane domains of rhodopsin by deep mutational scanning. Science Advances. 2020;6(10):eaay7505. doi:10.1126/sciadv.aay7505

| | |
|---|---|
| Paper DOI | https://doi.org/10.1126/sciadv.aay7505 |
| Article license | No reuse licence declared in Crossref (AAAS / Science Advances; Europe PMC records the article as CC BY) |
| Data obtained from | The ±9-cis-retinal ratios reported for Penn et al. variants in McKee et al. 2021 JBC Table S1 (CC BY 4.0). The Penn 2020 supplement itself releases sequencing counts only, which are out of scope here |
| Data location | https://doi.org/10.1016/j.jbc.2021.101359 |
| **License on the data in this folder** | **CC BY 4.0 (via the McKee 2021 open-access supplement that carries these values)** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
