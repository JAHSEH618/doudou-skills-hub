#!/usr/bin/env python3
"""Build the public radar archive. Only reports, report assets and two ledgers ship."""
from pathlib import Path
import argparse
import html
import json
import re
import shutil
from urllib.parse import quote
import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
REPO = "https://github.com/JAHSEH618/doudou-skills-hub"
SITE = "https://jahseh618.github.io/doudou-skills-hub"
def escape(s):
    return html.escape(str(s), quote=True)

def strip_frontmatter(text):
    return re.sub(r"\A---\n.*?\n---\n", "", text, count=1, flags=re.S)

def frame(title, body, prefix="", path=""):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Paper Radar</title>
<meta name="description" content="AI 工程化论文雷达：硬件、模型、软件系统与工程方法。保留原始出处、验证层级和适用边界。">
<link rel="canonical" href="{SITE}/{path}"><link rel="stylesheet" href="{prefix}site.css"></head>
<body id="top"><a class="skip" href="#main">跳到正文</a><div class="shell">
<header class="site-header"><a class="wordmark" href="{prefix}index.html">论文雷达 / Paper Radar</a>
<nav aria-label="主导航"><a href="{prefix}index.html#archive">往期</a><a href="{prefix}judgments.html">判断账本</a><a href="{REPO}">GitHub</a></nav></header>
{body}<footer>保留原始出处，区分实测与推断。<br>报告由 Paper Radar 整理；数值与适用边界请一并阅读。<a class="back-top" href="#top">回到顶部 ↑</a></footer></div></body></html>'''

def render_article(source, destination, prefix, source_path):
    text = strip_frontmatter(source.read_text())
    title = re.search(r"^# (.+)$", text, re.M).group(1)
    md = markdown.Markdown(extensions=["extra", "toc", "sane_lists"],
        extension_configs={"toc": {"slugify": slugify_unicode, "toc_depth": "2-3"}})
    content = md.convert(text)
    content = re.sub(r"(<table>.*?</table>)", r'<div class="table-scroll">\1</div>', content, flags=re.S)
    body = f'''<div class="page-tools"><a href="{prefix}index.html">← 全部报告</a>
<a href="{REPO}/blob/master/{quote(source_path)}">查看 Markdown 原文</a></div>
<main id="main" class="reading"><article class="prose">{content}</article>
<aside class="contents" aria-label="文章目录"><details open><summary>本页目录</summary>{md.toc}</details></aside></main>'''
    destination.write_text(frame(title, body, prefix, str(destination.relative_to(OUT))), encoding="utf-8")
    return title

def stats_for(path):
    file = ROOT/"reports/assets"/path.stem/"stats.json"
    return json.loads(file.read_text()) if file.exists() else {}

def summary(stats):
    papers = sum(v["full"]+v["abstract"] for v in stats.get("lines", {}).values())
    full = stats.get("practice_full",stats.get("practice",0)) or 0
    short = stats.get("practice_abstract",0) or 0
    return f"{papers} 篇论文 · {full+short} 条实践" if papers else "论文与工程实践"

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"reports").mkdir(exist_ok=True)
    shutil.copy2(ROOT/"site/site.css",OUT/"site.css")
    shutil.copytree(ROOT/"reports/assets",OUT/"reports/assets",dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    reports = sorted((ROOT/"reports").glob("*.md"),reverse=True)
    assert reports, "No reports found"
    items=[]
    for source in reports:
        title=render_article(source,OUT/"reports"/(source.stem+".html"),"../","paper-radar/reports/"+source.name)
        stats=stats_for(source)
        items.append((source,title,stats))
    for name in ["judgments","seen-papers"]:
        render_article(ROOT/"state"/(name+".md"),OUT/(name+".html"),"","paper-radar/state/"+name+".md")
    latest,title,stats=items[0]
    rows=[]
    for source,title,data in items:
        mode=data.get("mode","周扫")
        date=source.stem[:10]
        label = title.split("（")[0].replace("论文雷达 · ", "")
        label = label if label.startswith(mode) else mode+" · "+label
        rows.append(f'<li><time datetime="{date}">{date}</time><div><h3><a href="reports/{source.stem}.html">{escape(label)}</a></h3><p>{escape(data.get("window",""))} · {escape(summary(data))}</p></div></li>')
    body=f'''<main id="main"><section class="intro"><h1>值得读，也经得起追问。</h1><p>AI 工程化论文与实践简报。每期沿硬件、模型、软件系统、工程方法四条线扫描，把结果、边界与原始出处放在一起。</p></section>
<section class="latest" aria-labelledby="latest-title"><div><span class="issue-meta">最新一期 · {latest.stem[:10]}</span><h2 id="latest-title">先看发生了什么，<br>再看结论在哪成立。</h2><p>{escape(summary(stats))} · {stats.get("news",0)} 条资讯</p><a class="read" href="reports/{latest.stem}.html">阅读本期报告 →</a></div>
<aside><p>【全文】与【仅摘要】分开标注。<br>核验细节保留在每期附录。</p><a href="judgments.html">翻阅持续更新的判断账本 ↗</a></aside></section>
<section id="archive"><h2>往期报告</h2><ul class="archive">{"".join(rows)}</ul></section></main>'''
    (OUT/"index.html").write_text(frame("论文与工程实践",body),encoding="utf-8")
    (OUT/".nojekyll").write_text("")
    print(f"Built {len(reports)} reports, 2 ledgers, index and assets → {OUT}")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,default=ROOT.parent/"_site")
    OUT=parser.parse_args().out.resolve()
    if OUT==ROOT or ROOT in OUT.parents and OUT!=ROOT.parent/"_site":
        raise SystemExit("Use an output directory outside paper-radar source.")
    build()
