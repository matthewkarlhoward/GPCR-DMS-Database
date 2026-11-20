# GPR161_Howard2026

**M. Howard 2026 (Coyote-Maestas)**, *bioRxiv* 2026. DOI: [10.64898/2026.10.30.762644](https://doi.org/10.64898/2026.10.30.762644)
GPR161 (GPR161, UniProt Q8N6U8). DMS. MaveDB: yes (urn:mavedb:00001323).

- Cells: HEK293T landing-pad line, one variant per cell (pooled)
- Library: DIMPLE library: 10,032 missense, 503 synonymous, 508 single deletions
- Method: Three FACS assays: anti-FLAG surface stain; split-mNeonGreen2 whole-cell abundance; CRE-eGFP basal cAMP. Lilace scoring
- Main score: Lilace posterior mean effect, synonymous = 0, negative = less readout
- Uncertainty: score_se = Lilace posterior SD
- Source: https://github.com/matthewkarlhoward/2026_GPR161_mutational_scan (data/scores); MaveDB urn:mavedb:00001323; Zenodo 23755947

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
| `tables/abundance_variant_scores.csv.gz` | 10,954 | 17 | 50% | Lilace output, abundance |
| `tables/cre_variant_scores.csv.gz` | 10,973 | 17 | 50% | Lilace output, basal cAMP |
| `tables/merged_variant_scores.csv.gz` | 10,927 | 23 | 50% | all three assays merged, with position effects, z-scores and phenotype class |
| `tables/surface_variant_scores.csv.gz` | 10,968 | 17 | 50% | Lilace output, surface |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `COLUMNS.md`, `METHODS.md`, `abundance_variant_scores.tsv`, `cre_variant_scores.tsv`, `merged_variant_scores.tsv`, `surface_variant_scores.tsv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Howard MK, Whiteman S, Grimes PR, Macdonald C, Manglik A, Coyote-Maestas W. Mapping the sequence determinants of constitutive activity in GPCRs. bioRxiv. 2026. doi:10.64898/2026.10.30.762644

| | |
|---|---|
| Paper DOI | https://doi.org/10.64898/2026.10.30.762644 |
| Article license | CC BY 4.0 (bioRxiv preprint) |
| Data obtained from | Author GitHub repository matthewkarlhoward/2026_GPR161_mutational_scan (data/scores); also MaveDB urn:mavedb:00001323 and Zenodo 23755947 |
| Data location | https://github.com/matthewkarlhoward/2026_GPR161_mutational_scan |
| **License on the data in this folder** | **CC BY 4.0 (repository LICENSE-DATA); repository code MIT; MaveDB score sets CC0 1.0** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
