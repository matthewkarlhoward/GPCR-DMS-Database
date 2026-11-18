# ADRB2_Jones2020

**Jones 2020 (Kosuri)**, *eLife* 2020. DOI: [10.7554/eLife.54895](https://doi.org/10.7554/eLife.54895)
β2AR (ADRB2, UniProt P07550). DMS. MaveDB: no.

- Cells: HEK293T, barcoded variants integrated (pooled)
- Library: Single amino-acid substitutions (7,800 of 7,828), no synonymous or stop
- Method: Barcoded CRE transcriptional reporter (RNA-seq of barcodes), normalised to forskolin-stimulated expression
- Main score: Reporter output normalised to the mean of frameshift (null) controls in the same condition, averaged over 2 repeats (paper.Rmd 'Norm'). 1 = frameshift-like; the WT-like value is the synonymous scalar in output/scalars.csv
- Uncertainty: score_se = paper.Rmd 'Uncert' = 0.5·sqrt(Σ SD²/scale²) over repeats
- Source: https://github.com/KosuriLab/b2-dms (output/lib-med.csv.gz, output/scalars.csv)

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
| `tables/class-norm-int.csv.gz` | 26,258 | 6 | 65% | per condition x repeat x position x residue class |
| `tables/lib-med.csv.gz` | 62,424 | 10 | 65% | per condition x repeat x variant: median, MAD, mean, SD, CV, N of barcodes (pre-normalisation) |
| `tables/negs-med.csv.gz` | 3,312 | 10 | 65% | frameshift / negative-control barcodes |
| `tables/scalars.csv.gz` | 16 | 7 | no positions | per condition x repeat normalisation scalars (synonymous and frameshift) |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `class-norm-int.csv.gz`, `lib-med.csv.gz`, `negs-med.csv.gz`, `paper.Rmd`, `scalars.csv`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Jones EM, Lubock NB, Venkatakrishnan A, Wang J, Tseng AM, Paggi JM, Latorraca NR, Cancilla D, Satyadi M, Davis JE, Babu MM, Dror RO, et al. Structural and functional characterization of G protein–coupled receptors with deep mutational scanning. eLife. 2020;9:e54895. doi:10.7554/eLife.54895

| | |
|---|---|
| Paper DOI | https://doi.org/10.7554/eLife.54895 |
| Article license | CC BY 4.0 (eLife) |
| Data obtained from | Kosuri lab GitHub repository KosuriLab/b2-dms (output/) |
| Data location | https://github.com/KosuriLab/b2-dms |
| **License on the data in this folder** | **MIT** |
| License text | https://opensource.org/licenses/MIT |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
