"""Rebuild the data files in the repo from the authors' originals in <study_id>/source/.

  python code/build.py            build into build/ (git-ignored)
  python code/build.py --check    build, then compare the data files with the committed ones; exit 1 if any differ
  python code/build.py --install  build, then copy the data files over the committed ones

Data files: every <study_id>/tables/ (the CSVs and INDEX.csv) and merged/. Steps: build_master (one long table)
-> extract_sources (every source table, all columns) -> package_by_study (GPCRdb columns, INDEX) -> build_merged.

The documentation (study README.md and LICENSE.txt, studies.csv, licenses.csv, LICENSE.md, NOTICE.md,
REFERENCES.md, CITATION.cff, README.md, .zenodo.json) is maintained by hand and never written here. build/ also
gets a draft of each study README's tables section, for reference. add_citations.py drafts the licence and
citation files into build/ when run on its own after a build.
Needs: python >= 3.9, pandas >= 2.2, openpyxl, pyarrow, and pdftotext (poppler) on PATH.
"""
import argparse, gzip, os, runpy, shutil, sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE))
os.environ.setdefault("GPCR_DMS_OUT", str(CODE.parent / "build"))
from paths import OUT, REPO  # noqa: E402


def content(p):
    b = p.read_bytes()
    return gzip.decompress(b) if p.suffix == ".gz" else b


def generated():
    """The data files of the build: <study_id>/tables/* and merged/*."""
    def is_data(rel):
        return (len(rel.parts) == 3 and rel.parts[1] == "tables") or rel.parts[0] == "merged"
    return sorted(p for p in OUT.rglob("*") if p.is_file() and is_data(p.relative_to(OUT)))


def compare():
    same, diff, new = [], [], []
    for p in generated():
        rel = p.relative_to(OUT)
        q = REPO / rel
        (new if not q.exists() else same if content(p) == content(q) else diff).append(rel)
    made = {p.relative_to(OUT) for p in generated()}
    stale = sorted(p.relative_to(REPO) for sid in {r.parts[0] for r in made if len(r.parts) > 1}
                   for p in (REPO / sid / "tables").glob("*") if p.relative_to(REPO) not in made)
    print(f"\n{len(same)} identical, {len(diff)} differ, {len(new)} new, {len(stale)} committed but no longer built")
    for label, xs in (("differ", diff), ("new", new), ("stale", stale)):
        for x in xs:
            print(f"  {label:6s} {x}")
    return not (diff or new or stale), stale


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="compare the build with the committed files")
    ap.add_argument("--install", action="store_true", help="copy the build over the committed files")
    a = ap.parse_args()
    if OUT == REPO:
        sys.exit("GPCR_DMS_OUT must not be the repo itself; use --install to update committed files")
    if shutil.which("pdftotext") is None:
        sys.exit("pdftotext not found (install poppler)")
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "_stage").mkdir(parents=True)

    import build_master, extract_sources, build_merged
    print("1/4 master table")
    m = build_master.build()
    cols = ["study_id", "receptor", "gene", "uniprot", "study", "year", "journal", "doi", "scan_type", "in_mavedb"]
    m[cols].drop_duplicates("study_id").to_csv(OUT / "_stage" / "study_meta.csv", index=False)
    print("2/4 source tables")
    extract_sources.run()
    print("3/4 per-study tables, GPCRdb numbering")
    runpy.run_path(str(CODE / "package_by_study.py"), run_name="__main__")
    print("4/4 merged long table")
    build_merged.write(m, OUT / "merged")
    (OUT / "_stage" / "study_meta.csv").replace(OUT / "study_meta.csv")   # kept for add_citations.py
    shutil.rmtree(OUT / "_stage")

    if a.check or a.install:
        ok, stale = compare()
        if a.install:
            for p in generated():
                q = REPO / p.relative_to(OUT)
                q.parent.mkdir(parents=True, exist_ok=True)
                if not q.exists() or content(p) != content(q):
                    shutil.copy2(p, q)
            for s in stale:
                (REPO / s).unlink()
            print(f"installed into {REPO}")
        elif not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
