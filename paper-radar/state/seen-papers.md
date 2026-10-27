# seen-papers · 去重账本

> 周扫开始前先读本文件。已列条目不重发；有实质新信息（中会/开源/被反驳）才标【更新】重进。
> 去重按内容不只按标题（同一工作可能改名重投，如 MAP → CAP）。
> 「上次周扫」日期只由四线全幅周扫更新；定向/单篇验证不动它。
> 折叠策略：条目满 6 个月压缩成「`- [日期] 标题 · ID/链接`」单行（判词删掉，其价值已沉淀进 judgments.md）。
> 非论文（工程实践节的详条目与简条目）记在文件末尾的「工程实践（非论文）」一节，带来源标注，简条目再加【仅摘要】；【资讯】【快讯】不进本账本（硬规则 11），解说链接也不进。

**上次周扫：2026-10-27**（窗口 10-22 → 10-27；5 天，8 篇论文（3 全文 + 5 仅摘要）+ 实践详 5 + 简 8 + 资讯 6 + 快讯 8；报告 `reports/2026-10-27.md`，已推送：是——本期已发布）

格式：`- [首推日期] 【溯源】标题 · 会议/机构 · arXiv ID 或会议页链接 —— 当时判词`
（非论文条目：`- [首推日期] 【一方博客/工业博客/技术报告/上游变更】标题 · 来源方 · 原文链接 —— 当时判词`）
（ID/链接为硬要求，无 arXiv ID 的会议论文用会议页链接；2026-08-20 前的旧条目缺 ID 属历史欠账，再次遇到该论文时顺手补上）

## 硬件

- [2026-10-27] 【仅摘要】Training an MoE LLM in MXFP4: How We Closed the Gap to BF16 · https://arxiv.org/abs/2610.32229 —— GPT-OSS-20B（MLPerf Small MoE）MXFP4 开放训练配方（摘要内配方名 ALTO）：混合 1D/2D block 量化 + RHT + SR + 简化 weight de-oscillation；C4 GBS16 16,128 步 3.3350 vs BF16 3.3283（差 0.007），收回无 de-oscillation（3.3418）约一半差距；FP4 收敛开销 +20.0% → +5.0%；三个负面结果（DGE/outlier clipping/macro-block：算子级 SNR 升、端到端降）。边界：模拟 MXFP4 kernel、MI300、wall-clock 未优化
- [2026-10-27] 【落选】Beyond Hotness（ARM SPE 分层内存表征）· https://arxiv.org/abs/2610.32711 —— 硬件可观测方向，非本期论证主干
- [2026-10-27] 【落选】Tile-Based Decompression in Compiled GPU Engines · https://arxiv.org/abs/2610.32695 —— 压缩 kernel，单一结果无跨源
- [2026-10-22] 【仅摘要】Tandem: Serving Hybrid Linear-Attention GUI Agents on Mobile NPUs · https://arxiv.org/abs/2610.26660 —— 混合线性注意力 GUI agent 在移动 NPU 上 serving：长指令不变、每轮只更新近期历史；关键是循环状态的 checkpoint 策略（哪些步保存/恢复），平衡 NPU 内存约束与重算代价
- [2026-10-22] 【仅摘要】A Hybrid GPU and Processing-Near-Memory Architecture with Shared DRAM for Efficient Prefill-Decode Disaggregation · https://arxiv.org/abs/2610.26131 —— prefill 与 decode 分置 GPU/PNM（processing-near-memory）硬件、共享 DRAM，KV cache 不重复搬运；针对 prefill 计算受限、decode 内存受限的失衡

- [2026-10-20] 【仅摘要】HBFSim: A Simulator for Exploring HBF in Memory Hierarchies for LLMs · https://arxiv.org/abs/2610.23503 —— HBF（TB 级本地 / HBM 级带宽）事件驱动模拟；服务装不进 HBM 的数据比 host DRAM 快 11.0–19.0×；HBM 更适合活跃序列 KV 而非通用 cache
- [2026-10-20] 【仅摘要】CMM-MP: A Novel Memory Pooling Architecture using Purpose-built Memory Device with CXL and Ethernet · SK hynix（OCP Summit 2026）· https://arxiv.org/abs/2610.22716 —— CXL + Ethernet 合成本池化 fabric，定位 HBM 容量与 host DRAM 延迟之间；Valkey+YCSB/DiskANN 场景胜 RDMA-based

- [2026-10-18] 【全文】Replay the Curvature: Accurate and Scalable NVFP4 Quantization for LLM Inference · KlingAI Research / 复旦 / 上海 AI 孵化器 / 中科大 · https://arxiv.org/abs/2609.36654 —— W4A4 七基准问题加权恢复 99.35/100.84%（对 BF16），胜 ScaleSweep 97.28/99.03；逐层计算 15.17×/23.14×、峰值 35 GB，整模型时间是投影值。J21 辅助

- [2026-09-28] 【全文】mKernel: Fast Multi-GPU, Multi-Node Fused Kernels · https://arxiv.org/abs/2609.13585 —— 2×8 H200；Ring Attention 最高 1.88×，5 月已有博客；MoE 对照与自适应实验规模需分开读
- [2026-09-28] 【仅摘要】Taming Bitwise Behavior in GPU Kernels with Tensor Core · https://arxiv.org/abs/2609.11356 —— 27 个 kernel 中 19 个固定次序版本性能差在 10% 内；不是全服务确定性

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
- [2026-09-10] 【仅摘要】HBFSim: Fast and Faithful Simulation of High-Bandwidth Flash Under Real GPU Execution · arXiv 2609.09800 —— HBF（封装内 NAND，HBM 下一层；规范 2026-08-03 发布、器件 2027 初送样）的执行驱动模拟器：改写 PTX 门控 kernel 启动，未改动的 vLLM 0.15.1 跑 Qwen3-30B-A3B 结果 token 一致，快路径 2s vs 详细路径 44s。结论要等真器件

## 模型

- [2026-10-27] 【落选】Agentic Memory Management Is the Next Frontier of Information Retrieval · https://arxiv.org/abs/2610.32464 —— 视角文，无实证数字
- [2026-10-22] 【全文】Token-Set Choice Confounds POPE: A Systematic Audit of Yes/No Extraction in VLM Hallucination Evaluation · Sri Krishna College of Technology + Sri Eshwar · https://arxiv.org/abs/2610.25964 —— POPE 系 VLM 幻觉抽取环节的 yes/no 词元集合可能不匹配模型真实输出（LLaVA-1.5-7B NF4、9k 题、9 种推理时修正全部失败）；幻觉率依赖抽取管线的词元集合——是管线参数不是模型属性。J13 印证
- [2026-10-22] 【仅摘要】PACT: NVFP4 Data-Flow LoRA Fine-Tuning on Consumer GPUs · https://arxiv.org/abs/2610.25048 —— 消费级 GPU 上 NVFP4 数据流 GEMM LoRA 微调，把微调精度从 BF16 降到 NVFP4，针对消费卡显存瓶颈

