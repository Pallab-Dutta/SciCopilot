#!/usr/bin/env python3
"""Stage a product's own blog source from the central blog-src/.

    python3 .github/scripts/product_blog.py <product> <out-dir> [--src blog-src]

Copies blog-src/ to <out-dir>, keeps only the content whose front matter says
`agent: "<product>"`, rewrites the home page title/description from
products/<product>.toml, and puts that file in place as <out-dir>/product.toml. Then build with:

    hugo --source <out-dir> --config hugo.toml,product.toml

The central blog keeps every post in its listings; for these posts it links to the product site
and turns the old address into a redirect page (layouts/partials/moved.html).
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

AGENT_RE = re.compile(r'(?m)^agent:\s*["\']?([A-Za-z0-9_-]+)["\']?\s*$')


def front_matter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def agent_of(md: Path) -> str:
    m = AGENT_RE.search(front_matter(md.read_text(encoding="utf-8")))
    return m.group(1) if m else ""


def _toml_str(path: Path, key: str) -> str:
    """First `key = "value"` in a small TOML file (no tomllib: runs on any Python 3.8+)."""
    m = re.search(rf'(?m)^\s*{re.escape(key)}\s*=\s*"([^"]*)"', path.read_text(encoding="utf-8"))
    return m.group(1) if m else ""


def stage(product: str, out: Path, src: Path) -> list[str]:
    overlay = src / "products" / f"{product}.toml"
    if not overlay.is_file():
        raise SystemExit(f"no product config: {overlay}")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(src, out, ignore=shutil.ignore_patterns("products"))
    shutil.copy(overlay, out / "product.toml")

    content = out / "content"
    kept: list[str] = []
    # A page is a bundle dir (index.md) or a single .md file. Section _index.md files stay.
    for md in sorted(content.rglob("*.md")):
        if not md.exists() or md.name == "_index.md":
            continue
        unit = md.parent if md.name == "index.md" else md
        if agent_of(md) == product:
            kept.append(str(unit.relative_to(content)))
        elif unit.is_dir():
            shutil.rmtree(unit)
        else:
            md.unlink()

    title = _toml_str(overlay, "title") or "Blog"
    desc = _toml_str(overlay, "description")
    (content / "_index.md").write_text(
        f'---\ntitle: "{title}"\ndescription: "{desc}"\n---\n\n{desc}\n', encoding="utf-8")
    return kept


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    product, out = argv[0], Path(argv[1])
    src = Path(argv[argv.index("--src") + 1]) if "--src" in argv else Path("blog-src")
    kept = stage(product, out, src)
    print(f"[product-blog] {product}: {len(kept)} page(s)")
    for k in kept:
        print(f"  {k}")
    if not kept:
        print("[product-blog] nothing to build", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
