# seen-papers · 去重账本

> 周扫开始前先读本文件。已列条目不重发；有实质新信息（中会/开源/被反驳）才标【更新】重进。
> 去重按内容不只按标题（同一工作可能改名重投，如 MAP → CAP）。
> 「上次周扫」日期只由四线全幅周扫更新；定向/单篇验证不动它。
> 折叠策略：条目满 6 个月压缩成「`- [日期] 标题 · ID/链接`」单行（判词删掉，其价值已沉淀进 judgments.md）。
> 非论文（工程实践节的详条目与简条目）记在文件末尾的「工程实践（非论文）」一节，带来源标注，简条目再加【仅摘要】；【资讯】【快讯】不进本账本（硬规则 11），解说链接也不进。

**上次周扫：2026-09-08**（窗口 08-24 → 09-08；15 天，已声明扩容至 12 篇）

格式：`- [首推日期] 【溯源】标题 · 会议/机构 · arXiv ID 或会议页链接 —— 当时判词`
（非论文条目：`- [首推日期] 【一方博客/工业博客/技术报告/上游变更】标题 · 来源方 · 原文链接 —— 当时判词`）
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
- [2026-08-23] 【全文】FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving · CASIA+UCAS+微信腾讯 · arXiv 2608.19758 —— 稀疏 prefill 从原型推到生产：mean correction 补极端稀疏精度、FA3/4 对齐 kernel（PackGQA/warp spec/pingpong/FP8）、原生 paged KV + continuous batching 可作 SGLang backend。全文验证：前作 FlashPrefill=arXiv 2603.06199（3 月），公开声明的 V2 非换壳；标题 47.26× 是对过时的 FA2，对 FA3/4 稠密基线 30.49×(FP8)/17.54×(BF16) 但那是稀疏 vs 稠密；**端到端 SGLang TTFT 只有 4.8×**——微基准与端到端差一个数量级。前作仓库是 vLLM 0.10.0/0.12.0 的 patch loader（同 EcoServe 形态，采用即背 rebase），V2 代码未见发布。**全部实测只在 H20**（特供 SKU，算力砍/带宽保留，系统性放大省算力类优化），H100/B200 收益预期缩水
- [2026-08-23] 【仅摘要】PTXBench: Benchmark and Adapt LLMs for GPU Kernel Optimization with Architecture-specific PTX · Stanford(Olukotun)+CMU+RadixArk · arXiv 2608.17379 —— H100/B200 上测 LLM 写架构专属 PTX；方法论贡献是把「目标指令是否真被执行」与「性能是否有竞争力」拆开测，两者不等价；复杂 attention backward 成功率大幅下降；无任何模型稳定匹配前沿库。与 CAKE/KernelArc 连读，是这条线里唯一认真区分"看起来对"和"真的快"的
- [2026-08-23] 【仅摘要】KernelArc: A Multi-Agent Framework for GPU Kernel Optimization · IMEC · arXiv 2608.17071 —— 落选池。多 agent 并行搜 kernel，SOL-ExecBench 若干任务榜首；与 CAKE 高度同构
- [2026-08-23] 【仅摘要】rl-triton: High-Performance Triton GPU Kernels for RL Credit Assignment · arXiv 2608.17641 —— 落选池。七种 RL 信用分配算法统一成一个结合律 scan，比 torch-compile 快 1.6–5.70×；面向大规模并行仿真，LLM 后训练不直接受益
- [2026-09-08] 【全文】Hardware-Aware FP4 FlashAttention-4 · Graphcore Research 技术报告（单作者） · arXiv 2609.04105 —— 把 J9 的根因从「softmax-bound」收窄到 TMEM 512 逻辑列被两 score bank + 两 output bank 吃满的存储所有权问题；Direct-P 在 GB200 上前向 2.13× BF16、单卡 8B 完整更新 1.14×；关键负面结论：每条测过的 MXFP4 P/V 训练轨迹都发散，分布式训练只能留 FP8 P/V。「full FP4」只指 attention 四个操作数，非端到端；继承 HAO AI Lab 调度；复现材料称在附录 E，仓库状态未核
- [2026-09-08] 【仅摘要】TrainSDC: Characterizing and Mitigating Silent Data Corruption in Large Language Model Training · arXiv 2608.30769 —— 前向脆弱性高度依赖位置（Q/K 路径故障产生持续训练偏移），反向脆弱性由梯度指数分布决定而非位置；Q/K 重算 + 残差增益监控 + 指数感知梯度缩放，开销 1.65%–6.76%。是故障注入不是生产坏卡，仅 Llama 3.2-1B / Qwen3-0.6B
- [2026-09-08] 【仅摘要】OCGQuant: Outlier-Companion Grouping for NVFP4 Quantization · EMNLP 2026 Main · arXiv 2609.00066 —— 定义 Collateral Quantization Error，把离群通道与低幅值通道配对改善 NVFP4 block 组成；Llama3/Qwen3 上困惑度最低、下游平均准确率最高，prefill 加速接近 RTN、峰值解码显存持平。只报困惑度+下游平均，缺多步推理任务
- [2026-09-08] 【仅摘要】HBQ: Hierarchical Scaling Block Quantization · arXiv 2609.00450 —— 落选池。大 block + significand 二级缩放，W4A5 达 W4A16 级精度、硅面积小于 NVFP4，配 28nm ASIC；自研加速器团队向

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
- [2026-08-23] 【仅摘要】Learning how to Forget: Fine-tuning for Long-Context Sparse Attention · AWS Labs · arXiv 2608.19920 —— 给稀疏注意力做微调，对任何 KV cache 策略适用，模型与策略协同适配；单张 A100 40GB 可跑；常超过用精确注意力（序列并行）训出的模型。H2O 为其实验中最强策略，配 SDPA kernel。开源库 KeysAndValues（github.com/awslabs/keys_values）
- [2026-08-24] 【全文】TreeWY: Speculative Verification for Gated DeltaNet Hybrids · Thomson Reuters（单作者） · arXiv 2608.20961 —— GDN 混合模型的投机解码内存问题：循环状态是前缀有损摘要不能挪指针回滚，现行 full-state snapshotting 每个 draft 位置存一份完整快照且分支间不可共享。树结构 WY 变换把整棵 draft 树变成一次三角求解，commit 只重建被接受的那个状态，存小伪值矩阵（每头小 128×）。peak KV 低 2–3×，抢占 2531→1365，接受长度基本不变（175 配对点平均 |Δ|=0.039）。全文验证：**收益完全条件性**——gmu 0.6/并发 256 时吞吐 1.49×、p99 TTFT 约 40× 低，内存不紧时 0.97–0.99×（略输），gmu 0.9 拐点根本不出现；**vLLM main 的 fork、明说未上游、无仓库链接**（同 EcoServe/FlashPrefill V2 形态）；基线公平（对 vLLM 生产默认 storeall，附录 D 对 ReplaySSM 同 sweep），但**最接近的并发工作 Bole（arXiv 2608.01651）没做 head-to-head**（Bole 无代码，作者自陈）；边界 = B200 178GiB + Qwen3.5-35B-A3B(TP1)/397B-A17B(TP8) + 贪心 + prefix caching 全程关闭 + 深度 3 MTP。树「已启用且正确，不是提速」
- [2026-08-24] 【仅摘要】Jacobian-guided Noise Injection for Quantization Robustness in LLMs · Amazon · arXiv 2608.20988 —— 把量化稳定性瓶颈指到 softmax（对离群值敏感 + Jacobian 依赖状态），理论上证明压 Jacobian 范数可给退化定界，据此往 pre-attention logits 注零均值高斯噪声、**方差由 Jacobian Frobenius 范数导出**（非拍脑袋、非直接惩罚 Jacobian）。低比特 WikiText 相对困惑度改善最多 40%，SigLIP ImageNet-1K Top-1 相对增益最多 +37%。与 J9 同一算子两端撞上：softmax 同时是性能墙和精度墙。注意是**训练期**策略不是 PTQ 插件
- [2026-08-24] 【仅摘要】Is Multimodal Speculative Decoding Ready for Diffusion-Based Parallel Drafting? · 中国联通+南大 · arXiv 2608.20743 —— 落选池。综述+跨架构实证，结论「块并行/扩散式起草在多模态基本没被探索」。摘要里 3.6× 是 DFlash/DSpark 的**纯文本**数字不是多模态结果
- [2026-08-24] 【仅摘要】Knowing but Not Saying: Preventing Factual Access Failures in LLM SFT via Recall-Anchored Distillation · arXiv 2608.20794 —— 落选池。把 SFT 域外事实退化从「灾难性遗忘」细化成 factual access failure：开放式事实回答失败≠底层事实被抹掉。若成立会改写账本里 SFT-遗忘那条的机制描述
- [2026-08-24] 【仅摘要】Rethinking Expressivity and Efficiency in Test-Time Training (E2-TTT) · Fraunhofer IOSB+NUS+KIT 等 · arXiv 2608.21308 —— 未展开。TTT 靠推理期持续更权重处理长上下文，现有方法在 per-token 更新的表达力与 chunk-wise 近似的硬件效率之间取不好平衡
- [2026-08-23] 【仅摘要】An Empirical Study of Reward Specification and Benchmark Reliability in GRPO-based LLM Unlearning · 瓦伦西亚大学 · arXiv 2608.17804 —— 四种奖励设计对比（LoRA-GRPO/RWKU）；核心是负面结论：优化成功≠行为改变，forget 分数/留出补全审计/终态 rollout 审计/训练动态四个视角互相矛盾；归因到奖励 hacking 端点、GRPO policy-support 限制、探针错配
- [2026-09-08] 【全文】Post-Training Science for Supervised Fine-Tuning · Baseten · arXiv 2609.01244 —— SFT 决策链单变量全扫（Qwen3 0.6–32B + Llama 3.1/3.2，四个客户数据集，LoRA/全量两臂，970/1008 cell）：LoRA 最优 LR 跨尺度跨 family 平坦在 1e-3（≈全量的 33×）且原封迁移到留出 30B MoE，MoE 落在激活/总参的几何平均处；r=64/α=32 站得住，rank 32 只让 0.003 nats；验证 loss 仅在同 cell 内可信、跨 family 不可迁移，Fisher trace 平坦度无额外信息；过约 2 epoch 后 loss 过拟合而判定质量不升、IFEval 退化，加数据不推高 epoch 上限；Muon 优势很窄。四个数据集匿名不公开；生成器与评判器同源（数据由迭代 SFT 改到通过同一 judge 生成）
- [2026-09-08] 【仅摘要】Modern Transformers Are Implicit Hybrids: From Functional Differentiation to Principled Hybrid Architecture Design (HwH) · arXiv 2609.02986 —— RFIS/RPD 两个干预指标给出检索头/位置头完整分类，被中低频带（Global Positional Band）隔开且该边界随训练长度位置尺度移动；两条原则：位置建模只在局部、全局访问走位置无关检索；头粒度分配+按层定制。HwH 用 NoPE FA + LA，FA:LA 低于 1:3 仍保持能力。与账本内 HydraHead（头粒度）同向
- [2026-09-08] 【仅摘要】Behaviorally Effective LoRA Writes Are Sparse and Structured · arXiv 2609.01374 —— 落选池。有行为效果的 LoRA 写入远比低秩参数化暗示的集中，per-module top-k 最优在 k∈{2,4}，晚层 q_proj/o_proj/down_proj 少数方向影响超大；机制漂亮但离可操作还有距离

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
- [2026-08-23] 【全文】FleetSieve: Decision-Critical Profiling for SLO-Aware LLM Fleet Configuration · arXiv 2608.19659 —— 按「测量能多大程度改变下游分配决策」选 profiling 点。**真正值钱的是顺带测出的两个事实**：(1) Chat C128 上 TP4/TP8 都跑 11.27 req/s 但 completion-p99 46.4s vs 25.2s，只有 TP8 过 30s SLO——吞吐相同时可行 TP 仍不同；(2) 16 卡下错误配置在 1.3× 需求损失 1.93 req/s + 12.4pp，0.7× 需求被富余容量完全掩盖——低负载测不出配置错误。方法自身收益报得诚实：固定对比省 6.9%，200 次随机均值 5.4%(CI 3.5–7.2%)，Chat 省 21.5% 而 **Code 类它不是最省的**。全文验证：v1 无换壳；**未见代码仓库**（最大短板）；基线充分（8 种对照同起点同分配器）；边界=单节点 H100 + 31B + FP8 + vLLM + TP{2,4,8} + 关投机解码 + Azure trace，跨节点/MoE/开投机均未测
- [2026-09-08] 【仅摘要】Adaptive Context Parallelism for Production LLM Serving (Vertumnus) · arXiv 2609.04774 —— 请求级按放置代价（预测排队延迟+缓存感知 prefill 时间+GPU 时间成本）在不同 CP 度 worker 间路由，集群级秒级 split/merge 调 worker 构成，加跨 CP 度的全局 prefix-cache 管理；64 卡，最高评测负载下平均 TTFT 最多 -28.1%、token 加权 SLO 达成 +13.3pp。「最高负载下」是作者自加限定（印证 J1）；互联未披露（J12 老问题）
- [2026-09-08] 【仅摘要】ContextPipe: Database-Inspired Context Assembly for Long-Horizon Agents · arXiv 2609.00749 —— 落选池。上下文装配类比查询执行（Plan-Bind-Optimize-Execute-Feedback + EXPLAIN ANALYZE），总 token -31%、LLM 调用 -23%、响应时间 -9%，但 KV cache 命中率下降；仅 SWE-bench Pro Qutebrowser 子集初步评估

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
- [2026-08-23] 【仅摘要】The Working Set of a Coding Agent: Coherence Debt in Repository-Scale Tasks · arXiv 2608.16630 —— 仓库级编码=重建耦合事实图，两条通道（近期上下文/参数记忆）都不覆盖的部分叫 coherence debt。7 模型×5 harness。154 次闭卷试验无一完成；facts 进 prompt 后 299/300 达 ≥9/12。改名版 Pydantic 迁移 70 次里 66 次七个模型停在同一分数、通过完全相同的 24/79 测试。**可用性决定结果，距离不决定**（128K 字符最远端与紧邻编辑处一样好用）。全通过测试的 harness 配置 token 差 >10×。**缺事实产生错的工作而非没有工作**——建立在「读了什么」上的观测看到的是已被填上的洞。标准与代码冲突时跟标准走：**过时 convention 文件比没有文件代价更高**。SWE-bench 上读取行为不再预测成功（参数记忆替代）