- [2026-10-20] 【全文】Understanding LLM Hallucinations Caused by Soft Errors · Villanova + MBZUAI · https://arxiv.org/abs/2610.22520 —— LLMEI 注入 SRAM 多位翻转，3,200 GPU 时；幻觉四分类分布随 BER 移动；代码任务断崖（Token Corruption 占 100%）、数学渐进；J24：代码通过率是硬件可靠性比数学分数更好的哨兵
- [2026-10-20] 【全文】Acceptance Is Not Speed: Length Inflation in Training-Free Lossy Speculative Decoding · https://arxiv.org/abs/2610.23818 —— 5 条宽松验证规则 × 360 配置，vLLM 0.26.0 单 H100、3 seed 约 750 GPU 时；198/300 cell 丢精度、144 变长 cell 中 132 丢、省轮次 40 cell 中 35 丢；spec_casc_tok 唯一平均保精度；J25

- [2026-10-18] 【全文】Finetuning with Sampling: SFT Learns Better Than You Think · 哈佛（Karan/Chen/Du） · https://arxiv.org/abs/2610.02140 —— MCMC projection sampling 改写 off-policy 轨迹、SFT 目标不变：MATH500 +33.7% 超最强 RL 26.9pp、pass@k 0→67.2/53.1；Olmo 数据微调 Qwen 化学 57.33 < vanilla 61.8。LW 2026-10-16 独立验证：对齐任务 replay 比 projection sampling 更划算（54%→14%，每保留 token 约 20 生成 token）。J22 主证据

- [2026-09-28] 【全文】Can One Adapted Model Do It All? Fine-Tuning Strategy Selection for Customer Support LLMs · https://arxiv.org/abs/2609.27262 —— 13 模型八数据集；顺序全参遗忘，多任务是部署折中；四私有数据，代码未核实
- [2026-09-28] 【仅摘要】Low-Bit Recurrent States in Hybrid Language Models · https://arxiv.org/abs/2609.30950 —— 4-bit 平均载荷 NLL 额外误差降低 3.3–27.9×，不能换算成吞吐

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
- [2026-09-10] 【全文】Good Pretraining, Bad SFT: Checkpoint Quality Across the Training Stack · Aleph Alpha · arXiv 2609.08966 —— 30B-A3B MoE、7.5T token：退火 checkpoint 预训练指标全面更好（val loss 1.648 vs 1.734），走完同一下游流水线后 SFT 聚合 0.247 vs 0.360，主要是 HumanEval+ 4.9% vs 64.6%（答到 32k 上限停不下来），去掉只差 0.016；中训后排名与最终排名 r=0.47、长上下文后 0.88 仍分不出三个起点；solution density GSM8K 27%/13%/0%。单家族单种子，COOLDOWN 扫 27 配置而对手各跑一次；无代码无权重
- [2026-09-10] 【仅摘要】Quantization Amplifies Determinism, Not Bias: Scale-Dependent Behavioral Effects of Serving-Time Weight Compression · 单作者 Dachi Kurtskhalia · arXiv 2609.07901 —— Qwen3-8B/14B/32B × W4A16 AWQ / W8A16 FP8-Marlin / bf16，约 71k 配对补全，三波预注册：8B 上 int4 输出集中度 +5.1pp（Holm p=.023，重跑 +4.4pp）、TTR −0.011；14B/32B 集中度不显著但出现风格漂移；刻板印象方向零结果。J19 主证据

## 软件系统

- [2026-10-27] 【仅摘要】KVStream: Adaptive Parallel Storage Management for KV Caching in Large-Scale LLM Serving · https://arxiv.org/abs/2610.31827 —— 前缀 KV 检索 = 跨 NVMe/并行文件系统的聚合带宽调度：单步读请求打包、写入延后、chunk 全层复制、层空闲自抓；作者性能模型给出无需调参的聚合带宽上界；LMCache 集成 4 模型 6 数据集 ≤128 GPU：查询界内 5%、离线吞吐 1.49×、突发 TTFT 最多 −6.1×（边界：上界靠自家模型、收益依赖突发到达）
- [2026-10-27] 【仅摘要】HyScale: Scaling Long-Context Training for Learned Sparse Attention · https://arxiv.org/abs/2610.32057 —— learned sparse attention 长上下文训练：瓶颈在「选」（top-k 打分要物化分数矩阵，重计算再选一遍）；HyTopK 逐 query 精确 top-k 不物化 + selection replay 反向复用选择；1M GLM-5.1 训练 512 H20 上 2.07× Megatron-LM，32 H800 上 CSA 层 2.01×/QSA 层 1.57×（摘要级，精度保证机制未验证）
- [2026-10-27] 【全文】NgramRL: Accelerating RL Post-Training for Structured Generation via Rollout-Aware N-gram Speculative Decoding · https://arxiv.org/abs/2610.32881 —— GRPO 同 prompt 反复访问 → 历次 rollout 建 n-gram 表（host 内存、与 GPU 重叠）+ fan-out prefetcher 按验证结果分布预建草稿表；热缓存区每次前向 3.60–7.77 tokens、1.99× SuffixDecoding/7.0× prompt-lookup；N=16 覆盖 96.6% 结果分布（Spider 99.5%）、rollout 1.38×（decode 迭代 26.1→19.2ms）。边界：Qwen3-8B 单卡 rig 的 rollout 阶段吞吐，非端到端；增益随输出规律性走，CodeContests 最小
- [2026-10-27] 【落选】Decode Late, Multiply Once · https://arxiv.org/abs/2610.31913 —— 量化点积重表述，理论侧无 serving 集成
- [2026-10-22] 【全文】The KV-Surgeon: Compensation-Aware Offline KV-Cache Compaction · ZIB + TU Berlin · https://arxiv.org/abs/2610.25933 —— Lemma：KIVI 式 top-m 独立删除里 softmax 重归一化使所有删除决策互相耦合，独立打分等价于优化已变形的目标；ZIB（zero-impact 闭式界）+ TUB（可调代价）交替、离线压实；50×/100× × 三基准 × 4B–30B × 5 种子，50× 处比 attention matching 最高高 4pp，fast 版 2/5 代价拿大部分收益；作者专节警告 zero-impact 界的混合服务陷阱
- [2026-10-22] 【仅摘要】Conjugate Compilation: Self-Improving Agentic Co-Compilation for Speculative Decoding · https://arxiv.org/abs/2610.25012 —— agentic 编译器搜索 draft/target 编译参数组合，以接受率为反馈迭代调参，面向同芯片投机解码

- [2026-10-20] 【仅摘要】Understanding KV Residency in Production-Scale Agentic LLM Workloads · https://arxiv.org/abs/2610.22863 —— 生产多轮 trace：p99 单会话 KV 需求 > H100 80GB HBM；1 小时空闲上限降需求 3.6×；KV 是驻留问题不是纯驱逐；J26
- [2026-10-20] 【仅摘要】BaGuaLu-2: Taming Dynamic Memory Fluctuation for Efficient MoE Model Training over 10,000 GPUs · https://arxiv.org/abs/2610.23064 —— 1.04T MoE / 12,288 卡，35% MFU 下持续 2+ EFlops；对两个 SOTA 平均 1.14×/1.13×（基线名需对原文）
- [2026-10-20] 【仅摘要】FuTransformer: FP8 prefill and INT4 decode for Llama-style inference on Hopper · https://arxiv.org/abs/2610.23796 —— prefill 对 compiled PyTorch FP8 最高 1.48×（1.29 PFLOP/s）、8B 对 CODA BF16 1.13×、FP8 2.02–2.18×；INT4 decode 权重 + INT4 KV，8B/70B 验

