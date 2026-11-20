"""Where the build reads from and writes to.

Every input is a file already in this repository: the authors' originals in `<study_id>/source/`, the GPCRdb
residue table at the repo root, and `code/crossref_citations.json`. Nothing is downloaded during a build.

Output goes to `build/` (git-ignored) unless GPCR_DMS_OUT is set. `python code/build.py --check` rebuilds
into `build/` and compares the result with the committed files.
"""
import os
from pathlib import Path

CODE = Path(__file__).resolve().parent
REPO = CODE.parent
OUT = Path(os.environ.get("GPCR_DMS_OUT", REPO / "build")).resolve()
GPCRDB_TABLE = REPO / "gpcrdb_residue_numbering.csv"
CROSSREF = CODE / "crossref_citations.json"


def src(study_id, name):
    """Path to an original file in `<study_id>/source/`. Fails loudly if it is not there."""
    p = REPO / study_id / "source" / name
    if not p.is_file():
        raise FileNotFoundError(2, f"missing source file for {study_id}", str(p))
    return p