- [2026-08-24] 【仅摘要】Don't Solve, Just Compare: Tiny Advisors for Runtime Intervention in LLM Agents (COTA) · 新加坡国立 · arXiv 2608.21027 —— 运行时干预光检测失败不够，还得给恢复方向；但 expert solver / 生成式 critic 两条路都要求干预侧**再具备一次任务求解能力**，与 actor 冗余且贵。COTA 把干预降格成「只做比较」：tiny comparator 判断采样备选是否带来更好后续，反复比较决定是否干预；训练信号来自**同前缀反事实分支**的成对监督；备选作**非绑定建议**返回，重规划仍由原 actor 做。WebShop/ALFWorld/τ³-Retail × 三 actor 九个设置全改善。核心结论：**辅助模型显著弱于 actor 时干预依然有效**——比较比求解便宜。与 J6 同族但更进一步（验证者不但要独立，还可以远弱于生成者）。全是学术环境，无生产轨迹
- [2026-08-24] 【仅摘要】Structure for Reading, Prose for Writing: Asymmetric Structural Conditioning in Multi-Agent Document Authoring · ML Research Labs(Trellis Data) · arXiv 2608.20786 —— 已部署投标应答系统（主权约束下开源权重）对比同机构真实提交的人写标书。**评估方法发现**：评委在 55 节里判不劣 40 / 更优 4 / 无遗漏，但 gap 分类后 **68% 是系统信源里根本没有的内容**，15 个不利判决只有 6 个本可避免——「与 ground truth 有差异」多是信息可得性而非写作质量，不区分会系统性低估此类系统。**条件化不对称**：结构化标记改善抽取（三个阅读任务复现），但**不迁移到条件化**——指令材料从散文转嵌套 XML 使答案质量 74%→48%。另两条：**指名禁止某写法会让它集中而非消失**（96% 残留缺陷落在 prompt 点名的两种形式）；随机标注耦合确定性窗口函数使**字节相同文件**抽出需求数 68→51。一句话：结构放在读的地方，散文与自检放在写的地方
- [2026-09-08] 【仅摘要】Plan Pointers and Record-Directive Form in Budgeted Verification of Inherited Agent Memory · arXiv 2609.03450 —— 十二项预注册研究 14,760 次尝试：长度匹配的「判据」比裸 id 高 35.0 点[+31.2,+38.8]（六个直连厂商模型），但在九模型 OpenRouter 面板上未过预注册优越性判据；判据后追加 id 在三个 Claude 模型上完全抵消（Opus 5: 40/40→0/40），加一行批准语 +96.0 点可救回；换一个记忆库则所有模型都跟随判据。作者自限为「精确编辑在固定面板上的描述性效应」，不做机制主张。材料 Zenodo 冻结外部存档
- [2026-09-08] 【仅摘要】Bilevel Coordinated Reflection: A Game-Theoretic Approach to Multi-Agent LLM Systems · arXiv 2609.02750 —— 落选池。理论含「只观察生成轨迹的 gate 无法一致改进、环境接地的 gate 可以」不可能性结果（与 J6 同向），但实验只有 500 条 SWE-bench 上 72.2% vs 参考 70.8%，增量在噪声内

