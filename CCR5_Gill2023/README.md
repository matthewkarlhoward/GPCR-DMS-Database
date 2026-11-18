# CCR5_Gill2023

**Gill 2023 (Procko)**, *J Biol Chem* 2023. DOI: [10.1016/j.jbc.2023.105229](https://doi.org/10.1016/j.jbc.2023.105229)
CCR5 (CCR5, UniProt P51681). DMS. MaveDB: no.

- Cells: Expi293F (pooled transfection)
- Library: Single amino-acid substitution library incl. stop
- Method: FACS sort for myc surface stain or BiFC (Venus complementation with FLAG-WT-VN)
- Main score: log2 enrichment ratio (sorted vs naive) with WT subtracted (WT = 0); floor −3
- Uncertainty: score_se = |rep1 − rep2| / 2 (SEM, n = 2)
- Source: GEO GSE125426 (GSE125426_X4R5_BiFC_enrichment_ratios.xlsx)

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
| `tables/GSE125426_CCR5.csv.gz` | 7,203 | 7 | 80% | naive-library frequency and per-replicate log2 enrichment ratios (surface, BiFC) |

WT residues that differ from GPCRdb: none

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: `GSE125426_X4R5_BiFC_enrichment_ratios.xlsx`, `GSE125426_readme.txt`

## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> Gill KS, Mehta K, Heredia JD, Krishnamurthy VV, Zhang K, Procko E. Multiple mechanisms of self-association of chemokine receptors CXCR4 and CCR5 demonstrated by deep mutagenesis. Journal of Biological Chemistry. 2023;299(10):105229. doi:10.1016/j.jbc.2023.105229

| | |
|---|---|
| Paper DOI | https://doi.org/10.1016/j.jbc.2023.105229 |
| Article license | CC BY 4.0 (JBC; ASBMB open access) |
| Data obtained from | GEO series GSE125426 (GSE125426_X4R5_BiFC_enrichment_ratios.xlsx) |
| Data location | https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125426 |
| **License on the data in this folder** | **NCBI GEO: no restrictions on use or redistribution of the data; cite the source** |
| License text | https://www.ncbi.nlm.nih.gov/home/about/policies/ |
| Redistribution status | `clear` — An open licence explicitly permits redistribution of these numbers. |

Residue numbering added by this bundle comes from GPCRdb (https://gpcrdb.org), CC BY 4.0; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
