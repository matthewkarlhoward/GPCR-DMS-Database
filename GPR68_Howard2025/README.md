# GPR68_Howard2025

**M. Howard 2025**, *Cell* 2025. DOI: [10.1016/j.cell.2024.11.036](https://doi.org/10.1016/j.cell.2024.11.036)
GPR68 (GPR68, UniProt Q15743). DMS. MaveDB: yes (urn:mavedb:00001207).

- Cells: HEK293T landing-pad line, one variant per cell (pooled)
- Library: DIMPLE site-saturation library: missense, synonymous, single deletions and insertions
- Method: FACS sort-seq; Enrich2-format output (score, SE, epsilon)
- Main score: Enrich2 score relative to wild type; synonymous ≈ 0, negative = less signalling or surface expression
- Uncertainty: score_se = Enrich2 standard error
- Source: https://github.com/matthewkarlhoward/GPR68_DMS_Analysis (GPR68_DMS/figures/gpr68_scores_processed.csv); MaveDB urn:mavedb:00001207

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
| `tables/GPR68_replicate_scores.csv.gz` | 8,971 | 10 | 73% | per-replicate scores (3 replicates x 3 conditions) |
| `tables/gpr68_scores_processed.csv.gz` | 9,258 | 14 | 73% | Enrich2 score, SE and epsilon per condition |
| `tables/ph55_GOF.csv.gz` | 361 | 2 | 73% | position-level summary used for structure colouring (no header in source) |
| `tables/ph55_LOF.csv.gz` | 364 | 2 | 73% | position-level summary used for structure colouring (no header in source) |
| `tables/ph65_GOF.csv.gz` | 361 | 2 | 73% | position-level summary used for structure colouring (no header in source) |
| `tables/ph65_LOF.csv.gz` | 364 | 2 | 73% | position-level summary used for structure colouring (no header in source) |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `GPR68_replicate_scores.tsv`, `gpr68_scores_processed.csv`, `ph55_GOF.tsv`, `ph55_LOF.tsv`, `ph65_GOF.tsv`, `ph65_LOF.tsv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Howard MK, Hoppe N, Huang XP, Mitrovic D, Billesbølle CB, Macdonald CB, Mehrotra E, Rockefeller Grimes P, Trinidad DD, Delemotte L, English JG, Coyote-Maestas W, et al. Molecular basis of proton sensing by G protein-coupled receptors. Cell. 2025;188(3):671-687.e20. doi:10.1016/j.cell.2024.11.036

| | |
|---|---|
| Paper DOI | https://doi.org/10.1016/j.cell.2024.11.036 |
| Article license | Elsevier open-access user licence (CC BY-NC-ND-equivalent terms for the article text) — http://www.elsevier.com/open-access/userlicense/1.0/ |
| Data obtained from | Author GitHub repository matthewkarlhoward/GPR68_DMS_Analysis; also MaveDB urn:mavedb:00001207 |
| Data location | https://github.com/matthewkarlhoward/GPR68_DMS_Analysis |
| **License on the data in this folder** | **MIT (repository); MaveDB score set CC0 1.0** |
| License text | https://opensource.org/licenses/MIT |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