### Agent 记忆
- [2026-08-10] 【仅摘要】Agent Memory: Characterization and System Implications —— 主导成本是构建不是检索，构建是 embedding/prefill 主导，应作独立后台负载；maintenance 环节普遍缺失
- [2026-08-10] 【仅摘要】RecMem · ACL 2026 Findings —— 延迟固化：先进潜意识层，语义簇复现才调 LLM 抽取；构建 token 成本降最多 87% 且更准；可叠加到现有实现
- [2026-08-10] 【仅摘要】Memory in the LLM Era: Modular Architectures —— 12 方法首次同条件横评；上下文 50%→200% 几乎所有架构 F1 稳步下降（信噪比问题）
- [2026-08-10] 【仅摘要】Memory for Autonomous LLM Agents 综述 —— Pattern B（工作记忆+外部检索）是生产主力；agent 当前输入往往是糟糕的检索 query
- [2026-08-10] 【仅摘要】Hippocampus · MLSys 2026 —— 二进制签名 + 无损 token-ID 流，压缩域 Hamming-ball 搜索；检索延迟 1.1–31.5×；学术味重，瓶颈在延迟才看
- [2026-08-10] 【仅摘要】TiMem / MAGMA / GAM / MemWeaver —— LoCoMo/LongMemEval 刷分系，落地成本高，判为跳过
- [2026-08-17] 【仅摘要】RippleMem —— 自适应联想回忆（锚点→沿关联扩展补证据）；LongMemEval-S 最高 +11.87%，图构建成本降 ~30×（比其他图记忆实用的关键）
- [2026-08-17] 【仅摘要】ERSkill —— 检索行为表示成可执行 skill 与 router 共同演化 +31.3%；偏学术，判为跳过
- [2026-08-23] 【仅摘要】Explicit State Elicitation Is Not Enough: A Controlled Audit of Memory-Policy Classification · arXiv 2608.17247 —— 落选池。显式定义记忆状态有帮助，但加「状态输出字段」几乎无增益；给状态标签只是让预测被标签条件化
- [2026-08-23] 【仅摘要】Remember, Verify, or Ask? Cross-Family Evaluation of Memory Commitment in LLM Agents · arXiv 2608.19564 —— 落选池。记忆-澄清边界 140 场景基准，标注 κ=0.962；模型验证变化事实比向用户澄清歧义可靠得多。规模偏小
- [2026-09-08] 【全文】Measure Before You Manage: Evaluating Agent Working Memory in Coding Agents · Argonne+Columbia+休斯顿大学（AgenticOS workshop） · arXiv 2608.31057 —— 结论是「归因收益之前必须先量什么」：55 条归档轨迹的类型化对象记账显示语义不同的对象留存/压缩行为分化；两个语义感知策略的验证给出两条硬结论——标定期收益不一定迁移到留出任务、名义 token 预算相等不代表送达上下文与管理成本相等；四层框架 stored state/delivered context/management work/outcome。作者自标红线：样本不得相加当独立复现、检索追加实验复用开发集、评测非官方 SWE-bench、主要终点是过程指标、served revision 未钉死（自撞 J15）
- [2026-09-08] 【仅摘要】KVMem: Virtualizing Million-Token Agent Workspaces on a Consumer GPU · arXiv 2609.04852 —— 不压缩不重 prefill：溢出工作区历史作分页 KV 状态存 GPU/主机/NVMe 三层，用模型原生注意力空间索引挑块、物化受原生窗口约束的查询相关执行视图；DeepSWE 长上下文 Qwen3.8-27B 成功率 43.8%→48.4%；本地 24GB RTX 5090 笔记本 GPU 虚拟化 1M token（原生窗口 256K 的 4 倍），单会话 50 tokens/s
- [2026-09-10] 【仅摘要】Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding · Kushal Chakrabarti（单作者） · arXiv 2608.11095 —— 定向「agent 记忆」。1,867 仓库 247,694 条指令生命周期：指令文件一生 +226%，每提交净增 4.9 条，越老越删不掉（log-hazard −0.032/commit）；指令注释在反转 IFEval 里把多余增长从 +211.3% 压到 +1.4%，WildIFEval 指令跟随最多 +23.1%。边界：只测公开 GitHub 的 CLAUDE.md/AGENTS.md/copilot-instructions.md。印证 J2
- [2026-09-10] 【仅摘要】Context as an Environment: Programmatic Context Management for Long-Horizon Agents（Scroll） · 阿里巴巴+哥伦比亚大学 · arXiv 2608.21690 —— 定向「agent 记忆」。append-only 事件日志 + 持久 Python kernel，模型写代码查历史；Qwen3.8-Max 上 LongMemEval_S 94.8%、BEAM_10M 73.1%、LOCA_256K 86.7%。水分：表 2 各行 reader 不同（作者自认非受控对比），弱骨干 LOCA 跌到 22.7%
- [2026-09-10] 【仅摘要】Utility Under Attack: Agent Memory Poisoning and the Limits of Content Screening and Provenance Ranking · Arulnidhi Karunanidhi（独立作者） · arXiv 2608.21230 —— 定向「agent 记忆」。1.2% 平白假陈述把 LongMemEval 精度 0.850→0.300；四段写入筛查拒 0/360；来源加权无可用设置（出厂权重 p=0.80 等于不设防，加大则合法不可信证据也被压，精度 0.0417）。水分：被测筛查是作者自家 Aegis Memory。新增 J18
- [2026-09-10] 【仅摘要】Compact-Memory LLM Agents via Online Max-Member Clustering and Atom-Aware Packing（RSM-full） · arXiv 2609.04915 —— 落选池。4k 预算 83% 全上下文质量 / 32% token；RealMem 上与 BM25-RAG 打平。增量方法
- [2026-09-10] 【仅摘要】Agent Memory Is a Surface for Endogenous Authorization Laundering · arXiv 2609.01836 —— 落选池。五个写入模型在增量更新下为最多 50.2% 未授权请求造出假权限，执行器 98.6% 照办；两种防护以拒合法请求为代价。新增 J18 的来源之一
- [2026-09-10] 【仅摘要】Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory（PlanFence） · Purdue+Exeter · arXiv 2609.03340 —— 落选池。30 个工作流里 freshness-only 执行器全按旧计划行动；协议让计划引用记录并在动作前校验。作者自限为受控安全结果
- [2026-09-10] 【仅摘要】Dual-Layer Agentic Memory with Fast Write Routing and Slow Consolidation · arXiv 2608.22215 —— 落选池。1.7B/8B 级联写入路由剪 68% 冗余、保 98% QA EM；高价值记忆定期 SFT 进参数
- [2026-09-10] 【仅摘要】Understanding Stage-Wise Utility-Risk Trade-offs in LLM Agent Memory（MemGauge） · arXiv 2608.30177 —— 落选池。11 模型分写入/管理/检索三阶段测投毒风险，写入阶段阈值式转变；摘要无数字。新增 J18 的来源之一

