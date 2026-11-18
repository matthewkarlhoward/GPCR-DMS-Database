# Notice of changes

CC BY and CC BY-NC require a statement of what was changed. This is that statement. It applies to
every study folder; nothing study-specific was done beyond what is listed here.

Compiled 2026-11-18 from 23 study folders, 83 source tables.

## `source/` — unchanged

The authors' files exactly as downloaded from the source in each `LICENSE.txt`. Byte-for-byte
identical; no renaming of contents, no edits. Filenames were occasionally prefixed to keep two
studies' files apart in one folder.

## `tables/` — changed, as follows

Each file is one source table, converted to CSV. **No published value was altered, rescaled,
renamed, filtered or recomputed.** What was done:

1. **Format conversion.** Excel sheets, TSVs and (for `RHO_McKee2021`, `RHO_Penn2020`,
   `RHO_Roushar2022`) PDF supplementary tables were converted to CSV. Numbers are carried over as
   written; the PDF tables were parsed by text extraction and the row counts checked against the
   published tables.
2. **Multi-row headers joined.** Where a spreadsheet had two or three header rows, the levels were
   joined into one column name with ` | ` between them. No column was dropped or reordered.
3. **Variant keys added** at the front: `receptor`, `variant`, `pos`, `wt_aa`, `mut_aa`, parsed from
   the authors' own variant identifier. The original identifier column is still there, untouched.
4. **GPCRdb numbering added**: `gpcrdb_generic`, `gpcrdb_x`, `bw`, `segment`, `gpcrdb_aa`,
   `wt_matches_gpcrdb`. These are a join on `pos` against the GPCRdb residue table in
   `gpcrdb_residue_numbering.csv` (pulled 2026-11-18), not anything derived from the authors' data.
   `wt_matches_gpcrdb` flags the handful of positions where a study's wild-type residue differs
   from GPCRdb — those are left as published and flagged, never corrected.
5. **Nothing removed.** Every column of every source table is present. Sequencing read counts were
   kept where the authors released them in a per-variant table.

`tables/INDEX.csv` in each folder lists every table, its row count, every column name, and which
file in `source/` it came from.

## Study-level annotation

Each study `README.md` states the cell system, library, method, what the score means and how
uncertainty was reported. Those descriptions were written from the papers' methods sections for this
bundle; they are a summary by the compiler, not text from the authors. Where they disagree with the
paper, the paper is right.

## Attribution

No dataset here is the compiler's. Full citations: `REFERENCES.md`, `licenses.csv`, and each study's
`LICENSE.txt`.