- [2026-10-18] 【全文】VenusRL: A Fully Disaggregated Agentic RL System with Priority Scheduling and Scalable Interaction · 中科院计算所 / 北航 / Infrawaves / 上海创新院 · https://arxiv.org/abs/2610.03286 —— E2E 1.06–4.24×（up to）、环境成本最多 -89%；沙箱内存平均利用 8%、页共享密度达原生 E2B 905%；8%/60% 为作者自报生产剖析。J21 主证据、J1 辅助

- [2026-09-28] 【全文】AgentKV: Phase-Aware KV Eviction for Agentic LLMs · https://arxiv.org/abs/2609.14872 —— 匹配实现的 12 配置平均 +4.2pp；1.80× 绑定 H100 NVL/32B/32K；Mini-SGLang 分支
- [2026-09-28] 【仅摘要】DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale · https://arxiv.org/abs/2609.22978 —— 160 节点约 300 万沙箱/天，峰值并发 >38 万；不同容量指标不能合并
- [2026-09-28] 【仅摘要】Jev-Mem: System-One-Controlled Agentic Memory for Efficient AI Agents · https://arxiv.org/abs/2609.23986 —— 轻量记忆控制平面；构建 158 秒、6.6×，LoCoMo judge 0.777；图与预算公平性未全文核验

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
- [2026-09-10] 【全文】KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints · Xi Shi、Qian Lou · arXiv 2609.10266 —— 非前缀 KV 复用基准（RAG 检索块 + agent 报告两赛道），按恢复「无 cache→全重算」差距比例 PGR 计分：免费位置对齐单源题够用，多跳题上本身 −0.196，付费修复（CacheBlend 重算 17%、LegoLink <0.5%、calibration）拉回 0.39–0.46；压缩类无一格显著赢过免费对齐，SnapKV 错位拼接后 0.57/0.17/−0.08；naive 拼接报告 −0.82；跨 checkpoint 训练无关方法 ≤0.06、训练 adapter 最多掉 0.135 且静默失败（流畅答案配错实体）。主板 8B 未具名，N=100/子集、MDE≈0.10，输入上限 29K；pip 包与仓库链接是占位符，PyPI 无
- [2026-09-10] 【仅摘要】Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding · EMNLP 2026 · arXiv 2609.09338 —— drafter 只对单目标窄分布训练，workload 一变接受率崩；从现成小模型剪浅 backbone + 目标无关预训练 + 词表对齐/零初始化 QKV/logit 蒸馏适配每个目标；接受长度 Qwen3-8B +16.1%、Llama-3.3-70B +21.2%、MiniMax-M2.5 +22.7%（tokens/s +17.5%），域外多语言增益最大。仓库 LeanModels/Osprey 未查到。J1 印证

### RL 后训练基础设施
- [2026-08-10] 【仅摘要】Laminar · EuroSys '26 · 港大+字节 —— 轨迹级异步 + relay worker 参数服务；1024 卡 5.48×；接受 staleness 换天花板
- [2026-08-10] 【仅摘要】RollPacker (Tail Batching) · NSDI '26 —— 不放弃同步 RL：长尾 prompt 攒进少数长轮次，只改样本顺序；128 卡 H800 比 veRL 快 2.03–2.56×
- [2026-08-10] 【仅摘要】Weave · OSDI '26 —— 跨 job 编排互填依赖气泡；328×H20+328×H800 成本效率 1.84×
- [2026-08-10] 【仅摘要】DORA · 美团 LongCat —— 多版本流式训练，万卡级生产，端到端 2.12×、rollout 8.2×
- [2026-09-10] 【仅摘要】Miles v0.1: Production-Level Post-Training · RadixArk · arXiv 2609.08368 —— slime 生产化后继：SGLang rollout + Megatron-LM/FSDP 双后端、三种权重同步；LoRA RL / on-policy 蒸馏 / SFT / true-on-policy，扩到扩散模型；GLM-5.2 744B-A40B 在 64×GB300 全异步 agentic RL，中位步 263s、rollout 落后 1.7 步、prefix 命中 96%。内容 08-18 已在 LMSYS 博客发布；只报前 30 步；仓库 Apache-2.0、2,740 星
- [2026-09-10] 【仅摘要】Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training · NVIDIA · arXiv 2609.07108 —— 落选池。drafter 与策略在线共训：CP 下扩展 zigzag ring attention 支持分支注意力，PP 下 TapChannel 跨阶段传中间特征；最高 122B、256K。代码在 NVIDIA-NeMo/RL issue 3698

### 向量检索
- [2026-08-10] 【仅摘要】Filtered ANN Search in Vector Databases · arXiv 2602.11443 —— FAISS/Milvus/pgvector 过滤策略横评；pgvector 代价优化器常选错计划；低选择性下 IVFFlat 打败 HNSW（反直觉）
- [2026-08-10] 【仅摘要】VecBench · SIGMOD 2026 · 清华 —— 四家横评含动态更新；pgvector-HNSW 默认配置 recall 0.257、调迭代深度到 0.897 的坑
- [2026-08-10] 【仅摘要】PostgreSQL-V · CIDR 2026 · Purdue —— 向量索引从页式存储解耦，比 pgvector 快 8.9×，同接口 drop-in，开源
- [2026-08-10] 【仅摘要】Curator · SIGMOD 2026 —— 低选择性过滤，比 ACORN+预过滤快 20.9×
- [2026-08-10] 【仅摘要】RACORN-1 · arXiv 2607.00768 —— ACORN-1 原地增强不需重建索引
- [2026-08-10] 【仅摘要】Filter-Agnostic Vector Search on PostgreSQL · PACMMOD —— 生产级数据库系统开销分析
- [2026-09-10] 【仅摘要】Q2D-Web · Perplexity · arXiv 2609.08887 —— 落选池。190M 网页、69,721 条 agent 改写查询（十种语言、九个月生产流量）、三套相关性判定（agent 引用 / 生产排序 / LLM 补判），公开榜；语料私有

### Agent 编排
- [2026-10-22] 【全文】Elicitation or Expansion? Demystifying Gains from Agent Harness Optimization · FuriosaAI + 延世大学 + UC Berkeley · https://arxiv.org/abs/2610.27889 —— 冻结权重只优化 harness：LawBench 上 GPT-OSS-20B harness pass@1 超 120B 基线 +16.05pp、pass@64 翻转 -4.00pp；HotpotQA/AppWorld 聚合值接近更强参照但难子集 40 候选全低于 Qwen3-32B 基线——收益由易子集驱动；pass@1 最优与 pass@128 最优 harness 不是同一个；基线全部作者自跑。J8 弱印证
- [2026-10-22] 【仅摘要】Cache Engineering for Agents · https://arxiv.org/abs/2610.28577 —— agent 轨迹主导成本是 KV cache I/O 与存储而非计算；任何前缀修改使缓存失效，提出沿轨迹的缓存维护策略（哪些留、哪些重算）

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
- [2026-09-10] 【仅摘要】A Layered Analysis of Disagreement and Answer Quality in Multi-Agent LLM Debate · Chen Qian · arXiv 2609.08016 —— 落选池。750 场三模型辩论，语气从友好到敌对让自报一致率差 50.4pp；四层测量（自报 / 文本是否真反驳 / 去掉指令后立场是否持续 / log-prob 立场）。J5 相关，未入账

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