### RAG
- [2026-08-10] 【仅摘要】A Systematic Analysis of Chunking Strategies —— overlap 无可测收益纯增成本设 0；sentence≈semantic>token≫code；context cliff ~2.5k；最优 context 取决于目标（语义 500 / EM 2.5k）
- [2026-08-10] 【仅摘要】Dissecting Agentic RAG: A Component Ablation —— 固定 RRF 混合检索打败规则自适应路由；两轮检索捕获五轮 95% 收益；重排无条件保留、分解延迟紧张时先砍
- [2026-08-10] 【仅摘要】Is Agentic RAG worth it? · ACL 2026 Industry —— Enhanced RAG vs Agentic RAG 性能+成本对比，工业赛道取舍
- [2026-08-10] 【仅摘要】Agent-Orchestrated Adaptive RAG —— 同一套增强在 DevOps 和 MuSiQue 结论完全相反；反思机制最糟（延迟 6× 换微小提升）；69.2% 查询标准检索就够
- [2026-08-10] 【仅摘要】Retrieval Enhancements for RAG (Deployed Customer Support) · EACL 2026 Industry —— zero-shot LLM 识别高相关段落打败传统 cross-encoder
- [2026-08-10] 【仅摘要】eBay: Optimizing RAG for E-Commerce How-To · ACL 2026 Industry —— 生产系统完整工作流含部署指标
- [2026-08-10] 【仅摘要】SciRet —— MS MARCO 训练的 cross-encoder 在科学语料 P@5 0.600→0.404；重排上线前必须在自己域上测
- [2026-08-23] 【仅摘要】When Is Complex Chunking Worth It? A Multi-Objective Evaluation of Chunking Methods at Scale · CIKM 2026 · 帕绍大学+IT:U Linz · arXiv 2608.16586 —— 8 策略×2 语料×3 embedding 模型×多规模，同时量检索效果与系统成本（文档吞吐/查询吞吐/峰值内存）。昂贵方法很少稳定胜出；最优解随 embedding 模型/数据集/语料规模/目标指标漂移，无普适赢家；效果相近的方法运行成本差很多。代码 github.com/casparil/chunking-eval
- [2026-08-23] 【仅摘要】From Retrieved Context to Runtime Control: Adaptive Compression for Edge-based RAG · arXiv 2608.19535 —— 落选池。Jetson AGX Thor 实测 7B-8B 生成阶段吃约 90% 延迟/91% GPU 能耗；适中压缩率省 GPU 能耗 53.2%。只在边缘设备成立

