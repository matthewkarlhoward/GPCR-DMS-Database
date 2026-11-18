# GPCR-DMS Database

GPCR mutational scanning data, by study.

Archived on Zenodo: each GitHub release of this repository gets its own DOI. To cite it, use the "Cite this repository" button on GitHub (from `CITATION.cff`) or the DOI on the Zenodo record, and always cite the original paper for each dataset you use.

The raw per-variant data from 22 GPCR deep mutational scans, alanine scans and variant panels, one folder per study (23 folders: Gill 2023 and Boora 2026 each split by receptor). Nothing is merged across studies. Each dataset is aligned to GPCRdb residue numbering so positions can be matched between receptors. Built 2026-11-18.

## In each study folder
- `source/`: the original files exactly as published (GitHub repos pinned to a commit; MaveDB, Zenodo, GEO, journal and bioRxiv supplements).
- `tables/`: every per-variant table from those files as CSV, with all of the authors' columns. That includes replicate scores, standard errors, statistics, counts, curve fits and classifications. Five key columns go at the front:
  - `variant`, `pos`, `wt_aa`, `mut_aa`
  - GPCRdb numbering: `gpcrdb_generic` (e.g. 3.50x50), `gpcrdb_x` (e.g. 3x50, for comparing receptors), `bw`, `segment`, `gpcrdb_aa`, `wt_matches_gpcrdb`
- `tables/INDEX.csv`: each table's source file, row count and full column list.
- `README.md`: citation, cells, library, method, what the main score means, and provenance.

## Studies
| folder | receptor | paper | scan | tables | source files |
|---|---|---|---|---|---|
| `ADRB2_Heydenreich2023/` | β2AR | Heydenreich 2023 (Veprintsev), *Science* 2023 | alanine scan | 1 | 1 |
| `ADRB2_Jones2020/` | β2AR | Jones 2020 (Kosuri), *eLife* 2020 | DMS | 4 | 5 |
| `ADRB2_Mighell2026/` | β2AR | Mighell 2026 GPCR-MAPS (Lehner), *Nat Struct Mol Biol* 2026 | DMS | 1 | 1 |
| `AGTR1_Boora2026/` | AT1R | Boora 2026 (Heydenreich / Vaidehi), *bioRxiv* 2026 | alanine scan | 2 | 2 |
| `AGTR1_Cao2023/` | AT1R | Cao 2023 (Heydenreich), *Sci Signal* 2023 | alanine scan | 11 | 5 |
| `AVPR2_Mighell2025/` | V2R | Mighell 2025 (Lehner), *Nat Struct Mol Biol* 2025 | DMS | 1 | 1 |
| `CCR5_Gill2023/` | CCR5 | Gill 2023 (Procko), *J Biol Chem* 2023 | DMS | 1 | 2 |
| `CCR5_Heredia2018/` | CCR5 | Heredia 2018 (Procko), *J Immunol* 2018 | DMS | 3 | 3 |
| `CXCR4_Gill2023/` | CXCR4 | Gill 2023 (Procko), *J Biol Chem* 2023 | DMS | 1 | 2 |
| `CXCR4_Heredia2018/` | CXCR4 | Heredia 2018 (Procko), *J Immunol* 2018 | DMS | 3 | 3 |
| `GPR161_Howard2026/` | GPR161 | M. Howard 2026, *bioRxiv* 2026 | DMS | 4 | 6 |
| `GPR68_Howard2025/` | GPR68 | M. Howard 2025, *Cell* 2025 | DMS | 6 | 6 |
| `MC4R_Howard2025/` | MC4R | C. Howard 2025 (Octant), *eLife* 2025 | DMS | 14 | 17 |
| `OPRM1_Howard2026/` | µOR | M. Howard 2026, *bioRxiv* 2026 | DMS | 14 | 15 |
| `P2RY8_LaFlam2025/` | P2Y8 | LaFlam 2025, *Cell Genom* 2025 | DMS | 6 | 2 |
| `PTGFR_Boora2026/` | FP | Boora 2026 (Heydenreich / Vaidehi), *bioRxiv* 2026 | alanine scan | 2 | 2 |
| `RHO_Chen2026/` | Rho | Chen 2026, *PNAS* 2026 | DMS | 2 | 2 |
| `RHO_Manian2025/` | Rho | Manian 2026 (Comander), *Sci Adv* 2026 | DMS | 2 | 2 |
| `RHO_McKee2021/` | Rho | McKee 2021 (Schlebach), *J Biol Chem* 2021 | DMS (TM2 + TM7) | 1 | 1 |
| `RHO_Penn2020/` | Rho | Penn 2020 (Schlebach), *Sci Adv* 2020 | DMS (TM2 + TM7) | 1 | 2 |
| `RHO_Roushar2022/` | Rho | Roushar 2022 (Schlebach), *J Biol Chem* 2022 | targeted panel | 1 | 1 |
| `RHO_Wan2019/` | Rho | Wan 2019 (Comander), *Hum Mutat* 2019 | targeted panel | 1 | 1 |
| `TAS1R2_Park2019/` | T1R2 | Park 2019 (Procko), *J Biol Chem* 2019 | DMS | 1 | 1 |

