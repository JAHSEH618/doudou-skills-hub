#!/usr/bin/env python3
"""Build the editorial radar archive as static, accessible reading pages."""
from pathlib import Path
import argparse
import html
import json
import math
import re
import shutil
from urllib.parse import quote
import markdown
from markdown.extensions.toc import slugify_unicode

ROOT = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/JAHSEH618/doudou-skills-hub'
SITE = 'https://jahseh618.github.io/doudou-skills-hub'

def escape(value):
    return html.escape(str(value), quote=True)


def source_data(path):
    text = path.read_text()
    meta = {}
    match = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
    if match:
        for line in match[1].splitlines():
            if ': ' in line:
                key, value = line.split(': ', 1)
                try:
                    meta[key] = json.loads(value)
                except ValueError:
                    meta[key] = value
        text = text[match.end():]
    title = re.search(r'^# (.+)$', text, re.M).group(1)
    return meta, title, text



def frame(title, body, prefix='', path='', description='AI 工程化论文与实践。阅读原文、核对实验条件，持续记录判断。'):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Paper Radar</title><meta name="description" content="{escape(description)}">
<meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:type" content="article">
<link rel="canonical" href="{SITE}/{path}"><link rel="stylesheet" href="{prefix}site.css"></head>
<body id="top"><a class="skip" href="#main">跳到正文</a><div class="shell">
<header class="site-header"><a class="wordmark" href="{prefix}index.html"><span class="brand-symbol" aria-hidden="true">◉</span> 论文雷达<span class="brand-en">Paper Radar</span></a>
<nav aria-label="主导航"><a href="{prefix}index.html#archive">往期文章</a><a href="{prefix}judgments.html">判断账本</a><a href="{REPO}">GitHub ↗</a></nav></header>
{body}<footer><div><strong>Paper Radar</strong><p>硬件 · 模型 · 软件系统 · 工程方法</p><p>关于 AI 模型、系统与工程实践的持续阅读。</p></div><div class="footer-links"><a href="{REPO}">GitHub 原文 ↗</a><a href="#top">回到顶部 ↑</a></div></footer></div></body></html>'''



def enhance(content):
    content = re.sub(r'(<table>.*?</table>)', r'<div class="table-scroll">\1</div>', content, flags=re.S)

    content = re.sub(r'(<h3[^>]*>.*?</h3>)\s*<p>(.*?)</p>', r'\1<p class="source-line">\2</p>', content, flags=re.S)
    for url, entry in AUDIT.items():
        if entry['status'] in ('restricted', 'unverified', 'missing'):
            note = {'restricted': '访问受限', 'unverified': '链接待确认', 'missing': '原链接已失效'}[entry['status']]
            pattern = r'(<a href="'+re.escape(escape(url))+r'"[^>]*>.*?</a>)'
            content = re.sub(pattern, lambda m: m[1]+f'<span class="link-note">（{note}）</span>', content)
    return content


def render_article(source, destination, prefix, source_path, neighbors=''):
    meta, title, text = source_data(source)
    text = re.sub(r'^# .+\n', '', text, count=1, flags=re.M).strip()
    md = markdown.Markdown(extensions=['extra', 'toc', 'sane_lists'],
        extension_configs={'toc': {'slugify': slugify_unicode, 'toc_depth':'2-2'}})
    content = enhance(md.convert(text))
    is_report = source.parent.name == 'reports'
    if is_report:
        # Keep the introduction above the reading controls.
        split = content.find('<h2')
        opening, content = (content[:split], content[split:]) if split >= 0 else ('', content)
        lead = opening
        word_count = len(re.findall(r'[\u4e00-\u9fff]|\b[A-Za-z0-9]+\b', text))
        minutes = max(1, math.ceil(word_count/400))
        info = f'<span>{escape(("专题文章" if meta.get("mode") == "定向" else "技术札记"))}</span><time datetime="{meta.get("created",source.stem[:10])}">{meta.get("created",source.stem[:10])}</time><span>约 {minutes} 分钟</span>'
        updates = f'<p class="edit-note">更新于 <time datetime="{meta.get("updated",source.stem[:10])}">{meta.get("updated",source.stem[:10])}</time></p>'
    else:
        lead, info, updates = '', '持续记录', ''
    body = f'''<main id="main"><div class="page-tools"><a href="{prefix}index.html#archive">← 全部文章</a><a href="{REPO}/blob/master/{quote(source_path)}">Markdown 原文 ↗</a></div>