- [2026-08-24] 【全文】RAG Deserves an Index: Why Ingest-Time Compilation Beats Query-Time Interpretation · Endgame Labs+武藏野大学 · arXiv 2608.20845 —— 生产 RAG 每次查询让模型重推同一批原文含义再扔掉＝语义层全表扫描；解法是把贵活挪到写入时（ingest-time semantic compilation）。两层：增量维护 embedding + 编译期做过溯源校验的原子 claim。关键区分是**编译 payload 不是指针**（阅读模型直接消费带证据跨度与归属的 claim）。参考实现即普通 PostgreSQL，溯源是外键不是注释，校验门丢弃定位不到引文的候选（20 文档重放拒 1.1%，29 条里 28 条是「模型引用的其实是转述」）。全文验证：对三种分块基线 32 个格全胜（2.2k token 拿 85.2% vs 最好分块 16.3k 拿 72.5%，Holm 后 24 对比全存活），但对**最强基线**（上下文化分块+混合 RRF+重排，预注册）**统计打平**（88.0% vs 85.2%，p=0.202；16384 预算 87.4% vs 83.6%，p=0.076）**且方向在开发/留出集之间翻转**（作者主动报告不利的一半）——**真结论是成本不是精度：打平用约 21× 查询路径 token 买来（47.7k vs 2.2k），每查询再付一遍**；编译全语料 26.3M token/约 $32 ≈ 该语料 580–600 次查询，千次读内回本。三处打折：① 维护「增量比重建便宜 33.7×」是**合成 pilot**、作者自陈理想化属最好情况上界；② **抽取与评判共用 Kimi K2.6**（同族模型跨层，Measurement Without Validity 警告的相关失效，人工校准未落地）；③ 「完整协议与结果」在一份 **companion report** 里本文未承载。语料只有广播访谈转录——**对 claim 编译+溯源最占便宜的形态**，未测代码/技术文档/高频变更语料。独立佐证：分块阅读准确率随预算 81%→73%，fact payload 证据覆盖稳在 98–99%

## 工程方法