## GPCRdb numbering
`gpcrdb_residue_numbering.csv` is GPCRdb's residue table for the 13 receptors, pulled from gpcrdb.org on 2026-11-18. It lists, per residue:
- `display_generic_number`
- the BW, Wootten and Pin schemes
- the segment
- the residue

To compare a position across receptors, match on `gpcrdb_x` (class-independent: 3x50 is the DRY arginine in every class A receptor). Termini and long loops have no generic number.

The study WT residues agree with GPCRdb at every position except:
- β2AR 16 and 27 in GPCR-MAPS and Heydenreich (R16/Q27 vs GPCRdb's G16/E27)
- AT1R 160 in Cao 2023 (G vs S)

## Notes
- **Penn 2020 Rho** released only read counts. Its per-variant ±retinal ratio is in McKee 2021 Table S1, included in both Rho folders.
- **The Heydenreich β2AR values** come from the GPCR-MAPS Zenodo file, which mirrors Table S1.
- **Excel tables with stacked headers** (Cao, Boora, Procko-lab GEO files, P2Y8) have those headers joined with ` | ` so no label is lost.
- **Not included (no per-variant numbers released):**
  - Tate-lab thermostability alanine scans (β1AR, A2AR, NTS1)
  - Okuta 2016 ETB
  - Scott 2024 Rho

## Citation and licensing

**Every dataset here was published by someone else, and each one keeps its own license.** There is no
single license over the collection. Cite the paper for whichever data you use.

- `LICENSE.md` — the per-study license table, what each status means, and the conditions on the three
  non-commercial datasets.
- `REFERENCES.md` — the full citation for every paper, plus GPCRdb, MaveDB, the Zenodo deposits and the
  GEO accessions.
- `NOTICE.md` — exactly what was changed relative to the authors' files (required by CC BY / CC BY-NC).
- `licenses.csv` — the same thing machine-readable; the license columns are also in `studies.csv`.
- `<study>/LICENSE.txt` and the "Citation & license" section of each `<study>/README.md` — that study's
  citation, article license, data source and data license, restated in the folder itself.

Of the 23 folders: 19 carry a license that plainly permits redistribution (CC0, CC BY 4.0, MIT, or
NCBI GEO). Three are non-commercial — `RHO_Chen2026` (CC BY-NC-ND 4.0) and `AGTR1_Boora2026` /
`PTGFR_Boora2026` (CC BY-NC 4.0). One, `AGTR1_Cao2023`, is published supplementary data from a
subscription article with no stated reuse license, included with full citation; `LICENSE.md` says what
that means for reuse.

Generic residue numbers come from GPCRdb (CC BY 4.0). Cite Pándy-Szekeres et al. 2023 *NAR* and
Isberg et al. 2015 *TiPS*, and include: "We acknowledge the use of the GPCRdb database
(https://www.gpcrdb.org)."

The compilation itself — the scripts, the column layout, the GPCRdb join, the documentation — is MIT.
