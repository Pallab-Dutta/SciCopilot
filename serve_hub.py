from __future__ import annotations

import http.server
import os
import shutil
import socketserver
import subprocess
import webbrowser
from pathlib import Path


HOST = "127.0.0.1"
PORT = 8000
ROOT = Path(__file__).resolve().parent
BLOG_SRC = ROOT / "blog-src"
BLOG_OUT = ROOT / "blog"

# Where to look for the Hugo binary, in order: an explicit override, the PATH, then the
# pinned local install. The blog is served as static files under /blog/, so it has to be
# built before the server starts, the same way .github/workflows/deploy-pages.yml builds it.
PINNED_HUGO = "/home/pallab/Softwares/hugo_0.163.3/hugo"


def find_hugo() -> str | None:
    for cand in (os.environ.get("HUGO_BIN"), shutil.which("hugo"), PINNED_HUGO):
        if cand and Path(cand).exists():
            return cand
    return None


def build_blog() -> None:
    """Build blog-src/ into ./blog/ so the static server below serves the freshly built
    blog at /blog/, exactly as production does.

    The baseURL is pointed at localhost (not the real https://scicoagent.com/blog/ in
    hugo.toml) so the blog's own links and assets resolve against this server. Root-relative
    links like /assets/ and /agents.html keep working because they hit the repo root, which
    is what this server serves. Run the script again to rebuild after editing a post.
    """
    if not BLOG_SRC.is_dir():
        print(f"! {BLOG_SRC} not found; serving the static hub only.")
        return

    hugo = find_hugo()
    if not hugo:
        print("! Hugo not found. Set HUGO_BIN=/path/to/hugo, or install Hugo, to build the blog.")
        print(f"  Serving the existing ./{BLOG_OUT.name}/ output as-is (it may be stale).")
        return

    print(f"Building the blog from {BLOG_SRC.name}/ with {hugo} ...")
    try:
        subprocess.run(
            [
                hugo,
                "--source", str(BLOG_SRC),
                "--destination", str(BLOG_OUT),
                "--baseURL", f"http://{HOST}:{PORT}/blog/",
                "--cleanDestinationDir",  # drop stale files from a previous build
            ],
            check=True,
        )
        print(f"Blog built into ./{BLOG_OUT.name}/")
    except subprocess.CalledProcessError as exc:
        print(f"! Hugo build failed (exit {exc.returncode}); serving the previous ./{BLOG_OUT.name}/ output.")


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


def main() -> None:
    handler = http.server.SimpleHTTPRequestHandler

    with ReusableTCPServer((HOST, PORT), handler) as httpd:
        url = f"http://{HOST}:{PORT}/index.html"
        print(f"SciCopilot hub is available at {url}")
        print(f"Blog is available at   http://{HOST}:{PORT}/blog/")
        print("Press Ctrl+C to stop the server.")
        webbrowser.open(url)
        httpd.serve_forever()


if __name__ == "__main__":
    os.chdir(ROOT)
    build_blog()
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped.")
