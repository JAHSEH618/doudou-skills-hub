# 落档：两个 Obsidian vault

硬规则 9 的执行细节。规则本身在 SKILL.md：每次运行必落档，两处都写，缺一处即失败，失败要在对话里说明。

## 目录

| 代号 | 路径 | 用途 |
|---|---|---|
| `$DESK` | `/Users/okonma/Desktop/essays/radar/` | 跟论文 PDF 库同处一个 vault，桌面上翻报告时能顺手点开 PDF |
| `$ICLOUD` | `/Users/okonma/Library/Mobile Documents/iCloud~md~obsidian/Documents/radar/` | 独立 vault，走 iCloud 同步，手机上能看 |

`essays/` 既是 Obsidian vault 根，也是 PDF 库（`AI & Agent Related/` 在读、`past/` 存档）。`$ICLOUD` 是另一个独立 vault，只有 radar 报告，里面没有 PDF 库。

iCloud 写失败的常见原因：文件被换出、同步未就绪。要在对话里说清是哪一处、为什么。

## 传输层：直接写文件

用 Write 工具（或 shell 重定向）直接写 `$DESK/<文件名>.md` 和 `$ICLOUD/<文件名>.md`。不要读任何 `.vault-meta/transport.json`——那种快照会陈旧。

图表资源跟着一起走：

```bash
for V in "$DESK" "$ICLOUD"; do
  mkdir -p "$V/assets/<日期>"
  cp reports/assets/<日期>/* "$V/assets/<日期>/"
done
```

报告里的相对路径 `assets/<日期>/xxx.svg` 在三处都成立，正文不用改。

**不要走 `obsidian-cli`**，即使它可用。Obsidian CLI 是 GUI 的遥控器，要求 Obsidian 进程正在运行，不在就会把应用拉起来——跑一次论文扫描顺带弹出笔记软件是纯副作用。本 skill 只需要「往 vault 目录里写一个 md 文件」，filesystem 直写没有任何 GUI 依赖。

（2026-08-23 状态：这台机器 Obsidian 1.13.7，`obsidian-cli` 已随 brew cask 链到 `/opt/homebrew/bin/obsidian`，可用。仍然不用，理由如上，跟可不可用无关。）

Obsidian 会自己发现新文件，不需要通知它。

## 文件命名

| 模式 | 文件名 |
|---|---|
| 周扫 | `周扫 YYYY-MM-DD.md` |
| 定向 | `定向 <主题> YYYY-MM-DD.md` |
| 单篇验证 | `验证 <短名> YYYY-MM-DD.md` |

同日同模式重跑直接覆盖，不留副本。

## 笔记格式

frontmatter 用 YAML，正文是报告全文：

```yaml
---
type: radar
title: "周扫 2026-09-10"
mode: 周扫                        # 周扫 / 定向 / 单篇验证
window: 2026-09-08 → 2026-09-10   # 单篇验证填 -
paper_count: 8                    # 论文详条目数；单篇验证填 1
practice_count: 4                 # 工程实践·详条目数（简条目不计）；没有填 0
news_count: 5                     # 资讯条目数；没有填 0
created: 2026-09-10
updated: 2026-09-10
tags:
  - radar
  - paper
---
```

frontmatter 下面原样贴报告全文——不重写、不摘要、不删节。三份正文（`reports/`、`$DESK`、`$ICLOUD`）必须逐字一致；分歧时以 `reports/` 为准，报告要跟去重账本待在一起，否则会出现「归档里有这篇、去重账本里没有」的漏洞。

## 已有 PDF 交叉引用

`essays/` 下已有的 PDF 就是用户手动存过的论文。某篇候选在库里已有 PDF 时，在该条目后面加一行：

```
📁 已在库：essays/AI & Agent Related/<PDF 文件名>
```

写成纯文本路径，不要写 wikilink。PDF 库只在 `$DESK` 那个 vault 里，`$ICLOUD` 没有；三份正文又必须逐字一致，所以 wikilink 在 iCloud 那份必然是死链。

判断方式：把候选的 arXiv ID 和标题关键词去 `essays/` 下比对文件名，PDF 常按 arXiv ID 或标题命名，两种都要试。比对不上不用勉强。

## 索引维护

每次落档后往两个 vault 各自的 `_index.md` 表格顶部追加一行（最新在上）。两份索引除了开头那段说明可以不同，表格必须一致：

```
| [[周扫 2026-09-10]] | 周扫 | 09-08 → 09-10 | 8 (+4 实践 · 5 资讯) | 2026-09-10 |
```

篇数列写「论文数」，有工程实践详条目追加 `+N 实践`，有资讯追加 `N 资讯`，用 ` · ` 连；实践简条目不进索引。没有非论文就只写论文数。**不加新列**——旧行是 5 列，加列会让历史行错位。

链接用 `[[wikilink]]`（vault 的 `newLinkFormat` 是 shortest、`useMarkdownLinks` 是 false）。`_index.md` 不存在就新建。