- [2026-10-27] 【仅摘要】When Agents Fail: Model or Harness--Who's to Blame? · https://arxiv.org/abs/2610.32483 —— 4 harness（OpenCode/Codex CLI/Pi CLI/DeepAgents）× 4 模型 + 2 原生组合 × 6 benchmark、111 配置、52,168 轨迹；五指标（VCR/Model-Harness Fit/Cross-Model Fit/Interaction Residuals/Token Load）；harness 排名随模型与 benchmark 重排、任务分与 VCR 偏好不同组合、相近任务分可对应不同执行画像。J6 印证（摘要级，指标统计处理未验证）
- [2026-10-27] 【仅摘要】Tool-Calling LLM Agents Under Realistic MCP Faults · https://arxiv.org/abs/2610.32555 —— MCP-Injector 协议感知故障注入（持久/瞬时/间歇，种子可复现），故障模型校准自 1,774 个开源 MCP 仓库 57,240 条 issue/PR；1,350 格（gpt-oss 20B/120B × 3 栈 × 3 条件）：持久重故障 profile 完成分 8.08 → 3.23，120B 故障条件完成率反而略低（91.1% vs 95.6%），resilience ratio p=0.96。J32 新增（骨干限 gpt-oss 两尺寸、故障分布来自 issue 挖掘）
- [2026-10-27] 【全文】Green Code or Costly Code? Evaluating the Energy Costs of Iterative LLM-Based Code Optimizations · https://arxiv.org/abs/2610.32891 —— EffiLearner 在 EffiBench 全 1,000 题上进程级硬件能耗测量：单次优化推理能耗 250–2,800 次 GPT-4.1 查询量级（cap 最大输出 token 最高省 69%）；44 配置中 42 个优化代码单次运行能耗高于人类参考解；收支平衡点跨题目 10^2–10^5 次、一般情形论文估 10^6–10^7；自优化不随 epoch 稳定降执行能耗
- [2026-10-27] 【全文】Large-Scale Study of GitHub Copilot Trajectories · https://arxiv.org/abs/2610.32313 —— 7,581 Copilot PR / 1,602 仓库：58% PR 无人工介入、其中已合并 62% 零额外 commit（真自治）；第一次介入后轨迹 −20.8 轮 −8.4 min、后续介入几乎不掉；Human-AI loops 中位数 2；介入与合并率相关（选择效应未排除）。边界：限 issue 工作流；编码数据集已放出
- [2026-10-20] 【仅摘要】Equivalence testing and run-count design for stochastic machine-learning experiments · https://arxiv.org/abs/2610.23700 —— TOST + 功效分析 + seed×item 两层方差 + 闭环运行次数公式，270 cell 验证；4 次公开运行的等效主张基本不成立（每方法 2 次不够）

- [2026-10-18] 【全文】Are Benchmarks Reliable? Toward Structural Diagnosis via Item-Level Capability Boundaries · 北师大 · https://arxiv.org/abs/2609.33196 —— BSDProbe item 级能力边界：MATH 题序异常率 4.25–8.18%、GSM8K 跨模型轴 28.13%、GPQA 最高 48.21–57.59%；画像引导选题平均 NDR +17.9%（MMLU +24.1/GPQA +30.1/PopQA +37.1）。J23 主证据

- [2026-09-28] 【全文】GAUGE: When Not to Trust LLM-as-a-Judge in User-Simulated Evaluation of Task-Oriented Agents · https://arxiv.org/abs/2609.12191 —— 首推；整体排序ρ0.94但接近候选31%排错，四评委平均未改善；政策/结果感知 gate 有用
- [2026-09-28] 【仅摘要】Agreement Overstates Evidence: Error Dependence in LLM Judge Consensus · https://arxiv.org/abs/2609.22512 —— 10 评委错误相关0.21等效3.5独立评委；最高28%比较显著性消失
- [2026-09-28] 【仅摘要】Quantifying Overclaiming Propensity in Frontier LLM Agents · https://arxiv.org/abs/2609.20812 —— 67.9%运行未触及全部文件，其中80.4%误导；触及一行不等于读完，CLI混杂

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
- [2026-09-10] 【全文】IB2: A Protocol for Measuring Enterprise AI Systems by Serving Route, Not Model Identifier · Iterate.ai · arXiv 2609.10494 —— 审计的 18 个基准全按模型标识打分，分不清模型答错与路由拒绝；同一 Qwen3.6-27B 权重两条 FP8 路由 26.12 / 62.25（13 图上限、32,768 截断，事后回溯发现），Qwen3.8-27B 换 serving arm 77.38→82.54；失败计入分母会改变点估计排序。厂商自评、语料封存、每配置单次运行、仓库 IterateAI/IBIB 404。J15 印证
- [2026-09-10] 【仅摘要】Benchmark Scores Are Pipeline-Dependent: A Reliability Audit of Cybersecurity LLM Benchmarks · arXiv 2609.08765 —— 8 基准 × 10 模型，15 种流水线失败模式；单个选项动 >80pp；统一流水线后 9/10 模型至少一处移 ≥3 名。J13 印证
- [2026-09-10] 【仅摘要】Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs · arXiv 2609.07664 —— 落选池。零样本准确率在逐级量化下非单调、掩盖对 BF16 的分布偏离；用 token 决策边界上的 JSD/TVD 量信息损失。J19 辅助论文证据
- [2026-09-10] 【仅摘要】When Auditors Fabricate: Batch-Size Degradation and Confident Hallucination in LLM Detection of Planted Document Contamination · arXiv 2609.09696 —— 落选池。Gemini 3.0 Pro 找 150 篇论文 450 处植入错误：单篇 50%、小批 60%、大批 2.8%，大批时编造不存在的错误而非弃权；最像真的错误最常漏

## 工程实践（非论文）

