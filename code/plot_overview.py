"""Overview figure for the README: GPCR variant measurements per study, cumulative over time,
and receptor scans per year, split by scan type and by whether the data are in MaveDB.

Input: figures/gpcr_dms_measurements.csv, one row per published scan. `measurements` counts
variant x condition rows (one variant scored in one condition, e.g. one ligand or dose) from
the master table built from the files in this repository, excluding WT reference rows.
Rows with from_paper_text = True are not in this database (or, for Penn 2020, the released
values are McKee 2021's); their counts come from the paper text.

Run from the repository root:  python code/plot_overview.py
"""
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parent.parent
FIG = ROOT / "figures"
df = pd.read_csv(FIG / "gpcr_dms_measurements.csv")

COLOR = {"dms": "#2a78d6", "panel": "#8f8f8f", "ala": "#eb6834"}
NAME = {"dms": "DMS", "panel": "Targeted / random panel", "ala": "Receptor-wide alanine scan"}
LAYERS = [(c, m) for c in ("dms", "panel", "ala") for m in (True, False)]  # stacking order

mpl.rcParams.update({
    "font.family": "Helvetica", "font.size": 6, "text.color": "black",
    "axes.labelcolor": "black", "xtick.color": "black", "ytick.color": "black",
    "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5,
    "xtick.major.size": 2, "ytick.major.size": 2, "lines.linewidth": 0.5,
    "patch.linewidth": 0.5, "hatch.linewidth": 0.5,
    "legend.frameon": False, "legend.fontsize": 6,
    "axes.spines.top": False, "axes.spines.right": False,
    "pdf.fonttype": 42, "svg.fonttype": "none",
})


def style(cat, mave):
    """Solid fill = in MaveDB; white with hatching = not in MaveDB."""
    c = COLOR[cat]
    return dict(facecolor=c, edgecolor=c) if mave else dict(facecolor="white", edgecolor=c, hatch="//////")


fig = plt.figure(figsize=(7.0, 3.4))
gs = fig.add_gridspec(2, 2, width_ratios=[1.35, 1], hspace=0.45, wspace=0.42,
                      left=0.2, right=0.98, top=0.97, bottom=0.14)
axL, axT, axB = fig.add_subplot(gs[:, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 1])

# ---- left: measurements per study -------------------------------------------------------
y = np.arange(len(df))[::-1]
for yi, r in zip(y, df.itertuples()):
    axL.barh(yi, r.measurements, height=0.7, **style(r.category, r.in_mavedb))
    txt = (">1,200" if r.label.startswith("Rho  Scott") else f"{r.measurements:,}") + ("*" if r.from_paper_text else "")
    axL.text(r.measurements + 4000, yi, txt, va="center", ha="left")
axL.set_yticks(y, df.label)
axL.tick_params(axis="y", length=0)
axL.set_ylim(-0.7, len(df) - 0.3)
axL.set_xlim(0, 450_000)
axL.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v / 1000:g}k" if v else "0"))
axL.set_xlabel("Variant measurements (variant × condition)")
axL.spines["left"].set_visible(False)
axL.text(0, -0.13, "* Count from paper text (no per-variant score file released)",
         transform=axL.transAxes, ha="left", va="top")

# ---- top right: cumulative measurements -------------------------------------------------
years = np.arange(2008, 2027)
xs = np.append(years, years[-1] + 1)
base = np.zeros(len(xs))
for cat, mave in LAYERS:
    sub = df[(df.category == cat) & (df.in_mavedb == mave)]
    if sub.empty:
        continue
    cum = np.array([sub.loc[sub.year <= yr, "measurements"].sum() for yr in years]) / 1000
    cum = np.append(cum, cum[-1])
    axT.fill_between(xs, base, base + cum, step="post", linewidth=0.5, **style(cat, mave))
    base = base + cum
axT.step(xs, base, where="post", color="black", linewidth=0.5)
axT.set_xlim(2008, 2027)
axT.set_ylim(0, 1000)
axT.set_xticks([2008, 2012, 2016, 2020, 2024])
axT.set_ylabel("Cumulative variant\nmeasurements (thousands)")
tot, mv = df.measurements.sum(), df.loc[df.in_mavedb, "measurements"].sum()
axT.text(2008.3, 1000, f"{tot / 1000:.0f}k total; {mv / 1000:.0f}k ({mv / tot:.0%}) in MaveDB", va="top")
handles = [Patch(facecolor=COLOR[c], edgecolor=COLOR[c], label=NAME[c]) for c in ("dms", "panel", "ala")]
handles += [Patch(facecolor="black", edgecolor="black", label="In MaveDB"),
            Patch(facecolor="white", edgecolor="black", hatch="//////", label="Not in MaveDB")]
LEGEND = dict(handles=handles, loc="upper left", handlelength=1.6, handleheight=0.9,
              borderaxespad=0, labelspacing=0.4)
axT.legend(bbox_to_anchor=(0.0, 0.88), **LEGEND)

# ---- bottom right: receptor scans per year ----------------------------------------------
bottom = np.zeros(len(years))
for cat, mave in LAYERS:
    sub = df[(df.category == cat) & (df.in_mavedb == mave)]
    if sub.empty:
        continue
    h = np.array([sub.loc[sub.year == yr, "n_receptors"].sum() for yr in years])
    k = h > 0  # skip empty years so no zero-height outlines are drawn
    axB.bar(years[k], h[k], bottom=bottom[k], width=0.8, **style(cat, mave))
    bottom += h
axB.set_xlim(2007.3, 2026.7)
axB.set_xticks([2008, 2012, 2016, 2020, 2024])
axB.set_yticks(range(0, int(bottom.max()) + 2, 2))
axB.set_ylabel("Receptor scans per year")
axB.set_xlabel("Year published")
axB.legend(bbox_to_anchor=(0.06, 1.0), **LEGEND)

FIG.mkdir(exist_ok=True)
for ext in ("png", "svg", "pdf"):
    fig.savefig(FIG / f"gpcr_dms_overview.{ext}", dpi=600, facecolor="white")
print(f"total {tot:,}  in MaveDB {mv:,} ({mv / tot:.1%})")
