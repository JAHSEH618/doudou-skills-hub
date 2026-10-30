# 2026-10-30 研究笔记

## 运行上下文
- cron 每日推送（d7f1ea0448ec，2026-10-30 12:07 JST 触发），窗口 10-29 → 10-30（1 天）。窗口 ≤10 天，未触发硬规则 8 扩容声明。
- fetch_sources.py scan（后台，exit 0）：AIHot 136 条 + 热点 10 条，HN 1 条高分帖（SkyPilot Grace Blackwell 调度），X 固定 21 账号窗口内全部 0 帖，一方工程博客 feed 13 源，窗口内新条目 10 条（vLLM 1、HF 4、OpenAI 3、NVIDIA Developer 2；claude.dev、DeepMind、PyTorch 与被动组 5 源均 0）。
- **exa 四线论文检索全部失败**：9 条论文线查询（H1/H2/M1/M2/M3/S1/S2/E1/E2）返回 "exceeded your credits limit"，0 成功。降级三级后备：① arXiv API 关键词查询 9 条（原始 122 条，去重后窗口内独特新文 85 篇）；② 博客原文 curl 抓取（OpenAI 3 篇 403 → Wayback 2026-10-29 快照）；③ 内置 web_search（解说 exa 槽 4 条 + 资讯第一方链接定稿 2 条）。**降级已向用户说明，不写入阅读正文**（硬规则 3）。
- 本期产出：论文 8 篇（全文 3 + 摘要 5）、工程实践详 4 / 简 3、资讯 3、X 0（账号无帖，frontmatter supplement_x 0）、落选池 5。

## 来源缺口
- **Exa credits 用尽**（影响全部论文线检索 + 硬规则 16 解说 exa 槽）：论文候选全部来自 arXiv API 关键词查询，会议论文与非 arXiv 源的漏检率高于正常；解说搜索 exa 槽改用内置 web_search。已声明，非静默降级。
- **anthropic-engineering feed 解析失败**（0 篇，页面结构可能变了，errors 节记录，连续第二期）：本期 Anthropic 线 = claude.dev 0 帖 + X 0 帖 + AIHot 无 Anthropic 工程条目 → 正文无 Anthropic 条目。
- **OpenAI 3 篇原文 403**：misalignment / Model Spec / Ropes & Gray 用 Wayback 2026-10-29 快照核验内容；正文三处链接标「链接访问受限」（硬规则 6：403 单独标注，不称失效也不称验证通过）。
- **X 线 0 帖**：21 账号窗口内无帖，报告不设 X 讨论节（真实为空，非漏扫）。
- **36/37xxx 批次冲突核查**：今晨另一运行会话的 arXiv 批次（2610.36–37xxx）经 XML published 字段核验发布日为 2026-10-27，属 10-29 期窗口且已去重；本期窗口（10-29 → 10-30）的独特新文集合为 2610.39xxx，不补入 36/37xxx。
- **anthropic-engineering 之外**：candidates.json 无其他 errors（13 源中 1 错）。

## 硬规则 7 全文验证检查单（3 篇）
- **RLVR 2610.39295（全文）**：① 预印本 2026-10-29 首投，非旧作换壳；同族前作 2511.16231 / 2607.20543 / 2609.22547 已识别并划界（2609.22547 被其作者显式划界）。② 实证 = 转录已发表 pass@k 曲线（Qwen2.5-7B Omni-MATH GRPO），无新训练，无代码开源。③ 基线 = 基座模型（冻结对照臂），公平且恰为 J13 正面范例。④ 适用边界：单模型 × 单数据集；定理前提 exclusive specialization；「单次交叉」是紧界下的观测而非普适交叉数。
- **PDScope 2610.39216（全文）**：① 预印本 2026-10-29。② 许可证 = arXiv perpetual non-exclusive（转载权受限）；代码仓库 = 匿名占位（无独立复现路径）。③ 基线 kTransformers / Fate / HybriMoE / LMDeploy / vLLM，平台 A100/H100/H200 PCIe 4.0×16，无 NVLink/CXL 对比、不支持 overlap。④ 结论绑定 PCIe 4.0 + 24GB 上限 + 论文 batch 分布（batch 16 饱和）。
- **LinQuant 2610.39418（全文）**：① 预印本 2026-10-29。② 理论 + 仿真（Mamba-2 / Nemotron-H 8B 量化罚分 0.370→0.185），无生产 kernel。③ 7 个函数不变量为方法核心，边界 = 线性递归架构，非线性注意力 / 纯 Transformer 未覆盖。