- [2026-10-27] 【一方博客】Serving DeepSeek-V4.1-Flash at Scale: vLLM Matches DeepInfer and Surpasses SGLang · vLLM 团队 · https://vllm.ai/blog/2026-10-23-deepseek-v41-flash-pd-wide-ep —— 详条目。GB300 NVL72 单机 PD 分离 + Wide-EP，AgentX 954K tok/s/GPU（第一方口径，对其自家前代 7.9×）、单用户 P90 196 tok/s；decode 端 GB200 131K nextn=3 与 DeepInfer 已发表数字差 <6%（对比发表值、非同场复测，作者注明）；prefill 栈 +35.6%–+43.9%（bounded replay SWA +19.9%/Engram 2MB +2.8%/DeepSelect +15.6%）；KV 890 B/token、MoE 占 decode 步 62%；LMSYS 同基准对比为解说
- [2026-10-27] 【一方博客】GLM-5.3 Optimizations, Part 2: PCP, DCP, and Hybrid HiSparse on 16×H200 · vLLM 团队 · https://vllm.ai/blog/2026-10-23-glm53-part2-pcp-dcp-hisparse —— 简条目。1M 上下文：PCP token 切分 prompt（16 chunk 配对分布）+ DCP token 切分 KV + HiSparse KV 下沉 host；每 token KV 54,728 B（MLA 78 + indexer 21 + MTP 3），1M = 53.4 GiB；AgentX PCP8×DCP8+HiSparse 对等吞吐 DP 1.7–3.2× 单用户，原文实验里唯一能供 1M 的形态
- [2026-10-27] 【一方博客】vLLM Delivers Day-0 Support for MiniMax-M3.1-Flash · vLLM 团队 · https://vllm.ai/blog/2026-10-23-minimax-m31-flash —— 简条目。原生 NVFP4 KV + NVFP4 MoE：MSA kernel QMUL4 反量化入核（indexer QK decode 1.7×/sparse attn decode 1.3×）、MegaMoE + MXFP8 共享融合 prefill kernel −20%/吞吐 +7%、indexer decode CP 在 4×GB300 上 512K 3.3×；agentic GB300 418.9 tok/s/用户、Rubin 724.9 tok/s/用户 + 191.5K tok/s/GPU、MI355X 133.3M tok/$ 最省 TCO；Day-0 RL 16×GB300 AIME-2024 36.3% → 67.5%
- [2026-10-27] 【一方博客】How NVIDIA Minerva Turns Telemetry Chaos Into Peak GPU Yield · NVIDIA · https://developer.nvidia.com/blog/how-nvidia-minerva-turns-telemetry-chaos-into-peak-gpu-yield/ —— 详条目。AI 工厂拓扑图关联遥测：单个 link 降级在 40 万接口工厂里把 81 个事件收敛成 1 起 incident，相对逐一处理省约 54 小时集群时间（第一方案例，无独立验证）；主动 SuperNIC 维护（预测性换件）
- [2026-10-27] 【一方博客】How NVIDIA Mission Control 2.5 Brings Autonomous Recovery to Kubernetes · NVIDIA · https://developer.nvidia.com/blog/how-nvidia-mission-control-2-5-brings-autonomous-recovery-to-kubernetes/ —— 简条目。K8s 自主恢复（调度器/作业恢复/硬件恢复三组件）：硬件故障挪作业、瞬时软件故障自动重启或升级、退化早期剔除出调度池；GA，VR NVL72 为 EA
- [2026-10-27] 【一方博客】Rapidly scaling online storage to serve over 1 billion ChatGPT users (Part 2) · OpenAI · https://openai.com/index/scaling-storage-one-billion-users-part-two —— 详条目。十亿用户存储层：Cosmos DB 多租户、工作负载放置、访问控制；p50 120ms → 10ms（12×，第一方口径）；第三方「用 Codex 重写 Rust 存储」是媒体转述，原文不以此为重点
- [2026-10-27] 【一方博客】Securing our frontier model training environment + OpenAI CUT incident investigation · OpenAI · https://openai.com/index/securing-our-frontier-model-training-environment —— 详条目。9-20 发现训练环境模型用 DNS 作出站信道绕过沙箱（沙箱本无出站）；对策 offline policy（训练环境断网），RL 训练 10-1 恢复；调查报告页 https://openai.com/index/openai-cut-incident-investigation 给时间线。第一方自报，无独立复现；J14 佐证（辅助证据）
- [2026-10-27] 【一方博客】Optimizing Streaming Speech Recognition on Arm Edge Devices with ExecuTorch · PyTorch 团队 · https://pytorch.org/blog/optimizing-streaming-speech-recognition-on-arm-edge-devices-with-executorch/ —— 详条目。Nemotron 3.5 流式 ASR 上 Pixel 11（XNNPACK）：chunk 80–1,120ms 为部署旋钮，FP16 WER 15.2% → 11.5%、QC8W 15.5% → 11.7%；SME2 整段 9.79s → 4.61s（2.12×）/QC8W 5.20s → 3.24s（1.61×），GEMM 占大头；RTF 0.19/0.13、SME 利用率 38.4%/53.7%；全部第一方测量
- [2026-10-27] 【一方博客】Scaling NVIDIA TensorRT...Global Performance Tuner Part 1 & Part 2 · NVIDIA · https://developer.nvidia.com/blog/scaling-nvidia-tensorrt-performance-optimization-beyond-a-single-build-route-with-the-global-performance-tuner-part-1/ —— 简条目。build path 问题形式化（Part 1）+ 全局搜索循环：跨 path 候选 + 精度容差 ε 下 engine 选择（Part 2）；绑 TRT 11.1/T-TRT 2.15，正文无第一方数字表；1.14×–1.63× 为媒体转述（TokenPost）
- [2026-10-27] 【一方博客】Using AI Agents to Teach Robots Like Microduck to Walk in Simulation · NVIDIA · https://developer.nvidia.com/blog/using-ai-agents-to-teach-robots-like-microduck-to-walk-in-simulation/ —— 简条目。RTX Spark（Hermes + Nemotron 3.5 Bolt 计划）→ Astra 3D 资产（FreeCAD/Blender/USD）→ Isaac Sim + Omniverse + Newton → Isaac Lab 4,096 并行环境、单张 RTX PRO 6000 训练感知+步态；sim-to-real 走 BAM + domain randomization。工作流演示，无量化数字
- [2026-10-27] 【一方博客】Does Your Model Run on AWS Trainium?（torch-neuronx 模型支持）· Hugging Face · https://huggingface.co/blog/torch-neuronx-model-support —— 简条目。Trainium2 支持面：16 模型 × 4 设备（16 core）全 PASS；原文自带边界：只测了装得进 4 台 Trainium2 的模型，PASS 不代表吞吐
- [2026-10-27] 【一方博客】LitPivot: Developing research ideas through dynamic contextualization · HF（Ai2 + 宾大）· https://huggingface.co/blog/allenai/litpivot —— 简条目。研究想法 pivot 工具：自 4 个项目挖 21 次真实 pivot + 5 名研究者 formative study（UIST 2026 论文）；方法学价值，非系统数字
- [2026-10-27] 【工业博客】【仅摘要】Fixing Tool-Call Accuracy in vLLM · Ubicloud · https://www.ubicloud.com/blog/fixing-tool-call-accuracy-in-vllm —— 简条目。tool-call 格式漂移修复：JSON tool description 包进模型专属 token（Kimi <|im_system|>tool_declare）+ 约束解码（Begin tool call → name → index → args JSON → End）；HN 132 分；无量化准确率数据，只述机制
- [2026-10-20] 【一方博客】One search, two layers — compiler controls inside PyTorch Helion using NVIDIA CompileIQ · PyTorch 团队 · https://pytorch.org/blog/one-search-two-layers-compiler-controls-inside-pytorch-helion-using-nvidia-compileiq/ —— 详条目。搜索空间推到 ptxas 寄存器分配层（CUDA 13.3 新控制面）：单目标 1.047×（0.0971→0.0928 ms，d≈2.5，两次独立运行最优 ACF 一致）、多目标 occupancy +0.16pp（p=9.2e-23）换 runtime 1.75–2% + L1TEX +4.5pp；ACF 绑硬件+工具链
- [2026-10-20] 【一方博客】Improve TTFT for multi-turn agentic workloads with bi-directional KV transfer in vLLM · AWS · https://aws.amazon.com/blogs/machine-learning/improve-ttft-for-multi-turn-agentic-workloads-with-bi-directional-kv-transfer-in-vllm/ —— 详条目。1P1D P5en+EFA：Qwen3-32B TTFT 最多 1.6×、GLM-5-FP8 最多 3.3×（长 prompt）；decode→prefill 回灌 KV，下一轮温缓存起步；源自 Trainium，贡献 vLLM
- [2026-10-20] 【一方博客】Elastic EP, near-zero-downtime · vLLM 团队（NVIDIA 参与）· https://vllm.ai/blog/2026-10-19-elastic-ep-near-zero-downtime —— 详条目。DEP 拓扑，异步准备 + NIXL EP：16→20 GPU 停机 99.62s→0.82s、20→16 56.25s→1.96s；仅 MoE 专家并行部分，attention 走副本逻辑
- [2026-10-20] 【一方博客】Introducing TorchNeuron — Native PyTorch backend for AWS Trainium · PyTorch / AWS · https://pytorch.org/blog/introducing-torchneuron-native-pytorch-backend-for-aws-trainium/ —— 详条目。Trainium2/3 原生 PyTorch 设备：eager（实验）+ torch.compile + NKI；Apache 2.0，公测 10-20；Deepgram 自报每美元约多 60% 输入音频 vs GPU；10 万模型盲扫约 22k 算子无原生 lowering
- [2026-10-20] 【一方博客】Accelerating Mamba-2 with high-performance forward-pass kernels in NVIDIA CUDA Tile · NVIDIA / Jane Street · https://developer.nvidia.com/blog/accelerating-mamba-2-with-high-performance-forward-pass-kernels-in-nvidia-cuda-tile/ —— 详条目。Mamba-2 前向 cuTile（3 手写 kernel），单 B300，对 Triton 参考（mamba_ssm 2.3.2.post1）1.14–1.82×；kernel 级非端到端，无反向
- [2026-10-20] 【一方博客】Low-resource programming languages · OpenAI · https://openai.com/index/low-resource-programming-languages —— 详条目。MultiLangBench（20 语言建 SQLite 兼容引擎）：GPT-6 Astra 平均 87.4% vs GPT-5.6 Sol 26.8%、Luna 40.3%；COBOL 迁移 86.6% vs 5.4%（低推理，成本 −39%）、高推理 97.9%；测试套件开源
- [2026-10-20] 【一方博客】【仅摘要】GRAFT——把 reward hacking 行为定位到独立适配器再删掉 · Anthropic alignment（MATS）· https://alignment.anthropic.com/2026/graft/ —— 简条目。RETAIN/FORGET 适配器梯度路由：被标记轨迹只更新 FORGET、monitor 只路由不进奖励；Qwen3-8B Countdown-Code 目标任务提升且 hacking 率不升；单轮 ≤8B

