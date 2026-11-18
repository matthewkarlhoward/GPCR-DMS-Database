"""Package the raw data by study: original files + every per-variant table with all columns, each aligned to GPCRdb numbering.

gpcr_dms_raw_by_study/
  README.md, studies.csv, gpcrdb_residue_numbering.csv
  <study_id>/README.md
  <study_id>/source/        original files, unmodified
  <study_id>/tables/        each source table as CSV, all columns kept, with variant keys + GPCRdb columns added at the front
"""
import shutil
import pandas as pd
from pathlib import Path
from annotations import STUDY

ROOT = Path(__file__).parent
SRC = ROOT / "raw_by_study"
OUT = ROOT / "deliver_by_study" / "gpcr_dms_raw_by_study"
if OUT.parent.exists():
    shutil.rmtree(OUT.parent)
OUT.mkdir(parents=True)

R = pd.read_csv(ROOT / "reference/gpcrdb_residue_numbering.csv", dtype={"bw": str, "gpcrdb_generic": str, "gpcrdb_x": str, "wootten": str, "pin": str})
R["gpcrdb_x"] = R.gpcrdb_generic.map(lambda g: f"{g.split('x')[0].split('.')[0]}x{g.split('x')[1]}" if isinstance(g, str) and "x" in g else None)
R.to_csv(OUT / "gpcrdb_residue_numbering.csv", index=False)
meta = (pd.read_parquet(ROOT / "gpcr_mutational_master.parquet",
                        columns=["study_id", "receptor", "gene", "uniprot", "study", "year", "journal", "doi", "scan_type", "in_mavedb"])
        .drop_duplicates("study_id").set_index("study_id"))
idx = pd.read_csv(ROOT / "source_tables_index.csv")
GCOLS = ["gpcrdb_generic", "gpcrdb_x", "bw", "segment", "gpcrdb_aa"]

summary = []
for sid in sorted(meta.index):
    m, s = meta.loc[sid], STUDY[sid]
    d = OUT / sid
    shutil.copytree(SRC / sid / "source", d / "source")
    (d / "tables").mkdir()
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
        out.to_csv(d / "tables" / name, index=False)
        mm = out[out.wt_matches_gpcrdb.eq(False)].drop_duplicates("pos")
        rows.append(dict(table=f"tables/{name}", rows=len(out), source_columns=t.columns, from_file=t.from_file, what=t.note,
                         with_generic_number=f"{out.gpcrdb_generic.notna().mean():.0%}" if out.pos.notna().any() else "no positions",
                         wt_mismatches=", ".join(f"{a}{int(p)} (GPCRdb {b})" for a, p, b in zip(mm.wt_aa, mm.pos, mm.gpcrdb_aa)) or "none",
                         columns=t.column_names))
    tb = pd.DataFrame(rows)
    tb.to_csv(d / "tables" / "INDEX.csv", index=False)
    src_files = sorted(p.name for p in (d / "source").iterdir())
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
