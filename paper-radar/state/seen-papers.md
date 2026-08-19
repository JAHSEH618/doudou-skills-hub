# seen-papers · 去重账本

> 周扫开始前先读本文件。已列条目不重发；有实质新信息（中会/开源/被反驳）才标【更新】重进。
> 去重按内容不只按标题（同一工作可能改名重投，如 MAP → CAP）。
> 「上次周扫」日期只由四线全幅周扫更新；定向/单篇验证不动它。
> 折叠策略：条目满 6 个月压缩成「`- [日期] 标题 · ID/链接`」单行（判词删掉，其价值已沉淀进 judgments.md）。

**上次周扫：2026-08-17**（窗口 08-10 → 08-17，来自对话导出回填）

格式：`- [首推日期] 【溯源】标题 · 会议/机构 · arXiv ID 或会议页链接 —— 当时判词`
（ID/链接为硬要求，无 arXiv ID 的会议论文用会议页链接；2026-08-20 前的旧条目缺 ID 属历史欠账，再次遇到该论文时顺手补上）

## 硬件

- [2026-08-10] 【仅摘要】SDCs in the Wild · OSDI '26 · 字节 —— 合成压测漏 60%+ 坏卡；用触发失败的确切 workload 回放定位；确定性训练吞吐损失仅 0.01%
- [2026-08-10] 【仅摘要】AEGIS: Safeguarding LLM Training at Scale · OSDI '26 · 清华+字节 —— 在线 SDC 检测，cSensor–cVerifier 两阶段，3500 万 GPU 小时 0.86% 开销抓 18 起
- [2026-08-10] 【仅摘要】SysOM-AI · 阿里 · arXiv 2603.29235 —— eBPF 三路信号（CPU 栈/GPU kernel/NCCL）分层差分诊断；8 万 GPU 一年，<0.4% 开销，诊断中位从几天到 10 分钟
- [2026-08-10] 【仅摘要】ARGUS · arXiv 2606.20374 —— 万卡常驻 tracing，KDE 聚类把 kernel 事件压 3700×，<2% 开销
- [2026-08-10] 【仅摘要】Eroica · NSDI '26 —— 10 万卡生产 1.5 年，97.5% 疑难性能问题定位率，一行 import 接入
- [2026-08-10] 【仅摘要】Mycroft · 字节 —— NCCL 集合通信可观测性，<10 个 tracepoint，90% 情况 15 秒检测
- [2026-08-10] 【仅摘要】ByteRobust · SOSP '25 · 字节 —— 9600 卡三个月 ETTR 97%；哲学：快速粗粒度隔离 > 昂贵精确根因
- [2026-08-10] 【仅摘要】Revisiting Reliability in Large-Scale ML Research Clusters · Meta —— 硬件故障只影响 0.2% job 却吃 18.7% 运行时；小 job 应纳入优化目标；含 MTTF 外推模型
- [2026-08-10] 【仅摘要】Sparing Strategies to Minimize Reliability Impact · MLSys 2026 · Meta —— 备件策略闭式解（block 大小/备用数），集群采购直接可用
- [2026-08-10] 【仅摘要】Achieving Cloud-Grade SLOs for Local MoE Inference (CPU–GPU Hybrid) · OSDI '26 —— 商用 CPU + 消费级 GPU 跑旗舰 MoE 不量化不蒸馏；私有化交付的非 H100 路线
- [2026-08-17] 【仅摘要】FlashAttention-4 · MLSys 2026 · Tri Dao 组 —— Blackwell 非对称硬件缩放：tensor core 翻倍但指数单元/SMEM 没动，attention 变 softmax-bound；B200 BF16 1613 TFLOPs/s
- [2026-08-17] 【仅摘要】Attn-QAT —— B200 上 FP4 attention 只有「NVFP4 QK + BF16/FP8 PV」一种配置提速（1.3×）；B300 指数翻倍后同 kernel 1.74×；「上 Blackwell+FP4=4×」假设是错的
- [2026-08-17] 【仅摘要】FOCUS · 腾讯 —— 量化/反量化 scale 解耦，可学习全精度系数；NVFP4 下 Qwen3-4B 恢复 98.2% FP16 准确率，零额外推理开销
- [2026-08-17] 【仅摘要】Search Your Block Floating Point Scales! · MLSys 2026 —— 默认 max-abs 定 scale 次优，E4M3 尾数位可搜索；量化误差降 26%
- [2026-08-17] 【仅摘要】ThriftAttention —— 5% 的 block 走 FP16 就恢复 89.1% 的 FP4→FP16 差距；代价 KV cache 内存 +28%
- [2026-08-17] 【仅摘要】Diagnosing FP4 Inference —— 敏感度地图：MLP up/down projection 一致最敏感，attention projection 低；早期层也可能高敏感（反直觉）
- [2026-08-17] 【仅摘要】Reimagining LLM Inference Infrastructure with Memory-Centric KV Cache Servers · HotInfra 2026 —— 「数据中心在建 GPU 仓库解决内存问题」；CXL PIM 测算每百万 token $0.61 vs $24.24（back-of-envelope，打折看）
- [2026-08-17] 【仅摘要】SAC · 阿里 —— CXL cache line 粒度取稀疏注意力活跃 KV 条目；真实 XConn XC50256 硬件；比 RDMA baseline 吞吐 2.1×、TTFT 9.7×
- [2026-08-17] 【仅摘要】HyMCache · SK hynix —— CXL-HM（少量 DRAM + SSD）；比本地 LMCache 快 3.0×；比 Mooncake 低 30% 但 DRAM 省 16×
- [2026-08-17] 【仅摘要】ITME · SK hynix —— FPGA 原型 + CMM 实测，吞吐 +35.7%，量级小但硬件验证扎实
- [2026-08-17] 【仅摘要】DAK —— TMA 重新用途化直接访问远端内存绕过 HBM 暂存；GH200/NVLink-C2C 上比 SOTA 快 3×
- [2026-08-17] 【仅摘要】CAKE: Compiler–Agent Co-Design for Frontier Kernel Evolution —— agent 写 Cake IR + harness 回定位诊断且自身可演化；生成的 KDA kernel 比官方 FlashKDA 快 2.05×，已提 PR 到 FlashInfer
- [2026-08-17] 【全文】Who Should Own the Expert Cache? · Waterloo —— E=896 万亿 MoE 上民间定理翻转：内核 LRU 与同域 oracle 打平（75.3% vs 74.6%），跨域 oracle 崩 LRU 稳；router 知识该做 admission/advice 不是重造 eviction。保留：依赖未公开 companion paper 的零拷贝读路径，证据集中 GH200
- [2026-08-17] 【仅摘要】FlashMoE —— SSD 专家缓存用 ML 逼近 Belady，比 LRU 高 21% 命中；注意与 Expert Cache 篇结论矛盾——它测的是 E=128 侧，两篇对读看分野

