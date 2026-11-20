"""Build CNR2_MoralesPastor2025/tables/ from the authors' Supplementary Data 1.

Source: Morales-Pastor et al. 2025 Nat Commun 16:5265, Supplementary Data 1
(41467_2025_60003_MOESM3_ESM.xlsx), kept unmodified in CNR2_MoralesPastor2025/source/.

What this does, in the same way as the other study folders (see ../NOTICE.md):
  - joins the two header rows with " | " (the group label is carried across its merged cells);
  - keeps every column and every row, including the WT reference row and the one stray cell
    (Q8 = 35, no header) as column `unlabelled_col_Q`;
  - adds receptor / variant / pos / wt_aa / mut_aa, parsed from the authors' `mutant` column,
    and the GPCRdb columns, joined on `pos` from ../gpcrdb_residue_numbering.csv.
No value is changed.

Run from the repository root:  python code/build_cnr2_moralespastor2025.py
"""
import re
from pathlib import Path

import openpyxl
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
SID = "CNR2_MoralesPastor2025"
SRC = ROOT / SID / "source" / "41467_2025_60003_MOESM3_ESM.xlsx"
OUT = ROOT / SID / "tables" / "MoralesPastor2025_SupplementaryData1.csv.gz"

ws = openpyxl.load_workbook(SRC, data_only=True).worksheets[0]
rows = [list(r) for r in ws.iter_rows(values_only=True)]
ncol = max(len(r) for r in rows)
rows = [r + [None] * (ncol - len(r)) for r in rows]

# group labels from row 1, carried across merged ranges
group = list(rows[0])
for rng in ws.merged_cells.ranges:
    if rng.min_row == 1:
        for c in range(rng.min_col, rng.max_col + 1):
            group[c - 1] = rows[0][rng.min_col - 1]
names = []
for j in range(ncol):
    g, n = group[j], rows[1][j]
    if n is None and g is None:
        n = f"unlabelled_col_{openpyxl.utils.get_column_letter(j + 1)}"
    names.append(" | ".join(str(x) for x in (g, n) if x is not None))
body = [r for r in rows[2:] if any(c is not None for c in r)]
src = pd.DataFrame(body, columns=names)
src = src.loc[:, [c for c in src.columns if not (c.startswith("unlabelled_col_") and src[c].isna().all())]]

# variant keys
def parse(m):
    s = str(m)
    if s.lower() == "wt":
        return "WT", None, None, None
    w, p, a = re.fullmatch(r"([A-Z])(\d+)([A-Z])", s).groups()
    return s, int(p), w, a

keys = pd.DataFrame([parse(m) for m in src["mutant"]], columns=["variant", "pos", "wt_aa", "mut_aa"])
keys.insert(0, "receptor", "CB2")
keys["pos"] = keys["pos"].astype("Int64")

g = pd.read_csv(ROOT / "gpcrdb_residue_numbering.csv", dtype=str)
g = g[g.gpcrdb_entry.eq("cnr2_human")].assign(pos=lambda d: d.pos.astype(int)).set_index("pos")
for col in ["gpcrdb_generic", "gpcrdb_x", "bw", "segment", "gpcrdb_aa"]:
    keys[col] = keys["pos"].map(lambda p: g[col].get(p) if pd.notna(p) else None)
keys["wt_matches_gpcrdb"] = [None if pd.isna(p) else (w == a) for p, w, a in zip(keys.pos, keys.wt_aa, keys.gpcrdb_aa)]

out = pd.concat([keys, src], axis=1)
OUT.parent.mkdir(parents=True, exist_ok=True)
out.to_csv(OUT, index=False, compression={"method": "gzip", "mtime": 0})

mut = out[out.variant.ne("WT")]
idx = pd.DataFrame([{
    "table": f"tables/{OUT.name}",
    "rows": len(out),
    "source_columns": src.shape[1],
    "from_file": "Nat Commun Supplementary Data 1 (41467_2025_60003_MOESM3_ESM.xlsx)",
    "what": "per-mutant surface expression, Emax correction factors, raw and normalised Gαi2 / β-arrestin1 Emax and pEC50 (HU-210), MD-simulated flag, coupling profile; includes the WT reference row",
    "with_generic_number": f"{mut.gpcrdb_generic.notna().mean():.0%}",
    "wt_mismatches": "none" if mut.wt_matches_gpcrdb.all() else "; ".join(mut.loc[~mut.wt_matches_gpcrdb.astype(bool), "variant"]),
    "columns": " ; ".join(src.columns),
}])
idx.to_csv(ROOT / SID / "tables" / "INDEX.csv", index=False)
print(f"{len(out)} rows ({len(mut)} mutants + WT), {src.shape[1]} source columns, "
      f"{mut.gpcrdb_generic.notna().mean():.0%} with generic number, WT mismatches: {idx.wt_mismatches[0]}")
