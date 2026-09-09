#!/usr/bin/env python3
"""paper-radar 图表渲染器。只用 Python 标准库，输出 SVG。

用法：
    python3 render_charts.py <assets_dir>

<assets_dir> 形如 reports/assets/2026-09-08，里面要先有一个 stats.json。
渲染两张图到同一目录：
    volume.svg  本期体量（各线条目数 + 配额线 + 全文/仅摘要占比）
    trend.svg   跨期趋势（自动扫描 assets_dir 的父目录下所有 stats.json）

stats.json 字段见 SKILL.md「图表」一节。
SVG 自带浅色/深色两套配色，跟随阅读器主题，Obsidian 和 GitHub 都能正常渲染。
"""

import json
import sys
from pathlib import Path

FONT = "-apple-system, 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"

# 两套主题共用的记号颜色：在白底和深底上都能读
C_FULL = "#3b6fd4"      # 全文验证
C_ABSTRACT = "#a8c0e8"  # 仅摘要
C_PRACTICE = "#c07830"  # 工程实践
C_NEWS = "#8a8a94"      # 快讯
C_POOL = "#b0b0ba"      # 落选池
C_QUOTA = "#c0392b"     # 配额线

STYLE = f"""
  <style>
    .bg   {{ fill: #ffffff; }}
    .fg   {{ fill: #24292f; }}
    .mut  {{ fill: #6b7280; }}
    .grid {{ stroke: #e5e7eb; }}
    text  {{ font-family: {FONT}; }}
    @media (prefers-color-scheme: dark) {{
      .bg   {{ fill: #1e1f22; }}
      .fg   {{ fill: #e6e6e6; }}
      .mut  {{ fill: #9aa0a6; }}
      .grid {{ stroke: #3a3d42; }}
    }}
  </style>
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------- 体量图

def render_volume(stats, out_path):
    lines = stats["lines"]                      # 四条线，每条 {full, abstract}
    cap = stats["paper_cap"]
    papers_full = sum(v["full"] for v in lines.values())
    papers_abs = sum(v["abstract"] for v in lines.values())
    papers = papers_full + papers_abs

    rows = []
    for name in ("硬件", "模型", "软件系统", "工程方法"):
        v = lines.get(name, {"full": 0, "abstract": 0})
        rows.append((name, [(v["full"], C_FULL), (v["abstract"], C_ABSTRACT)], None))
    rows.append(("SEP", None, None))
    rows.append(("论文合计", [(papers_full, C_FULL), (papers_abs, C_ABSTRACT)], cap))
    rows.append(("SEP", None, None))
    rows.append(("工程实践", [(stats["practice"], C_PRACTICE)], stats.get("practice_cap", 4)))
    rows.append(("快讯", [(stats["news"], C_NEWS)], stats.get("news_cap", 5)))
    rows.append(("落选池", [(stats["pool"], C_POOL)], stats.get("pool_cap", 5)))

    pad_l, pad_r, pad_t = 92, 56, 46
    row_h, sep_h, bar_h = 30, 12, 17
    plot_w = 560
    unit = plot_w / max(cap, 12)

    height = pad_t + sum(sep_h if r[0] == "SEP" else row_h for r in rows) + 62
    width = pad_l + plot_w + pad_r

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="本期体量">',
         STYLE,
         f'<rect class="bg" width="{width}" height="{height}" rx="6"/>',
         f'<text class="fg" x="{pad_l}" y="24" font-size="14" font-weight="600">'
         f'本期体量 · {esc(stats["date"])}</text>',
         f'<text class="mut" x="{pad_l}" y="40" font-size="11">'
         f'窗口 {esc(stats.get("window", "-"))} · 虚线为配额上限</text>']

    y = pad_t
    for name, segs, quota in rows:
        if name == "SEP":
            y += sep_h
            continue
        cy = y + row_h / 2
        p.append(f'<text class="fg" x="{pad_l - 10}" y="{cy + 4:.1f}" font-size="12.5" '
                 f'text-anchor="end">{esc(name)}</text>')
        total = sum(v for v, _ in segs)
        x = pad_l
        by = cy - bar_h / 2
        if total == 0:
            p.append(f'<text class="mut" x="{pad_l + 3}" y="{cy + 4:.1f}" font-size="11.5">'
                     f'本线无货</text>')
        for val, color in segs:
            if val <= 0:
                continue
            w = val * unit
            p.append(f'<rect x="{x:.1f}" y="{by:.1f}" width="{w:.1f}" height="{bar_h}" '
                     f'rx="2.5" fill="{color}"/>')
            x += w
        if total > 0:
            p.append(f'<text class="fg" x="{x + 7:.1f}" y="{cy + 4:.1f}" font-size="12" '
                     f'font-weight="600">{total}</text>')
        if quota:
            qx = pad_l + quota * unit
            p.append(f'<line class="q" x1="{qx:.1f}" y1="{by - 5:.1f}" x2="{qx:.1f}" '
                     f'y2="{by + bar_h + 5:.1f}" stroke="{C_QUOTA}" stroke-width="1.4" '
                     f'stroke-dasharray="3,2.5"/>')
            # 配额数字只标在「论文合计」上——那是唯一会逐周变的上限（8 或 12）；
            # 实践/快讯/落选的 4/5/5 是常数，逐行重复只会挤成一团。
            if name == "论文合计":
                p.append(f'<text x="{qx:.1f}" y="{by - 9:.1f}" font-size="9.5" fill="{C_QUOTA}" '
                         f'text-anchor="middle">上限 {quota}</text>')
        y += row_h

    ly = height - 30
    legend = [("全文验证", C_FULL), ("仅摘要", C_ABSTRACT), ("工程实践", C_PRACTICE),
              ("快讯", C_NEWS), ("落选池", C_POOL)]
    lx = pad_l
    for label, color in legend:
        p.append(f'<rect x="{lx}" y="{ly - 8}" width="10" height="10" rx="2" fill="{color}"/>')
        p.append(f'<text class="mut" x="{lx + 14}" y="{ly + 1}" font-size="11">{esc(label)}</text>')
        lx += 16 + len(label) * 11.5
    p.append("</svg>")
    out_path.write_text("\n".join(p), encoding="utf-8")
    return papers


# ---------------------------------------------------------------- 趋势图

SERIES = [
    ("论文详条目", "papers", C_FULL),
    ("全文验证", "full", "#2f8f5b"),
    ("工程实践", "practice", C_PRACTICE),
    ("判断账本累计", "judgments", "#8a5fbf"),
]


def render_trend(all_stats, out_path):
    all_stats = sorted(all_stats, key=lambda s: s["date"])
    dates = [s["date"][5:] for s in all_stats]
    data = {}
    for label, key, color in SERIES:
        if key == "papers":
            vals = [sum(v["full"] + v["abstract"] for v in s["lines"].values()) for s in all_stats]
        elif key == "full":
            vals = [sum(v["full"] for v in s["lines"].values()) for s in all_stats]
        else:
            vals = [s.get(key, 0) for s in all_stats]
        data[key] = vals

    vmax = max(max(v) for v in data.values())
    ymax = ((vmax // 5) + 1) * 5

    pad_l, pad_r, pad_t, pad_b = 46, 118, 48, 44
    plot_w, plot_h = 470, 200
    width = pad_l + plot_w + pad_r
    height = pad_t + plot_h + pad_b

    def px(i):
        return pad_l + (plot_w * i / max(len(dates) - 1, 1) if len(dates) > 1 else plot_w / 2)

    def py(v):
        return pad_t + plot_h - (v / ymax) * plot_h

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="跨期趋势">',
         STYLE,
         f'<rect class="bg" width="{width}" height="{height}" rx="6"/>',
         f'<text class="fg" x="{pad_l - 30}" y="24" font-size="14" font-weight="600">'
         f'跨期趋势（共 {len(dates)} 期）</text>']

    for i in range(0, ymax + 1, 5):
        gy = py(i)
        p.append(f'<line class="grid" x1="{pad_l}" y1="{gy:.1f}" x2="{pad_l + plot_w}" '
                 f'y2="{gy:.1f}" stroke-width="1"/>')
        p.append(f'<text class="mut" x="{pad_l - 8}" y="{gy + 4:.1f}" font-size="10.5" '
                 f'text-anchor="end">{i}</text>')

    for i, d in enumerate(dates):
        p.append(f'<text class="mut" x="{px(i):.1f}" y="{pad_t + plot_h + 20:.1f}" '
                 f'font-size="11" text-anchor="middle">{esc(d)}</text>')

    for label, key, color in SERIES:
        vals = data[key]
        pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(vals))
        p.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" '
                 f'stroke-linejoin="round"/>')
        for i, v in enumerate(vals):
            p.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3.4" fill="{color}"/>')
            p.append(f'<text class="fg" x="{px(i):.1f}" y="{py(v) - 9:.1f}" font-size="10.5" '
                     f'text-anchor="middle">{v}</text>')

    # 右侧图例贴着各自末点放，但末点挨得近时标签会叠在一起——按 y 排序后
    # 强制 15px 最小间距推开。
    ends = sorted(((py(data[k][-1]), lbl, c) for lbl, k, c in SERIES), key=lambda e: e[0])
    placed = []
    for y0, lbl, color in ends:
        ly = y0 if not placed else max(y0, placed[-1] + 15)
        placed.append(ly)
        p.append(f'<text x="{pad_l + plot_w + 9:.1f}" y="{ly + 4:.1f}" '
                 f'font-size="11.5" fill="{color}">{esc(lbl)}</text>')

    p.append("</svg>")
    out_path.write_text("\n".join(p), encoding="utf-8")


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    d = Path(sys.argv[1]).resolve()
    stats = json.loads((d / "stats.json").read_text(encoding="utf-8"))
    n = render_volume(stats, d / "volume.svg")

    all_stats = []
    for f in sorted(d.parent.glob("*/stats.json")):
        all_stats.append(json.loads(f.read_text(encoding="utf-8")))
    render_trend(all_stats, d / "trend.svg")

    print(f"volume.svg  {n} 篇论文 / 实践 {stats['practice']} / 快讯 {stats['news']}")
    print(f"trend.svg   {len(all_stats)} 期")


if __name__ == "__main__":
    main()