## 硬规则 10 核验记录（实践详 4）
- **ML4 双帖（vLLM serving + HF Le Chonk，2026-10-29 同日开放权重）**：① 双第一方源互核；② 1T / A52B、800K 上下文、GGUF 24GB 单卡、DSpark 每步接受 2.9 token、NVFP4 + DCP/PCP + NIXL、1.65× 等数字齐；③ 绑定 vLLM 当前版本 + Blackwell 平台；④ 厂商发布稿动机已注，数字可跨帖互核。
- **SkyPilot Grace Blackwell（HN 132 分 21 评论）**：① 第一方产品发布稿（推 Platform / Frontier Trainer），动机写入条目；② GR00T N1.7 在 512×GB300 上 +14.4%（NVIDIA GR00T 团队对照，YouTube 发布）、NVL72 16 节点切片可用节点 +27%（对 18 节点切片）；**自查纠正：初稿误记 GR00T 为 2.3×，grep 原文复核后改 +14.4%**；③ NVIDIA 官方发布的切片对照模型作独立锚点；④ 自报集群不可用率 ≈2%。
- **OpenAI misalignment**：① 第一方；② 四层框架 + 3 个真实 incident + 召回率 dashboard，无公开定量阈值（机制级数字齐）；③ 绑定 GPT-6 Astra 线当前版本；④ 安全叙事动机已注，激励问题正面讨论（监控本身制造隐藏激励）。
- **NVIDIA MLIP**：① 第一方；② BF16x9/TF32x3 张量核心 FP32 仿真、17,280 原子 GEMM 2.2–2.5×，实验设置可复现；③ 绑定 Blackwell；④ 厂商性能稿，数字方向与 LinQuant 对读（精度方向相反）。

## 实践简条目与过滤记录（简 3，过滤 2）
- 简：Vera Rubin（NVIDIA，**原帖 2026-08-24，本窗口 feed 重现**，账本原无此条，按原文日期标注）；IBM Granite Switch 4.1.1（HF）；AnySpeechRecognizer + AnyDecisionModel（HF，同一 feed 帖）。简条目未读原文，核验点写进条目。
- 过滤（硬规则 19 记理由）：Model Spec（OpenAI）= 政策/训练规范更新，非工程实践或技术发布；Project ProtoStar（HF）= 开放科学倡议，四线之外。

## 解说搜索（硬规则 16，lookup 1 次 + exa→web_search 1 次封顶）
- SkyPilot：HN 132 分 21 评论（lookup 命中，进正文）。
- OpenAI misalignment：HN 讨论 + Latent Space（细薄）。
- RLVR / PDScope / LinQuant：无现成第三方解说，只记录，正文不写占位。RLVR 同族前作 3 篇经 web_search（exa 降级槽）识别：2511.16231 最早观察到反转；2607.20543 诊断反转并提出 PBA；2609.22547 同期手稿被作者划界。
- vLLM ML4 / HF Le Chonk / MLIP：无合格解说。

## 资讯去重与处置（3 条保留）
- 剔除：Genie 4、Nemotron Transcribe（10-29 期已报，账本查重命中）。
- 保留：Anthropic S-1（anthropic.com/news/s1-sec，10-26 公告，10-29 全文公开）；OpenAI Pro/Business 用量上限翻倍（help.openai.com release note，10-29 @thsottiaux 宣布）；Ropes & Gray 法律尽调（openai.com 案例页）。

## 判断账本处置记录
- J1（并发分布决定收益可见性）、J12（互联带宽反向约束架构）：PDScope 支撑追加（全文，主证据）。
- J4（NVFP4）：ML4 辅助证据追加（一方博客，MoE 专家侧大规模样本，attention 侧边界不变）。
- J13（差分指标配冻结对照臂）、J21（数字带条件集读）：RLVR 机制印证追加（全文，主证据）。
- J28 新增：pass@1 收益带 pass@k 代价（3 篇论文跨源收敛：RLVR 全文主证据 + 2511.16231 / 2607.20543 摘要级前作）。
- judgments 总数 28，本期更新 6 条。正文误引修正：RLVR 节 J1 → J21。

## 链接审计
- audit_links.py --workers 12：324 条 = reachable 256 + x-original 37 + restricted 18 + unverified 13。
- 本期报告内 3 条 restricted（openai.com misalignment、help.openai.com Pro tiers、openai.com ropes-gray，均 403）：正文已加「链接访问受限」短说明；内容经 10-29 存档快照核对，不标失效。
- 其余 restricted / unverified 属历史报告记录，本期未改历史内容。

## 构建与发布
- 构建与 push 结果见本笔记末行（运行后回填）。
