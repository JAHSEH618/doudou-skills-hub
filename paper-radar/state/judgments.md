# judgments · 工程判断账本

> 只收跨来源收敛的判断（≥2 个独立来源），单篇孤立结论不进。
> 周扫双向联动：印证→追加证据刷新日期；反驳→标【存疑】并在周报显式提醒。
> 证据以【论文】为主；非论文（一方博客/工业博客/技术报告/上游变更）只能作辅助证据，必须标类型如「（一方博客，辅助证据）」，且不得占多数、不得是唯一证据——每条判断至少一篇论文撑着。
> 【快讯】（X 等社交资讯）一律不得作证据。
> 只增不删：彻底被反驳→标【已废弃】保留原文；合并→保留较小编号，另一条标【已并入 Jx】；J 编号永不复用。
> 首批 10 条提取自 2026-08-10 / 08-17 对话（寻找AI工程化相关论文.txt）。

---

### J1 · 任何推理优化必须在你真实的并发分布下重测，不能照搬论文数字

- **支撑**：Speculative Decoding: Performance or Illusion?（加速比全是 batch=1–4 测的，batch=128 就崩）；QSpec（W4A4「无损」是评测偏差，基准缺多步推理任务就会过于乐观）；FleetSieve（新形态：不只加速比会变——**吞吐相同时 SLO 可行性仍不同**，Chat C128 上 TP4/TP8 都跑 11.27 req/s 但 completion-p99 46.4s vs 25.2s，只有 TP8 过 30s SLO）
- **边界**：对量化、PD 分离、prefix caching、投机解码全部成立；测量类结论普遍适用。FleetSieve 追加一条推论：**低负载下测不出配置错误**（0.7× 需求时富余容量完全掩盖错误决策，1.3× 时才暴露 1.93 req/s + 12.4pp 的损失），压测负载必须打到接近 SLO 边界。TreeWY 追加**第三种 regime 变量：HBM 预算**——同一份 kernel 在 gmu 0.6/并发 256 下吞吐 1.49×、p99 TTFT 约 40× 低，在 gmu 0.9 下拐点根本不出现且吞吐 0.97–0.99×（**略输**）。至此「加速比」这个数字至少要带三个限定：并发分布（J1）、卡型算力-带宽配比（J14）、内存压力 regime（本条）
- **更新**：2026-08-24

### J2 · 约束和数据不要写在 tool/skill description 里——那个位置生效权重垫底，工具的「存在」本身就是压过指令的强信号

- **支撑**：Harness-IF（优先级实测：system prompt/项目文件/user 前，工具描述/skill 描述垫底）；LLM within MCP Matters（54,000 次试验：搜索工具存在时 9 个模型对 instruction 内嵌数据命中率掉到 <15%）；When Single-Agent with Skills Replace MAS（skill 库 |S|>30 相变崩塌，语义混淆度驱动）。工业侧独立佐证：monday.com 工具分级+渐进发现、Stripe ~150 skill 上限（博客，辅助证据）
- **边界**：约束往 system prompt / 项目文件放；per-server prompt engineering 是权宜不是解法。Working Set of a Coding Agent 从反方向印证了项目文件的高权重，并给出代价：标准与代码冲突时 agent 跟标准走，哪怕标准规定的是更差的代码——**一份过时的 convention 文件比没有文件代价更高**，所以项目规则文件必须跟着代码一起维护，不维护就删
- **更新**：2026-08-23

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
- **边界**：验证循环的 +1.5pp 卡在分数分布顶端，是「中游」和「接近榜首」的差距——别因贡献小而砍。Working Set of a Coding Agent 追加两条：全部通过测试的 harness 配置之间 token 消耗差 >10×（同样正确、成本差一个数量级，harness 是可优化维度）；且缺事实时 agent **编造而非阻塞**，所以「读了哪些文件」类的观测指标看到的是一个已被填上的洞——**验证必须打在产出上，不能打在读取行为上**
- **更新**：2026-08-23