## 模型

- [2026-08-10] 【仅摘要】Give Me BF16 or Give Me Death? —— 量化选型标准参考（50 万次评估）：FP8 基本无损、W4A16 同步最省、W8A8 异步更优；2024 年底作，不覆盖 FP4/NVFP4
- [2026-08-10] 【仅摘要】QSpec: Speculative Decoding with Complementary Quantization · EMNLP 2025 —— W4A4 草稿 + W4A16 验证共享权重零切换成本；顺带戳破 W4A4「无损」是评测偏差（数学/代码掉最多 51%）
- [2026-08-17] 【仅摘要】HALO / HypeNet —— 2.3B token（<0.01% 预训练数据）把 Qwen3 蒸馏成 RNN-attention 混合；512K 解码 3.0×；关键是层选择算法 + HyPE 位置编码
- [2026-08-17] 【仅摘要】MiniCPM-SALA —— 9B 规模落地，稀疏:线性 1:3 混合，成本比从头训降 75%；单 A6000D 256K 达全注意力 3.5×，支持 1M
- [2026-08-17] 【仅摘要】HydraHead —— head 才是混合异构注意力的自然粒度；7:1 LA:FA 匹配 3:1 层级混合；只训 15B token
- [2026-08-17] 【仅摘要】STILL —— 层内混合 + self-saliency 选 token；训练 token 从 1000B+ 砍到 0.04B，恢复 86.2% 全注意力性能
- [2026-08-17] 【仅摘要】DeltaNet / GDN / KDA / GDN-2 统一对照 —— KDA+Muon 验证损失最低，纯 GDN+AdamW 吞吐最高；只测训练吞吐没测推理（作者自承）
- [2026-08-17] 【仅摘要】Beware of the Batch Size —— LoRA 变体互相矛盾的根源是 batch size 超参；调好后 vanilla LoRA 匹配复杂变体；最优 batch size 对 rank/模型尺度不变、对数据集规模敏感（可小模型扫参迁移）
- [2026-08-17] 【仅摘要】Amazon Nova LoRA target module 消融 —— o_proj 单模块惊人一致从不彻底失败，比 o_proj+fc2 只差 2% 但延迟低 22.6%；qkv 单独用波动极大
- [2026-08-17] 【仅摘要】LoRA in RAG Pareto 分析 —— Pareto 前沿全是 q/v-only adapter（结构性，非参数量）；最强 LoRA 3B ≈ 未适配 8B 但省 9GB 显存
- [2026-08-17] 【仅摘要】LoRA 秩选择理论 —— 二分结论：约束 ERM 下 over-ranking 严格有害（r=128 崩到接近随机）；nuclear-norm 后截断下无害
- [2026-08-17] 【仅摘要】SFT vs LoRA vs ICL 对照 —— SFT 16 样本学会新技能但灾难性遗忘；LoRA 遗忘少但要临界数据量；ICL 保旧知识但教不会复杂技能

