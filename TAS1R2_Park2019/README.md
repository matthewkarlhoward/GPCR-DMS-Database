# TAS1R2_Park2019

**Park 2019 (Procko)**, *J Biol Chem* 2019. DOI: [10.1074/jbc.RA118.006173](https://doi.org/10.1074/jbc.RA118.006173)
T1R2 (TAS1R2, UniProt Q8TE23). DMS. MaveDB: no.

- Cells: Expi293F (pooled transfection)
- Library: Single amino-acid substitution library incl. stop
- Method: FACS sort for T1R2 surface (anti-FLAG) or partner T1R3 co-surface (anti-myc); Enrich deep-sequencing pipeline
- Main score: log2 enrichment ratio (sorted vs naive library) with WT subtracted (WT = 0); floor −4
- Uncertainty: score_se = |rep1 − rep2| / 2 (SEM, n = 2)
- Source: GEO GSE115751 (GSE115751_enrichment_ratios_T1R2.xlsx)

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
| `tables/GSE115751_enrichment_ratios_T1R2.csv.gz` | 17,115 | 7 | 27% | naive-library frequency and per-replicate log2 enrichment ratios for both sorts |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `GSE115751_enrichment_ratios_T1R2.xlsx`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Park J, Selvam B, Sanematsu K, Shigemura N, Shukla D, Procko E. Structural architecture of a dimeric class C GPCR based on co-trafficking of sweet taste receptor subunits. Journal of Biological Chemistry. 2019;294(13):4759-4774. doi:10.1074/jbc.RA118.006173

| | |
|---|---|
| Paper DOI | https://doi.org/10.1074/jbc.RA118.006173 |
| Article license | CC BY 4.0 (JBC; ASBMB open access) |
| Data obtained from | GEO series GSE115751 (GSE115751_enrichment_ratios_T1R2.xlsx) |
| Data location | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115751 |
| **License on the data in this folder** | **NCBI GEO: no restrictions on use or redistribution of the data; cite the source** |
| License text | https://www.ncbi.nlm.nih.gov/home/about/policies/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
