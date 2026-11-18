# RHO_Wan2019

**Wan 2019 (Comander)**, *Hum Mutat* 2019. DOI: [10.1002/humu.23762](https://doi.org/10.1002/humu.23762)
Rho (RHO, UniProt P08100). targeted panel. MaveDB: yes (urn:mavedb:00000099-a-1).

- Cells: see paper (pooled flow assay without barcodes)
- Library: 210 curated rhodopsin variants (literature + diagnostic VUS) plus WT
- Method: Pooled flow-cytometry surface-expression sort, NGS readout
- Main score: MaveDB score as deposited (surface expression)
- Uncertainty: none deposited (CI in source file)
- Source: MaveDB urn:mavedb:00000099

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
| `tables/mavedb_00000099-a-1.csv.gz` | 211 | 9 | 64% | nan |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `mavedb_00000099-a-1.csv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Wan A, Place E, Pierce EA, Comander J. Characterizing variants of unknown significance in rhodopsin: A functional genomics approach. Human Mutation. 2019;40(8):1127-1144. doi:10.1002/humu.23762

| | |
|---|---|
| Paper DOI | https://doi.org/10.1002/humu.23762 |
| Article license | CC BY-NC-ND 4.0 (Human Mutation, Wiley) — http://creativecommons.org/licenses/by-nc-nd/4.0/ |
| Data obtained from | MaveDB score set urn:mavedb:00000099-a-1 |
| Data location | https://www.mavedb.org/experiment-sets/urn:mavedb:00000099 |
| **License on the data in this folder** | **CC0 1.0 (public domain dedication). The authors' own MaveDB deposit carries CC0, so redistribution of the scores is unrestricted even though the article is ND** |
| License text | https://creativecommons.org/publicdomain/zero/1.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
