#!/usr/bin/env python3
"""paper-radar 图表渲染器。只用 Python 标准库，输出 SVG。

用法：
    python3 render_charts.py <assets_dir>

<assets_dir> 形如 reports/assets/2026-09-08，里面要先有一个 stats.json。
渲染三张图到同一目录：
    volume.svg     本期体量（各区条目数 + 配额线）
    judgments.svg  判断账本关系（本期来源 → 动了哪几条 J；stats.json 没有 graph 就不出）
    trend.svg      跨期趋势（自动扫描 assets_dir 的父目录下所有 stats.json）

stats.json 字段见 references/charts.md。
旧格式（2026-09-10 前，只有 practice / news 两个字段）按映射读：practice → practice_full，
news → flash；缺的字段在趋势图上画成断点，不画 0。
SVG 自带浅色/深色两套配色，跟随阅读器主题，Obsidian 和 GitHub 都能正常渲染。
"""

import json
import sys
from pathlib import Path

FONT = "-apple-system, 'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif"

# 两套主题共用的记号颜色：在白底和深底上都能读
C_FULL = "#3b6fd4"       # 全文验证
C_ABSTRACT = "#a8c0e8"   # 仅摘要
C_PRACTICE = "#c07830"   # 工程实践·详
C_PRACTICE_L = "#e8c9a8" # 工程实践·简
C_NEWS = "#2f8f5b"       # 资讯
C_FLASH = "#8a8a94"      # 快讯
C_POOL = "#b0b0ba"       # 落选池
C_QUOTA = "#c0392b"      # 配额线
C_JUDG = "#8a5fbf"       # 判断账本

DEFAULT_CAPS = {"practice_full": 6, "practice_abstract": 8, "news": 8, "flash": 8, "pool": 5}

STYLE = f"""
  <style>
    .bg   {{ fill: #ffffff; }}
    .fg   {{ fill: #24292f; }}
    .mut  {{ fill: #6b7280; }}
    .grid {{ stroke: #e5e7eb; }}
    .box  {{ fill: #f6f8fa; }}
    text  {{ font-family: {FONT}; }}
    @media (prefers-color-scheme: dark) {{
      .bg   {{ fill: #1e1f22; }}
      .fg   {{ fill: #e6e6e6; }}
      .mut  {{ fill: #9aa0a6; }}
      .grid {{ stroke: #3a3d42; }}
      .box  {{ fill: #2a2c31; }}
    }}
  </style>
"""


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def normalize(stats):
    """把旧格式映射成新格式。缺失字段保持 None，让趋势图画断点。"""
    s = dict(stats)
    if "practice_full" not in s:
        s["practice_full"] = s.get("practice")
        s["practice_abstract"] = None
        s["flash"] = s.get("news")
        s["news"] = None
        s["commentary"] = None
    return s


def text_w(s, size):
    """粗估文本宽度：CJK 按 1 em，其余按 0.55 em。"""
    return sum(size if ord(ch) > 0x2E80 else size * 0.55 for ch in s)


# ---------------------------------------------------------------- 体量图

