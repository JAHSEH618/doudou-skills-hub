---
type: "radar"
title: "瓶颈移到了模型的外围"
description: "瓶颈从模型和代码本身挪到了它们的外围：Anthropic 公开内部版本控制系统 Scion，monorepo 日合并从 5 月约 2,500 涨到 9 月 3 万+，用控制面加内容寻址数据面拆掉文件 diff 模型；Google Research 同期开源 Harness²，冻结权重、递归调优 agent 的 harness 外壳，三个职业基准单步最高提 11.5 分。另含 Anthropic 将 5% 股权投入公益基金的动态。"
mode: "每日推送"
window: "10-18 → 10-19"
created: "2026-10-19"
updated: "2026-10-19"
supplement_blogs: 0
supplement_x: 0
paper_count: 0
practice_count: 2
practice_abstract_count: 0
news_count: 1
---

# 瓶颈移到了模型的外围

这期的信号都指向同一处：改进的主战场，从模型和代码本身，挪到了它们的外围。Anthropic 的 monorepo 日合并量从 5 月的约 2,500 次涨到 9 月的 3 万+，增量里多数是 agent 的提交——写代码不再是吞吐瓶颈，瓶颈挪到了代码的协作、校验和分发这一层：怎么让上千个 agent 同时改同一个库、互不踩踏，又让每次检查从分钟级回到秒级。Google Research 同期开源了 Harness²，思路正好对偶：模型权重冻结不动，把改进押在包裹模型的那套 harness 外壳上，靠递归调优外壳来抬 agent 的表现。

两份材料，一层是代码的周边基础设施，一层是模型周边的脚手架，方向一致：中心够快之后，可改进的空间往两边移。这期把 Scion 的设计、实测数字和它自己写明的适用边界拆开读，再看 Harness² 怎么在不碰权重的情况下调优外壳、数字和代价各是什么，最后附一条 Anthropic 将 5% 股权投入公益基金的动态。

## 一天三万次合并，文件 diff 撑不住

Scion 要解决的问题，先用三个数字框定。一个内部 monorepo，主分支历史约 100 GB，压缩后的工作副本在 25 GB 以上；光是 CI 每天就要做约 2,500 万次代码检查（还没算开发环境、agent 沙箱和研究任务）。如果沿用「每个分支都拉一份完整快照、每个消费方各拉一份」的朴素做法，一天就是 100 GB 乘以 2,500 万次，超过 600 PB 的 git 流量。

他们此前靠的是「几百个内部 git 镜像」：镜像彼此分叉、再定期和所谓「主数据源」对账。这套用法把延迟藏进了复杂性里，代价是不一致，而且随着 agent 提交量增长彻底不可扩展。Scion 的名字取自 1953 年的科幻片《禁闭岛》（Forbidden Planet）：船上 AI 把创造者的潜意识重建成一个看似真实的投影，船员误以为是现实。取名是刻意的，因为 agent 产出的代码看上去像称职工程师的手笔，其实是一份投影。

## 把版本控制拆成控制面和数据面

Scion 的架构分两层。控制面是权威层，落在 Spanner 上，记录每个文件的每个版本、改了什么、何时改的，也就是「任意时间点的代码库形态」以及从一个形态走到另一个形态的路径。数据面是内容寻址存储（CAS），只存内容寻址的对象：同样的字节只存一份，存进去永不重写，新内容只是追加。

分发靠三级缓存：本机磁盘、区域、全局，每一层都在砍冷启动和拉取时间，官方给的口径是每一级命中率都在 99% 以上。结果是检查从分钟级回到秒级，而且不再需要一个中央「git 镜像」去同步一个巨大的 blob，取而代之的是缓存内容寻址对象、就近服务请求者的全局缓存。

这套设计的血缘是现成的：内容寻址存储、Bazel 的远程缓存、CRDT，以及 Datomic 的「不可变 + 因果一致」。（一方博客，辅助证据，架构叙述与数字均为 Anthropic 自述。）

## 数字和它们的边界

实测数字按原文照录：CI 侧因检查提速收回约 25% 的 CPU 容量；本地开发环境的 checkout 快两个数量级（分钟到秒）；相对原来的 git 镜像部署，基础设施占用在 CPU 和内存上小 200 倍；各级缓存命中率 99% 以上。一个 7 人团队用 5 个月建完 Scion、另一套入库系统 Antique 和约 6 个相邻组件，并完成全量迁移。

