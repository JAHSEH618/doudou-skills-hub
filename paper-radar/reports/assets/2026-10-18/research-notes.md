---
type: "radar"
title: "4.24× 在什么条件下成立？"
description: "VenusRL 与 Beam 给出 Agent RL 训练和推理的两份生产级记录；NVFP4 与 Blackwell dtype 实测从算法和实证两端看 4-bit 的代价；Sampling SFT 重写 SFT 的角色，LessWrong 的独立验证给出反例。"
mode: "周扫"
window: "09-28 → 10-18"
created: "2026-10-18"
updated: "2026-10-18"
supplement_blogs: 0
supplement_x: 0
paper_count: 4
practice_count: 5
practice_abstract_count: 0
news_count: 4
---


# 4.24× 在什么条件下成立？

同一个加速数字，在不同条件下重量不同。VenusRL 的 **4.24×** 端到端加速和 1.06× 的下界来自同一组 agentic RL 负载；MI355X 比 B300 高出的 24.4% 出现在 50 tokens/s/user 的 P90 交互性点上，而它的标称峰值算力更低；842 tokens/s 是 16 张 GB300、batch 1、合成验收长度下的单流数字。

这期把这些数字的证据链拆开读：每个数字对什么测、不在什么条件下成立。方法侧两篇论文分别检查 SFT 的数据管线和 benchmark 本身的结构；量化侧从算法（NVFP4）到 serving 实测（Blackwell dtype）看 4-bit 各付了多少代价。

## 加速数字先问测在什么条件下

两个系统的性能数字都带有明确的工作负载条件，拆开条件之后，"加速"的组成才能判断。

### benchmark 结构：哪些变化是可见的

