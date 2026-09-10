# 图表：stats.json 与三张 SVG

一份 `stats.json` 是唯一输入，`scripts/render_charts.py` 一次产出三张 SVG。三张图各回答一个固定问题、各有固定位置，全在「判断账本动态」一节：

| 图 | 回答什么 | 位置 |
|---|---|---|
| `volume.svg` 本期体量 | 各区出了多少条、配额用了几成 | 节头 |
| `judgments.svg` 判断账本关系 | 本期哪些来源动了哪几条 J、怎么动的 | 节中，图后接逐条文字 |
| `trend.svg` 跨期趋势 | 各区条目数与 J 总数逐期怎么走 | 节尾 |

SVG 由脚本生成，Obsidian 和 GitHub 都当普通图片渲染，不依赖 mermaid。2026-09-10 前的关系图是手写 mermaid，Obsidian 内置 mermaid 对 `<br/>`、`==>`、中文标签在不同版本里都翻过车，所以换成了 SVG。

## stats.json

报告定稿后数出各项条目数，写 `reports/assets/<日期>/stats.json`：

```json
{
  "date": "2026-09-10",
  "mode": "周扫",
  "window": "09-08 → 09-10",
  "paper_cap": 8,
  "lines": {
    "硬件":     {"full": 1, "abstract": 1},
    "模型":     {"full": 0, "abstract": 2},
    "软件系统": {"full": 1, "abstract": 2},
    "工程方法": {"full": 1, "abstract": 0}
  },
  "practice_full": 4,
  "practice_abstract": 6,
  "news": 5,
  "flash": 4,
  "pool": 5,
  "commentary": 3,
  "judgments": 16,
  "graph": {
    "sources": [
      {"id": "CE", "label": "Clean Engineering\n2609.04198", "type": "论文"},
      {"id": "DEC", "label": "Decagon 4.7× GPU 效率", "type": "工业博客"}
    ],
    "judgments": [
      {"id": "J15", "label": "共享 endpoint\n不是冻结仪器"},
      {"id": "J8",  "label": "微调对升级脆弱", "status": "存疑"}
    ],
    "edges": [
      {"from": "CE",  "to": "J15", "kind": "新增"},
      {"from": "DEC", "to": "J8",  "kind": "辅助"}
    ]
  }
}
```

字段：

- `lines.*.full` / `abstract`：该线【全文】和【仅摘要】的条目数。
- `paper_cap`：没扩容填 8，扩了填实际上限。
- `practice_full` / `practice_abstract`：工程实践详 / 简条目数。
- `news`：资讯条目数。`flash`：快讯条目数。`pool`：落选池。
- `commentary`：附了解说的论文数（不含「暂无人写解说」）。
- `judgments`：`state/judgments.md` 当前最大 J 编号。
- `*_cap`（可选）：某期配额与默认值（实践详 6 / 简 8 / 资讯 8 / 快讯 8 / 落选 5）不同时写，如 09-08 那期的 `practice_full_cap: 4`。
- `graph`：关系图数据。`sources` 是本期动了账本的来源，`type` 取【论文】/【一方博客】/【工业博客】/【技术报告】/【上游变更】；`judgments` 是被动到的 J，`status: "存疑"` 会画红框；`edges.kind` 只有四种：新增 / 印证 / 存疑 / 辅助。**只放本期真正动过的 J**，别把整本账本画上去。账本没动就不写 `graph`，脚本不出关系图，报告里写「无变化」。
- `label` 里用 `\n` 分行，最多两行；脚本会把 J 编号并进第一行。

单篇验证不写 `stats.json`——写了会污染趋势图。

### 旧格式兼容

2026-09-10 前的文件只有 `practice` 和 `news` 两个字段，脚本按 `practice → practice_full`、`news → flash` 读，缺的字段在趋势图上画断点（不画 0）。08-23 / 08-24 两期保持旧格式不回改；09-08 已迁到新格式。

## 生成

```bash
python3 scripts/render_charts.py reports/assets/2026-09-10
```

脚本只用标准库。输出的 SVG 自带浅色深色两套配色。报告里用相对路径引用：

```
![本期体量](assets/2026-09-10/volume.svg)
![判断账本关系](assets/2026-09-10/judgments.svg)
![跨期趋势](assets/2026-09-10/trend.svg)
```

这个路径在 skill 侧和两个 vault 侧都成立——落档时 `assets/<日期>/` 整个目录跟着复制。

趋势图靠扫描 `assets/*/stats.json` 自动加长。**不要为了画趋势另开第三本账**。

## 论文原图（可选）

首推的全文验证论文，许可证允许时抓一张关键图放进附录该篇的验证记录之后。

**硬规则 13｜只嵌 CC 许可的图，其余只给链接**。报告会进公开仓库，arXiv 默认的 perpetual non-exclusive 许可没有给第三方转载权。抓图前先核：

```bash
curl -sL https://arxiv.org/abs/<id> | grep -o 'creativecommons[^"]*'
```

有 `creativecommons.org/licenses/…` 才嵌。只显示 `nonexclusive-distrib` 的，改成在正文写一句「关键图见原文 Figure N」加链接。

抓和压缩：

```bash
curl -sL https://arxiv.org/html/<id> | grep -o 'src="[^"]*\.png"'
curl -sL -o fig.png "https://arxiv.org/html/<id>v1/<图路径>"
sips -Z 960 -s format jpeg -s formatOptions 82 fig.png --out fig-<id>-fN.jpg && rm fig.png
```

嵌入必须带出处和许可：

```
![FP4 与 BF16 的重建差异](assets/2026-09-08/fig-2609.04105-f5.jpg)
*Figure 5，出自 [arXiv 2609.04105](https://arxiv.org/abs/2609.04105)，CC BY 4.0。<一句话说这张图在讲什么>*
```

论文没有 HTML 版、或者图本身看了也没用的，跳过。这是锦上添花，不是每篇都要凑一张。