## 软件系统

### 推理服务与调度
- [2026-08-10] 【仅摘要】Speculative Decoding: Performance or Illusion? · MLSys 2026 · Berkeley —— 首个生产级引擎（vLLM）系统评估：加速比都是 batch=1–4 测的，batch 上去就崩（EAGLE 1.73×→1.21×）；含理论上界推导
- [2026-08-10] 【仅摘要】Strata: Hierarchical Context Caching · OSDI '26 · Stanford+NVIDIA —— HBM/CPU/SSD 三层 KV cache，解 I/O-bound；已进 SGLang 生产，比 vLLM-LMCache 快 5×
- [2026-08-10] 【全文】EcoServe · OSDI '26 · 中山大学 · arXiv 2504.18154 —— 时间维度部分 PD 分离（rolling activation/macro instance），32 卡 L20 以太网 1.96–2.51× goodput。全文验证发现：2025 年 4 月旧作、vLLM 0.7.3 source fork（生产采用=长期背 rebase）、L20 特供卡结论迁移性存疑；「拿走 idea 别拿代码」
- [2026-08-10] 【仅摘要】Pragmatic Exploration of Prefill-Decode Disaggregation · MLSys 2026 · NVIDIA —— 几十万设计点扫描：只有 prefill-heavy + 10B 以上才值得 PD 分离
- [2026-08-10] 【仅摘要】ECHO: KV Cache Offloading for Native Sparse Attention · OSDI '26 —— 稀疏注意力 KV offloading，长上下文吞吐 2.1×
- [2026-08-10] 【仅摘要】SmartGen · arXiv 2607.28150 —— KV 三类差异化传输（普遍重要/上下文相关/不重要），TTST 降 4.3×；针对云上租实例自建推理
- [2026-08-10] 【仅摘要】Lynx · arXiv 2607.01831 —— KV 按比特位切 Anchor/Residual 流渐进传输；INT4 的 TTFT + BF16 的精度
- [2026-08-10] 【仅摘要】NetKV · arXiv 2606.03910 —— 网络感知调度：忽略网络项让「只看缓存」的调度任意次优；评分插件形式，TTFT 最多 -21.2%
- [2026-08-10] 【仅摘要】SmoothAgent · arXiv 2607.00151 —— 上下文工程操作（offload/压缩/摘要）每次打翻 KV cache 触发重 prefill；异步预计算 TTFT 最多降 11.9×

### RL 后训练基础设施
- [2026-08-10] 【仅摘要】Laminar · EuroSys '26 · 港大+字节 —— 轨迹级异步 + relay worker 参数服务；1024 卡 5.48×；接受 staleness 换天花板
- [2026-08-10] 【仅摘要】RollPacker (Tail Batching) · NSDI '26 —— 不放弃同步 RL：长尾 prompt 攒进少数长轮次，只改样本顺序；128 卡 H800 比 veRL 快 2.03–2.56×
- [2026-08-10] 【仅摘要】Weave · OSDI '26 —— 跨 job 编排互填依赖气泡；328×H20+328×H800 成本效率 1.84×
- [2026-08-10] 【仅摘要】DORA · 美团 LongCat —— 多版本流式训练，万卡级生产，端到端 2.12×、rollout 8.2×