### J7 · RAG 里系统级决策压过算法选择；一套省钱默认值：overlap=0、sentence chunking、检索深度封顶 2–3 步、重排保留但必须在自己域上先测

- **支撑**：A Systematic Analysis of Chunking Strategies（overlap 无收益纯增成本；context cliff ~2.5k）；When Is Complex Chunking Worth It · CIKM 2026（复杂 chunking 罕见稳定胜出，最优解随四要素漂移）；Dissecting Agentic RAG（两轮检索捕获五轮 95% 收益；固定 RRF 打败规则路由）；SciRet（域不匹配的 cross-encoder P@5 0.600→0.404）；Agent-Orchestrated Adaptive RAG（同一增强跨域结论翻转，反思机制延迟 6× 换微小提升）；VecBench（pgvector-HNSW 默认 recall 0.257 配置坑）
- **边界**：agentic 增强要选择性、带成本意识地加——DevOps 域 69.2% 查询标准检索就够。When Is Complex Chunking Worth It（CIKM 2026）把这条推到 chunking 环节：8 策略×2 语料×3 embedding 模型同时量效果与系统成本，**昂贵方法（contextual/summary/semantic，都要额外调 LLM）很少稳定胜出**，最优解随 embedding 模型/数据集/语料规模/目标指标四者组合漂移，且效果相近的方法运行成本差很多——chunking 是多目标设计决策，不是「选个最好的」。RAG Deserves an Index（arXiv 2608.20845）把这条推到一个**新轴：把语义工作挪到 ingest 时**（编译 payload 而非指针，溯源做成外键约束）。**扩展时保留其真实强度**：对三种分块基线 32 格全胜，但对最强基线（上下文化分块+混合 RRF+重排）是**统计打平**（88.0% vs 85.2%，p=0.202）**且方向在开发/留出集之间翻转**——真正买到的是 **21× 更少的查询路径 token**（47.7k→2.2k）而不是精度，编译成本在约 580–600 次查询内回本。三处打折：维护那条 33.7× 是合成 pilot 的最好情况上界；抽取与评判共用同一个 Kimi K2.6（见 J13）；完整协议在未核验的 companion report 里。语料只有广播访谈转录——**对 claim 编译最占便宜的形态**，代码/技术文档/高频变更语料未测。顺带独立复现了 context 非精度中性：分块阅读准确率随预算 81%→73%，而编译 payload 的证据覆盖稳在 98–99%
- **更新**：2026-08-24

### J8 【存疑】· 微调对模型升级脆弱是结构性规律，模型迭代越快越成立；先把 harness/prompt 空间做到见顶，再考虑动权重

- **支撑**：MAP/CAP（70% 不微调，理由是升级脆弱+维护成本，因果是结构性的）；One Recipe, Many Harnesses（harness 是补偿层，可演化可蒸馏）。工业侧佐证：Shopify 飞轮明确「harness 改进见顶后才转参数空间」（博客，辅助证据）
- **【存疑】2026-08-24 · UpgradeBench（arXiv 2608.20918）从两个方向挑战**：
  1. **脆弱性不是普遍规律，是分任务的**。九次真实升级跳上，意图分类（数据绑定：标签体系、调用格式）冻结旧专家保留 99–101% 可得收益、耐久 >14 个月，四代过去重训基线只动 0.2 分而 zero-shot 涨 21——底座变强完全没吃掉这个护城河。而 text-to-SQL（底座绑定：推理能力）单跳丢最多 59%、三代内归零、H50 短于一个发布间隔。本条原文按无差别的结构性规律陈述，**过强**。应收窄为：**底座绑定的能力对升级脆弱，数据绑定的能力不脆弱**。
  2. **「harness 先行」这个排序也被顶了一下**：C4 报告权重资产的交付优势约为 prompt 资产的 80×，且**不比 prompt 资产更脆弱**，而 prompt 资产的最优选择反倒**跨代翻转**（prompt 资产自身也是升级脆弱的）。
