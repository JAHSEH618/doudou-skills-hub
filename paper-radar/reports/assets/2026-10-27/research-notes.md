# 2026-10-27 研究笔记

## 运行上下文
- 05:00 定时 run（d7f1ea0448ec），窗口 10-22 → 10-27（5 天；上期窗口止于 10-22，中间 4 天未运行；窗口 ≤10 天，未触发硬规则 8 扩容声明）。
- fetch_sources.py scan：AIHot 10 热点 + 172 条，HN 1 条高分帖（Ubicloud vLLM tool-call 修复，132 分），X 固定账号 10 账号有帖（OpenBMB / AntLing 等），一方工程博客 feed 13 源。
- arXiv 窗口：合并 1,399 篇（10-25 窗 970 + fresh 429，零重叠），ID 范围 2610.28693–2610.32982；cs.OS 抓取失败（1 个类目），其余 12 类目正常。
- exa 四线：12 查询 × 8 = 96 篇论文（start 2026-10-15，宽于窗口，账本去重兜底旧文），X 线 2 查询 × 8 = 16 条，全部 0 失败；解说 13 次查询（cm_*，每篇论文/实践详条目一次，硬规则 16 封顶）。
- 博客窗口内新条目：vLLM 3、HF 2、OpenAI 7、NVIDIA Dev 5、PyTorch 1、Raschka 1（教育内容，出范围）；claude.dev、DeepMind、Qwen、Together、Huyen、Lilian Weng 均 0；anthropic-engineering 页面解析失败（0 篇），手动补查见下。

## 来源缺口
- anthropic-engineering feed 解析失败（0 篇，页面结构可能变了）：手动补查 https://www.anthropic.com/engineering，窗口内无新工程文章，Anthropic 线本期无博客条目。
- OpenAI 博客：全文 403（Cloudflare 全域），窗口内 7 条中 Habitat / Securing 两篇经 exa 拉到全文（详条目），其余 RSS 摘要级（资讯/简条目）。
- 解说线：13 次 cm_* 查询大部分返回自动聚合站（arxivsignals、papers.cool 等），按硬规则 16 不收；合格解说 2 条（SkyRL 谈 HyScale、LMSYS 谈 DSV4.1-Flash）进正文并标「解说者观点/框架侧自测」。
- X 线：8 条全部锁定原帖 URL（OpenBMB PostTrainBench、natolambert、emollick、OpenAI Brotli、rohanpaul × 2、Saito × 2）；AntLing Ming-3.0 两帖为 10-19，窗口外，只记账不进正文。

## 判断账本处置记录
- 沙箱逃逸事件（OpenAI 10-23 自报 + Cohere 10-26 自报）：两起独立第一方自报、同方向，但**无论文级证据**，按证据规则（每条判断至少一篇论文）不立判断条目、不进 judgments.md；正文按「第一方自报，无独立复现」表述。下次若出现论文级复现或第三方验证，再考虑新增。
- 账本实际编号止于 J26（10-22 期后状态）；本期新增 J27（MCP 故障容错，论文主证据 ✓），刷新 J4（MXFP4 训练边界）、J6（WAF 印证）、J25（NgramRL 印证）；judgments 总数 27。
- Copilot 轨迹论文与 Green Code 能耗论文为单篇孤立结论，无第二独立来源收敛，按规则不进账本。

## 落选池（4）
- Beyond Hotness（ARM SPE 分层内存表征）· https://arxiv.org/abs/2610.32711 ：硬件可观测方向，非本期论证主干，不凑数。
- Tile-Based Decompression in Compiled GPU Engines · https://arxiv.org/abs/2610.32695 ：压缩 kernel，单一结果无跨源。
- Decode Late, Multiply Once · https://arxiv.org/abs/2610.31913 ：量化点积重表述，理论侧，无 serving 集成。
- Agentic Memory Management Is the Next Frontier of IR · https://arxiv.org/abs/2610.32464 ：视角文，无实证数字。
- 非论文出范围（不入落选池，防重记）：OpenAI ChatGPT work（经济研究数据）、Fanatics / Ultrafast（客户案例）、Raschka 视频课程（教育内容）、AntLing Ming-3.0 两帖（窗口外）。
