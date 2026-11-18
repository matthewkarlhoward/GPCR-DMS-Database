# RHO_Manian2025

**Manian 2026 (Comander)**, *Sci Adv* 2026. DOI: [10.1126/sciadv.aef3518](https://doi.org/10.1126/sciadv.aef3518)
Rho (RHO, UniProt P08100). DMS. MaveDB: yes (urn:mavedb:00001275-a-1).

- Cells: see paper
- Library: All 6,612 missense variants plus synonymous and stop
- Method: Surface-abundance immunoassay (method 1) and membrane-proximity assay (method 2)
- Main score: MaveDB score as deposited (trafficking score)
- Uncertainty: score_se as deposited
- Source: MaveDB urn:mavedb:00001275

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
| `tables/mavedb_00001275-a-1.csv.gz` | 7,246 | 8 | 75% | nan |
| `tables/mavedb_00001275-a-2.csv.gz` | 7,244 | 8 | 75% | nan |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `mavedb_00001275-a-1.csv`, `mavedb_00001275-a-2.csv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Manian KV, Ludwig CH, Zhao Y, Abell NS, Warneford-Thomson R, Chan H, Casey ZO, Yang X, Root DE, Albert ML, Comander J. A comprehensive map of missense trafficking variants in rhodopsin and their response to pharmacologic correction. Science Advances. 2026;12(31):eaef3518. doi:10.1126/sciadv.aef3518

| | |
|---|---|
| Paper DOI | https://doi.org/10.1126/sciadv.aef3518 |
| Article license | No reuse licence declared in Crossref (AAAS / Science Advances; the article is open access and Europe PMC records it as CC BY) |
| Data obtained from | MaveDB score sets urn:mavedb:00001275-a-1 and -a-2 |
| Data location | https://www.mavedb.org/experiment-sets/urn:mavedb:00001275 |
| **License on the data in this folder** | **CC0 1.0 (public domain dedication)** |
| License text | https://creativecommons.org/publicdomain/zero/1.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