- **存疑不等于推翻**：C4 是附录 pilot 只测一个 task/hop，证据强度低；UpgradeBench 血脉止于 Qwen3-8B(2025-04)、比发表早 16 个月，日历数字不可外推；且 J8 的另一半支撑（MAP/CAP 的维护成本理由）本篇没测，未被直接反驳。等第二个独立来源再决定是收窄改写还是废弃。
- **边界**：不是「永不微调」——有持续生产失败数据回流能力的团队，权重更新是 harness 天花板之后的下一层
- **更新**：2026-08-24

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

### J13 · 逐题/逐项的差分类指标（transition、expansion、pass@k）必须配单独测量的 null 或冻结对照臂——否则冻结模型自己就能刷出「能力变化」

- **支撑**：Phantom Gains（冻结 Qwen3-8B 走同一评测管线：单次贪心解码给出 clr=1.5，expansion rate=0.280；连「要求 m≥2 次成功」这个自然修复的 null 在 110 次冻结对比上也是 0.058[0.038,0.078] 而非 0）；Beyond Pass@k · arXiv 2608.14711（pass@k 的 n 被普遍误用成单次提交的测试数而非独立 rollout 数，绝对值虚高 0.85–0.97）；Measurement Without Validity · arXiv 2608.00794（任务生成/用户模拟/评判三层复合，有效性上界 V_total ≤ V₁×V₂×V₃，同族模型跨三层时还会更紧）
- **支撑追加（2026-08-24）**：No Judgment Without a Reason · arXiv 2608.20938（Qwen3-1.7B 预测 judgment receipt 达 98.41% 精确准确率，但**对来源顺序做保义置换后同一 receipt 只有 54.8% 能复现**，cube 预测 49.2%——高分掩盖非稳健的干净实例；且该研究**在开结果前用 content hash 冻结**，其预注册假设「cube 监督会改善 receipt 预测」被自己的数据拒绝：−1.42pp[−2.87,−0.30]，0.6B 三种子复现一致）；RAG Deserves an Index · arXiv 2608.20845（**抽取与评判共用 Kimi K2.6**，正是 Measurement Without Validity 说的同族模型跨管线多层导致有效性上界更紧的情形；作者已披露，人工校准与换族重判在做但未落地）
- **边界**：这是评测方法论规则，不针对特定训练方法。四条实操：① null 几乎白送——多臂实验里每条臂的 checkpoint 0 都是对未训练模型的一次独立评测；② 一次冻结对比不构成 null，三臂研究拥有的复现数还不够；③ transition 类指标比 accuracy 少约 10× 统计功效，百题级 pilot 分辨不出来；④ **保义扰动（置换来源顺序、改写不改义）是成本极低、区分度极高的探针**——一个能把 98% 打回 55% 的测试值得对任何高分结果默认跑一遍。与 J10 互补：J10 管「结论会不会过期」，J13 管「结论一开始是不是测量伪影」
- **更新**：2026-08-24

### J14 · 读任何 kernel/量化加速比，先查它测的是哪张卡的算力-带宽配比；中国特供 SKU（H20/L20）算力被砍而带宽基本保留，会系统性放大「省算力」类优化的收益

- **支撑**：FlashPrefill V2（全部实测只在 H20；稀疏注意力正是省算力类优化，微基准 47.26× vs 端到端 SGLang TTFT 4.8×，差一个数量级）；EcoServe（32 卡 L20 上 1.96–2.51× goodput，H100 上作者自承「remains competitive」＝没优势）；Attn-QAT（同一份 kernel B200 上 1.3×、B300 上 1.74×，差别只在指数单元数量）
- **边界**：方向可以反过来——省带宽/省显存类优化在特供卡上收益会被**低估**。与 J9 的关系：J9 是 Blackwell 代际内的非对称缩放，J14 是同代际不同 SKU 间的配比差异，两者叠加意味着「加速比」这个数字不带卡型就没有意义。另注意跟 J12（互联带宽约束架构）是两个独立轴：J12 管节点间，J14 管卡内
- **更新**：2026-08-23