<header class="article-header"><div class="issue-meta">{info}</div><h1>{escape(title)}</h1>{updates}</header>
<div class="reading"><article class="prose"><div class="lede">{lead}</div>
<details class="mobile-toc"><summary>跳转到文章章节</summary>{md.toc}</details>{content}
{neighbors}</article><aside class="contents" aria-label="文章目录"><p class="contents-label">本文目录</p>{md.toc}</aside></div></main>'''
    destination.write_text(frame(title, body, prefix, str(destination.relative_to(OUT)), meta.get('description',title)), encoding='utf-8')
    return title



def build():
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'reports').mkdir(exist_ok=True)
    shutil.copy2(ROOT/'site/site.css', OUT/'site.css')
    for stale in ('link-audit.html', 'link-audit.json'):
        (OUT/stale).unlink(missing_ok=True)
    shutil.copytree(ROOT/'reports/assets',OUT/'reports/assets',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc','research-notes.md'))
    reports = sorted((ROOT/'reports').glob('*.md'), key=lambda p:(p.stem[:10],p.stem.endswith('weekly')), reverse=True)
    assert reports, 'No reports found'
    items = [(source,*source_data(source)[:2]) for source in reports]
    for i,(source,meta,title) in enumerate(items):
        neighbor_links = []
        for j,label in [(i-1,'较新一期'),(i+1,'较早一期')]:
            if 0 <= j < len(items):
                other,_,other_title = items[j]
                neighbor_links.append(f'<a href="{other.stem}.html"><span>{label} · {other.stem[:10]}</span><strong>{escape(other_title)}</strong></a>')
        nav = f'<nav class="neighbors" aria-label="相邻文章">{"".join(neighbor_links)}</nav>'
        render_article(source,OUT/'reports'/(source.stem+'.html'),'../','paper-radar/reports/'+source.name,nav)
    for name in ['judgments','seen-papers']:
        render_article(ROOT/'state'/(name+'.md'),OUT/(name+'.html'),'','paper-radar/state/'+name+'.md')
    latest,meta,title = items[0]
    rows = []
    for source,details,heading in items:
        rows.append(f'<li><div class="archive-date"><time datetime="{source.stem[:10]}">{source.stem[:10]}</time><span>{escape(("专题文章" if details.get("mode") == "定向" else "技术札记"))}</span></div><div><h3><a href="reports/{source.stem}.html">{escape(heading)}</a></h3><p>{escape(details.get("description",""))}</p></div><a class="row-arrow" href="reports/{source.stem}.html" aria-label="阅读{escape(heading)}">↗</a></li>')
    body = f'''<main id="main"><section class="home-intro"><h1>AI 工程，逐篇读。</h1><p>从论文到实现，记录模型、系统与评估中的具体进展。<br>关心方法怎样实现，也关心它在什么条件下有效。</p></section>
<section class="latest" aria-labelledby="latest-title"><div class="latest-main"><div class="issue-meta"><span>最新一期</span><time datetime="{latest.stem[:10]}">{latest.stem[:10]}</time></div><h2 id="latest-title"><a href="reports/{latest.stem}.html">{escape(title)}</a></h2><p>{escape(meta.get('description',''))}</p><a class="read" href="reports/{latest.stem}.html">展开阅读 <span aria-hidden="true">↗</span></a></div><aside class="latest-aside"><h3>从研究到实践</h3><p>论文里的实验，博客里的实现，以及作者在 X 上继续展开的讨论。</p><p>把相关材料放在一起，读清一个具体的技术问题。</p><a href="reports/{latest.stem}.html#x-上的技术讨论">读 X 上的技术讨论 →</a></aside></section>
<section id="archive" class="archive-section"><div class="section-heading"><h2>全部文章</h2><span>{len(items)} 期 · 按发布日期</span></div><ul class="archive">{''.join(rows)}</ul></section>
</main>'''
    (OUT/'index.html').write_text(frame('AI 工程，逐篇读', body),encoding='utf-8')
    # The full link audit is a repository artifact, not part of the reading flow.
    (OUT/'.nojekyll').write_text('')
    print(f'Built {len(reports)} reports, 2 ledgers, index and assets → {OUT}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=ROOT.parent/'_site')
    OUT = parser.parse_args().out.resolve()
    if OUT == ROOT or ROOT in OUT.parents and OUT != ROOT.parent/'_site':
        raise SystemExit('Use an output directory outside paper-radar source.')
    audit_data = json.loads((ROOT/'site/link-audit.json').read_text())
    AUDIT = {entry['url']:entry for entry in audit_data['links']}
    build()
