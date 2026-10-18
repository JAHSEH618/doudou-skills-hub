#!/usr/bin/env python3
"""Re-skin a purple-template Dan Koe translation into the dark Dan-Koe-themed site page.

Usage: transform_dankoe_dark.py <src_html> <dst_html>
Keeps the translated body content (h1/h2/h3/p/img/blockquote/lists), strips the
purple template chrome, adds heading anchors + TOC, wraps in the dark frame
(dankoe.css design system: black / white Spectral / sage green #54675e).
"""
import re
import sys
from pathlib import Path

SERIES = 'Koe Letters'
CANONICAL = 'https://jahseh618.github.io/dankoe-zh/'
FRAME = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:type" content="article">
<link rel="canonical" href="{canonical}"><link rel="stylesheet" href="dankoe.css"></head>
<body id="top"><a class="skip" href="#main">跳到正文</a><div class="shell">
<header class="site-header"><a class="wordmark" href="index.html"><span class="brand-mark" aria-hidden="true"></span>Dan Koe<span class="wordmark-sub">翻译</span></a>
<nav aria-label="主导航"><a href="index.html">全部翻译</a><a href="https://jahseh618.github.io/doudou-skills-hub/">论文雷达</a><a href="https://letters.thedankoe.com/archive">Dan Koe 原站 ↗</a><a href="https://github.com/JAHSEH618/dankoe-zh">GitHub ↗</a></nav></header>
<main id="main"><article>
<div class="article-header"><h1>{title}</h1><p class="meta"><span>{date}</span><span>{series}</span><span>约 {mins} 分钟</span></p></div>
{toc}
<div class="reading">
{content}
</div>
<p class="back-link"><a href="index.html">← 返回全部翻译</a></p>
<p class="source-link"><a href="{source}" rel="noopener">原文链接 ↗</a></p>
</article></main>
</div></body></html>
'''


def strip_tags(html_text: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html_text)).strip()


def main():
    src, dst = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    text = src.read_text()

    m = re.search(r'<body[^>]*>(.*?)</body>', text, re.S)
    assert m, 'no <body> found'
    content = m.group(1).strip()

    source_url = re.search(r'<p class="source-link">.*?href="([^"]+)"', content, re.S)
    source_url = source_url.group(1) if source_url else ''
    date_m = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', content)
    date = date_m.group(1) if date_m else ''

    # strip purple template chrome
    content = re.sub(r'<h1[^>]*>.*?</h1>', '', content, count=1, flags=re.S)
    content = re.sub(r'<div class="stats">.*?</div>', '', content, flags=re.S)
    content = re.sub(r'<div class="section-divider">.*?</div>', '', content, flags=re.S)
    content = re.sub(r'<p class="meta">.*?</p>', '', content, flags=re.S)
    content = re.sub(r'<p class="source-link">.*?</p>', '', content, flags=re.S)
    # conclusion box becomes a styled note block
    content = content.replace('<div class="conclusion-box">', '<div class="note">')

    # strip emoji / keycaps from headings
    EMOJI = r'[\U0001F000-\U0001FAFF\u2600-\u27BF\uFE0F\u20E3]+'
    content = re.sub(r'(<h1[^>]*>)\s*%s?\s*' % EMOJI, r'\1', content)
    content = re.sub(r'(<h2[^>]*>)\s*%s?\s*' % EMOJI, r'\1', content)
    content = re.sub(r'(<h3[^>]*>)\s*\d+\s*%s?\s*' % EMOJI, r'\1', content)
    content = re.sub(r'(<h[23][^>]*>)\s*%s\s*' % EMOJI, r'\1', content)

    assert 'stats' not in content, 'stats block survived'
    assert 'style="' not in content, 'inline style survived'
    assert 'conclusion-box' not in content

    # heading anchors + TOC (h2 level)
    h2s, h3s = [], []
    for h in re.finditer(r'<h2[^>]*>(.*?)</h2>', content, re.S):
        h2s.append(strip_tags(h.group(1)))
    for h in re.finditer(r'<h3[^>]*>(.*?)</h3>', content, re.S):
        h3s.append(strip_tags(h.group(1)))

    counter = {'h2': 0, 'h3': 0}

    def tag_heading(mo):
        level, inner = int(mo.group(1)), mo.group(2)
        if level == 2:
            counter['h2'] += 1
            counter['h3'] = 0
            return f'<h2 id="s{counter["h2"]:02d}">' + inner + '</h2>'
        counter['h3'] += 1
        return f'<h3 id="s{counter["h2"]:02d}-{counter["h3"]:02d}">' + inner + '</h3>'

    content = re.sub(r'<h([23])[^>]*>(.*?)</h\1>', tag_heading, content, flags=re.S)

    toc_items = '\n'.join(
        f'<li><a href="#s{i + 1:02d}">{t}</a></li>' for i, t in enumerate(h2s)
    )
    toc = f'<nav class="toc" aria-label="目录"><h2>目录</h2><ol>\n{toc_items}\n</ol></nav>'

    # meta
    cjk = len(re.findall(r'[\u4e00-\u9fff]', content))
    latin = len(re.findall(r'[A-Za-z]+', content))
    mins = max(5, round((cjk / 400) + (latin / 120)))

    title_m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S)
    title = strip_tags(title_m.group(1)) if title_m else dst.stem
    title = re.sub(EMOJI, '', title).strip()

    p_first = re.search(r'<p[^>]*>(.*?)</p>', content, re.S)
    desc = strip_tags(p_first.group(1)) if p_first else title
    desc = desc[:118]

    page = FRAME.format(
        title=title, desc=desc, canonical=CANONICAL + dst.name,
        date=date, series=SERIES, mins=mins, toc=toc,
        content=content.strip(), source=source_url,
    )
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(page)
    assert page.count('<h1') == 1
    print(f'{dst}  ({len(page)} chars, {len(h2s)} h2 / {len(h3s)} h3, ~{mins} min)')


if __name__ == '__main__':
    main()
