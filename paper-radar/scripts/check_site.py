#!/usr/bin/env python3
"""Check generated local links, images and fragment targets without network calls."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import sys
import xml.etree.ElementTree as ET
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.add(a["id"])
        for key in ("href","src"):
            if key in a:self.links.append((tag,a[key]))
        if tag=="img":assert a.get("alt"),"Image missing alt text"
root=Path(sys.argv[1]).resolve()
pages={p:Page(p.read_text()) for p in root.rglob("*.html")}
errors=[]
for path,page in pages.items():
    for tag,link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target/= "index.html"
        if not target.is_relative_to(root):errors.append(f"{path.name}: outside site: {link}")
        elif not target.exists():errors.append(f"{path.name}: missing: {link}")
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f"{path.name}: missing anchor: {link}")
for svg in root.rglob("*.svg"):ET.parse(svg)
if errors:raise SystemExit("\n".join(errors))
print(f"PASS: {len(pages)} HTML pages; local links, anchors, image alt text and SVG XML.")

