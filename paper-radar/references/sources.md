# 信源：怎么搜

信源分级表和硬规则在 SKILL.md。这里是执行细节：脚本怎么跑、每类信源怎么找、解说怎么找。

## 一次周扫 / 定向的搜索顺序

1. `python3 scripts/fetch_sources.py scan --since <窗口起点> --out reports/assets/<日期>/candidates.json`（定向加 `--topic "<主题>"`）。一次拉齐 AIHot 热点榜、AIHot 关键词命中、必搜账号本人帖、HN ≥100 分帖，写成候选 JSON。stdout 的摘要先看，JSON 再细读。
2. 论文：四条线逐线用 exa 搜，每线 2–3 个角度（硬规则 3、4）。
3. 非论文：从候选 JSON 里挑，再用 exa 补脚本盖不到的（AIHot 未收录的账号、>7 天前的博客、按来源方名字搜的一方博客）。
4. 解说：每篇论文 `python3 scripts/fetch_sources.py lookup "<标题>"` 一次 + exa 一次（见下）。
5. 快讯与解说里的 X 链接：`fetch_sources.py x <链接>` 核正文，再写。

`candidates.json` 留在 assets 目录里，跟着落档一起走，方便回查当期候选池。

## AIHot

`https://aihot.news/api/v1`，匿名只读，不需要 key，脚本已封装。要知道的几点：

- **窗口只有 24h / 7d**。周扫窗口超过 7 天时 AIHot 只盖后 7 天，脚本 `notes` 会写明，报告开头要照抄一句「AIHot 只盖后 7 天，更早资讯靠 HN 与 exa」。
- `mode=all` 才有基础设施内容；`selected` 池是面向大众的精选，vLLM / SGLang 这类几乎没有。脚本一律用 `all`。
- `q=<X handle>` 能匹配来源名，返回该账号本人的帖（`links.original` 就是 x.com 原帖）。但 AIHot 只收录了它自己的账号清单，`x-accounts.txt` 里的必搜账号多数它没有——脚本会打印「AIHot 未收录」名单，这些走 exa。
- 报告里条目链接一律用 `links.original`（原始出处，硬规则 11），不用站内页。`hot-topics` 的 story 页只在资讯 headline 上作「时间线」附链。
- 许可：个人非商业免费；报告进公开仓库不算镜像，但资讯节末尾要加一行「部分资讯经 AIHOT 聚合发现，链接均指向原始出处」。
- AIHot 挂了（脚本 `errors` 非空）不能静默，报告开头声明，跟 exa 那条同款。

## HN

`hn.algolia.com/api/v1/search`，无需 key，脚本已封装。两个用途：

- **资讯 / 实践候选**：`scan` 按固定关键词查窗口内的帖，**≥100 分**才进候选（低于这个基本没有讨论价值）。Algolia 是全文模糊匹配，脚本已过滤成「关键词每个词都在标题或链接里」。
- **解说**：`lookup "<论文标题>"` 查讨论串，返回分数和评论数。HN 上的博客讨论远比论文多，实践详条目也照查。

引用格式：`[HN 53 评论](https://news.ycombinator.com/item?id=…)`。

## 核一条 X 原帖

exa 抓不到 x.com。用 `python3 scripts/fetch_sources.py x <链接...>`，走公开的 oEmbed 端点拿作者和正文，不需要登录。快讯每条发出前都过一遍，AIHot 给的中文摘要只是索引，正文以 oEmbed 返回为准。

## X 账号清单

`references/x-accounts.txt`，`## 组名 !` 的组每期必搜（推理 / 训练基础设施、模型厂国内），其余组被动收——只从 AIHot 返回里认，不主动搜。

AIHot 未收录的必搜账号走 exa。**不要一个账号一次查询**：按组合并成 2–3 个查询（如「vLLM SGLang FlashInfer release announcement」「DeepSeek Qwen Kimi GLM new model release」），从返回里认 x.com 链接。搜不到就记为本期无货，不为一个账号反复搜。

清单里搜不到的 handle（拼错、改名、停更）直接删。

## 解说（硬规则 16 的执行）

每篇论文两步，封顶：

1. `fetch_sources.py lookup "<标题>"`：HN 讨论串 + AIHot 收录。
2. exa 一次：`query` 写成「X thread or blog post explaining <标题> <arXiv id>」，`objective` 里明说排除 arXiv 本身和自动聚合站。

从返回里挑，按优先级：作者 thread（标「作者侧」）> HN 讨论串 > 第三方人写 thread / 博客 / Substack > 中文媒体 / 知乎 / 公众号 > alphaXiv 人写评论。同档次中文优先。

**不收**：Lattice、emergentmind、deeplearn.org、machineweather、hypaterra、fugumt、arxivlens、papers.cool、paper.dou.ac、newsfi、bittide.aicompass、AI Trend Notifier 这类自动聚合站；alphaXiv 和 HF papers 页的自动 overview；dreaming.press、recsys-frontier 日报、cctest.ai 这类署名「claude-opus · reviewed by a human editor」的 AI 内容站；moltbook 之类 agent 社交网的帖；LinkedIn 上的日报式汇总账号（dAIy、Bayes Labs）。判断标准一条：必须是人在讲这篇论文。附之前打开看一眼，确认是人写的、确实在讲这篇。

一周内的小众论文多数搜不到合格解说，这是常态。找不到就不写解说行；首推例外，必须写「解说：暂无人写解说」。

## 非论文的其他搜法

脚本之外仍走 exa、同样多角度：按来源方名字搜（`Anthropic engineering blog`、`vLLM blog`）；按项目 release 页（GitHub releases / 官方 changelog）；按主题 + 实践词（`engineering blog`、`in production`、`we scaled`）。

## 论文全文获取

优先抓 arXiv 的 HTML 版（abs 页的 HTML 链接，或 `ar5iv.org/abs/<id>`）——PDF 经 exa 抓取常失败或丢公式表格。代码仓库状态直接看 GitHub 仓库页的 commit 活跃度和 fork 基线版本，不轻信论文里「code available」一句话。