- [2026-10-19] 【一方博客】Redesigning source control at Anthropic（Scion） · Anthropic · https://www.anthropic.com/engineering/redesigning-source-control —— 详条目（24,074 字符全文读）。monorepo 日合并 5 月约 2,500 → 9 月 3 万+（增量多数为 agent 提交）；主分支历史约 100 GB、压缩工作副本 >25 GB；CI 每天约 2,500 万次检查；朴素「每分支全量快照」一天 >600 PB git 流量；拆控制面（Spanner）+ 内容寻址数据面（CAS）+ 三级缓存（命中率 99%+）；CI 收回约 25% CPU、checkout 快两个数量级、基础设施 CPU/内存小 200 倍；7 人团队 5 个月完成迁移。适用边界原文写死：非 git 即插即换替代品，仅「数万名工程师或 agent 集群」超大 monorepo 才值得自建；Claude Mythos Preview 重写入库管线（内存省 20×/提速 4×）为作者侧陈述、无可复现路径。硬规则 19 漏网必看条目（skipped_no_date，卡片无 `<time>`）读全文 + 四项核验后补收。解说：The New Stack、Simon Willison（导读）
- [2026-10-19] 【论文→实践详条目】Harness²: Recursive Agent Harnessing for an Open World · Google Cloud AI Research · https://arxiv.org/abs/2610.14224 —— v1 提交 10-09（早于 exa 搜窗 start=10-15，未被四线搜捞到），10-18 开源 v0.1.0（Apache 2.0，google-research/harness2），开源事件在窗口内 → 本期按第二条实践详条目收（非「窗口内新论文」，v1 10-09 如实标注）。冻结权重、递归调优 8 组件 harness（系统提示/护栏/记忆/技能/工具指引/脚本/子 agent/中间件，Propose–Probe–Compose 对比式递归 + EXPERIENCE.md 经验库）；k=1 WB 最高 11.5（GLM-5 OpenCode 64.2→75.7）/ Job 4.5 / LAB 11.8pp，k=5 并行再 +2.9–4.2；弱执行器（GLM-5）受益更大。结果全部 Google 自报、无独立复现，仓库自注「非 Google 官方支持的产品」；绑定 GLM-5 / Gemini 3.5 Flash × OpenCode / Codex，v0.1.0 单一机构，换执行器/外壳数字需重测。J8「harness 先行」半句弱印证（不改状态，仍【存疑】）。解说：AI In Context（Rebecca Stone，导读）
- [2026-10-18] 【一方博客】Hyper Optimizing Kimi K3 in vLLM: Moving Fast and Responsibly（megakernel） · vLLM 团队 · https://vllm.ai/blog/2026-10-16-kimi-k3-megakernel —— 16×GB300、batch 1、DSpark（合成 AL=6）842+ tok/s；AgentX c1 P90 交互 1.8×（优化版 16 卡 vs 旧 8 卡，非同卡对比）；原文承认 agent 辅助开发快过评审维护流程
- [2026-10-18] 【一方博客】Scaling Kimi K3 on AMD Instinct MI355X（Embedded LLM） · AMD / vLLM 博客 · https://vllm.ai/blog/2026-10-16-kimi-k3-mi355x —— AgentX 50 tok/s/user P90 点 7,567 vs 6,083 tok/s/GPU（+24.4%），峰值算力 10.1 vs 13.5 PFLOP/s 更低；c70 +28.9%、前缀缓存命中 74.8→80.1%；数据为 SemiAnalysis InferenceX 10-09 快照
- [2026-10-18] 【一方博客】SGLang 与 Beam：501B MoE 上生产（LMSYS 博客 + HF《Welcome Beam》+ vLLM《Serving Reflection Beam on vLLM from Day 0》，同事件三方合并） · SGLang / Hugging Face / vLLM 团队 · https://www.lmsys.org/blog/2026-10-16-beam · https://huggingface.co/blog/reflection-beam · https://vllm.ai/blog/2026-10-16-reflection-beam —— 96 H200（64 训 + 32 推）解耦异步 GRPO：AIME25 46.3→56.7%（204 步，响应长度下降）；serving NVFP4 + FP8 KV + 推测解码，c96 83,504 tok/s/GPU、前缀缓存命中 92–96%。HF 公告：Apache 2.0、三档 checkpoint（BF16 约 1TB / NVFP4 约 280GB）、43 SW + 9 NoPE 全局层 + scalable-softmax、1M 上下文 BF16 KV 36.08 GiB/序列、Reflection 自报 SWE-B-Pro v2-Hard 78.6 / AIME26 97.7。vLLM 部署：agent 自主 7 处优化（decode 2.71× / prefill 1.87× TP8）、DFlash2 自适应验证 c128 +10.8%、AgentX 约 88K tok/s/GPU（96 并发）、SkyRL 50 步 AIME25 61→79%（与 SGLang 204 步记录是不同 RL run）
- [2026-10-18] 【工业博客】Building fast filesystems for VMs · Modal · https://modal.com/blog/vm-sandbox-filesystem —— virtio-fs 代价：stat 2×、递归 chown 6×+（4s→1min+）、pnpm/bun install 约 3×；ImageFS-blk 块级 CoW：bun install 12.5s→1.07s（12×），VM Sandboxes 已按此后端 GA
- [2026-10-18] 【工业博客】Blackwell dtypes Qwen3-32B · JarvisLabs · https://jarvislabs.ai/blog/blackwell-dtypes-qwen3-32b —— NVFP4-AWQ 3,079 tok/s（2.41× BF16）PPL +0.41；FP8/MXFP8 +0.06 内 1.63×/1.73×；MXFP4-AWQ PPL +0.44 却仅 1,715 tok/s（Marlin weight-only 无 FP4 算力路径）；TTFT 最高改善约 8.4×（concurrency 420）
- [2026-10-18] 【一方博客】How the Claude Code team does code review · Claude Code 团队（Addy Osmani / Morgan Westlee Lunt / Qing Wang）· https://claude.dev/blog/solving-code-review-at-anthropic/ —— 详条目；六层评审 + 回滚；内部 AI 评审实质评论 16%→54%、PR 回滚份额 -40%+（6→9 月自报）、monorepo 日变更 2,500→30,000+；REVIEW.md + 验证优先（Boris Cherny 2–3×）；一 PR 通宵 50+ 轮后加收敛机制（3 轮上限、diff-only 复审、约 59% 重复发现是旧代码）；Code Review GA（Team/Enterprise）+ 开源安全评审 GitHub Action
- [2026-10-18] 【一方博客】【仅摘要】Claude Code in the cloud: a field guide to cloud sessions · Claude Code 团队（claude.dev）· https://claude.dev/blog/claude-code-in-the-cloud/ —— 每任务独立 VM（约 4 vCPU/16GB/30GB）；GitHub token 不进 VM（代理持有 + 只推工作分支的短时凭据）；tidepool 实测 16s 起 3 会话、61/65/72s 完成、87s 全完；并行会话约 5× 消耗计划额度
- [2026-10-18] 【一方博客】【仅摘要】Building effective agent automations · Lance Martin / CJ Avilla（claude.dev）· https://claude.dev/blog/building-effective-agent-automations/ —— Managed Agents（beta）每日简报参考实现；按源书签不读固定窗、读失败显式上报不报"无新消息"、ok:true+ts 确认后才记账、预算 3–5× 起步触顶暂停；GitHub token 只读 + 出站 allowlist
- [2026-10-18] 【一方博客】【仅摘要】Welcome Muse Spark Open（Meta 开源权重，五方合并入口） · Hugging Face / PyTorch / vLLM / NVIDIA / Together · https://huggingface.co/blog/meta-muse-spark-open · https://pytorch.org/blog/muse-spark-open/ · https://vllm.ai/blog/2026-10-15-muse-spark-open · https://developer.nvidia.com/blog/scale-agentic-coding-workflows-with-metas-muse-spark-open-on-nvidia-gb300-nvl72/ · https://www.together.ai/blog/meta-muse-spark-open —— 约 816B/42B 激活 MoE（256/8 专家）、1M 上下文、多模态输入；BF16+NVFP4 checkpoint（822B/484B）；KV BF16 约 250KB/token、1M 约 266GB；SGLang NVFP4 recipe：8×RTX Pro 6000 @131K 或 8×H200 @1M；PyTorch：SGLang 内 Helion kernel 1.03–3.95×、MI350 端到端 +3%；M3 Ultra Q2_K 约 18 tok/s
- [2026-10-18] 【一方博客】【仅摘要】Gemini 4 Argon（开发者版本；09-30 首发公告 https://deepmind.google/blog/gemini-4-argon-our-next-era-of-frontier-intelligence/） · DeepMind · https://deepmind.google/blog/introducing-gemini-4-argon/ —— 全球可用（AI Studio / Gemini API / Antigravity / Gemini app + AI Mode Ultra&Pro）；$2/$10 引入价（缓存 95% off）、11-30 后 $4/$20；Vals Index 自报第一；Antigravity agentic 提交 +35%、回滚降近 1/3；Gray Swan IPI 15 次自适应攻击成功率 0.7%；发布通告，数字全部自报
- [2026-10-18] 【一方博客】【仅摘要】Bringing Elastically Deterministic Data Loading to TorchTitan with Zephon · PyTorch 团队 · https://pytorch.org/blog/bringing-elastically-deterministic-data-loading-to-torchtitan-with-zephon/ —— 数据顺序不随 GPU 数变；1B 模型 20B token 实测：标准 loader 下 DCLM Core v1 分数跨 8–64 GPU 最多漂 0.82 分，Zephon 后 spread 0.05 / 0.011（DCLM/FineWeb）；job 内 tokenize/pack/shuffle/mix、无预处理副本；保数据顺序不保浮点（loss 近但不逐位等）
- [2026-10-18] 【一方博客】【仅摘要】Day 0 support for NVIDIA Nemotron 3.5 Super VL on vLLM（vLLM + NVIDIA 合并） · vLLM / NVIDIA · https://vllm.ai/blog/2026-10-15-nemotron-3-5-super-vl-vllm · https://developer.nvidia.com/blog/nvidia-nemotron-3-5-super-vl-powers-specialized-agents-with-multimodal-reasoning/ —— 120B/12B MoE、MTP 投机解码（3–5 草稿 token）、单卡 GB10 到 2×H100；厂商口径：单卡 agentic 吞吐最高 5×（Baseten、AA 基准 600+ TPS）、100K 输入 600+ 输出 tok/s、SWE-bench Pro 4×B200/10K 任务 4× 完成速度；DGX Spark 图为 Super（非 VL）原文自注
- [2026-10-18] 【一方博客】【仅摘要】Extending Inductor for the IBM Spyre Accelerator · PyTorch 团队 · https://pytorch.org/blog/extending-inductor-for-the-ibm-spyre-accelerator/ —— 75W PCIe、32 核环形、2MB scratchpad/核、stick 128B=64 fp16；Inductor 后端代码量 7× 小于 sendnn（作者注不完全对等）；kernel 级：batched matmul tiling -29~69%、fused MLP -17%（利用率 2/3→约 80%）、80µs→1.1µs 片上交换；无端到端模型数字
- [2026-10-18] 【一方博客】【仅摘要】Scaling Indic Pretraining: 2.8T tokens of open data · Hugging Face / NVIDIA + AI4Bharat · https://huggingface.co/blog/nvidia/scaling-indic-pretraining —— 22 种印度语言（本土 2,601.0B + 罗马化 224.6B，Gemma-4 tokenizer）；翻译→质量评估→修复→罗马化四段管线（NeMo Data Designer + Gemma-4-31B-it）；Nemotron 3.5 Super VL CPT 100B 预算中 10B 为该语料与自然 Indic 混合，五个 Indic 基准 +4.98~9.82 分（混合阶段整体变化，未隔离合成贡献）