两处要标清楚。其一，原文提到用 Claude Mythos Preview（一个预览模型，读者现在测不了）重写 git 到 Scion 的入库管线，内存省 20 倍、提速 4 倍，这是作者侧陈述，没有可复现路径。其二，适用边界是原文自己写死的：Scion 与 git 并非即插即换，只有跑「数万名工程师或 agent 集群」的超大 monorepo 才值得自建；Anthropic 的 token 预算「不是大多数团队能轻易复制的那种约束」，他们是在约束内做工程，没有把约束消除；agent 产出的代码仍要过「称职工程师会对自己工作做的那种校验」，Scion 不降低这条标准。这是一份「特定规模下才成立」的系统设计记录，小团队照搬既没必要也没有前提。

第三方评论两篇作导读：The New Stack 的标题就点出了边界——「Anthropic 为 AI 级编码自研了 git 替代品，但你拿不到」；Simon Willison 的笔记从 git 视角梳理了 Scion 与现有工具的位差。（均为第三方评论，导读；观点归作者，不进入判断账本。） · [The New Stack（10-15）](https://thenewstack.io/anthropic-scion-git-replacement/) · [Simon Willison（10-14）](https://simonwillison.net/2026/Oct/13/redesigning-source-control-at-anthropic/) · [原文（10-13，10-15 更新）](https://www.anthropic.com/engineering/redesigning-source-control)

## 冻结权重，递归调优 agent 的外壳

Harness² 把 agent 拆成「模型 + harness」：模型权重冻结，harness 是包裹模型的那套运行脚手架——系统提示、护栏、记忆、技能、工具指引、脚本、子 agent、中间件插件，一共 8 个可编辑组件，每个挂载成一个文件。要优化的是这套外壳，不是权重。它做两层递归。任务级递归针对当前任务改外壳，走「Propose–Probe–Compose」对比式三步：先跑一遍参考执行，再提两个候选，一个针对跨领域复发的 agent 通病（规划、工具使用、上下文管理），一个针对当前领域的知识与流程；两个候选在同一任务上分别执行、对比行为差异，只保留有执行证据支持的修改。harnessing 级递归在每个任务之后，把采纳的外壳和「在什么条件下、为什么有效」的经验写进一个持续更新的改进库（EXPERIENCE.md），引导下一个任务的调优。整套流程不靠 ground-truth 验证器，靠的是行为对比，不是对答案。

数字按论文照录。在 WorkBuddy-Bench、JobBench 和 Harvey 法律基准（LAB）上，冻结 GLM-5 和 Gemini 3.5 Flash 两个执行器、跑 OpenCode 和 Codex 两套外壳，3 次运行取均值。单步（k=1）在所有配置上都提升：WorkBuddy-Bench 最高 11.5 分（GLM-5 在 OpenCode 下 64.2 到 75.7）、JobBench 4.5 分、LAB 部分通过率 11.8 个百分点；并行递归加到 k=5，再提 2.9–3.9（WB）、3.0–4.2（Job）、2.6–6.7 个百分点（LAB）。一个值得记的结果是弱执行器受益更大：GLM-5 在 WorkBuddy-Bench 和 LAB 上的绝对增益都高于 Gemini 3.5 Flash，论文据此说，一个配了更好外壳的弱模型能跑赢配了弱外壳的强模型。对照里，离线搜索外壳的 Meta-Harness 和检索式记忆 ReasoningBank 表现参差，ReasoningBank 在编码任务上甚至低于基线最多 6.6 分。

几处要标清楚。论文 10-9 就上了 arXiv，但代码开源和曝光在 10-18（v0.1.0，Apache 2.0，仓库 google-research/harness2），本窗口内的信号是开源这件事，不是论文本身。结果全部是 Google 自报，没有独立复现，仓库也明说「不是 Google 官方支持的产品」。代价是真实的：k=1 时单个任务要一次参考执行、两次探针、一次终局执行，token 和墙钟都翻倍往上，论文也把它放在计算-性能的帕累托前沿上读，不是无条件更优。还有安全侧：框架会重写并执行自己的外壳组件，README 直接建议使用者自己沙箱化，评测前关断对基准答案和评分标准的网络访问。这是一份「先穷尽外壳空间再谈权重」的强证据，但它是 v0.1.0、单一机构、绑定 GLM-5 / Gemini 3.5 Flash 与 OpenCode / Codex 这两对组合，换执行器和外壳，数字要重测。

第三方解读一篇作导读：AI In Context 的 Rebecca Stone（10-18）从工程视角把 8 个组件和两步递归拆开，也点出「每任务多次执行」的成本。（第三方解读，导读；观点归作者，不进入判断账本。） · [AI In Context（10-18）](https://www.aiincontext.com/articles/google-open-sources-harness2-framework-that-improves-agents-without-touching-mod-26bc8a57) · [论文（10-9 提交）](https://arxiv.org/abs/2610.14224) · [开源仓库（10-18 曝光）](https://github.com/google-research/harness2)

## 同期产品与工具动态

- 10-18，Anthropic 设立公益基金，承诺把 5% 的公司股份投入新设的 Anthropic Public Benefit Fund（以全资 LLC 而非 501(c)(3) 设立），公司估值每上一个 50% 台阶、董事会可再追加 2%；叠加联创既有捐赠承诺，约 20% 的股份将定向公益。 · Anthropic Newsroom · [原文](https://www.anthropic.com/news/public-benefit-fund)

## 判断账本变动（本期）

- **J8（微调对模型升级结构性脆弱；先把 harness/prompt 空间做到见顶再考虑动权重）追加弱印证（不改状态）**：Harness²（arXiv 2610.14224，v1 提交 10-09、10-18 开源）在权重冻结下单步最高 +11.5 分（WorkBuddy-Bench）、JobBench +4.5、LAB +11.8pp，k=5 并行再 +2.9–4.2；弱执行器（GLM-5）受益更大。为「harness 先行」半句提供直接证据，但不触及「微调对升级是否结构性脆弱」的存疑点，且与本条【存疑】记录的 C4「权重资产 80× 交付优势」构成张力——维持【存疑】，最后更新日期刷至 2026-10-19。
- **Scion**（单一一方博客）不满足证据规则（≥2 独立来源且至少一篇论文），不单独触发任何 J，不进 judgments。

## 落选池（窗口内、已过粗筛、未进正文）

无。窗口内（10-18→10-19）arXiv 四线按提交日期无新提交（各线最新 10-15/16，exa 池 86 篇全 v1=10-15），没有「窗口内已过粗筛」的落选论文。

## 去重与排除记录

- **DeepSeek V4.1-Flash-1017**（10-17）：AIHot 热点命中，第一方 `api-docs.deepseek.com/zh-cn/changelog` 与 `/news/news261017/` 均 curl 200；但已在 2026-10-18 期报过 → 去重排除，不收。
- **Scion**（Anthropic，10-13 发布 / 10-15 更新）：13 个必看博客源窗口内 posts=0，唯一例外是 anthropic 源 1 条 `skipped_no_date`（文章卡片无 `<time>` 元素）。10-18 那次回扫被静默跳过；经核验未出现在 10-18 报告与账本 → 硬规则 19 漏网必看条目，读全文 + 四项核验后作为工程实践详条目收进本期。
- **Harness²**（arXiv 2610.14224）：v1 提交 10-09，早于 exa 搜窗（start=10-15），故未被 exa 四线搜捞到；经 AIHot 热点「Google Research 开源 Harness²」+ web_search 复核，开源事件 10-18 在窗口内 → 补为第二条实践详条目。按开源事件日期收，不是「窗口内新论文」；论文 v1 10-09 如实标注。
- **arXiv 86 篇候选**（exa 四线，includeDomains=arxiv.org，start=10-15 end=10-19）：去重后 86 篇，抽样 20 篇 abs 页核验全部 v1=10-15，落在 10-18→10-19 窗口外 → paper_count=0，无收录。

## 附录 · 核验记录

### 实践详条目核验（两条）

- **Scion（【一方博客】，辅助证据）**
  - 第一方还是转述：第一方（anthropic.com/engineering），非转述。
  - 可验证数字 + 上下文：齐全。日合并 5 月约 2,500 → 9 月 3 万+；主分支历史约 100 GB、压缩工作副本 >25 GB；CI 每天约 2,500 万次检查；朴素全量快照一天 >600 PB git 流量；CI 收回约 25% CPU；checkout 快两个数量级；基础设施 CPU/内存小 200 倍；缓存命中率 99%+；7 人团队 5 个月完成迁移。
  - 时间戳与版本绑定：发布 10-13、更新 10-15（meta + 正文前 40 行核对）；描述的是当前内部系统，无上游推翻。
  - 营销动机：自家系统工程博客，但给出可独立核查的规模数字与适用边界（非即插即换、仅超大 monorepo 值得自建）；「Claude Mythos Preview 重写入库管线，内存省 20×、提速 4×」为作者侧陈述、无可复现路径 → 已在条目内标注。
  - 全文抓取：web_extract 24,074 chars。
  - 解说（硬规则 16）：exa 1 次（无域名过滤，start=10-12 end=10-19）→ The New Stack（10-15）、Simon Willison（10-14）。
- **Harness²（【论文】arXiv 2610.14224，Google Cloud AI Research）**
  - 预印本真实时间线：abs 页 v1 提交 2026-10-09；非旧作换壳，10-18 开源 v0.1.0（Apache 2.0，google-research/harness2）。
  - 代码仓库状态：已开源（10-18 曝光），Apache 2.0；README 自注「非 Google 官方支持的产品」。
  - 基线公平性：4 个基线（含 Meta-Harness、ReasoningBank 离线对照）；结果全部 Google 自报，无独立复现。
  - 硬件/版本适用边界：绑定 GLM-5 / Gemini 3.5 Flash × OpenCode / Codex 两对组合，v0.1.0，单一机构；换执行器/外壳数字需重测。
  - 实验设置：3 次运行均值±SD、#Steps 指标、k=1 主表 / k=5 并行、editor Claude Opus 4.8。
  - 全文抓取：abs 页 web_extract 2,805 chars + HTML 全文 16,715 chars（含 offset 53 段 12,951 chars）；局限/风险段 search 176 matches。
  - 关键数字核对：k=1 WB 最高 11.5（GLM-5 OpenCode 64.2→75.7）、Job 4.5、LAB 11.8pp；k=5 再 +2.9–3.9（WB）/+3.0–4.2（Job）/+2.6–6.7pp（LAB）；弱执行器增益更大；ReasoningBank 编码任务低于基线最多 6.6。
  - 解说（硬规则 16）：web_search + AIHot → AI In Context（Rebecca Stone，10-18）。

### 资讯核验（一条）

- **Anthropic 公益基金**（10-18）：第一方 `anthropic.com/news/public-benefit-fund` curl 200；5% 股份投入 Anthropic Public Benefit Fund（全资 LLC 非 501(c)(3)）、估值每上 50% 台阶董事会可再追加 2%、叠加联创既有捐赠约 20% 定向公益。有第一方公告页 → 进资讯，不作证据。

### 社区/热度核验

- AIHot 扫描：10 热点（含「Google Research 开源 Harness²」「Anthropic 公益基金」「DeepSeek V4.1-Flash-1017」）；HN 窗口内 0 高分相关项。
- X 固定账号（21 个）窗口内全部 0 帖 → X 讨论节不收（宁缺毋滥）。

### 搜索与筛选记录（本期）

1. `fetch_sources.py scan --since 2026-10-18 --out reports/assets/2026-10-19/candidates.json`：since 10-18；errors 0；AIHot 10 热点；HN 0；X 21 账号全 0 帖；13 个必看/被动博客源窗口内 posts 全 0，唯一例外 anthropic 源 1 条 `skipped_no_date`（Scion 卡片无 `<time>`）。
2. Exa 四线搜索（exa_direct.py 直连 REST，includeDomains=arxiv.org，startPublishedDate=2026-10-15，endPublishedDate=2026-10-19，numResults=10，key 走 EXA_KEY 环境变量）：hardware ×4、model ×3、software ×3、eval ×3 共 13 条查询 → 去重 86 篇唯一论文，抽样 20 篇 abs 核验全 v1=10-15（窗口外）。注：exa_api.py 的 `type` 字段当前 API 不接受 "research paper"，已绕过改直连。
3. arXiv API 各线核验：cs.LG 最新 10-15、cs.CL/DC/DB/AR 最新 10-15/16；10-18→10-19 提交窗内四线零新提交。
4. Scion 解说补搜（scion_lookup.py，exa 1 次，无域名过滤）→ The New Stack、Simon Willison。
5. Harness² 发现与核验：AIHot 热点 + web_search「Google Research open source Harness agent optimization framework」→ arXiv 2610.14224；web_extract abs + HTML 全文；web_search（limit 6）复核开源日期 10-18。
6. 资讯核验：web_search「Anthropic Public Benefit Fund site:anthropic.com」→ newsroom 页；curl 200。DeepSeek V4.1-Flash-1017 changelog/news curl 200（去重排除）。
