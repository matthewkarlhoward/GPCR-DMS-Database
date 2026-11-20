# MC4R_Howard2025

**C. Howard 2025 (Lubock)**, *eLife* 2025. DOI: [10.7554/eLife.104725](https://doi.org/10.7554/eLife.104725)
MC4R (MC4R, UniProt P32245). DMS. MaveDB: no.

- Cells: HEK293-derived reporter cells (Octant platform), barcoded variants (pooled)
- Library: Site-saturation library: 19 missense + stop at 332 positions (no synonymous)
- Method: Barcoded transcriptional reporters: CRE for Gs (DMS5, DMS11), UAS/Gq reporter (DMS8); negative-binomial GLMM per condition
- Main score: log2 fold change of reporter output, variant vs wild type, within each condition (model coefficient). 0 = WT-like; negative = less reporter output
- Uncertainty: score_se = standard error of the log2 fold change
- Source: https://github.com/octantbio/mc4r-dms (sumstats/*unnormalized.tsv, sumstats/pipeline-outputs/dms11-combined.sumstats.tsv)

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
| `tables/MC4R-DMS11-DefectSumstats.csv.gz` | 13,930 | 8 | 75% | DMS11 marginal defect ± Ipsen 17 |
| `tables/MC4R-DMS11-RescueSumstats.csv.gz` | 6,965 | 7 | 75% | DMS11 chaperone rescue |
| `tables/MC4R-DMS5-Gs-unnormalized.csv.gz` | 53,064 | 7 | 75% | per-condition log2FC vs WT (Gs) |
| `tables/MC4R-DMS5-Gs.csv.gz` | 46,431 | 8 | 75% | contrasts vs forskolin (Gs) |
| `tables/MC4R-DMS8-Gq-unnormalized.csv.gz` | 46,431 | 7 | 75% | per-condition log2FC vs WT (Gq) |
| `tables/MC4R-DMS8-Gq.csv.gz` | 39,798 | 8 | 75% | contrasts vs untreated (Gq) |
| `tables/Supplementary-Table-S2-variant-classifications.csv.gz` | 220 | 7 | no positions | Supplementary Table S2: variant classifications |
| `tables/dms11_combined.csv.gz` | 41,790 | 12 | 75% | full GLMM coefficient table, DMS11 |
| `tables/dms11_combined.csv.gz` | 41,790 | 8 | 75% | marginal means, DMS11 |
| `tables/dms5_combined.csv.gz` | 55,720 | 12 | 75% | full GLMM coefficient table, DMS5 |
| `tables/dms5_combined.csv.gz` | 55,720 | 8 | 75% | marginal means, DMS5 |
| `tables/dms8_combined.csv.gz` | 48,755 | 12 | 75% | full GLMM coefficient table, DMS8 |
| `tables/dms8_combined.csv.gz` | 48,755 | 8 | 75% | marginal means, DMS8 |
| `tables/mc4r-dms.csv.gz` | 92,862 | 11 | 75% | processed aMSH/THIQ x Gs/Gq table used in the paper |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `MC4R-DMS11-DefectSumstats.tsv`, `MC4R-DMS11-RescueSumstats.tsv`, `MC4R-DMS5-Gs-unnormalized.tsv`, `MC4R-DMS5-Gs.tsv`, `MC4R-DMS8-Gq-unnormalized.tsv`, `MC4R-DMS8-Gq.tsv`, `Supplementary-Table-S2-variant-classifications.tsv`, `dms11-combined.marginals.tsv`, `dms11-combined.sumstats.tsv`, `dms5-combined.marginals.tsv`, `dms5-combined.sumstats.tsv`, `dms8-combined.marginals.tsv`, `dms8-combined.sumstats.tsv`, `mc4r-dms.tsv`, `mc4r-dms_README.md`, `mc4r-wt.tsv`, `sumstats_README.md`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Howard CJ, Abell NS, Osuna BA, Jones EM, Chan LY, Chan H, Artis DR, Asfaha JB, Bloom JS, Cooper AR, Liao A, Mahdavi E, et al. High-resolution deep mutational scanning of the melanocortin-4 receptor enables target characterization for drug discovery. eLife. 2025;13:RP104725. doi:10.7554/eLife.104725

| | |
|---|---|
| Paper DOI | https://doi.org/10.7554/eLife.104725 |
| Article license | CC BY 4.0 (eLife) |
| Data obtained from | Octant GitHub repository octantbio/mc4r-dms (sumstats/) |
| Data location | https://github.com/octantbio/mc4r-dms |
| **License on the data in this folder** | **MIT** |
| License text | https://opensource.org/licenses/MIT |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