### 向量检索
- [2026-08-10] 【仅摘要】Filtered ANN Search in Vector Databases · arXiv 2602.11443 —— FAISS/Milvus/pgvector 过滤策略横评；pgvector 代价优化器常选错计划；低选择性下 IVFFlat 打败 HNSW（反直觉）
- [2026-08-10] 【仅摘要】VecBench · SIGMOD 2026 · 清华 —— 四家横评含动态更新；pgvector-HNSW 默认配置 recall 0.257、调迭代深度到 0.897 的坑
- [2026-08-10] 【仅摘要】PostgreSQL-V · CIDR 2026 · Purdue —— 向量索引从页式存储解耦，比 pgvector 快 8.9×，同接口 drop-in，开源
- [2026-08-10] 【仅摘要】Curator · SIGMOD 2026 —— 低选择性过滤，比 ACORN+预过滤快 20.9×
- [2026-08-10] 【仅摘要】RACORN-1 · arXiv 2607.00768 —— ACORN-1 原地增强不需重建索引
- [2026-08-10] 【仅摘要】Filter-Agnostic Vector Search on PostgreSQL · PACMMOD —— 生产级数据库系统开销分析

### Agent 编排
- [2026-08-10] 【仅摘要】Capable language models can outgrow the benefits of collaboration · Nature MI —— 单 agent 基线 ~45% 是多 agent 收益分水岭；无集中验证的架构错误放大 17.2× vs centralized 4.4×
- [2026-08-10] 【仅摘要】Single-Agent LLMs Outperform MAS Under Equal Thinking Token Budgets —— 算力归一化后单 agent 打平或胜出；MAS 收益部分是未计入的额外算力；context 被污染（非删减）到重度时 MAS 反超
- [2026-08-10] 【仅摘要】When Do Multi-Agent Systems Help? (Information Bottleneck) —— MAS 真正优势只在有界 relay 下；对弱模型稳定有帮助，对强模型缩小甚至反转
- [2026-08-10] 【仅摘要】OrchBench —— per-agent 16k limit 时多 agent +0.302，128k 时 +0.007；工作状态装得下一个 context 时协调是纯开销；附确定性模拟评估工具（1.3% token，r=0.816）
- [2026-08-10] 【仅摘要】When Do Multi-Agent LLM Systems Outperform Single-Agent —— CLI benchmark 单 agent 每个任务族全胜且方差更小；router-guided 比永远单 agent 更差
- [2026-08-10] 【仅摘要】When Single-Agent with Skills Replace MAS and When They Fail —— skill 库容量相变：|S|>30 陡降、120 时剩 45%；驱动退化的是语义混淆度不只是库大小；分层路由救回 +37–40%
- [2026-08-10] 【仅摘要】DACS: Dynamic Attentional Context Scoping —— orchestrator 双模式 REGISTRY(≤200 token 摘要)/FOCUS；flat-context steering 从 N=3 的 60% 崩到 N=10 的 21%；+17–20pp
- [2026-08-10] 【仅摘要】ClawArena-Team —— manager 瓶颈是权限授予不是感知（无模型 workspace 权限精度 >50%）；成本与管理质量脱钩（100× 成本 vs <4× 分数）
- [2026-08-17] 【仅摘要】Harness-IF —— 规则合规率虚高：AP-Acc 比总准确率低 3.6–7.4pp；实际生效顺序 system prompt/项目文件/user 前、工具描述/skill 描述垫底
- [2026-08-17] 【仅摘要】One Recipe, Many Harnesses —— 自演化 harness = 共享抽象 playbook + 不可迁移的生态边际（32–52%）；跨语言 bootstrap 可行（平均保留 0.63）
- [2026-08-17] 【仅摘要】The Scaffolding Matters More Than the Interface —— MCP vs CLI 主导效应是 scaffolding；纯 CLI 便宜 5–28×；agent 经常无视分配的接口，不验证行为的对比测的是未知混合物
- [2026-08-17] 【仅摘要】Trace: TRajectory Attribution for Automated Context Engineering · KDD 2026 —— 轨迹里的隐式不满信号定位失败的 context 源；CREATE vs UPDATE 决策需真读文件（33%→83%）

