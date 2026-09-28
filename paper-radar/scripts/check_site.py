#!/usr/bin/env python3
"""Check generated local links, images and fragment targets without network calls."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
import sys
import json
import xml.etree.ElementTree as ET
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__();self.ids=set();self.links=[];self.h1=0;self.feed(text)
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:
            assert a["id"] not in self.ids, f"Duplicate id: {a['id']}"
            self.ids.add(a["id"])
        if tag=="h1":self.h1+=1
        for key in ("href","src"):
            if key in a:self.links.append((tag,a[key]))
        if tag=="img":assert a.get("alt"),"Image missing alt text"
root=Path(sys.argv[1]).resolve()
pages={p:Page(p.read_text()) for p in root.rglob("*.html")}
audit_path=Path(__file__).resolve().parents[1]/"site/link-audit.json"
audit={entry["url"]:entry for entry in json.loads(audit_path.read_text())["links"]}
errors=[]
for path,page in pages.items():
    if page.h1!=1:errors.append(f"{path.name}: expected one h1, found {page.h1}")
    if path.parent==root/"reports":
        for phrase in ("原始扫描范围", "核验说明", "本次补充", "扫描统计", "来源与链接检查"):
            if phrase in path.read_text():errors.append(f"{path.name}: process copy in reading page: {phrase}")
    for tag,link in page.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:
            if u.netloc in ("jahseh618.github.io",) or link.startswith("https://github.com/JAHSEH618/doudou-skills-hub"):continue
            if link not in audit:errors.append(f"{path.name}: external link needs audit: {link}")
            elif audit[link]["status"]=="missing":errors.append(f"{path.name}: confirmed missing external link: {link}")
            continue
        target=(path.parent/unquote(u.path)).resolve() if u.path else path
        if target.is_dir():target/= "index.html"
        if not target.is_relative_to(root):errors.append(f"{path.name}: outside site: {link}")
        elif not target.exists():errors.append(f"{path.name}: missing: {link}")
        elif u.fragment and target in pages and unquote(u.fragment) not in pages[target].ids:
            errors.append(f"{path.name}: missing anchor: {link}")
for svg in root.rglob("*.svg"):ET.parse(svg)
if list(root.rglob("research-notes.md")) or (root/"link-audit.json").exists():
    errors.append("Research/audit records must remain repository-only")
if errors:raise SystemExit("\n".join(errors))
print(f"PASS: {len(pages)} HTML pages; links, anchors, headings, image alt text, SVG XML and editorial boundaries.")
