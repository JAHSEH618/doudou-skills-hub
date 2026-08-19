# judgments · 工程判断账本

> 只收跨来源收敛的判断（≥2 个独立来源），单篇孤立结论不进。
> 周扫双向联动：印证→追加证据刷新日期；反驳→标【存疑】并在周报显式提醒。
> 证据以论文为主；工业博客只能作辅助证据，必须标「（博客，辅助证据）」，且不得是唯一证据。
> 只增不删：彻底被反驳→标【已废弃】保留原文；合并→保留较小编号，另一条标【已并入 Jx】；J 编号永不复用。
> 首批 10 条提取自 2026-08-10 / 08-17 对话（寻找AI工程化相关论文.txt）。

---

### J1 · 任何推理优化必须在你真实的并发分布下重测，不能照搬论文数字

- **支撑**：Speculative Decoding: Performance or Illusion?（加速比全是 batch=1–4 测的，batch=128 就崩）；QSpec（W4A4「无损」是评测偏差，基准缺多步推理任务就会过于乐观）
- **边界**：对量化、PD 分离、prefix caching、投机解码全部成立；测量类结论普遍适用
- **更新**：2026-08-17

### J2 · 约束和数据不要写在 tool/skill description 里——那个位置生效权重垫底，工具的「存在」本身就是压过指令的强信号

- **支撑**：Harness-IF（优先级实测：system prompt/项目文件/user 前，工具描述/skill 描述垫底）；LLM within MCP Matters（54,000 次试验：搜索工具存在时 9 个模型对 instruction 内嵌数据命中率掉到 <15%）；When Single-Agent with Skills Replace MAS（skill 库 |S|>30 相变崩塌，语义混淆度驱动）。工业侧独立佐证：monday.com 工具分级+渐进发现、Stripe ~150 skill 上限（博客，辅助证据）
- **边界**：约束往 system prompt / 项目文件放；per-server prompt engineering 是权宜不是解法
- **更新**：2026-08-17

### J3 · Agent 记忆系统的主导成本是构建不是检索；构建应作为独立可调度的后台负载，不挂在请求路径上

- **支撑**：Agent Memory: Characterization and System Implications（构建是 embedding/prefill 主导，与延迟敏感 QA 流量共置直接冲突）；RecMem（延迟固化把构建 token 成本降 87% 且更准，反证构建是主要可优化项）
- **边界**：长生命周期 agent 还要补 maintenance（freshness/裁剪），现有系统普遍缺失
- **更新**：2026-08-17

### J4 · attention 量化上 NVFP4 稳定优于 MXFP4

- **支撑**：Attn-QAT、Search Your Block Floating Point Scales、Diagnosing FP4 Inference 多篇一致；机制上 NVFP4 的 E4M3 scale（16 值组）比 MXFP4 的 E8M0（32 值组）表达力强
- **边界**：结论限 attention 量化；权重 PTQ 另议
- **更新**：2026-08-17

### J5 · 单 agent 起步，多 agent 当作需要实证证明的优化假设；工作状态装得下一个 context window 时，协调是纯开销

- **支撑**：Capable language models can outgrow the benefits of collaboration（~45% 基线分水岭，87% 架构选择准确率）；OrchBench（16k limit +0.302 → 128k +0.007）；Equal Thinking Token Budgets（算力归一化后单 agent 打平或胜出）；Information Bottleneck（MAS 优势只在有界 relay 下）；CLI benchmark 篇（单 agent 全任务族胜且方差小）
- **边界**：context 被污染（非删减）到重度、或真需要分解/角色专业化/交叉验证时 MAS 才有理；无集中验证的 MAS 错误放大 17.2×
- **更新**：2026-08-17

### J6 · Agent 可靠性靠系统级设计（scaffolding、验证门、人在环），不靠模型/算法创新；验证者必须独立于生成者

- **支撑**：MAP/CAP（可靠性是头号难题，解法全是系统级；主动用能力换可靠性）；Where Does Agent Reliability Come From?（scaffolding+prompt +9.5pp vs 验证循环 +1.5pp；验证换回生成模型后救回任务 6→2，模型倾向给自己写的东西找理由）；KDD workshop 确定性断言门 +12.4pp
- **边界**：验证循环的 +1.5pp 卡在分数分布顶端，是「中游」和「接近榜首」的差距——别因贡献小而砍
- **更新**：2026-08-17

