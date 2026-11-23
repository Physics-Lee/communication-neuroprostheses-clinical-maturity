# Communication Neuroprostheses — Part III: Clinical Maturity · Interactive Edition

The **third part (Clinical Maturity)** of the review *"Speech, Typing, and Handwriting Neuroprostheses for People with Paralysis: Data Openness, Independent Reproduction, and Clinical Maturity"* as a **single-file interactive HTML edition** (no dependencies, opens directly in any browser).

This is the sibling of the two other interactive editions of the same review:

| Part | Interactive edition | Repository |
|---|---|---|
| I · Data Openness | [`communication_neuroprostheses_timeline.html`](https://github.com/Physics-Lee/communication-neuroprostheses-timeline) | [`Physics-Lee/communication-neuroprostheses-timeline`](https://github.com/Physics-Lee/communication-neuroprostheses-timeline) |
| II · Independent Reproduction | [`communication_neuroprostheses_reproduction.html`](https://github.com/Physics-Lee/communication-neuroprostheses-reproduction) | [`Physics-Lee/communication-neuroprostheses-reproduction`](https://github.com/Physics-Lee/communication-neuroprostheses-reproduction) |
| **III · Clinical Maturity** | **`communication_neuroprostheses_clinical_maturity.html`** (this repo) | **`Physics-Lee/communication-neuroprostheses-clinical-maturity`** |

> This work is a product of **we-linking**; non-commercial use with attribution (matching the two sibling repositories).

---

## What is inside the HTML

| Section | Manuscript anchor | Content |
|---|---|---|
| **Figure 4** — Clinical translation | `fig:clinical` | 10 panels (a)–(j) in three rows — surgery-related (a–c), decoding technology (d–f), patient paradigm (g–j) — separated by dashed rules with rotated row tags. Vector-rendered inline SVG. |
| **Table 3** — Cross-subject generalization | `tab:crosssubject` | 10 studies in 4 groups (ASR engineering reference, surface EMG, bulk-field intracranial, intracortical communication BCIs), with a **Data release filter** (open / partial / closed) and the full column definitions in a collapsible block. |
| **Figure 5** — Mandarin outlook | `fig:mandarin` | 5 panels (a)–(e): new survivors per year, phoneme counts, characters vs. words, the Pinyin articulatory trap, and Mandarin tone decoding. Vector-rendered inline SVG. |

### Interactive features

- **Panel chips grouped by row** — click any `(a)`…`(j)` / `(a)`…`(e)` chip to dim the other panels and open the panel's **full manuscript caption** (all numbers and citations) in a spotlight with Prev / Next navigation (`Esc` or `×` to close).
- **Click the figure itself** — every panel carries a transparent hit region (native tooltip = panel name); hover previews the focus, click pins it.
- **Table 3 data-release filter** — rows filter by open / partial / closed, empty groups hide, live visible-study count.
- Fullscreen buttons, per-section Show/Hide toggles, and a staggered entrance cascade (scroll-based reveal with reduced-motion / no-JS static fallbacks; deliberately **not** IntersectionObserver-based, which some embedded webviews never dispatch).

## Provenance & build

Everything is generated from the manuscript's own figure pipeline — nothing is redrawn by hand:

```text
../20261012_Comment_on_Recent_Progress_of_Language_BCI/figures/
    main_fig_4.py  --+
    main_fig_5.py  --+-->  python build_clinical_maturity_html.py
    fig_common.py  --+      (renders in memory, tags panels, namespaces ids)
                                |
template.html  -----------------+-->  communication_neuroprostheses_clinical_maturity.html
```

- Figure 4 / Figure 5 are the **exact vector renders** of `main_fig_4.py` / `main_fig_5.py` (electrode-retention data: `figures/data_fig_hahn_retention.json`); Table 3 is transcribed 1:1 from `latex/main.tex` (`tab:crosssubject`).
- The build script writes **nothing** into the manuscript repository (read-only sister repo; only its figure modules are imported).

### Rebuild

```bash
python build_clinical_maturity_html.py
```

Requires `matplotlib` and the manuscript repository at `D:\repositories\20261012_Comment_on_Recent_Progress_of_Language_BCI` (path pinned in the build script, same convention as the sibling repos' renderers).

## Repository layout

| Path | Role |
|---|---|
| `communication_neuroprostheses_clinical_maturity.html` | **The deliverable.** Generated artifact — never hand-edit; rebuild instead. |
| `template.html` | Page shell (CSS + Table 3 markup + panel captions + JS) with `__SVG_FIG4__` / `__SVG_FIG5__` / `__DATE__` placeholders. Edit this. |
| `build_clinical_maturity_html.py` | Build script: renders the two figures to SVG, injects per-panel hit regions, namespaces SVG ids (`f4-` / `f5-` prefixes), fills the template. |
| `tmp/` | Scratch (SVG snapshots, verification screenshots). Gitignored. |
| `AGENTS.md` | AI collaborator guide. |

## License & Attribution

This work is a product of **we-linking**. Non-commercial use with attribution, matching the two sibling repositories (CC BY-NC 4.0 lineage). Panel captions and figure content are owned by the manuscript repository; third-party publications referenced in the captions remain subject to their own terms.