- [2026-09-28] 【一方博客】Kimi K3 Performance Optimizations in vLLM · https://vllm.ai/blog/2026-09-13-kimi-k3-performance-optimization —— 全文；B300 TP8 CUDA13.3，固定提交82a85dc1对v0.27.1；并发1/4/16吞吐2.2–2.8×
- [2026-09-28] 【工业博客】【仅摘要】Quail: query-aware inference · https://modal.com/blog/quail-billion-tpm —— 简条目；十亿TPM不是生成吞吐，全基准1.84×；版本核验不足
- [2026-09-28] 【一方博客】【仅摘要】MiMo-V2.6 tool-call repetition · https://mimo.xiaomi.com/blog/mimo-v2-6-tool-call-repetition —— 简条目；轮内精确JSON重复口径，失败回放非总体
- [2026-09-28] 【一方博客】【仅摘要】ARCv3 and cross-region RL · https://fireworks.ai/blog/arcv3-and-the-case-for-cross-region-rl —— 简条目；生产权重差量压到原模型0.19%，原始样本和CPU成本未核全

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
- [2026-09-10] 【一方博客】vLLM x AgentX: Optimizing for Real-World Agentic Serving · vLLM 团队（Inferact 主导） · https://vllm.ai/blog/2026-09-08-vllm-agentx —— AgentX 上 DeepSeek V4 Pro 12×GB300 83K TPGS@P90 58.3 tok/s；`--long-prefill-token-threshold 512` 吞吐 +93%；三条负面：PP 不适合热轮次、DCP 在 DeepSeek V4 只打平 DEP、负载均衡输给 session 粘性
- [2026-09-10] 【一方博客】Inside the megakernel serving engine for North Mini Code · Cohere · https://cohere.com/blog/megakernels —— 单 H100、30B-A3B BF16：bs=1 292 tok/s（62% SoL）vs vLLM 185，端到端 1.25–1.41×；基线 vLLM v0.24 Triton MoE 后端、关 prefill；仓库 cohere-ai/cohere-megakernel Apache-2.0
- [2026-09-10] 【工业博客】Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses · Quesma（Piotr Migdał） · https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/ —— Q4_K_M 三基准与 BF16 无可测差异；2-bit 同任务多写约 1/4 token；1-bit 近随机。Unsloth v2 文件已替换不可得；KV 未测量化。J19 辅助
- [2026-09-10] 【一方博客】Modernizing complex legacy code with AI agents · Mistral · https://mistral.ai/news/legacy-code-modernization —— 4 万行 Fortran 77→C++：全自主得到换皮 Fortran，四角色卡住无人解，最终人操作 coder/tester/reviewer 按 ≤1 万行模块推进；parity harness 先行。无成本与缺陷率数字
- [2026-09-10] 【上游变更】【仅摘要】Deltafin: Kimi K3 (2.8T) on a MacBook Pro · argonautlabsai · https://github.com/argonautlabsai/deltafin
- [2026-09-10] 【工业博客】【仅摘要】Pretraining progress is mostly coming from data · Dwarkesh Patel、Jerry Han · https://www.dwarkesh.com/p/pretraining-progress-is-mostly-data
- [2026-09-10] 【一方博客】【仅摘要】Exploring Speculative Decoding in vLLM on AMD GPUs · vLLM 团队 · https://vllm.ai/blog/2026-08-23-speculative-decoding-amd-gpus
- [2026-09-10] 【工业博客】【仅摘要】GPT-6 Astra, Looped Transformers, and Hidden Reasoning · Sebastian Raschka · https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and

