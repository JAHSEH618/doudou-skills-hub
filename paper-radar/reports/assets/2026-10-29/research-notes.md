# 2026-10-29 研究笔记

## 运行上下文
- 17:05 手动补跑（d7f1ea0448ec，补 10-28/10-29 两个失败日），窗口 10-27 → 10-29（2 天；arXiv cutoff 10-26 与上期重叠，账本去重兜底旧文）。窗口 ≤10 天，未触发硬规则 8 扩容声明。
- fetch_sources.py scan：AIHot 143 条，HN 0 条高分帖，X 固定账号 21 账号，一方工程博客 feed 13 源。
- arXiv 窗口：13 类目合并 1,218 篇，ID 范围见 exa/arxiv_window.json；screened 1,226 条（含跨类目去重前）。
- exa 四线：11 论文线查询 × 8 + 2 X 线查询 × 8 = 99 条结果，0 失败（start 2026-10-15，宽于窗口，账本去重兜底旧文）。
- 博客窗口内新条目：HF 3、OpenAI 6、NVIDIA Dev 4、PyTorch 1、DeepMind 2、Together 1；claude.dev、vLLM、Qwen、Raschka、Huyen、Lilian 均 0；anthropic-engineering 页面解析失败（0 篇），见下。

## 来源缺口
- anthropic-engineering feed 解析失败（0 篇，页面结构可能变了）：candidates.json errors 节记录「blog page:anthropic-engineering: anthropic engineering 页解析到 0 篇文章，页面结构可能变了」。Anthropic 线本期靠 exa 与 X 线兜底，进正文 2 条（judgment calls RCT + 漏洞研究），均为摘要级核验。
- OpenAI 博客：窗口内 6 条，Gemini 4 Carbon / Genie 4 为 DeepMind 线资讯；OpenAI 侧进正文 0 条详条目（RSS 摘要级）。
- 8-DGX 补记：NVIDIA「Running Frontier-Class AI Models Across 8 DGX Spark Nodes」2026-10-22 发布，落在上期 10-22 → 10-27 窗口内但上期未处理，本期窗口 10-27 → 10-29 之外——不入本期正文，登记 seen-papers 防重复处理（【补记，不入正文】条目）。

## 判断账本处置记录
- 账本实际编号止于 J26（10-27 期后状态）；本期未新增判断条目，刷新 J19（MXFP8 权重同步 F2 支撑追加）、J26（CF × SGLang 隔离侧 + WAKMan 淘汰策略侧各一条支撑追加）；judgments 总数 26。
- J3 误引修正：KV 泄漏与 WAKMan 两处判分引用由 J3 改判 J26（隔离/容量记账归属）。

## 落选池（6）
- SPARTA（三值权重端侧长上下文）· https://arxiv.org/abs/2610.34824 ：单源结果，未跨源收敛。
- Request-Adaptive Execution（hybrid attention/SSM 逐请求自适应）· https://arxiv.org/abs/2610.37432 ：软件系统线配额已满，贡献点与 MCF 重叠。
- TAO（工具感知联合调度）· https://arxiv.org/abs/2610.37230 ：单源，无独立印证。
- When Is Additional Retrieval Worthwhile?（成本感知 RAG）· https://arxiv.org/abs/2610.37358 ：负面结果向，工程方法线配额已满。
- From Self-Confidence to Statistical Accuracy（HITL 评估）· https://arxiv.org/abs/2610.35698 ：与 TROJAN 方向重叠但在评估侧，留待后续。
- 非论文出范围（不入落选池，防重记）：8-DGX Spark 8 节点（窗口外，补记防重）。

## 发布阻塞与恢复记录
- 本次 run 在 300 次迭代预算耗尽时中断：报告初稿、stats.json、三张图、pr_ledger.py 已落盘；账本回写、链接审计、构建、push 由兜兜会话内续跑完成（2026-10-29 深夜）。
- 中断前模型侧出现「Model busy; unload pending」409（oMLX 卸载窗口），非网关宕机。