### Agent 记忆
- [2026-08-10] 【仅摘要】Agent Memory: Characterization and System Implications —— 主导成本是构建不是检索，构建是 embedding/prefill 主导，应作独立后台负载；maintenance 环节普遍缺失
- [2026-08-10] 【仅摘要】RecMem · ACL 2026 Findings —— 延迟固化：先进潜意识层，语义簇复现才调 LLM 抽取；构建 token 成本降最多 87% 且更准；可叠加到现有实现
- [2026-08-10] 【仅摘要】Memory in the LLM Era: Modular Architectures —— 12 方法首次同条件横评；上下文 50%→200% 几乎所有架构 F1 稳步下降（信噪比问题）
- [2026-08-10] 【仅摘要】Memory for Autonomous LLM Agents 综述 —— Pattern B（工作记忆+外部检索）是生产主力；agent 当前输入往往是糟糕的检索 query
- [2026-08-10] 【仅摘要】Hippocampus · MLSys 2026 —— 二进制签名 + 无损 token-ID 流，压缩域 Hamming-ball 搜索；检索延迟 1.1–31.5×；学术味重，瓶颈在延迟才看
- [2026-08-10] 【仅摘要】TiMem / MAGMA / GAM / MemWeaver —— LoCoMo/LongMemEval 刷分系，落地成本高，判为跳过
- [2026-08-17] 【仅摘要】RippleMem —— 自适应联想回忆（锚点→沿关联扩展补证据）；LongMemEval-S 最高 +11.87%，图构建成本降 ~30×（比其他图记忆实用的关键）
- [2026-08-17] 【仅摘要】ERSkill —— 检索行为表示成可执行 skill 与 router 共同演化 +31.3%；偏学术，判为跳过

### RAG
- [2026-08-10] 【仅摘要】A Systematic Analysis of Chunking Strategies —— overlap 无可测收益纯增成本设 0；sentence≈semantic>token≫code；context cliff ~2.5k；最优 context 取决于目标（语义 500 / EM 2.5k）
- [2026-08-10] 【仅摘要】Dissecting Agentic RAG: A Component Ablation —— 固定 RRF 混合检索打败规则自适应路由；两轮检索捕获五轮 95% 收益；重排无条件保留、分解延迟紧张时先砍
- [2026-08-10] 【仅摘要】Is Agentic RAG worth it? · ACL 2026 Industry —— Enhanced RAG vs Agentic RAG 性能+成本对比，工业赛道取舍
- [2026-08-10] 【仅摘要】Agent-Orchestrated Adaptive RAG —— 同一套增强在 DevOps 和 MuSiQue 结论完全相反；反思机制最糟（延迟 6× 换微小提升）；69.2% 查询标准检索就够
- [2026-08-10] 【仅摘要】Retrieval Enhancements for RAG (Deployed Customer Support) · EACL 2026 Industry —— zero-shot LLM 识别高相关段落打败传统 cross-encoder
- [2026-08-10] 【仅摘要】eBay: Optimizing RAG for E-Commerce How-To · ACL 2026 Industry —— 生产系统完整工作流含部署指标
- [2026-08-10] 【仅摘要】SciRet —— MS MARCO 训练的 cross-encoder 在科学语料 P@5 0.600→0.404；重排上线前必须在自己域上测

## 工程方法

- [2026-08-10] 【仅摘要】Measuring Agents in Production (MAP/CAP) · ICLR 2026 · arXiv 2512.04123 —— 生产 Agent 实证调研（20 访谈+306 问卷）；数据采集 2025 年 4–11 月：当论点读别当现状读，步数/框架/评估数字已过期；论点（能力换可靠性、系统级设计解可靠性）衰减慢。已改名 CAP 投 ICML 2026，数据未刷新
- [2026-08-10] 【仅摘要】Where Does Agent Reliability Come From? · arXiv 2607.17044 —— 归因拆解：scaffolding+prompt +9.5pp、验证循环 +1.5pp（但卡在分布顶端）；验证者必须独立于生成者；厂商自评
- [2026-08-10] 【仅摘要】Making Sense of AI Agents Hype —— 234 场从业者演讲的架构模式；样本是公开演讲有幸存者偏差，与 MAP 对读（新鲜度和真实度反着来）
- [2026-08-10] 【仅摘要】Ao et al. 2026 non-identifiability 定理 —— 架构同时在工具/检索/transcript 长度上有差异时，性能差异无法归因「协调更好」；多 agent 论文的负面结论比正面更可信

## 提及未展开（窗口外或判为跳过，防止当新货重推）

- Cascade —— per-request latency budget 调度（8 月初，窗口外）
- FlashBoot —— 亚秒级权重加载（8 月初，窗口外）
- CoinRAG —— nugget 级 KV 复用（8 月初，窗口外）
- MoE-Infinity —— 开源库非论文；落地首选，Expert Cache 篇说明其频率排序部分可能多余
