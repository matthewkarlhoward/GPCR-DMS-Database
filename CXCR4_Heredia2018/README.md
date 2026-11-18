# CXCR4_Heredia2018

**Heredia 2018 (Procko)**, *J Immunol* 2018. DOI: [10.4049/jimmunol.1800343](https://doi.org/10.4049/jimmunol.1800343)
CXCR4 (CXCR4, UniProt P61073). DMS. MaveDB: yes (urn:mavedb:00000048-a-1).

- Cells: Expi293F (pooled transfection)
- Library: Single amino-acid substitution library incl. stop
- Method: FACS sort for surface (anti-myc), CXCL12 binding, antibody 12G5 binding
- Main score: MaveDB score as deposited: log2 enrichment ratio, WT = 0
- Uncertainty: none deposited
- Source: MaveDB urn:mavedb:00000048

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
| `tables/mavedb_00000048-a-1.csv.gz` | 7,021 | 9 | 76% | nan |
| `tables/mavedb_00000048-b-1.csv.gz` | 7,021 | 7 | 76% | nan |
| `tables/mavedb_00000048-c-1.csv.gz` | 7,021 | 7 | 76% | nan |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `mavedb_00000048-a-1.csv`, `mavedb_00000048-b-1.csv`, `mavedb_00000048-c-1.csv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Heredia JD, Park J, Brubaker RJ, Szymanski SK, Gill KS, Procko E. Mapping Interaction Sites on Human Chemokine Receptors by Deep Mutational Scanning. The Journal of Immunology. 2018;200(11):3825-3839. doi:10.4049/jimmunol.1800343

| | |
|---|---|
| Paper DOI | https://doi.org/10.4049/jimmunol.1800343 |
| Article license | Oxford University Press standard publication reuse rights (The Journal of Immunology) — https://academic.oup.com/pages/standard-publication-reuse-rights |
| Data obtained from | MaveDB score sets urn:mavedb:00000048-a/-b/-c |
| Data location | https://www.mavedb.org/experiment-sets/urn:mavedb:00000048 |
| **License on the data in this folder** | **CC0 1.0 (public domain dedication)** |
| License text | https://creativecommons.org/publicdomain/zero/1.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
