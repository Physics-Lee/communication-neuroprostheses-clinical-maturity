# -*- coding: utf-8 -*-
"""Build the single-file interactive HTML edition of the review's Part III
(Clinical maturity) into ``communication_neuroprostheses_clinical_maturity.html``.

Inputs (read-only, sister repositories under D:\\repositories):
  * ``20261012_Comment_on_Recent_Progress_of_Language_BCI/figures/``
    - ``main_fig_4.py``  -> Figure 4 (clinical translation, 10 panels a-j, 3 rows)
    - ``main_fig_5.py``  -> Figure 5 (Mandarin outlook, 5 panels a-e)
    - ``fig_common.py`` + ``data_fig_hahn_retention.json`` (run dependencies)
  * ``template.html`` (this directory) - page shell with ``__SVG_FIG4__``,
    ``__SVG_FIG5__`` and ``__DATE__`` placeholders.

What this script does per figure:
  1. renders the figure to a matplotlib SVG string (in memory; nothing is
     written into the sister repository),
  2. tags each matplotlib axes group ``<g id="axes_N">`` with
     ``class="panel" data-panel="<letter>"`` so CSS/JS can dim/highlight panels,
  3. appends transparent per-panel hit rectangles (with native ``<title>``
     tooltips) that receive hover/click events,
  4. namespaces every ``id``/``url(#...)``/``xlink:href="#..."`` with an
     ``f4-``/``f5-`` prefix so the two inline SVGs cannot collide,
  5. strips the XML prolog/DOCTYPE and the fixed pt ``width``/``height``
     attributes (the ``viewBox`` drives responsive sizing).

Run:  python build_clinical_maturity_html.py
"""
import io
import os
import re
import sys
import datetime as dt

WORK = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = (r"D:\repositories"
           r"\20261012_Comment_on_Recent_Progress_of_Language_BCI\figures")
OUT_HTML = os.path.join(
    WORK, "communication_neuroprostheses_clinical_maturity.html")
TEMPLATE = os.path.join(WORK, "template.html")

# axes-creation order per figure (matches the <g id="axes_N"> indices 1..N)
FIG4_LETTERS = list("abcdefghij")          # ax_a .. ax_j
FIG5_LETTERS = list("eeedcba")             # ax_a_title, ax_a, ax_a2, ax_b, ax_c, ax_d, ax_e
FIG_TITLES = {
    "4": {"a": "Non-speech sites: no usable signal",
          "b": "Electrode retention",
          "c": "Two craniotomies",
          "d": "Cross-subject",
          "e": "New-user few-shot calibration",
          "f": "Daily calibration burden",
          "g": "Self-gen vs copy",
          "h": "Attempted vs inner speech",
          "i": "Typing beats speech",
          "j": "Online voice vs text"},
    "5": {"a": "New survivors per year (China)",
          "b": "Phonemes EN/Mandarin",
          "c": "Characters vs words",
          "d": "Same Pinyin 'i', different tongues",
          "e": "Mandarin tone decoding"},
}


def render_figure_svgs():
    """Import the sister figure modules and capture their SVG output."""
    os.chdir(FIG_DIR)
    sys.path.insert(0, FIG_DIR)
    fig_letters = {"main_fig_4": FIG4_LETTERS, "main_fig_5": FIG5_LETTERS}
    import fig_common                      # noqa: import from the figures dir
    captured = {}

    def capture(fig, stem):
        buf = io.StringIO()
        fig.savefig(buf, format="svg", bbox_inches="tight")
        # measure panel geometry in the same frame the saved SVG uses
        ren = fig.canvas.get_renderer()
        tb = fig.get_tightbbox(ren)        # inches, includes figure-level artists
        exts = [ax.get_window_extent(ren) for ax in fig.axes]  # display px
        captured[stem] = {"svg": buf.getvalue(), "tb": tb, "exts": exts,
                          "dpi": fig.dpi, "letters": fig_letters[stem]}

    # patch BEFORE the figure modules star-import fig_common
    fig_common.save_fig = capture

    import main_fig_4                     # noqa: registers capture via star-import
    import main_fig_5                     # noqa
    main_fig_4.main_fig_4()
    main_fig_5.main_fig_5()
    return captured