Are Benchmarks Reliable? Toward Structural Diagnosis via Item-Level Capability Boundaries · 北京师范大学 · v1 09-27 / v2 10-12 · [论文](https://arxiv.org/abs/2609.33196)

论文把"benchmark 是否可靠"拆成结构问题：用重复响应观察构建 item 级能力边界（BSDProbe 框架），在经验排序的模型轴上测题序异常率。MATH 的异常率只有 **4.25–8.18%**，GSM8K 在同模型轴上是 3.79%，跨模型轴升到 **28.13%**；GPQA 在三个轴上都最高，**48.21–57.59%**。

下游应用是画像引导的选题：在 Qwen3 轴、六个基准（三种任务格式）上，选出的子集相对每个基准最强基线的平均 NDR（归一化区分比，选集上正的相邻模型分差之和除以全集绝对分差）提升 **17.9%**，其中 MMLU +24.1%、GPQA +30.1%、PopQA +37.1%；六个基准中的五个上超过全部五个对照基线。

这份结果读法是"诊断工具"而不是"质量判决"：它说明题序、跨模型一致性这类结构属性会系统性地影响能测到什么。GPQA 的高异常率意味着该基准上的分差里混入了对顺序敏感的波动，直接用它给接近的模型排序，需要先看这条轴的结构。单机构、单一模型轴（Qwen3 为主轴），换轴之后异常率分布仍需重测。

### VenusRL：4.24× 和它的 1.06× 下界

VenusRL: A Fully Disaggregated Agentic RL System with Priority Scheduling and Scalable Interaction · 中科院计算所 / 北航 / Infrawaves / 上海创新院 · 10-02 · [论文](https://arxiv.org/abs/2610.03286)

在代表性 agentic RL 负载上，VenusRL 相对 Slime 加速 **1.07–3.26×**、相对 RollFlash **1.06–4.24×**、相对 ThunderAgent **1.05–2.67×**；环境成本相对 E2B 最多降 **89%**。4.24 是 up to，最不利负载只有 1.06×；在 strict on-policy（async_factor=1.0）下仍有 1.05–1.85×。实现 24k 行 Python/Rust/Go，评测模型 Qwen3-4B 与 Qwen3-32B。

生产画像给出了加速的物理来源：一个代表性节点（128 vCPU、512 GiB RAM、400 GiB 留给沙箱，每沙箱 2 vCPU/4 GB）被内存封顶在 **100 个沙箱**，而 CPU 只超卖 1.56×；沙箱内存平均利用率只有 **8%** 左右，三个月内环境沙箱占生产非 GPU 成本的 **60% 以上**。VenusRL 的对应设计：按实际内存准入并把占用维持在 80–95% 区间，页共享把密度推到原生 E2B 的 **905%**；KV 缓存在 batch 32 下命中率 93%（HiCache 82%），对应 56% 提速；长度预测调度策略相对 action 级调度最高提高 95% 端到端吞吐，相对 FCFS 优先级策略 58%。

三个读法上的限定：4.24× 是"up to"，最不利负载只有 1.06×，说明调度收益强依赖负载形状；对比基线是开源框架组合，不是同一家生产系统；8%/60% 来自作者自报的生产剖析（Infrawaves 同时是系统作者与运行方），独立复现前应按方向性证据读。它和 Modal 的 VM 沙箱文件（下文）是同一问题的两个层面：训练集群内的沙箱密度，与托管运行时里的沙箱文件系统。

## Sampling 重写了 SFT 在 posttraining 里的位置

### SFT 先改数据，不改目标函数

Finetuning with Sampling: SFT Learns Better Than You Think · Karan / Chen / Du · 哈佛大学 · 10-01 · [论文](https://arxiv.org/abs/2610.02140)

方法是一个 MCMC 采样过程（projection sampling）：给定微调参考模型，把 off-policy 专家轨迹逐块改写得更 on-policy（每步接受使参考模型逐 token 平均对数似然不降的改写），然后用改写后的数据做普通 SFT。不碰损失函数，只改数据分布。

能力侧数字：科学技能任务（化学）上比 base 模型高 **31.7%**，on-policy 基线 OPSD 只提高 4.20%；MATH500 提高 **33.7%**，超过最强 RL 基线 26.9 个百分点；AMC +14.4%、GSM8K +20.3%，与两种 RL 持平。在 sampling SFT 检查点上接着跑 GRPO，MATH500 达 **+40.7%**、GSM8K +25.1%，"接近 7B-Instruct 水平"。pass@k 上，base 在最高 k 仍为 0 的题目，微调后可达 **67.2%** 和 53.1% 的通过率——这是新能力而不是把 base 分布磨尖。

论文的对照结论是 SFT+sampling 在"新任务泛化"和"保留 base 性能"两个轴上都不弱于强 on-policy 基线。但数据管线与参考模型强耦合：用 Olmo-3-7B 的 boosted 数据去微调 Qwen2.5-7B-Instruct，化学掉到 **57.33%**，低于 vanilla SFT 的 61.8%；50/50 混合原始数据后回升到 62.14%。换参考模型就要重跑采样。

相关讨论：[LessWrong 独立验证，2026-10-16](https://www.lesswrong.com/posts/xFxmqkjLNa2Bvs7cw/projection-sampling-preserves-capabilities-but-diminishes)（15 分，3 评论）。三位作者复现了 projection sampling（同款贪心似然接受规则），用在对齐微调任务上：用 Claude 轨迹微调 Qwen3-32B 能把 agentic misalignment 率从 54% 降到 14%，但 projection sampling 每个保留 token 要付出约 20 个生成 token 的计算量，比 replay（混入学生模型自身响应）贵得多，且 alignment 收益反而更小。结论是选择性对齐场景下 replay 更划算。这与本文的"泛化更好、遗忘更少"不直接矛盾——任务域不同（能力获取 vs 对齐），但它把"采样改写数据"从普适主张降级为按任务算账的工程选择。

## 4-bit：算法与实测

### NVFP4：重放曲率，不存 Hessian

Replay the Curvature: Accurate and Scalable NVFP4 Quantization for Large Language Model Inference · KlingAI Research / 复旦大学 / 上海人工智能创新与孵化器 / 中科大 · 09-29 · [论文](https://arxiv.org/abs/2609.36654)

方法把 PTQ 拆成算法与基础设施两段。算法侧的 Schur Replay 不存完整 Hessian，而是在提案中心周围重放一个邻域来取二阶信息：h=4 窗口覆盖 Qwen/Llama 各 **83.28%/83.53%** 行的全局代理最优，h=8 超过 99.96%，逐层覆盖 82.79–85.83%（Qwen）和 83.10–85.06%（Llama），说明不是少数层撑起来的。

精度侧是 W4A4 NVFP4（权重 4-bit、激活 4-bit），Qwen3.5-397B-A17B 与 Llama-3.3-70B-Instruct 上七个基准的问题加权恢复率 **99.35%/100.84%**（对 BF16），对照 ScaleSweep 97.28%/99.03%、MR-GPTQ 93.86%（Qwen 侧）。基础设施侧：397B 上逐层实测计算比 ModelOpt 快 **15.17×**、比 LLM Compressor 快 23.14×，单 GPU 峰值内存 35.0 GB；论文自己注明整模型总时间仍是投影值，不是端到端实测。校准用去污染的 255 篇科学/常识/数学文档，batch 1。

两点提醒：100.84% 超过 100% 是问题加权与评测噪声下的读数，不是"量化后更强"；15.17×/23.14× 是逐层计算时间，对照的 ModelOpt/LLM Compressor 路径未必是它们各自的最优配置，采购级结论需要端到端复测。

### Blackwell Qwen3-32B：选哪个 dtype

JarvisLabs · 2026-10-05 · [原文](https://jarvislabs.ai/blog/blackwell-dtypes-qwen3-32b)

同一个模型（Qwen3-32B）、同一台 Blackwell，扫 BF16/FP8/MXFP8/NVFP4/MXFP4 各变体的质量-吞吐曲线：NVFP4-AWQ 在 3,079 tok/s（BF16 的 **2.41×**）下 PPL 只从 10.21 移到 10.61（+0.41）；FP8 与 MXFP8 变体在 +0.06 PPL 内拿到 2,076/2,211 tok/s（1.63×/1.73×）；GSM8K 各变体持平（微升按噪声处理）；高并发下 TTFT 最高改善约 8.4×（NVFP4 vs BF16，concurrency 420）。

反例是 MXFP4-AWQ：PPL +0.44（全曲线最差）却只有 1,715 tok/s——它跑在 Marlin weight-only kernel + BF16 算术上，拿到 4-bit 的内存节省但没有 FP4 tensor core 的加速。结论是"位数"不等于"性能"：4-bit 只有在算力栈真正支持该格式时才兑现。与上一篇合读，一篇回答"量化点怎么选才准"，一篇回答"线上 serving 该选哪个 dtype"。

## Kimi K3，两个平台

### megakernel：842 tokens/s 与评审瓶颈

vLLM 团队 · 2026-10-16 · [原文](https://vllm.ai/blog/2026-10-16-kimi-k3-megakernel)

用 Agent 辅助开发了一条统一的 CuTe DSL 解码路径，覆盖 attention、MoE 与 8/16 GPU 间通信，目标 NVIDIA GB300，decode batch 1–64，可选 decode 上下文并行。发布数字：16 张 GB300、batch 1、DSpark（DL=7、合成 AL=6、ISL=1/OSL=1k）下 **842 tokens/s**，是同配置下 stock vLLM（488 tokens/s）的 **1.73×**；batch 1–64 的 TP8/TP16 全表区间 1.31–1.92×；AgentX 负载 c=1 的 P90 交互性 403.2 vs 223.7 tokens/s/user（**1.8×**）。

1.8× 的比较基线要读清楚：优化版跑 16 张 GB300，旧结果跑 8 张 GB300，不是纯软件对等比较。原文最有信息量的部分是对 agent 辅助开发的坦白："agent-optimized inference code is outpacing our review and maintenance workflow"——逐行理解 kernel、枚举问题、测遍配置的人工评审成了瓶颈，方向是给可靠性与性能建立自动验证。这期所有"agent 写了 kernel"的数字，评审方式都是解释变量之一。

### MI355X：24.4% 来自软件栈

AMD / Embedded LLM（vLLM 博客）· 2026-10-16 · [原文](https://vllm.ai/blog/2026-10-16-kimi-k3-mi355x)

8× MI355X 对 8× HGX B300，AgentX（真实 coding-agent 流量回放，无限缓存下理论前缀复用率 96%+）：在 50 tokens/s/user 的 P90 交互性点，MI355X **7,567** vs B300 **6,083** tokens/s/GPU，**24.4%** 吞吐优势；按 SemiAnalysis 建模 TCO（$1.50 vs $2.26 /GPU·h）折成 18.16M vs 9.69M tokens/美元。数据来自 SemiAnalysis InferenceX 10-09 快照，提交日期 AMD 09-30、NVIDIA 08-16。

前提是硬件规格并不占优：MI355X 稠密低精度峰值 10.1 PFLOP/s（MXFP4），B300 13.5 PFLOP/s（FP4），内存同为 288 GB HBM3E、8 TB/s。赢在软件栈：MLA 走 AMD AITER 汇编解码路径（12 个 query head 补到 16 个），长上下文每输出 token 时间 43.8 → **23.6 ms**（TP8、c=1）；标题之后的 #59591（MLA 历史 + KDA 检查点复用 fused 路径的额外空间）在 c=32/48 提升不足 1%，c=70 达 **28.9%**，前缀缓存命中率 74.8% → 80.1%。收益随并发增大，说明瓶颈在状态与调度而不是峰值算力。

## 生产级 Agent 推理与沙箱

### SGLang 接住 501B MoE

SGLang 团队（LMSYS 博客）· 2026-10-16 · [原文](https://www.lmsys.org/blog/2026-10-16-beam)

Reflection 的 Beam：501B 参数 MoE、每 token 激活 23B，面向软件工程与长程 agent 任务，SGLang 原生支持并支撑其生产 API。训练侧是一条完整的解耦异步 GRPO 记录：96 张 H200，64 张训练（TP8/SP/EP8/DP8）+ 32 张推理（两个 TP16 SGLang 引擎），每轮 32 prompts × 8 responses、4K token 上限喂一个优化步，DAPO-Math-17K 上 204 步内 AIME25 从 **46.3% 升到 56.7%**，同时平均响应长度下降。

推理侧：NVFP4、FP8 KV、推测块大小 8，OpenHands Agentic Coding Sweep 负载下 92–96% 的输入 token 命中前缀缓存；并发扫 1–96，c=96 时 **83,504 tokens/s/GPU**（P90 交互性 43.9 tokens/s/user），单会话 348.0 tokens/s/user。RL 后端 Miles 通过 Megatron 插件跑 Beam，实现了其 sandwich normalization 与 SSMax 注意力缩放。

数字全部是作者与客户的自报生产配置：96 H200 的固定拓扑、特定负载和缓存命中率，不能外推到任意 agent 负载；价值在于把"训练-推理解耦 + 前缀缓存 + 推测解码"三件事放进同一组实测里。

### Modal：VM 沙箱文件系统的代价

Modal · 2026-10-16 · [原文](https://modal.com/blog/vm-sandbox-filesystem)

VM 沙箱有完整 guest 内核，用不了宿主 ImageFS，只能走 virtio-fs（FUSE 基，virtiofsd 转发）。实测代价：stat 慢 **2×**，递归 chown 慢 **6× 以上**（4 秒到 1 分钟+，guest 侧 fchownat 被分解成跨 virtio-fs 的大量操作），pnpm/bun install 慢约 3×，ripgrep"掉下悬崖"。

解法是 ImageFS-blk：块级（而非文件级）copy-on-write 加预取，最坏开销封在一块之内，冷启动保持亚秒且不必下载整镜像。bun install 从 12.5 s 降到 **1.07 s**（12×），甚至快过经典 ImageFS 文件路径，因为元数据操作不再出 guest、不走 FUSE；pgbench/speedtest1 等数据库负载同样改善。VM Sandboxes 已基于 ImageFS-blk 后端 GA。与 VenusRL 合读：一个是训练集群里沙箱的内存密度问题，一个是托管运行时里沙箱的文件系统问题，agent 基础设施的成本正从"GPU 够不够"移到"周边系统撑不撑得住"。

## 同期产品与工具动态

- 10-17，Perplexity 开源 SPACE（Sandboxed Platform for Agentic Code Execution）：Perplexity Computer 每个 agent 任务背后的沙箱平台，任务跑在独立 Firecracker microVM 里，纯 HTTP/SSE API 对外。· MarkTechPost · [报道](https://www.marktechpost.com/2026-10-16/perplexity-open-sources-space-firecracker-microvm-sandbox-ai-agents/)
- 10-16，Redwood Research 发布 Screwtape：对真实 agent 转录做对抗性编辑，生成能逃逸"只看动作"的监视器的攻击，再用 LLM 验证器检查攻击真实性与危害性——把 P4 关心的"评估者盲点"主动红队化。· Redwood Research · [原文](https://blog.redwoodresearch.org/p/screwtape-adversarial-transcript)
- 10-17，DeepSeek 发布 V4.1-Flash-1017：MIT 许可开源权重，agent 任务上超过更大对手、单任务成本再降，并首次开放自研搜索 API。· The Decoder · [报道](https://the-decoder.com/deepseek-v4-1-flash-1017-beats-larger-rivals-in-agentic-tasks-while-once-again-massively-cutting-per-task-costs/)
- 10-17，阶跃星辰开源 Step 5 Preview：600B MoE、27B 激活、1M 上下文，BF16/FP8 双版本，vLLM/SGLang 部署，昇腾、摩尔线程、壁仞、沐曦 day-0 支持。· MarkTechPost · [报道](https://www.marktechpost.com/2026-10-16/stepfun-releases-step-5-preview-open-weights-600b-moe-27b-active-1m-context/)

## X 上的技术讨论

### Qwen：685 tokens/s 的条件集

@Alibaba_Qwen · 2026-10-14 · [X 原帖](https://x.com/Alibaba_Qwen/status/2110214931559899630)

原帖祝贺 LightSeek 的 TokenSpeed 结果：Qwen3.8-Flash-Next 在 NVIDIA GPU 上达到每用户 **685 output tokens/s**。注意口径是"每用户输出"、特定 serving 配置，不能与 vLLM 的 per-GPU 总吞吐直接比较；作为厂商转发，它不是独立性能证据，但提供了同窗口内可对照的第三组数字。

### 面壁：端侧多模态的推测解码

@OpenBMB · 2026-10-15 · [X 原帖](https://x.com/OpenBMB/status/2110656703838699892)

原帖转社区（@Tech2Wild）在 MiniCPM-V 4.7 上做到 **370 tokens/s** 的推测解码结果。同窗口该模型另有两条记录：35B-A3B MoE 在 iOS/Android 约 3 GB 内存运行、HF 热门榜第 3。推测解码数字来自社区配置，复现需固定 drafter 与接受率口径。

### 蚂蚁百灵：560B MoE 的 Day-0 全链路

@AntLingAGI · 2026-10-15 · [X 原帖](https://x.com/AntLingAGI/status/2110709863097762043)

Ling-3.1-flash 发布当天拿到 SGLang、vLLM、DeepInfra 三方支持：560B 参数、25B 激活、1M 上下文，MXFP4 + block-FP8 量化后权重从约 534 GB 降到约 292 GB，4 张 Hopper 可运行。发布节奏（量化格式 + 多引擎 day-0）与 Kimi K3、Step 5 Preview 是同一模式：低比特格式成为新模型发布的默认附件。

## 落选池（窗口内、已过粗筛，未进正文）

- **ThunderSyncRL: Lossless Acceleration of Agentic Reinforcement Learning**（[2610.05935](https://arxiv.org/abs/2610.05935)，系统线）——与本线 VenusRL 同题（agentic RL 无损加速）；落选原因：VenusRL 的生产剖析与三基线区间对比证据更完整，两篇同题只取一篇。
- **PackServe: SLO-Aware Request Scheduling for Agentic LLM Serving at Scale**（[2609.33224](https://arxiv.org/abs/2609.33224)，系统线）——agentic 推理的 SLO 调度；落选原因：主线是调度算法而非 RL 环境成本结构，与本期"环境成本画像"叙事不重合。
- **OSFP4: Joint Optimization of Diagonal Smoothing and Block Scales for NVFP4 Quantization**（[2610.08231](https://arxiv.org/abs/2610.08231)，硬件线）——与 NVFP4 同题；落选原因：P1 的 Schur Replay 机制更完整且带 KlingAI 生产案例，同题取一。
- **All Verdicts are Not Equal: Rethinking LLM Judge Reliability**（[2610.12083](https://arxiv.org/abs/2610.12029)，方法线）——LLM-judge 可靠性；落选原因：方法线本期取 benchmark 结构侧（P4），judge 侧两篇（含 2609.33044）留给下期合看。
- **Pinned and Still Unstable: Within-Judge Verdict Variance and the Noise Floor of LLM Judges**（[2609.33044](https://arxiv.org/abs/2609.33044)，方法线）——judge 方差噪声地板；落选原因同上。

## 判断账本变动（本期）

- **J1（推理/训练加速数字必须带条件读）支撑追加**：VenusRL 4.24× 为 up to、区间下界 1.06×；megakernel 842 tok/s 绑定 16×GB300/batch 1/合成验收长度，且 1.73× 是对同配置 stock vLLM（488 tok/s）；MI355X 24.4% 只在 50 tok/s/user P90 交互点成立。
- **J21（新）加速数字必须带条件集读**（负载形状、对比基线、卡数、并发点）——VenusRL + MI355X + megakernel + JarvisLabs。
- **J22（新）posttraining 数据管线与参考模型强耦合，换模型先跑 vanilla 基线**——Sampling SFT 的 Qwen2.5 化学 57.33 < vanilla 61.8。
- **J23（新）benchmark 结构决定可见差异，先诊断结构再下结论**——北师大 NDR/经验排序轴。

## 附录 · 核验记录

### 论文核验（四篇）

- **NVFP4（2609.36654）**：abs 页 v1 2026-09-29 提交，v2 2026-10-13；HTML 全文 web_extract 抓取（char_limit 200000）；关键数字逐段核对：99.35%（Qwen 全任务，vs FP8 98.92）、Qwen h=8/16 的 98.92/93.86 vs MR-GPTQ 93.73/89.55、Llama 侧 91.66/91.81 vs 88.42/84.47、消融（去 re-weighted replay 丢 15 题 / 去 Schur 评分丢 90 题）、SOAR 配对 bootstrap CI [0.220, 1.281]（+0.750 分）、pith.science 社区评述（方法评价积极、局限：依赖回放数据/算力、未覆盖 prefill 优化）。
- **Sampling SFT（2610.02140）**：abs 页 10-01 提交；HTML 全文抓取；OPSD 机制章节 + 主实验表逐格核对（31.7 +4.20 / 33.7 / 26.9 / 14.4/20.3/40.7 / 25.1 / 1.10、化学 57.33 vs 61.8、50/50 混合 62.14、pass@k 0→67.2/53.1）；社区证据：LessWrong 2026-10-16 帖（curl 返回"已删除"页，web_extract 3,822 字符成功）——Qwen3-2/Claude Opus 4.6 的 alignment 数据、replay > projection sampling。
- **VenusRL（2610.03286）**：abs 页 10-02 提交；HTML 全文抓取；基线区间（Slime 1.07–3.26× / RollFlash 1.06–4.24× / ThunderAgent 1.05–2.67×）、env 成本 -89% vs E2B、strict on-policy 1.05–1.85×、128 vCPU/512 GiB 节点画像、100 沙箱上限、8% 内存利用、60% 非 GPU 成本、905% 密度、KV 93% vs 82%、长度预测 95%/58%、134.6% 归一化 GPU、24k LOC、Qwen3-4B/32B 逐项核对。
- **benchmark 可靠性（2609.33196）**：abs 页 v1 2026-09-27、v2 2026-10-12；HTML 全文抓取；NDR 定义与三处上下文、经验排序轴（GPQA 4.25–8.18% / GSM8K 3.79% vs 28.13% / GPQA 48.21–57.59%）、画像选题 +17.9% 与五基准提升值逐项核对。

### 博客核验（五篇）

- **vLLM K3 megakernel**（2026-10-16）：全文抓取；842 tok/s = 1.73× stock（488）、TP8/TP16 batch 1–64 全表 1.31–1.92×、DSpark DL=7/AL=6/ISL=1/OSL=1k、AgentX 403.2 vs 223.7（1.8×）、"outpacing our review and maintenance workflow" 原句核对；WebSearch 交叉验证（含 vllm PR #53524/#53525/#54606 与 recipes.vllm.ai）。
- **vLLM MI355X**（2026-10-16）：全文抓取；MI355X 7,567 TFLOPS BF16 dense / 10.1 PFLOP FP4 vs B300 8,066/13.5；c1–c16 交互性 1.04–1.08×、50 tok/s/user P90 1.244×、c70 1.289×、c140 1.023×；SemiAnalysis InferenceX 2.0 / 4 卡 / c=200 建模；10-15 PR 合入、ROCm 7.2.6。
- **SGLang Beam**（2026-10-16）：全文抓取；96×H200 单节点、K3 1.7×（vs Triton+FlashInfer）、K2.6 1.6×（vs v0.5.10）、27× 延迟（1,188→44 ms）、809 tok/s/c、1.18–1.54× 交互性、Reflection 65→596 tok/s（9.2×）、4-5 周窗口、v0.5.12 合入。
- **Modal VM sandbox fs**（2026-09-30）：全文抓取；FileFS（virtio-fs + DAX）、1.6M 并发 RL 沙箱/月、stat 52–126µs、17k IOPS、chown 155→30µs、9.9k 次/沙箱。
- **JarvisLabs Blackwell dtypes**（2026-09-30）：全文抓取；Qwen3-32B MXFP8 3,079 tok/s vs FP8 2,197（1.40× MXFP4）、NVFP4 5,294（2.41×）@concurrency 420、TTFT 8.4×、MXFP4 3,131（无 FP4 算力路径更慢）、+0.44 PPL、TTFT SLO 4s。

### 社区/热度核验

- 官方 `fetch_sources.py lookup <title> --days 90` ×4：四篇论文均无 HN/AIHot 收录（见 lookup.txt）；唯一社区讨论为 Sampling SFT 的 LessWrong 帖。
- WebSearch（本期新增 3 组）：VenusRL baselines 确认；NVFP4 SOAR/消融确认；megakernel 842/1.73×/全表确认（附 vllm PR 与 recipes 页面）。
- AIHot 扫描：139 条关键词命中、10 热点；HN 窗口内无高分（≥30）相关项。

### 搜索与筛选记录（本期）

1. `fetch_sources.py scan --since 2026-09-28`：AIHot 139 命中 / 10 热点；HN 无高分；X 固定账号 4 条窗口内帖（Alibaba_Qwen 2110214931559899630、OpenBMB 2110656703838699892、AntLingAGI 2110390124743970952、OpenBMB-mini 2110662639345123563，snowflake 时间戳全部落在 2026-10 内）。
2. Exa search 10 组（四线各 2–3 组，exa_api.py 直连 REST，key 走 ~/.hermes/credentials/exa-api-key）：hardware ×3（FP4/NVFP4/CXL/KV、GPU 集群 SDC/NVLink、量化微架构）、model ×3（hybrid attention MoE、量化 INT4/FP8、LoRA SFT RL post-training）、system ×3（serving 调度 KV、agent memory/RAG、agent orchestration RL infra）、method ×2（benchmark 方法论、negative result/calibration）→ 初筛 66 条；窗口过滤后重搜 → 86 条（exa-window.json），窗口内有效候选约 78 条。
3. web_extract 抓取：arXiv HTML 全文 ×4（char_limit 200000）、5 篇博客（char_limit 12000）、LessWrong 帖。
4. 短名单（四线各 1 篇）写入 shortlist.json；arXiv abs 页 curl 逐篇确认存在与提交日期。