## 提及未展开（窗口外或判为跳过，防止当新货重推）

- Cascade —— per-request latency budget 调度（8 月初，窗口外）
- FlashBoot —— 亚秒级权重加载（8 月初，窗口外）
- CoinRAG —— nugget 级 KV 复用（8 月初，窗口外）
- OpenAI《ChatGPT's expanding world of work》（10-26）—— 经济研究数据，出四线范围
- OpenAI × Fanatics / Ultrafast CUT 事故调查（10-26）—— 客户案例，出范围
- Raschka: Building Reasoning Models from the Ground Up（10-23）—— 视频课程，教育内容
- AntLing Ming-3.0 系列语音模型 + 本地工作流两帖（10-19，窗口外）· https://x.com/AntLingAGI/status/2112395816300388539 · https://x.com/AntLingAGI/status/2112395707659526510
- MoE-Infinity —— 开源库非论文；落地首选，Expert Cache 篇说明其频率排序部分可能多余
- InferenceX 官方预览 TPUv7 Ironwood vs Blackwell/Blackwell Ultra · SemiAnalysis · https://newsletter.semianalysis.com/p/tpu-inferencex-full-steam —— 落选池。TPU 在 FP8 聚合服务上性能每美元最高优 50%、TPUv7 无原生 FP4；但基于私有 beta 的 TorchTPU 栈与其自有 fork，外部不可独立复现（预计 10 月中开源），且是付费产品预览稿，按硬规则 10 第 4 条降级
- Invalidation Contracts for Cross-Episode Agent Memory · arXiv 2609.00243 —— 定向「agent 记忆」判为跳过。缓存的 API 错误修复建议加版本戳；7 模型 9,400 episode，合规率随模型翻转（Haiku 4.5 100% vs Sonnet 5 ≤11%）
- What It Costs to Compose, Rebuild, and Correct Precomputed Memory · arXiv 2608.30647 —— 定向「agent 记忆」判为跳过。KV cache 级「预计算记忆」拼接退化、重建成本高、忽略旁置纠正；Llama-3.1-8B
- What Makes Agent Memory Useful for Reliable Unanswerable Question Handling? · arXiv 2608.27924 —— 判为跳过。记忆对 UAQ 的收益选择性且跨数据集脆弱
- Hindsight Memory-PRM · arXiv 2608.29605；MemGuard · arXiv 2608.21867；InjecMEM · arXiv 2608.23471；Towards a Formal Definition of Agent Memory · arXiv 2608.11654 —— 定向「agent 记忆」窗口内见过，判为跳过
- System X（KV 决策模型）· arXiv 2610.25456 —— 本期窗口内，初疑属 harness 论证群，复核为 KV 决策模型、不在本期论证内，不凑数
- Shopify Sidekick 分工架构（GTC Berlin 演讲转述）· https://x.com/shao__meng/status/2112889195178181033 —— 原谈日期早于本期窗口，记入「继续阅读」；转述称快 7 倍、成本降约 90%，未核验原文