- [2026-08-24] 【全文】UpgradeBench: A Decision-Centric Benchmark for Upgrading Fine-Tuned LLM Specialists · 阿里+长江商学院 · arXiv 2608.20918 —— **本周只读一篇**。沿 Qwen 7–8B 完整真实发布序列（1.5-7B-Chat 2024-02 → 2-7B 2024-06 → 2.5-7B 2024-09 → 3-8B 2025-04，14 个月）测九跳，六任务三类、两尺度，训练侧成本一等输出，量化 freeze/port/refresh/retrain 决策。三个常识没活下来：① **脆弱性分任务不普遍**——意图分类冻结跨九跳保留 99–101%、耐久 >14 个月（四代重训基线只动 0.2 分而 zero-shot 涨 21）；text-to-SQL 单跳丢最多 59%、三代归零、H50 短于一个发布间隔；组织变量是**底座绑定 vs 数据绑定**（横切判别/生成的表面区分）。② **裸抄 adapter 由权重连续性决定不由架构形状决定**——架构相同但独立预训练 run 之间 Banking77 92.8%→42.9%（**低于不挂 adapter 的 60.7%**），贴到同权重继续预训练后代则达重训参考水平；OLMo 预注册距离消融：46B token 保留 0.88–0.99、2.9T token 掉地板，退火与 model soup 不额外损伤。③ 权重空间迁移方法在这条真实血脉**三跳里两跳根本没定义**。可抄：预指定决策策略在 33 个 episode 上重放（决策门与打分用不相交两半）**平均质量后悔 0.37pp、零行为回退、只花永远重训 1/3 预算**；CKA 探针（256 prompt）排可移植性 Spearman 0.74。全文验证：v1 无换壳（早期草稿的「half-life」已拆成 H50/H0）；**数据窗口 vs 发表差约 16 个月**——血脉止于 Qwen3-8B(2025-04)，Qwen3.5(2026-02) 不在内，日历数字不可外推、可外推的是底座/数据绑定这个结构性论点；**声明释出全部产物但正文无仓库 URL、检索也没找到**（最大短板）；基线罕见扎实（固定 QLoRA 配方、底座恒定、配对 bootstrap CI、OLMo 三条预测预注册、R 只在 O−F 下界 >2pp 时展示）；边界＝**整个研究 98 次训练/193 评测格跑在一张 RTX 4090**，只覆盖 QLoRA 不覆盖全参，7–8B 与 1.5–1.8B，Qwen+OLMo，不涉 MoE；C4「权重资产优势约 prompt 资产 80×」是**附录 pilot 只测一个 task/hop**，强度远低于正文
- [2026-08-24] 【仅摘要】No Judgment Without a Reason: Counterfactual Receipts for Versioned AI Evaluators · 阿里+长江商学院（与 UpgradeBench 同组作者同日两篇） · arXiv 2608.20938 —— 评委可以**保住正确标签却因错误理由改判**，而多数协议只记标签对不对。把评委状态拆成 grounds/norms/authority 三类有类型来源，替换任意子集得八格 judgment cube；judgment receipt = 能复现修订裁决的极小来源替换族。关键区分：**执行过的反事实才能认证 receipt，语言模型只能预测一张**。ReasonBench：845 独立切分来源单元→19,520 case + 7,200 配对对照，五种子研究开结果前用 content hash 冻结。Qwen3-1.7B 直接预测 receipt 达 **98.41%**；预测完整 cube 反降至 96.99%，配对差 −1.42pp[−2.87,−0.30]——**冻结前登记的「cube 监督会改善」假设被拒**，Qwen3-0.6B 三种子复现一致(−1.26pp)。**真正产出是高分掩盖了什么：保义置换来源顺序后同一 receipt 只有 54.8%(直接)/49.2%(cube) 能复现**。可抄：把评委版本迁移当需认证对象 + 上保义置换测试（把 98% 打回 55% 的低成本探针）
- [2026-08-24] 【仅摘要】Beyond Endpoint Gains: A Weight-Delta Audit of Medical Specialization · IIT Kanpur+Oracle Health AI+MBZUAI · arXiv 2608.20768 —— 落选池。不看端点分差而审计「释出的权重更新本身」，配对 weight-delta path audit，用两对公开的通用→医疗专家 checkpoint。与 UpgradeBench 是同一问题的另一侧切法
- [2026-08-24] 【仅摘要】When Trust Meets Truth: Trust–Truth Separability in LLM-as-Judge · NII+阿姆斯特丹大学等 · arXiv 2608.21097 —— 落选池。LLM 评委多维评估里「可信」与「为真」能否分开。与 No Judgment 同线，规模较小
- [2026-08-24] 【仅摘要】Asymmetric Capacity Allocation in Self-Refinement Pipelines · UCI+Drexel · arXiv 2608.21345 —— 落选池。首个按阶段（生成/批判/修订）系统考察模型尺寸的工作，指出把模型尺寸当实现细节会浪费资源。方向对，数字待核

