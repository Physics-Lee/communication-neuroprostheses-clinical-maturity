# AGENTS.md — `communication-neuroprostheses-clinical-maturity/`

This repository holds the **Part III (Clinical Maturity) interactive HTML edition** of the three-part review on implanted communication neuroprostheses: one generated single-file HTML covering **Figure 4** (clinical translation, panels a–j), **Table 3** (cross-subject generalization), and **Figure 5** (Mandarin outlook, panels a–e).

**Working language: English.** All code comments, commit messages, and agent/user-facing communication in this repository must use English.

---

## Repository Contents

| File | Role | Edit Policy |
|---|---|---|
| [`communication_neuroprostheses_clinical_maturity.html`](communication_neuroprostheses_clinical_maturity.html) | **Generated deliverable** — the single-file interactive edition (inline SVGs of Figures 4 & 5 + interactive Table 3 + spotlight captions). | **Never hand-edit.** Edit `template.html` and rebuild. |
| [`template.html`](template.html) | Page shell: CSS, Table 3 markup, panel-chip/spotlight/filter JS, and the `__SVG_FIG4__` / `__SVG_FIG5__` / `__DATE__` placeholders. The `FIG4` / `FIG5` JS arrays carry each panel's verbatim manuscript caption. | **Primary file to edit.** Keep panel captions verbatim-synced with `latex/main.tex`. |
| [`build_clinical_maturity_html.py`](build_clinical_maturity_html.py) | Build script: imports the manuscript repo's figure modules, captures SVG output in memory, tags `<g id="axes_N">` groups with `data-panel`, appends transparent per-panel hit rects, namespaces every SVG id (`f4-` / `f5-` prefixes), strips fixed pt dimensions, fills the template. | Keep self-contained; the manuscript-repo path is pinned at the top. |
| [`tmp/`](tmp/) | Scratch area (captured SVG snapshots, headless-browser verification screenshots). | Gitignored; safe to delete. |
| [`README.md`](README.md) | Documentation. | Keep in sync with the template/build behavior. |

---

## Sister Repositories (read-only)

1. **Manuscript repo (the single source of truth for every number and caption)**: `../20261012_Comment_on_Recent_Progress_of_Language_BCI` — `latex/main.tex` (captions of `fig:clinical`, `tab:crosssubject`, `fig:mandarin`) and `figures/` (`main_fig_4.py`, `main_fig_5.py`, `fig_common.py`, `data_fig_hahn_retention.json`). **Iron rule: never write into it.** The build only imports its figure modules; a `__pycache__/` appearing in its `figures/` is the normal Python side effect of that import and is acceptable.
2. **Part I**: `../20261106_communication_neuroprostheses_timeline` (GitHub: `Physics-Lee/communication-neuroprostheses-timeline`) — Figure 1 timeline, Table 1 cohort, Figure 2a–d benchmark.
3. **Part II**: `../20261106_communication_neuroprostheses_reproduction` (GitHub: `Physics-Lee/communication-neuroprostheses-reproduction`) — Figure 2e–g reproductions, Figure 3 phase/memory, Table 2 ledger, Figure 6 CTC-TLG limits.

Numbers referenced in the captions (e.g., the 12.8% ASR anchor, panel values) are verified facts owned by the manuscript repo — do not re-derive them here.

---

## Data Flow & How to Build

```bash
python build_clinical_maturity_html.py
```

```text
20261012_...comment repo/figures/{main_fig_4, main_fig_5, fig_common}.py
        |  (imported; save_fig monkey-patched to capture SVG + panel bboxes in memory)
        v
build_clinical_maturity_html.py
        +--> tags axes groups  <g id="axes_N">  ->  class="panel" data-panel="<letter>"
        +--> appends per-panel transparent hit rects (hover dim / click -> spotlight)
        +--> namespaces ids + url(#)/xlink refs with "f4-"/"f5-" prefixes
        +--> strips XML prolog / DOCTYPE / fixed pt width+height (viewBox drives sizing)
        +--> fills template.html  ->  communication_neuroprostheses_clinical_maturity.html
```

The build asserts every template token and every `axes_N` group exists — a matplotlib or figure-script change that alters the axes count fails the build loudly instead of silently mislabeling panels.

---

## Load-Bearing Conventions (Do Not Break)

1. **The generated HTML is never hand-edited.** Every change goes through `template.html` (shell, captions, JS) or the build script (SVG post-processing), then a rebuild.
2. **SVG id namespacing is load-bearing.** Two inline matplotlib SVGs collide on hashed `clipPath` ids (`pXXXXXX`) and both define generic ids (`axes_1`, `text_1`, ...); the `f4-` / `f5-` prefixes applied to every `id`, `url(#...)` and `xlink:href="#..."` are what keep both figures rendering. Do not bypass `postprocess_svg`.
3. **Panel-caption text must stay verbatim** with the manuscript captions in `latex/main.tex` (`fig:clinical`, `tab:crosssubject`, `fig:mandarin`). If a caption changes upstream, update the `FIG4` / `FIG5` arrays in `template.html` in the same pass — the HTML is a publication artifact, not a paraphrase.
4. **Figure/panel numbering follows the manuscript float order** (Figure 4 = `fig:clinical`, Table 3 = `tab:crosssubject`, Figure 5 = `fig:mandarin`). Do not renumber if the manuscript adds floats — re-check `main.tex` instead.
5. **Axes-to-letter mapping is pinned in one place** (`FIG4_LETTERS` / `FIG5_LETTERS` in the build script). Figure 5's tone block is *three* matplotlib axes (`eeedcba`: title + curves + bars) merged into one spotlight panel — the mapping folds them by unioning bounding boxes.
6. **The entrance cascade must not use IntersectionObserver** (some embedded webviews never dispatch it; verified 2026-11-23). The scroll/resize + `getBoundingClientRect` fallback in `template.html` is the mechanism.
7. **Esafenet DLP rule**: `.md` files written through harness `Write`/`Edit` tools get transparently encrypted (magic header `e0a891e7d8f205ac`). Create/modify `.md` files via a Python script run through Bash, then verify the first bytes are not that magic header.
8. **Commit messages in English** (repository working language).

---

## Verification Checklist (after any rebuild)

1. `python build_clinical_maturity_html.py` prints `[ok]` and the byte sizes.
2. Serve the folder (`python -m http.server ...`) or open the file directly; check:
   - 10 + 5 panel chips render (Figure 4 chips grouped under the three row tags);
   - clicking a chip dims the other panels and fills the spotlight with the full caption;
   - Table 3 filter (open / partial / closed) leaves 3 / 6 / 1 studies and hides empty groups;
   - no browser-console errors (a silent JS failure leaves the page blank because `.rv` stays at `opacity: 0`).
3. Headless screenshots (see `tmp/shots/` for the reference round): page top (Figure 4 rows a–c visible), full page (all three sections + footer), and an interaction round (panel (d) pinned + Table 3 filtered to `open`).

---

## License & Attribution

This work is a product of **we-linking**. Non-commercial use with attribution, matching the two sibling repositories (CC BY-NC 4.0 lineage). Panel captions and figure content are owned by the manuscript repository; third-party publications referenced in the captions remain subject to their own terms.
