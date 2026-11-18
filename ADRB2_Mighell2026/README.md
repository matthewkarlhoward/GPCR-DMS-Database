# ADRB2_Mighell2026

**Mighell 2026 GPCR-MAPS (Lehner)**, *Nat Struct Mol Biol* 2026. DOI: [10.1038/s41594-026-01907-3](https://doi.org/10.1038/s41594-026-01907-3)
β2AR (ADRB2, UniProt P07550). DMS. MaveDB: no.

- Cells: HEK293T Bxb1 landing pad (attB), one variant per cell (pooled)
- Library: Site-saturation library incl. synonymous, stop and deletions
- Method: GPCR-MAPS: HA-tag surface stain; TEV-protease transcriptional recruitment reporter (Gal4-UAS-Citrine) for Nb80 and β-arrestin
- Main score: Normalised score with replicates combined (source *_reps_comb / *_norm_comb_score); per-replicate scores, read and barcode counts are in the same table
- Uncertainty: score_se = SEM across replicates where given; dose-series points have no SE
- Source: https://zenodo.org/records/15363336 (b2AR_all_data_annot.csv.gz)

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
| `tables/b2AR_all_data_annot.csv.gz` | 9,087 | 139 | 65% | per-replicate scores, reads, barcode counts, combined scores, dose series, Emax/EC50 fits, annotations |

WT residues that differ from GPCRdb: `tables/b2AR_all_data_annot.csv.gz`: R16 (GPCRdb G), Q27 (GPCRdb E)

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `b2AR_all_data_annot.csv.gz`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Mighell TL, Lehner B. GPCR-MAPS: high-resolution functional and allosteric mapping of G-protein-coupled receptor activation functions and bias. Nature Structural & Molecular Biology. 2026;33(11):1718-1732. doi:10.1038/s41594-026-01907-3

| | |
|---|---|
| Paper DOI | https://doi.org/10.1038/s41594-026-01907-3 |
| Article license | CC BY 4.0 (Nature Structural & Molecular Biology) |
| Data obtained from | Zenodo record 15363336 (b2AR_all_data_annot.csv.gz) |
| Data location | https://zenodo.org/records/15363336 |
| **License on the data in this folder** | **CC BY 4.0** |
| License text | https://creativecommons.org/licenses/by/4.0/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
