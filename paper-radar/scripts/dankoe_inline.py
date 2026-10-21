#!/usr/bin/env python3
"""Make a self-contained copy of a dankoe page (inline CSS + absolute links) for chat delivery."""
import re
import sys
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://jahseh618.github.io/dankoe-zh/'
DANKOE_SITE = ROOT.parents[1] / 'dankoe-zh'  # sibling repo: ~/Downloads/dankoe-zh

def main():
    src, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
    text = src.read_text()
    css = (DANKOE_SITE / 'dankoe.css').read_text()
    text = re.sub(r'<link\b[^>]*href="dankoe\.css"[^>]*/?>', f'<style>\n{css}\n</style>', text)

    def fix_href(m):
        attr, href = m.group(1), m.group(2)
        if href.startswith(('http://', 'https://', '#', 'mailto:')):
            return m.group(0)
        return f'{attr}="{urljoin(BASE, href)}"'

    text = re.sub(r'(href|src)="([^"]+)"', fix_href, text)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text)
    print(out)

if __name__ == '__main__':
    main()
