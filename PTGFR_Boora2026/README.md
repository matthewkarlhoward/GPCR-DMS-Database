# PTGFR_Boora2026

**Boora 2026 (Heydenreich / Vaidehi)**, *bioRxiv* 2026. DOI: [10.64898/2026.08.28.747882](https://doi.org/10.64898/2026.08.28.747882)
FP (PTGFR, UniProt P43088). alanine scan. MaveDB: no.

- Cells: see paper (individually transfected mutants)
- Library: Alanine scan of the full receptor
- Method: Surface ELISA; Gαq/11 and Gα12/13 activation biosensor CRCs with PGF2α
- Main score: Signalling: log(Emax/EC50) activity (ec50_log, emax = % WT). Expression: % WT
- Uncertainty: SE as published
- Source: bioRxiv 10.64898/2026.08.28.747882 Data S1 and S3

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
| `tables/Boora2026_DataS1.csv.gz` | 359 | 41 | 73% | all columns incl. FDR tests and effect classes |
| `tables/Boora2026_DataS3.csv.gz` | 40 | 16 | 80% | all columns incl. FDR tests and effect classes |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `boora_media-1.xlsx`, `boora_media-3.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Boora TS, Chen H, Cho A, van der Velden WJC, Namkung Y, Cao Y, Paranjpe JY, Heydenreich FM, Rodin AS, Branciamore S, Vaidehi N, Laporte SA. Allosteric pathways govern Gα protein coupling selectivity at promiscuous GPCRs. bioRxiv. 2026. doi:10.64898/2026.08.28.747882

| | |
|---|---|
| Paper DOI | https://doi.org/10.64898/2026.08.28.747882 |
| Article license | CC BY-NC 4.0 (bioRxiv preprint) — http://creativecommons.org/licenses/by-nc/4.0/ |
| Data obtained from | bioRxiv supplementary Data S1 and S3 |
| Data location | https://doi.org/10.64898/2026.08.28.747882 |
| **License on the data in this folder** | **CC BY-NC 4.0. Non-commercial use only; adaptation allowed with credit** |
| License text | http://creativecommons.org/licenses/by-nc/4.0/ |
| Redistribution status | `permissive-with-conditions` — An open licence permits redistribution, with conditions a reuser must respect (see below). |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