- [2026-08-10] 【仅摘要】Measuring Agents in Production (MAP/CAP) · ICLR 2026 · arXiv 2512.04123 —— 生产 Agent 实证调研（20 访谈+306 问卷）；数据采集 2025 年 4–11 月：当论点读别当现状读，步数/框架/评估数字已过期；论点（能力换可靠性、系统级设计解可靠性）衰减慢。已改名 CAP 投 ICML 2026，数据未刷新
- [2026-08-10] 【仅摘要】Where Does Agent Reliability Come From? · arXiv 2607.17044 —— 归因拆解：scaffolding+prompt +9.5pp、验证循环 +1.5pp（但卡在分布顶端）；验证者必须独立于生成者；厂商自评
- [2026-08-10] 【仅摘要】Making Sense of AI Agents Hype —— 234 场从业者演讲的架构模式；样本是公开演讲有幸存者偏差，与 MAP 对读（新鲜度和真实度反着来）
- [2026-08-10] 【仅摘要】Ao et al. 2026 non-identifiability 定理 —— 架构同时在工具/检索/transcript 长度上有差异时，性能差异无法归因「协调更好」；多 agent 论文的负面结论比正面更可信
- [2026-08-23] 【全文】Phantom Gains: Auditing Self-Improvement Against a Measured Null · UCD+Georgia Tech+大连理工 · arXiv 2608.20290 —— **本周只读一篇**。Qwen3-8B 三轮 rank-32 LoRA 自训练 + 冻结 θ₀ 对照走同一管线，找出七个测量失效点，每个缺对照时都会反转结论。F1 单次贪心解码非状态：冻结模型自比得 6 学会/9 退化，clr=1.5（batching 伪影；串行去掉 3/4，但仍有 2% 贪心判定会变）。F2 expansion 统计量无 null：冻结模型 k=128 评两次「扩展」7/25 道 AIME，rate=0.280。F7 藏在 F2 的修复里：m≥2 阈值的 null 在 110 次冻结对比上是 0.058[0.038,0.078] 而非 0。另有 F3 固定 token 上限遇风格漂移把最有效臂判为最破坏、F4 transition 指标比 accuracy 少约 10× 功效、F5 种子方差 clr 跨 0.55–1.53、F6 欠功效探针造出 10 点幽灵安全下降。修正后：外部蒸馏改善 8–11/22 道稀达题，三种自训练 0–2 道（β=1.91, p<1e-8）；自训练破坏 88–106/1163 道 band 题 vs 地板 8。全文验证：v1 无换壳；仓库 github.com/chengxuphd/phantom-gains（Apache-2.0，2026-08-19 建，复现不需 GPU/网络，但 0 star/1 贡献者无第三方验证）；对照设计本身即论点（冻结对照同管线 + 蒸馏正对照三方面对齐）；边界=单模型族+仅 LoRA+3 轮，**具体数值别外推，可外推的是方法论**——多臂实验每条臂的 checkpoint 0 都是未训练模型的独立评测，null 几乎白送
- [2026-09-08] 【全文】Clean Engineering, Unstable Measurement: A Preregistered Reliability Failure of Black-Box LLM Observers on Shared Endpoints · 谢菲尔德大学+Ranplan Wireless/Cambridge AI+ · arXiv 2609.04198 —— **本周只读一篇**。两轮预注册战役都卡在仪器验证：同窗口重复排序 Spearman 0.400（要求 0.90）、逐字节隔日重放 0.78（要求 0.99），而投递/schema/请求哈希/metadata 全满格。三机制：标签-语义映射偏置强度与信号相当、候选分差低于噪声底七个数量级、逐字节相同输入返回不同排序被 exact-permutation 读数放大。换指标无用；748,000 次调用的模拟设计 500 次过 0 次。等一天无用（0.805 vs 0.800）、换厂商无用（四家三辖区共享噪声底 0.74–0.88，system_fingerprint 三种模式都不预测）、自建 batch-invariant kernel 只在空闲时有用（并发下分歧 8.4×）、读数区分度跟错误类型走不跟大小走。**52,988 是审计量不是样本量**（真实为 31 任务组/100 重放对/每臂 10 窗口/3,060 人造错误判定）；0.90 与 0.99 是作者自定阈值；作者自承任务族制造了自己的最坏情况；未核到公开仓库
- [2026-09-08] 【仅摘要】Judging LLM-as-a-Judge: Concerning Rubric Artifacts in LLM-based Automated Text Generation Evaluation · EMNLP 2026 · arXiv 2609.02942 —— 只用 rubric 文本训练、完全看不到被评回答的分类器就能非平凡地预测 judge 输出；反事实扰动下把候选回答或 rubric 判据反转，judge 常不可靠地不更新决定。5 页短文，未给「非平凡」的数值区间。与 No Judgment Without a Reason 机制同族
- [2026-09-08] 【仅摘要】Does task decomposition improve automatic NLG evaluation? · EMNLP 2026 · arXiv 2609.01139 —— 干净的负面结果：多个 NLG 数据集上找不到任何证据表明拆解带来提升，此前报告的收益来自把人类标注当训练数据用而非拆解本身；有人类标注时不拆解的 LLMaJ 即可与人类标注者打平。限 NLG 评估任务族
- [2026-09-10] 【全文】What Eviction Destroys: A Restore-Counterfactual Audit of Forgetting in Agent Memory · Megagon Labs（Chen Shen，CBW@COLM 2026 workshop） · arXiv 2609.08279 —— **定向「agent 记忆」只读一篇**。restore counterfactual 把预算下的错误拆成不可逆/可恢复/残余：LongMemEval-S 80k 预算 FIFO/随机/去冗余的不可逆份额 0.67–0.73，8k 全部 1.00；精度匹配的策略间测不出不可逆率差异（分辨率 1.2–6pp）；预算-精度曲线不报读取机制不可跨论文比较。仓库 megagonlabs/restore-counterfactual 单次提交 0 星；reader/judge 同为 GPT-4o-mini（40 题校准自一致 1.0）。CC BY-NC-SA。新增 J16、印证 J15
- [2026-09-10] 【全文】Selective Forgetting: A Graph-Based Memory Framework for Long-Term LLM Agents · 多伦多都会大学 · arXiv 2608.28978 —— 定向「agent 记忆」本线第二。匹配预算下图记忆 F1 0.417 对平铺 0.468（Δ=−0.050，CI [−0.085,−0.016]），助手轮回忆题判定 0.911→0.607；遗忘模块剪 9.8% 节点 F1 不变。水分：GPT-4o-mini 身兼抽取/回答/评判，每配置单次运行，无随机剪枝对照。CC BY。新增 J17
- [2026-09-10] 【仅摘要】Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability · LinkedIn · arXiv 2609.05339 —— 定向「agent 记忆」。四种记忆换写入模型：固定 schema 图 +0.0004，压缩笔记 +9.91/−13.28 不对称，RAG 半迁移只拿 4.96/11.90；笔记损失 80% 在构建时丢，RAG 81% 在检索；只靠记忆库修复 48 例全败，留原始历史修回 34 例。边界：48 条合成历史，Llama-3.1-8B↔Qwen2.5-7B 单一跨族。J17 边界、J8 弱印证不解除存疑
- [2026-09-10] 【仅摘要】Harness the Memory: A Holistic Evaluation of Memory Substrates in Memory Agents · arXiv 2608.15008 —— 定向「agent 记忆」。11 基底×3 骨干×4 基准×26 指标同 harness：无基底全面领先；结构化图对话 QA 领先但 agent 任务被帕累托支配且慢 10–100×；检索深度对 QA 有益对序列决策有害（注意力探针）。设计规则「用写入深度换读取广度」。代码「接收后开源」未见。新增 J16、J17
- [2026-09-10] 【仅摘要】MemTrapBench: Benchmarking Cognitive Traps in LLM Memory Use · 浙大+NUS+东北大学 · arXiv 2608.20202 —— 定向「agent 记忆」。推理固化/信念扭曲两类陷阱，两模型族五记忆框架全部低于无记忆基线，最强也掉 >10%；一条推理时提示（AdaptiveMem）补回大部分。边界：任务专为诱发陷阱构造。新增 J16

## 工程实践（非论文）

> 工程博客 / 技术报告 / 上游变更的去重区（硬规则 5）。快讯不进这里。
> 格式：`- [首推日期] 【来源标注】标题 · 来源方 · 原文链接 —— 当时判词`

