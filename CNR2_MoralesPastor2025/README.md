# CNR2_MoralesPastor2025

**Morales-Pastor 2025 (Selent / Veprintsev)**, *Nat Commun* 2025. DOI: [10.1038/s41467-025-60003-0](https://doi.org/10.1038/s41467-025-60003-0)
CB2 (CNR2, UniProt P34972). alanine scan. MaveDB: no.

- Cells: HEK293T, individually transfected mutants
- Library: Alanine scan of the full receptor (native Ala → Val). The paper reports 360 mutants; Supplementary Data 1 lists 359 (no row for position 298) plus a WT reference row
- Method: Surface expression; Gαi2 activation (Rap1GAP effector translocation) and β-arrestin1 recruitment, both by ebBRET (EMTA biosensors), concentration–response with the agonist HU-210; curves fitted with a Hill slope of 1, averaged over biological triplicates
- Main score: Surface expression in % WT; Emax and pEC50 for Gαi2 and β-arrestin1, raw and normalised (Emax corrected for expression and divided by WT; pEC50 given relative to WT, as described in the paper's methods); a coupling-profile class per mutant
- Uncertainty: none per mutant in this table (means of biological triplicates)
- Source: Nat Commun Supplementary Data 1 (`41467_2025_60003_MOESM3_ESM.xlsx`)

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
| `tables/MoralesPastor2025_SupplementaryData1.csv.gz` | 360 | 16 | 71% | Supplementary Data 1: expression, Emax correction factors, raw and normalised Gαi2 / β-arrestin1 Emax and pEC50, MD-simulated flag, coupling profile |

WT residues that differ from GPCRdb: none.

Notes on the values, all left as published:

- Where a mutant gave no measurable response, the authors entered 0 for its raw Emax and pEC50; the normalised pEC50 of those mutants then equals the WT pEC50 (e.g. D130A, Gαi2). Seven mutants have a blank pEC50 for one pathway.
- The sheet has one cell outside the table with no header (Q8 = 35). It is kept as `unlabelled_col_Q`.

`tables/INDEX.csv` lists every column of every table. The table is rebuilt from `source/` by `../code/build.py`, like every other study's.

## source/
Original files, unmodified: `41467_2025_60003_MOESM3_ESM.xlsx`

Not included: Supplementary Data 2–4 (molecular dynamics contact and network data, not per-mutant measurements) and the Source Data file. The MD trajectories are in GPCRmd (https://gpcrmd.org/dynadb/publications/1540/) and the analysis code in Zenodo 10.5281/zenodo.15270434.

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Morales-Pastor A, Miljuš T, Dieguez-Eceolaza M, Stępniewski TM, Ledesma-Martin V, Heydenreich FM, Flock T, Plouffe B, Le Gouill C, Duchaine J, Sykes DA, Nicholson C, Koers EJ, Guba W, Rufer AC, Grether U, Bouvier M, Veprintsev DB, Selent J. Multiple intramolecular triggers converge to preferential G protein coupling in the CB2R. Nature Communications. 2025;16:5265. doi:10.1038/s41467-025-60003-0

| | |
|---|---|
| Paper DOI | https://doi.org/10.1038/s41467-025-60003-0 |
| Article license | CC BY-NC-ND 4.0 (Nature Communications) |
| Data obtained from | Nat Commun Supplementary Data 1 (41467_2025_60003_MOESM3_ESM.xlsx) |
| Data location | https://doi.org/10.1038/s41467-025-60003-0 |
| **License on the data in this folder** | **CC BY-NC-ND 4.0** |
| License text | https://creativecommons.org/licenses/by-nc-nd/4.0/ |
| Redistribution status | `permissive-with-conditions` — An open licence permits redistribution, with conditions a reuser must respect (see below). |

CC BY-NC-ND 4.0: non-commercial use only, and no derivatives. The file in `source/` is unmodified; the
`tables/` version adds columns and is therefore adapted. A commercial user, or anyone needing a
derivative, should obtain permission from the authors / Springer Nature or use `source/` directly.

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