def render_volume(stats, out_path):
    lines = stats["lines"]                      # 四条线，每条 {full, abstract}
    cap = stats["paper_cap"]
    papers_full = sum(v["full"] for v in lines.values())
    papers_abs = sum(v["abstract"] for v in lines.values())
    papers = papers_full + papers_abs

    def q(key):
        return stats.get(key + "_cap", DEFAULT_CAPS[key])

    rows = []
    for name in ("硬件", "模型", "软件系统", "工程方法"):
        v = lines.get(name, {"full": 0, "abstract": 0})
        rows.append((name, [(v["full"], C_FULL), (v["abstract"], C_ABSTRACT)], None))
    rows.append(("SEP", None, None))
    rows.append(("论文合计", [(papers_full, C_FULL), (papers_abs, C_ABSTRACT)], cap))
    rows.append(("SEP", None, None))
    rows.append(("实践·详", [(stats["practice_full"], C_PRACTICE)], q("practice_full")))
    rows.append(("实践·简", [(stats["practice_abstract"], C_PRACTICE_L)], q("practice_abstract")))
    rows.append(("资讯", [(stats["news"], C_NEWS)], q("news")))
    rows.append(("快讯", [(stats["flash"], C_FLASH)], q("flash")))
    rows.append(("落选池", [(stats["pool"], C_POOL)], q("pool")))

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
        by = cy - bar_h / 2
        if any(v is None for v, _ in segs):
            p.append(f'<text class="mut" x="{pad_l + 3}" y="{cy + 4:.1f}" font-size="11.5">'
                     f'本期未统计</text>')
            y += row_h
            continue
        total = sum(v for v, _ in segs)
        x = pad_l
        if total == 0:
            p.append(f'<text class="mut" x="{pad_l + 3}" y="{cy + 4:.1f}" font-size="11.5">'
                     f'本区无货</text>')
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
            p.append(f'<line x1="{qx:.1f}" y1="{by - 5:.1f}" x2="{qx:.1f}" '
                     f'y2="{by + bar_h + 5:.1f}" stroke="{C_QUOTA}" stroke-width="1.4" '
                     f'stroke-dasharray="3,2.5"/>')
            # 配额数字只标在「论文合计」上——那是唯一会逐期变的上限（8 或 12）；
            # 其余配额是常数，逐行重复只会挤成一团。
            if name == "论文合计":
                p.append(f'<text x="{qx:.1f}" y="{by - 9:.1f}" font-size="9.5" fill="{C_QUOTA}" '
                         f'text-anchor="middle">上限 {quota}</text>')
        y += row_h

    ly = height - 30
    legend = [("全文验证", C_FULL), ("仅摘要", C_ABSTRACT), ("实践·详", C_PRACTICE),
              ("实践·简", C_PRACTICE_L), ("资讯", C_NEWS), ("快讯", C_FLASH), ("落选池", C_POOL)]
    lx = pad_l
    for label, color in legend:
        p.append(f'<rect x="{lx}" y="{ly - 8}" width="10" height="10" rx="2" fill="{color}"/>')
        p.append(f'<text class="mut" x="{lx + 14}" y="{ly + 1}" font-size="11">{esc(label)}</text>')
        lx += 20 + text_w(label, 11)
    p.append("</svg>")
    out_path.write_text("\n".join(p), encoding="utf-8")
    return papers


# ---------------------------------------------------------------- 判断账本关系图

EDGE_STYLE = {
    # kind: (stroke, width, dasharray)
    "新增": ("#c0392b", 2.4, None),
    "印证": (C_JUDG, 1.6, None),
    "存疑": ("#c0392b", 1.6, "6,4"),
    "辅助": ("#8a8a94", 1.3, "2,3"),
}
SOURCE_COLOR = {"论文": C_FULL}   # 其余类型（一方博客/工业博客/技术报告/上游变更）统一橙色