def panel_rects(info):
    """Per-panel bounding rects in the saved SVG's viewBox coordinates (pt)."""
    tb, exts, dpi = info["tb"], info["exts"], info["dpi"]
    w_pt, h_pt = tb.width * 72.0, tb.height * 72.0
    pad_in = (w_pt / 72.0 - tb.width) / 2.0      # savefig pad_inches (0.1)
    k = 72.0 / dpi
    x_off = (tb.x0 - pad_in) * 72.0
    y_off = (tb.y0 - pad_in) * 72.0
    rects = {}
    for ax_ext, letter in zip(exts, info["letters"]):
        x0 = ax_ext.x0 * k - x_off
        y_top = h_pt - (ax_ext.y1 * k - y_off)
        x1 = ax_ext.x1 * k - x_off
        y_bot = h_pt - (ax_ext.y0 * k - y_off)
        cur = rects.get(letter)
        if cur is None:
            rects[letter] = [x0, y_top, x1, y_bot]
        else:
            cur[0] = min(cur[0], x0); cur[1] = min(cur[1], y_top)
            cur[2] = max(cur[2], x1); cur[3] = max(cur[3], y_bot)
    return rects


def postprocess_svg(raw, letters, stem_num):
    """Clean matplotlib SVG + inject panel classes and hit rectangles."""
    prefix = "f%s-" % stem_num
    # strip XML prolog / DOCTYPE comments (inline-embedding hygiene)
    raw = re.sub(r"^<\?xml[^>]*\?>\s*", "", raw)
    raw = re.sub(r"<!DOCTYPE[^>]*>\s*", "", raw, flags=re.S)
    # tag the axes groups (matplotlib writes exactly one <g id="axes_N"> each)
    for idx, letter in enumerate(letters, start=1):
        tag = '<g id="axes_%d"' % idx
        assert tag in raw, "missing %s in figure %s SVG" % (tag, stem_num)
        raw = raw.replace(
            tag, '<g id="axes_%d" class="panel" data-panel="%s"' % (idx, letter), 1)
    # parse the authoritative viewBox
    m = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', raw)
    W, H = float(m.group(1)), float(m.group(2))
    # namespace every id + reference so two inline SVGs cannot collide
    raw = raw.replace('url(#', 'url(#' + prefix)
    raw = raw.replace('xlink:href="#', 'xlink:href="#' + prefix)
    raw = re.sub(r'\bid="', 'id="%s' % prefix, raw)
    # drop the fixed pt dimensions; the viewBox drives responsive sizing
    raw = re.sub(r'(<svg[^>]*?)\sheight="[0-9.]+pt"', r"\1", raw, count=1)
    raw = re.sub(r'(<svg[^>]*?)\swidth="[0-9.]+pt"', r"\1", raw, count=1)
    # give the root <svg> the id the page shell targets
    raw = raw.replace("<svg ", '<svg id="%ssvg" ' % prefix, 1)
    # per-panel transparent hit rects (hover dim + click -> spotlight)
    info = RENDERED[stem_num]
    titles = FIG_TITLES[stem_num]
    hits = ['<g id="panel-hits">']
    PAD = 6.0
    for letter, (x0, y_top, x1, y_bot) in panel_rects(info).items():
        x0 = max(0.0, x0 - PAD); y_top = max(0.0, y_top - PAD)
        x1 = min(W, x1 + PAD);   y_bot = min(H, y_bot + PAD)
        hits.append(
            '<g class="panel-hit" data-panel="%s">'
            '<title>Panel (%s) — %s</title>'
            '<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" rx="6" '
            'pointer-events="all"/></g>'
            % (letter, letter, titles[letter], x0, y_top, x1 - x0, y_bot - y_top))
    hits.append("</g>")
    raw = raw.replace("</svg>", "".join(hits) + "</svg>")
    return raw


RENDERED = {}


def main():
    captured = render_figure_svgs()
    # map capture stems (main_fig_4 / main_fig_5) -> numbers for postprocess
    RENDERED["4"] = captured["main_fig_4"]
    RENDERED["5"] = captured["main_fig_5"]

    svg4 = postprocess_svg(RENDERED["4"]["svg"], FIG4_LETTERS, "4")
    svg5 = postprocess_svg(RENDERED["5"]["svg"], FIG5_LETTERS, "5")

    with open(TEMPLATE, encoding="utf-8") as f:
        html = f.read()
    for token, value in (("__SVG_FIG4__", svg4), ("__SVG_FIG5__", svg5),
                         ("__DATE__", dt.date.today().isoformat())):
        assert token in html, "template token %s missing" % token
        html = html.replace(token, value)

    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("[ok] wrote %s (%.1f KB; fig4 SVG %.1f KB, fig5 SVG %.1f KB)"
          % (OUT_HTML, len(html.encode("utf-8")) / 1024.0,
             len(svg4.encode("utf-8")) / 1024.0,
             len(svg5.encode("utf-8")) / 1024.0))


if __name__ == "__main__":
    main()
