"""Package the raw data by study: every per-variant table with all columns, each aligned to GPCRdb numbering.

Writes, under the build output (same layout as the repo root):
  studies.csv, gpcrdb_residue_numbering.csv
  <study_id>/README.md
  <study_id>/tables/        each source table as CSV, all columns kept, with variant keys + GPCRdb columns added at the front
<study_id>/source/ (the authors' originals) is read in place from the repo and not copied.
"""
import pandas as pd
from pathlib import Path
from annotations import STUDY
from paths import OUT, REPO, GPCRDB_TABLE

SRC = OUT / "_stage"
OUT.mkdir(parents=True, exist_ok=True)

R = pd.read_csv(GPCRDB_TABLE, dtype={"bw": str, "gpcrdb_generic": str, "gpcrdb_x": str, "wootten": str, "pin": str})
R["gpcrdb_x"] = R.gpcrdb_generic.map(lambda g: f"{g.split('x')[0].split('.')[0]}x{g.split('x')[1]}" if isinstance(g, str) and "x" in g else None)
R.to_csv(OUT / "gpcrdb_residue_numbering.csv", index=False)
meta = pd.read_csv(SRC / "study_meta.csv").set_index("study_id")
idx = pd.read_csv(SRC / "source_tables_index.csv")
idx = idx.assign(_name=idx.table.map(lambda x: Path(x).name)).sort_values(["study_id", "_name"], kind="stable")
GCOLS = ["gpcrdb_generic", "gpcrdb_x", "bw", "segment", "gpcrdb_aa"]

summary = []
for sid in sorted(meta.index):
    m, s = meta.loc[sid], STUDY[sid]
    d = OUT / sid
    (d / "tables").mkdir(parents=True)
    r = R[R.uniprot.eq(m.uniprot)].set_index("pos")
    rows = []
    for t in idx[idx.study_id.eq(sid)].itertuples():
        df = pd.read_csv(SRC / sid / t.table, low_memory=False)
        pos = pd.to_numeric(df["pos"], errors="coerce")
        g = r.reindex(pos)[GCOLS].reset_index(drop=True)
        wt = df["wt_aa"].astype("string")
        g["wt_matches_gpcrdb"] = (wt == g.gpcrdb_aa.astype("string")).where(wt.notna() & g.gpcrdb_aa.notna())
        out = pd.concat([df[["variant", "pos", "wt_aa", "mut_aa"]], g, df.drop(columns=["variant", "pos", "wt_aa", "mut_aa"])], axis=1)
        out = pd.concat([pd.DataFrame({"receptor": [m.receptor] * len(out)}), out], axis=1)
        name = Path(t.table).name
        out.to_csv(d / "tables" / name, index=False, compression={"method": "gzip", "mtime": 0})
        mm = out[out.wt_matches_gpcrdb.eq(False)].drop_duplicates("pos")
        rows.append(dict(table=f"tables/{name}", rows=len(out), source_columns=t.columns, from_file=t.from_file, what=t.note,
                         with_generic_number=f"{out.gpcrdb_generic.notna().mean():.0%}" if out.pos.notna().any() else "no positions",
                         wt_mismatches=", ".join(f"{a}{int(p)} (GPCRdb {b})" for a, p, b in zip(mm.wt_aa, mm.pos, mm.gpcrdb_aa)) or "none",
                         columns=t.column_names))
    tb = pd.DataFrame(rows)
    tb.to_csv(d / "tables" / "INDEX.csv", index=False)
    src_files = sorted(p.name for p in (REPO / sid / "source").iterdir() if p.name != ".DS_Store")
    table_md = "\n".join(f"| `{x.table}` | {x.rows:,} | {x.source_columns} | {x.with_generic_number} | {x.what} |" for x in tb.itertuples())
    mism = "; ".join(f"`{x.table}`: {x.wt_mismatches}" for x in tb.itertuples() if x.wt_mismatches != "none") or "none"
    (d / "README.md").write_text(f"""# {sid}

**{m.study}**, *{m.journal}* {m.year}. DOI: [{m.doi}](https://doi.org/{m.doi})
{m.receptor} ({m.gene}, UniProt {m.uniprot}). {m.scan_type}. MaveDB: {m.in_mavedb}.

- Cells: {s['cell_system']}
- Library: {s['library']}
- Method: {s['method']}
- Main score: {s['score_definition']}
- Uncertainty: {s['se_definition']}
- Source: {s['source_url']}

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
{table_md}

WT residues that differ from GPCRdb: {mism}

`tables/INDEX.csv` lists every column of every table.

## source/
Original files, unmodified: {", ".join(f"`{f}`" for f in src_files)}
""")
    summary.append(dict(study_id=sid, receptor=m.receptor, gene=m.gene, uniprot=m.uniprot, study=m.study, journal=m.journal, year=m.year,
                        doi=m.doi, scan_type=m.scan_type, in_mavedb=m.in_mavedb, tables=len(tb), source_files=len(src_files)))
pd.DataFrame(summary).to_csv(OUT / "studies.csv", index=False)
print(pd.DataFrame(summary)[["study_id", "tables", "source_files"]].to_string())