def render_judgments(graph, stats, out_path):
    sources = graph["sources"]
    judgs = graph["judgments"]
    edges = graph["edges"]
    if not sources or not judgs or not edges:
        return 0

    # 右列按连着的左列位置排序（重心法），少交叉
    src_idx = {s["id"]: i for i, s in enumerate(sources)}
    def bary(j):
        xs = [src_idx[e["from"]] for e in edges if e["to"] == j["id"] and e["from"] in src_idx]
        return sum(xs) / len(xs) if xs else 1e9
    judgs = sorted(judgs, key=bary)
    jdg_idx = {j["id"]: i for i, j in enumerate(judgs)}

    font = 11.5
    line_h = 15
    box_pad = 8
    col_gap = 150
    pad_t, pad_b, pad_x = 50, 56, 22

    def lines_of(label):
        return [ln for ln in str(label).split("\n") if ln][:2] or [""]

    def box_w(items):
        return max(text_w(ln, font) for it in items for ln in lines_of(it["label"])) + box_pad * 2

    lw = max(150, min(260, box_w(sources)))
    rw = max(170, min(300, box_w([{"label": f'{j["id"]}【存疑】 · {j["label"]}'} for j in judgs])))
    box_h = line_h * 2 + box_pad * 2 - 4
    row_h = box_h + 14

    n_rows = max(len(sources), len(judgs))
    width = pad_x * 2 + lw + col_gap + rw
    height = pad_t + n_rows * row_h + pad_b

    # 两列各自垂直居中
    def top_y(n):
        return pad_t + (n_rows - n) * row_h / 2

    sx0, jx0 = pad_x, pad_x + lw + col_gap
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
         f'viewBox="0 0 {width} {height}" role="img" aria-label="判断账本关系">',
         STYLE,
         f'<rect class="bg" width="{width}" height="{height}" rx="6"/>',
         f'<text class="fg" x="{pad_x}" y="24" font-size="14" font-weight="600">'
         f'判断账本动态 · {esc(stats["date"])}</text>',
         f'<text class="mut" x="{pad_x}" y="40" font-size="11">左列本期来源，右列被动到的判断；'
         f'边的样式见图例</text>']

    def draw_box(x, y, w, label_lines, border, badge=None):
        p.append(f'<rect class="box" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{box_h}" '
                 f'rx="5" stroke="{border}" stroke-width="1.6"/>')
        ty = y + box_pad + line_h - 4
        for i, ln in enumerate(label_lines):
            weight = ' font-weight="600"' if (i == 0 and badge) else ""
            p.append(f'<text class="fg" x="{x + box_pad:.1f}" y="{ty + i * line_h:.1f}" '
                     f'font-size="{font}"{weight}>{esc(ln)}</text>')

    pos_s, pos_j = {}, {}
    for i, s in enumerate(sources):
        y = top_y(len(sources)) + i * row_h
        pos_s[s["id"]] = (sx0 + lw, y + box_h / 2)
        border = SOURCE_COLOR.get(s.get("type", "论文"), C_PRACTICE)
        draw_box(sx0, y, lw, lines_of(s["label"]), border)
        p.append(f'<text class="mut" x="{sx0 + lw - box_pad:.1f}" y="{y + box_h - 5:.1f}" '
                 f'font-size="9" text-anchor="end">{esc(s.get("type", "论文"))}</text>')
    for i, j in enumerate(judgs):
        y = top_y(len(judgs)) + i * row_h
        pos_j[j["id"]] = (jx0, y + box_h / 2)
        doubt = j.get("status") == "存疑"
        border = "#c0392b" if doubt else C_JUDG
        # J 编号并进第一行，框内维持两行，跟左列等高
        lab = lines_of(j["label"])
        lab[0] = j["id"] + ("【存疑】" if doubt else "") + " · " + lab[0]
        draw_box(jx0, y, rw, lab, border, badge=True)

    # 边画在框后面会被框盖住，所以先算框位置再画边，再把框重画一遍太啰嗦——
    # 直接把边插到框元素前面。
    edge_svg = []
    for e in edges:
        if e["from"] not in pos_s or e["to"] not in pos_j:
            continue
        x1, y1 = pos_s[e["from"]]
        x2, y2 = pos_j[e["to"]]
        stroke, sw, dash = EDGE_STYLE.get(e["kind"], EDGE_STYLE["印证"])
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        cx = (x1 + x2) / 2
        edge_svg.append(f'<path d="M{x1:.1f},{y1:.1f} C{cx:.1f},{y1:.1f} {cx:.1f},{y2:.1f} '
                        f'{x2:.1f},{y2:.1f}" fill="none" stroke="{stroke}" '
                        f'stroke-width="{sw}"{dash_attr} opacity="0.9"/>')
    p[4:4] = edge_svg

    ly = height - 26
    lx = pad_x
    for kind, (stroke, sw, dash) in EDGE_STYLE.items():
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        p.append(f'<line x1="{lx}" y1="{ly - 4}" x2="{lx + 26}" y2="{ly - 4}" stroke="{stroke}" '
                 f'stroke-width="{sw}"{dash_attr}/>')
        p.append(f'<text class="mut" x="{lx + 32}" y="{ly}" font-size="11">{esc(kind)}</text>')
        lx += 32 + text_w(kind, 11) + 22
    p.append(f'<rect x="{lx}" y="{ly - 11}" width="12" height="12" rx="2" class="box" '
             f'stroke="{C_FULL}" stroke-width="1.6"/>')
    p.append(f'<text class="mut" x="{lx + 17}" y="{ly}" font-size="11">论文</text>')
    lx += 17 + text_w("论文", 11) + 16
    p.append(f'<rect x="{lx}" y="{ly - 11}" width="12" height="12" rx="2" class="box" '
             f'stroke="{C_PRACTICE}" stroke-width="1.6"/>')
    p.append(f'<text class="mut" x="{lx + 17}" y="{ly}" font-size="11">非论文</text>')

    p.append("</svg>")
    out_path.write_text("\n".join(p), encoding="utf-8")
    return len(edges)


