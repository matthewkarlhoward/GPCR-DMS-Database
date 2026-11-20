"""Draft full citations and individually stated licensing for the by-study package, into build/.

Run after `python code/build.py`. The committed versions of these files are maintained by hand; use this
draft as a starting point when adding a study.

Writes:
  <study>/README.md     "Citation & license" section appended
  <study>/LICENSE.txt
  LICENSE.md            per-study table
  NOTICE.md             what was changed relative to the sources
  REFERENCES.md         all citations, incl. GPCRdb, MaveDB, Zenodo, GEO
  CITATION.cff
  studies.csv           + citation / licence columns
"""
import json, html, re
import pandas as pd
from pathlib import Path
from licenses import DOI, L, STATUS_NOTE, GPCRDB, MAVEDB_CITE

from paths import OUT, CROSSREF

CR = json.loads(CROSSREF.read_text())
TODAY = "2026-11-18"


def authors(a, n=12):
    def one(fam, giv):
        ini = "".join(p[0] for p in giv.replace("-", " ").split() if p and p[0].isalpha())
        return f"{fam} {ini}".strip()
    names = [one(f, g) for f, g in a]
    return ", ".join(names) if len(names) <= n else ", ".join(names[:n]) + ", et al"


def clean(s):
    """Crossref titles carry MathML/HTML markup and newlines; strip to plain text."""
    s = html.unescape(s)
    # sub/sup wrap their content on its own line; join it to the preceding word
    s = re.sub(r"\s*<(sub|sup)>\s*(.*?)\s*</\1>", r"\2", s, flags=re.S)
    s = re.sub(r"</?(sub|sup|i|b|em|strong|scp|mml:[a-z]+)[^>]*>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def citation(doi):
    c = CR[doi]
    j = clean(c["j"])
    t = clean(c["t"]).rstrip(". ")
    bits = f"{authors(c['a'])}. {t}. {j}. {c['y']}"
    if c["v"]:
        bits += f";{c['v']}"
        if c["i"]:
            bits += f"({c['i']})"
        if c["p"]:
            bits += f":{c['p']}"
    elif c["p"]:
        bits += f". {c['p']}"
    return bits + f". doi:{doi}"


def lic_line(k, v, url_key=None):
    u = v.get(url_key or "")
    return f"{v}" + (f" ({u})" if u else "")


meta = pd.read_csv(OUT / "study_meta.csv").set_index("study_id")   # written by build.py
sids = sorted(meta.index)

rows = []
for sid in sids:
    lic, doi = L[sid], DOI[sid]
    cite = citation(doi)
    al_url = lic.get("article_license_url", "")
    sec = f"""
## Citation & license

**Cite the original paper.** If you use these numbers, cite the authors' work, not this bundle:

> {cite}

| | |
|---|---|
| Paper DOI | https://doi.org/{doi} |
| Article license | {lic['article_license']}{f" — {al_url}" if al_url else ""} |
| Data obtained from | {lic['data']} |
| Data location | {lic['data_url']} |
| **License on the data in this folder** | **{lic['data_license']}** |
| License text | {lic['data_license_url']} |
| Redistribution status | `{lic['status']}` — {STATUS_NOTE[lic['status']]} |

Residue numbering added by this bundle comes from {GPCRDB['name']} ({GPCRDB['url']}), {GPCRDB['license']}; cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015 (see `../REFERENCES.md`).

`source/` holds the authors' files unmodified. `tables/` are the same tables converted to CSV with
variant and GPCRdb columns added — adapted versions, see `../NOTICE.md`.
"""
    r = OUT / sid / "README.md"
    r.write_text(r.read_text().split("\n## Citation & license")[0].rstrip() + "\n" + sec)

    (OUT / sid / "LICENSE.txt").write_text(f"""{sid}
Data license: {lic['data_license']}
License text: {lic['data_license_url']}
Redistribution status: {lic['status']} - {STATUS_NOTE[lic['status']]}

Source of the data: {lic['data']}
  {lic['data_url']}

Article license: {lic['article_license']}
{("  " + al_url + chr(10)) if al_url else ""}
Cite as:
  {cite}
  https://doi.org/{doi}

Generic residue numbers in tables/ are from GPCRdb ({GPCRDB['url']}), {GPCRDB['license']}.
  {GPCRDB['ack']}

The files in source/ are the authors' originals, unmodified. The files in tables/ are
converted and augmented versions of them; see ../NOTICE.md for exactly what changed.
This folder is a redistribution. Nothing here is a claim of ownership over the data,
and nothing here alters or extends the licenses above.
""")
    rows.append(dict(study_id=sid, receptor=meta.loc[sid].receptor, citation=cite, doi=doi,
                     article_license=lic["article_license"], data_source=lic["data"], data_url=lic["data_url"],
                     data_license=lic["data_license"], data_license_url=lic["data_license_url"],
                     redistribution_status=lic["status"]))

LT = pd.DataFrame(rows)
LT.to_csv(OUT / "licenses.csv", index=False)

# studies.csv gains the citation + licence columns
s = pd.read_csv(OUT / "studies.csv")
for c in ["receptor", "doi"]:   # restore if a previous run dropped them
    if c not in s.columns:
        s.insert(1 if c == "receptor" else len(s.columns), c, s.study_id.map(meta[c]))
NEW =["citation", "article_license", "data_source", "data_license", "data_license_url",
       "redistribution_status"]
s = s.drop(columns=[c for c in NEW if c in s.columns]).merge(
    LT[["study_id"] + NEW], on="study_id", how="left")
s = s[["study_id", "receptor", "gene", "uniprot", "study", "journal", "year", "scan_type", "in_mavedb", "tables",
       "source_files", "doi"] + NEW]
s.to_csv(OUT / "studies.csv", index=False)

# ---------------- LICENSE.md ----------------
def short(s):
    """First sentence only: split on a period followed by a space or end of string."""
    return re.split(r"\.(?:\s|$)", s.strip(), maxsplit=1)[0].rstrip(".").strip()


tbl = "\n".join(
    f"| `{x.study_id}` | {x.receptor} | {short(x.data_license)} | [link]({x.data_license_url}) | `{x.redistribution_status}` | {short(x.article_license.split('(')[0])} |"
    for x in LT.itertuples())
by_status = {k: LT[LT.redistribution_status.eq(k)].study_id.tolist() for k in STATUS_NOTE}
(OUT / "LICENSE.md").write_text(f"""# Licensing

Every dataset here was published by other people. **Each one keeps its own license**, listed below and
restated in that study's `LICENSE.txt` and `README.md`. There is no single license over the collection:
check the folder you are using.

Compiled {TODAY}. Licenses were read from the data source itself (repository `LICENSE`, Zenodo record,
MaveDB score-set metadata, GEO policy, or the publisher's supplementary terms) and from Crossref's
license field for each article. If a license has changed since, the source is authoritative, not this file.

## The data, by study

| study | receptor | data license | | status | article license |
|---|---|---|---|---|---|
{tbl}

Machine-readable: `licenses.csv`, and the licence columns in `studies.csv`.

## What the statuses mean

- **`clear`** ({len(by_status['clear'])} of {len(LT)} folders) — {STATUS_NOTE['clear']} CC0, CC BY 4.0, MIT, or NCBI GEO.
  Use them, cite the paper.
- **`permissive-with-conditions`** ({len(by_status['permissive-with-conditions'])}) — {', '.join('`'+x+'`' for x in by_status['permissive-with-conditions'])}.
  Open licenses with restrictions:
  - `RHO_Chen2026` is **CC BY-NC-ND 4.0**: non-commercial use only, and no derivatives. The `tables/`
    files add columns, so they are derivatives — for a strict reading, use `source/`. Commercial use
    needs permission from PNAS.
  - `AGTR1_Boora2026`, `PTGFR_Boora2026` are **CC BY-NC 4.0**: non-commercial use only; adaptation is
    allowed with credit.
- **`cite-only`** ({len(by_status['cite-only'])}) — {', '.join('`'+x+'`' for x in by_status['cite-only'])}.
  {STATUS_NOTE['cite-only']}
  - `AGTR1_Cao2023` (Science Signaling) is not open access and declares no data-reuse license. The
    alanine-scan values are the authors' published supplementary data, reproduced with full citation.
    AAAS permits reuse of figures and supplementary data for non-commercial scholarly purposes;
    anything beyond that — redistribution in a commercial product, for instance — needs AAAS
    permission. If you would rather not rely on that, delete the `AGTR1_Cao2023/` folder: nothing
    else here depends on it.

If you are an author of any of these datasets and want yours presented differently or removed,
say so and it will be changed.

## Residue numbering

Generic (GPCRdb / Ballesteros–Weinstein) numbers in every `tables/` file come from
{GPCRDB['name']} ({GPCRDB['url']}), {GPCRDB['license']} ([link]({GPCRDB['license_url']})). Cite
Pándy-Szekeres et al. 2023 and Isberg et al. 2015, and include:

> {GPCRDB['ack']}

## This bundle's own contribution

The scripts, the column layout, the GPCRdb join and the documentation are released under the MIT
License. This covers only the compilation — not the underlying data, which stays under the licenses
above.

```
MIT License

Copyright (c) 2026 Matthew K. Howard

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
""")

# ---------------- NOTICE.md ----------------
idx_all = pd.concat([pd.read_csv(OUT / sid / "tables" / "INDEX.csv").assign(study_id=sid) for sid in sids])
(OUT / "NOTICE.md").write_text(f"""# Notice of changes

CC BY and CC BY-NC require a statement of what was changed. This is that statement. It applies to
every study folder; nothing study-specific was done beyond what is listed here.

Compiled {TODAY} from {len(sids)} study folders, {len(idx_all)} source tables.

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
   `gpcrdb_residue_numbering.csv` (pulled {TODAY}), not anything derived from the authors' data.
   `wt_matches_gpcrdb` flags the handful of positions where a study's wild-type residue differs
   from GPCRdb — those are left as published and flagged, never corrected.
5. **Nothing removed.** Every column of every source table is present. Sequencing read counts were
   kept where the authors released them in a per-variant table.

`tables/INDEX.csv` in each folder lists every table, its row count, every column name, and which
file in `source/` it came from.

## `merged/` — changed, as follows

`merged/gpcr_dms_long.*` gathers each study's main published score into one long table (one row per variant
per condition). The published `score` and `score_se` are carried over unchanged. Added:

1. **Rows chosen and reshaped.** One row per variant x condition, taking the score column the authors
   present as their main result (the `score_type` and `source_file` columns say which). Rows with neither
   a score nor a curve fit are dropped.
2. **The same variant keys and GPCRdb numbering** as in `tables/`.
3. **`assay_class`**, a grouping of the assays by the compiler.
4. **`score_norm` and `score_rank`**, rescaled versions of `score` computed by the compiler
   (WT-like = 0, null-like = -1; and the percentile within the condition). These are new values, not the
   authors'. They are left empty for data under a no-derivatives license
   (`RHO_Chen2026`, `CNR2_MoralesPastor2025`).
5. **License columns** copied from `licenses.csv`.

## Study-level annotation

Each study `README.md` states the cell system, library, method, what the score means and how
uncertainty was reported. Those descriptions were written from the papers' methods sections for this
bundle; they are a summary by the compiler, not text from the authors. Where they disagree with the
paper, the paper is right.

## Attribution

No dataset here is the compiler's. Full citations: `REFERENCES.md`, `licenses.csv`, and each study's
`LICENSE.txt`.
""")

# ---------------- REFERENCES.md ----------------
seen, blocks = set(), []
for x in LT.itertuples():
    if x.doi in seen:
        continue
    seen.add(x.doi)
    same = LT[LT.doi.eq(x.doi)].study_id.tolist()
    blocks.append(f"**{', '.join('`'+s+'`' for same_ in [same] for s in same_)}**\n\n> {x.citation}\n\n"
                  f"Data: {x.data_source} — {x.data_url}  \nData license: {x.data_license}\n")
(OUT / "REFERENCES.md").write_text(f"""# References

Every dataset in this bundle, with the paper to cite and where the numbers came from. Also in
`licenses.csv` and `studies.csv`.

## Papers

{chr(10).join(blocks)}
## Resources used by this bundle

**Generic residue numbering** — GPCRdb, {GPCRDB['license']}, {GPCRDB['url']}

> {GPCRDB['cite'][0]}

> {GPCRDB['cite'][1]}

> {GPCRDB['ack']}

**MaveDB**, the source of nine of these score sets (all CC0) — https://www.mavedb.org

> {MAVEDB_CITE}

**Zenodo deposits**

> Mighell TL, Hwang S, Fleming KD, et al. b2AR_all_data_annot: GPCR-MAPS deep mutational scanning
> data for the β2-adrenergic receptor [Data set]. Zenodo. doi:10.5281/zenodo.15363336. CC BY 4.0

> Mighell TL, et al. V2R deep mutational scanning data [Data set]. Zenodo.
> doi:10.5281/zenodo.14216036. CC BY 4.0

**GEO series**

> GSE115751 — T1R2/T1R3 co-trafficking enrichment ratios (Park et al. 2019).
> https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE115751

> GSE125426 — CXCR4/CCR5 BiFC self-association enrichment ratios (Gill et al. 2023).
> https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE125426

**Code repositories** carrying released per-variant scores

- https://github.com/matthewkarlhoward/HaloTag-MOR_DMS_analysis — µOR (data CC BY 4.0)
- https://github.com/matthewkarlhoward/GPR68_DMS_Analysis — GPR68 (MIT)
- https://github.com/matthewkarlhoward/2026_GPR161_mutational_scan — GPR161 (data CC BY 4.0, code MIT)
- https://github.com/octantbio/mc4r-dms — MC4R (MIT)
- https://github.com/KosuriLab/b2-dms — β2AR (MIT)
""")

# ---------------- CITATION.cff ----------------
refs = []
for d in list(LT.drop_duplicates("doi").doi) + ["10.1093/nar/gkac1013", "10.1016/j.tips.2014.11.001"]:
    c = CR[d]
    au = "\n".join(f"      - family-names: \"{f}\"\n        given-names: \"{g}\"" for f, g in c["a"][:30])
    refs.append(f"""  - type: article
    title: "{clean(c["t"]).replace(chr(34), chr(39))}"
    doi: "{d}"
    year: {c['y']}
    journal: "{clean(c["j"])}"
    authors:
{au}""")
(OUT / "CITATION.cff").write_text(f"""cff-version: 1.2.0
message: >-
  This bundle redistributes other people's data. Please cite the original paper for each dataset you
  use (see REFERENCES.md and each study's LICENSE.txt), GPCRdb for the generic residue numbering,
  and, if useful, this compilation.
title: "GPCR-DMS Database: raw per-variant GPCR mutational scanning data by study, aligned to GPCRdb numbering"
abstract: >-
  Per-variant measurements from 21 published GPCR studies (deep mutational scans, receptor-wide
  alanine scans and variant panels) across 14 human receptors, in {len(sids)} datasets (one folder per receptor per study). Each study keeps its data as
  published, with its own license and citation; every table additionally carries GPCRdb generic and
  Ballesteros-Weinstein residue numbers. A merged long table (merged/) puts every study's main score in
  one file, with optional rescaled scores for comparing conditions.
authors:
  - family-names: "Howard"
    given-names: "Matthew K."
    affiliation: "University of California, San Francisco"
date-released: "{TODAY}"
license: MIT
repository-code: "https://github.com/matthewkarlhoward/GPCR-DMS-Database"
type: dataset
keywords:
  - GPCR
  - deep mutational scanning
  - alanine scanning
  - GPCRdb
  - variant effect
references:
{chr(10).join(refs)}
""")

print(LT[["study_id", "redistribution_status"]].to_string())
print("\nby status:", LT.redistribution_status.value_counts().to_dict())