### J7 · RAG 里系统级决策压过算法选择；一套省钱默认值：overlap=0、sentence chunking、检索深度封顶 2–3 步、重排保留但必须在自己域上先测

- **支撑**：A Systematic Analysis of Chunking Strategies（overlap 无收益纯增成本；context cliff ~2.5k）；Dissecting Agentic RAG（两轮检索捕获五轮 95% 收益；固定 RRF 打败规则路由）；SciRet（域不匹配的 cross-encoder P@5 0.600→0.404）；Agent-Orchestrated Adaptive RAG（同一增强跨域结论翻转，反思机制延迟 6× 换微小提升）；VecBench（pgvector-HNSW 默认 recall 0.257 配置坑）
- **边界**：agentic 增强要选择性、带成本意识地加——DevOps 域 69.2% 查询标准检索就够
- **更新**：2026-08-17

### J8 · 微调对模型升级脆弱是结构性规律，模型迭代越快越成立；先把 harness/prompt 空间做到见顶，再考虑动权重

- **支撑**：MAP/CAP（70% 不微调，理由是升级脆弱+维护成本，因果是结构性的）；One Recipe, Many Harnesses（harness 是补偿层，可演化可蒸馏）。工业侧佐证：Shopify 飞轮明确「harness 改进见顶后才转参数空间」（博客，辅助证据）
- **边界**：不是「永不微调」——有持续生产失败数据回流能力的团队，权重更新是 harness 天花板之后的下一层
- **更新**：2026-08-17

### J9 · Blackwell（B200）上 attention 已从 GEMM-bound 变为 softmax/SMEM-bound，FP4 的 4× tensor core 优势被指数单元掩盖；「上 Blackwell+FP4=4× 加速」的采购假设是错的

- **支撑**：FlashAttention-4（非对称硬件缩放：tensor core 翻倍、MUFU/SMEM 原地踏步，softmax+SMEM 超过 MMA 25–60%）；Attn-QAT（B200 只有 NVFP4-QK 配置提速 1.3×，额外量化 PV 比纯 BF16 还慢；B300 指数翻倍后 1.74×）
- **边界**：错的程度取决于 B200 还是 B300；混合线性注意力从算法侧绕开同一瓶颈，两条路可叠加
- **更新**：2026-08-17

### J10 · 测量/调研类论文要把数据采集窗口和发表日期分开读；负面/校准类结论比正面结论更可信

- **支撑**：MAP/CAP（12 月发表、数据 4–11 月采，改名重投数据未刷新）；Ao et al. 2026 non-identifiability 定理（架构在工具/检索/transcript 长度上同时有差异时，性能差异无法归因「协调更好」——负面结论恰好不受此混淆）；EcoServe（OSDI '26 发表、arXiv 2025 年 4 月旧作）
- **边界**：这是读法规则不是论文缺陷；快衰减的是快照数字，慢衰减的是结构性论点
- **更新**：2026-08-17

### J11 · 观测先于容错：先建可观测性再谈容错系统，反过来做基本白干

- **支撑**：Meta 失效分析（先知道故障长什么样）→ SysOM-AI/Eroica/ARGUS（观测层）→ ByteRobust（容错系统）的依赖链；SDCs in the Wild（没有 workload 级回放观测，坏卡问题会被当代码 bug debug 几周）
- **边界**：自建集群才完整适用；租云/调 API 团队取其结论部分（loss spike 不一定是你的代码）
- **更新**：2026-08-17

### J12 · 互联带宽反向约束服务架构：论文里的漂亮架构大多默认 NVLink+IB，普通云实例（10–35 Gbps）下结论会翻转

- **支撑**：Pragmatic PD Disaggregation（只有 prefill-heavy + 10B+ 才值得分离）；EcoServe（以太网集群走时间分离，H100 上「remains competitive」=没优势）；SmartGen/Lynx/NetKV（25 Gbps 链路上一次 KV 传输 3.2 秒吃光 TTFT 预算，催生整个「穷人版 PD 分离」设计空间）
- **边界**：读任何服务架构论文先查它假设的互联；你租到的实例网络决定架构能不能抄
- **更新**：2026-08-17
