#!/usr/bin/env python3
"""Editable cover art for the LaTeX cluster.

Each .svg in this folder is the SOURCE for one post/page cover. The site actually serves the
rasterised cover.png in the page bundle (link previews on X, LinkedIn and Slack do not render
SVG, so the og:image has to be raster). To change a cover:

    1. edit the .svg here (colours, headline, layout are plain text),
    2. run:  python render-covers.py
    3. commit the updated cover.png (and the .svg).

This folder lives under blog-src/ on purpose: Hugo does not build it (it only builds
content/, layouts/, static/, ...) and the Pages deploy excludes /blog-src/, so these sources
are versioned but never published.

Requires cairosvg:  pip install cairosvg
"""

from pathlib import Path

import cairosvg

HERE = Path(__file__).resolve().parent
CONTENT = HERE.parent / "content"
WIDTH, HEIGHT = 1200, 630  # standard Open Graph / Twitter card size

# source .svg (in this folder)  ->  destination cover.png (in its page bundle)
COVERS = {
    "latex-proofreader.svg": CONTENT / "latex-proofreader" / "cover.png",
    "ai-proofreader-for-latex.svg": CONTENT / "posts" / "ai-proofreader-for-latex" / "cover.png",
    "proofread-latex-without-breaking-equations.svg":
        CONTENT / "posts" / "proofread-latex-without-breaking-equations" / "cover.png",
    "best-latex-proofreader-comparison.svg":
        CONTENT / "posts" / "best-latex-proofreader-comparison" / "cover.png",
}


def main() -> None:
    for svg_name, png_path in COVERS.items():
        src = HERE / svg_name
        if not src.exists():
            print(f"skip: {svg_name} not found")
            continue
        cairosvg.svg2png(url=str(src), write_to=str(png_path),
                         output_width=WIDTH, output_height=HEIGHT)
        print(f"{svg_name} -> {png_path.relative_to(CONTENT.parent)}")
    print("done")


if __name__ == "__main__":
    main()