- [2026-09-08] 【工业博客】Fast autoscaling on GPUs · Feedly（Jash Dalvi） · https://feedly.com/engineering/posts/fast-autoscaling-on-gpus —— GPU 冷启动 15m21s→5m50s，方法是先拆三阶段（image pull/imports/replica init）再动手；含一条难得的负面数据：把权重与编译缓存烤进镜像在 Image Streaming 下并不本地，为省 28s 权重读付出 52s imports，净亏后拆掉。水分：无 GPU 型号/模型名/副本数/QPS，绝对值不可搬；VLLM_MEMORY_PROFILER_ESTIMATE_CUDAGRAPHS 未标 vLLM 版本
- [2026-09-08] 【工业博客】How we made one of our largest inference workloads 4.7× more GPU-efficient · Decagon（Nick Liu） · https://decagon.ai/blog/gpu-efficient-inference-serving-stack —— PD 分离 + 突发准入控制 + 缩短扩容可用时间，全生命周期少用约 80% GPU-hour。水分大：同时换了更高显存 GPU，4.7× 不可归因；无 GPU 型号/模型/基线/并发/绝对吞吐；带招聘 CTA。硬证据是两条负面观察——首批 PD 分离不快、更大配置反而更慢（→J1）；一次构建静默从 NVLink 回退 TCP（→J12）
- [2026-09-08] 【一方博客】【上游变更】Serving LLMs on Tenstorrent Hardware: Inside the vLLM TT Plugin · vLLM 团队 · https://vllm.ai/blog/2026-09-07-vllm-tt-plugin —— 无 TP/PP rank（MESH_DEVICE 取代 --tensor-parallel-size，插件直接拒绝 -tp/-pp）、调度步只能 prefill-only/decode-only/empty、采样可在设备上完成。水分：**零性能数字**（原文明说不引用），只能当设计文档；当前需从源码构建 vLLM **0.26.0**，落后主线 v0.28.0 两个 minor；投机解码/LoRA/prompt logprobs/多机/DP+MoE 均不支持
- [2026-09-10] 【上游变更】Codex Memory Internals: What It Remembers, Who Decides, and How It Compares to OpenCode · jczhu.com（个人，钉在 openai/codex 8444cf6） · https://jczhu.com/blog/codex-memory-internals/ —— 定向「agent 记忆」。两阶段后台流水线：抽取模型（10 天回看、6h 闲置门槛）→ SQLite → 全局租约 → 沙箱整合 agent 重写 MEMORY.md/memory_summary.md（≤256 输入、30 天未用可剪枝）；检索是渐进披露非向量 RAG；引用回写使用计数。stable 但默认关闭，无效果数字。J3 辅助证据
- [2026-09-10] 【一方博客】【上游变更】Give Your Coding Agents a Memory You Own（funes） · Hugging Face（David Corvoysier） · https://huggingface.co/blog/funes —— 定向「agent 记忆」。本地会话记录切块嵌入进 Lance，向量+BM25 融合、交叉编码器重排、时间加权；写入零蒸馏，可发布为 HF 数据集。无质量/延迟数字；仓库 6 月建、v1.3.0 09-01、349 星。J3 边界（与「写入深度换读取广度」反向）
- [2026-09-10] 【工业博客】【仅摘要】Agent memory as a file format · Cal Paterson（个人博客） · https://calpaterson.com/memoryfields.html —— 简条目。Markdown 页 + YAML 头 + SQLite 向量索引，语义跳转代替图遍历；无数字，HN 96 评论
- [2026-09-10] 【工业博客】【仅摘要】Context Compaction for Agents · OpenNash · https://opennash.com/blog/context-compaction-for-agents-keeping-long-horizon-sessions/ —— 简条目。压缩当有目标函数的有损策略
- [2026-09-10] 【工业博客】【仅摘要】Context compaction is silently destroying your LLM agent's memory · Shuo Liu（dev.to） · https://dev.to/linfordr/context-compaction-is-silently-destroying-your-llm-agents-memory-2pg2 —— 简条目。memory-anchor 库压缩前后快照对比，带推广
- [2026-09-10] 【上游变更】【仅摘要】agentmemory v0.9.29 · rohitg00 · https://github.com/rohitg00/agentmemory/releases/tag/v0.9.29 —— 简条目。Cursor 插件、Devin/DeepSeek Harness 连接器
- [2026-09-10] 【工业博客】【仅摘要】AI Agent Memory: How Production AI Agents Remember and Learn · Bhavishya Pandit（Substack） · https://bhavishyapandit9.substack.com/p/ai-agent-memory —— 简条目。写什么/存哪/怎么回来/何时删四决策

## 提及未展开（窗口外或判为跳过，防止当新货重推）

- Cascade —— per-request latency budget 调度（8 月初，窗口外）
- FlashBoot —— 亚秒级权重加载（8 月初，窗口外）
- CoinRAG —— nugget 级 KV 复用（8 月初，窗口外）
- MoE-Infinity —— 开源库非论文；落地首选，Expert Cache 篇说明其频率排序部分可能多余
- InferenceX 官方预览 TPUv7 Ironwood vs Blackwell/Blackwell Ultra · SemiAnalysis · https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam —— 落选池。TPU 在 FP8 聚合服务上性能每美元最高优 50%、TPUv7 无原生 FP4；但基于私有 beta 的 TorchTPU 栈与其自有 fork，外部不可独立复现（预计 10 月中开源），且是付费产品预览稿，按硬规则 10 第 4 条降级
- Invalidation Contracts for Cross-Episode Agent Memory · arXiv 2609.00243 —— 定向「agent 记忆」判为跳过。缓存的 API 错误修复建议加版本戳；7 模型 9,400 episode，合规率随模型翻转（Haiku 4.5 100% vs Sonnet 5 ≤11%）
- What It Costs to Compose, Rebuild, and Correct Precomputed Memory · arXiv 2608.30647 —— 定向「agent 记忆」判为跳过。KV cache 级「预计算记忆」拼接退化、重建成本高、忽略旁置纠正；Llama-3.1-8B
- What Makes Agent Memory Useful for Reliable Unanswerable Question Handling? · arXiv 2608.27924 —— 判为跳过。记忆对 UAQ 的收益选择性且跨数据集脆弱
- Hindsight Memory-PRM · arXiv 2608.29605；MemGuard · arXiv 2608.21867；InjecMEM · arXiv 2608.23471；Towards a Formal Definition of Agent Memory · arXiv 2608.11654 —— 定向「agent 记忆」窗口内见过，判为跳过