# ---------------------------------------------------------------- 趋势图

SERIES = [
    ("论文详条目", "papers", C_FULL),
    ("全文验证", "full", "#1f6f47"),
    ("实践·详", "practice_full", C_PRACTICE),
    ("资讯", "news", C_NEWS),
    ("判断账本累计", "judgments", C_JUDG),
]


def render_trend(all_stats, out_path):
    all_stats = sorted((normalize(s) for s in all_stats), key=lambda s: s["date"])
    dates = [s["date"][5:] for s in all_stats]
    data = {}
    for label, key, color in SERIES:
        if key == "papers":
            vals = [sum(v["full"] + v["abstract"] for v in s["lines"].values()) for s in all_stats]
        elif key == "full":
            vals = [sum(v["full"] for v in s["lines"].values()) for s in all_stats]
        else:
            vals = [s.get(key) for s in all_stats]
        data[key] = vals

    vmax = max(v for vs in data.values() for v in vs if v is not None)
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
         f'跨期趋势（共 {len(dates)} 期）</text>',
         f'<text class="mut" x="{pad_l - 30}" y="40" font-size="11">'
         f'断开处为该期未统计该项</text>']

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
        # None 处断线：把连续段分开画
        seg = []
        segments = []
        for i, v in enumerate(vals):
            if v is None:
                if seg:
                    segments.append(seg)
                seg = []
            else:
                seg.append((i, v))
        if seg:
            segments.append(seg)
        for seg in segments:
            if len(seg) > 1:
                pts = " ".join(f"{px(i):.1f},{py(v):.1f}" for i, v in seg)
                p.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="2" '
                         f'stroke-linejoin="round"/>')
            for i, v in seg:
                p.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="3.4" fill="{color}"/>')
                p.append(f'<text class="fg" x="{px(i):.1f}" y="{py(v) - 9:.1f}" font-size="10.5" '
                         f'text-anchor="middle">{v}</text>')

    # 右侧图例贴着各自末点放，但末点挨得近时标签会叠在一起——按 y 排序后
    # 强制 15px 最小间距推开。没有末点的（末期未统计）挂在最底下。
    def last_y(key):
        for v in reversed(data[key]):
            if v is not None:
                return py(v)
        return pad_t + plot_h
    ends = sorted(((last_y(k), lbl, c) for lbl, k, c in SERIES), key=lambda e: e[0])
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
    raw = json.loads((d / "stats.json").read_text(encoding="utf-8"))
    stats = normalize(raw)
    n = render_volume(stats, d / "volume.svg")

    n_edges = 0
    jpath = d / "judgments.svg"
    if raw.get("graph"):
        n_edges = render_judgments(raw["graph"], stats, jpath)
    elif jpath.exists():
        jpath.unlink()

    all_stats = []
    for f in sorted(d.parent.glob("*/stats.json")):
        all_stats.append(json.loads(f.read_text(encoding="utf-8")))
    render_trend(all_stats, d / "trend.svg")

    def show(v):
        return "未统计" if v is None else v
    print(f"volume.svg     论文 {n} / 实践 {show(stats['practice_full'])}+{show(stats['practice_abstract'])} "
          f"/ 资讯 {show(stats['news'])} / 快讯 {show(stats['flash'])}")
    print(f"judgments.svg  {n_edges} 条边" if n_edges else "judgments.svg  未生成（stats.json 无 graph）")
    print(f"trend.svg      {len(all_stats)} 期")


if __name__ == "__main__":
    main()
