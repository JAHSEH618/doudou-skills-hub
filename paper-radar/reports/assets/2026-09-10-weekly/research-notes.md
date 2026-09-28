---
type: "radar"
title: "同一份权重，换条服务链路就换了分数"
description: "从 KV 复用、模型后训练到 agentic serving，比较时必须一起固定输入、运行时与评测器。"
mode: "周扫"
window: "09-08 → 09-10"
created: "2026-09-10"
updated: "2026-09-29"
supplement_blogs: 2
supplement_x: 1
paper_count: 8
practice_count: 4
practice_abstract_count: 4
news_count: 7
---

# 同一份权重，换条服务链路就换了分数

模型评测的对象包含整条服务链路。KVShareArena 检查缓存拼接里的位置处理，IB2 比较相同权重经过不同运行时后的成绩，后训练研究又展示了输出提取规则对代码分数的影响。配置没对齐时，一个看似属于模型的差距，可能来自输入或输出处理。

实践部分集中在多轮 Agent 流量。前缀命中、会话路由和长请求调度会改变吞吐与交互延迟之间的选择；小 batch decode 的 kernel 优势也不能直接搬成端到端收益。读完这些材料，可以把下一轮性能比较需要固定的条件列得更具体。

上次周扫是 09-08，本期只有两天，论文 8 篇（上限 8，未扩容）。同一天已有一份定向报告，本期文件名和资源目录带 `-weekly` 后缀。AIHot 的 7 天窗口盖住了整个区间。本次走了 exa 与 `fetch_sources.py`（AIHot + HN，无报错），论文发现另外用 arXiv API 按提交日期补了一遍；已过 humanizer-zh。

## 阅读导引

- KV cache 离开出生上下文后，免费的位置对齐在单源题上就够用，多源题上不修的 cache 比不用 cache 还差，压缩类方法在复用场景下全线告负 · [arXiv 2609.10266](https://arxiv.org/abs/2609.10266) · 【论文】
- vLLM 在 SemiAnalysis AgentX 上给出三条端到端测出来的反直觉结论：PP 不适合热轮次、DCP 换个模型就不灵、负载均衡输给 session 粘性 · [vllm.ai](https://vllm.ai/blog/2026-09-08-vllm-agentx) · 【一方博客】
- 同一份 Qwen3.6-27B 权重在两条 FP8 路由上跑同一套题得 26.12 和 62.25，按模型名打分的基准分不清模型答错和路由拒绝 · [arXiv 2609.10494](https://arxiv.org/abs/2609.10494) · 【论文】
- 30B MoE 上预训练指标全面更好的退火 checkpoint，走完同一条下游流水线后反而更差 · [arXiv 2609.08966](https://arxiv.org/abs/2609.08966) · 【论文】
- NSA/CISA/FBI 联合通告点名 DeepSeek、月之暗面、阿里、MiniMax、阶跃、智谱六家做「工业规模蒸馏」 · [cisa.gov](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a) · 【资讯】

## 阅读导引

- [KV 复用怎样受位置处理影响](https://arxiv.org/abs/2609.10266)
- [后训练成绩为何受输出提取影响](https://arxiv.org/abs/2609.08966)
- [真实 Agent 流量对服务配置提出什么要求](https://vllm.ai/blog/2026-09-08-vllm-agentx)

## 本周只读一篇

### KVShareArena: KV-Cache Reuse Across Contexts and Model Checkpoints

Xi Shi、Qian Lou · 2026-09-09 · [arXiv 2609.10266](https://arxiv.org/abs/2609.10266) · 【论文】【全文】
把「KV cache 离开出生上下文后还能不能用」做成基准，两条赛道（RAG 检索块、多 agent 报告），按恢复了「不用 cache」到「全量重算」之间多大比例的差距（PGR）计分。免费的位置对齐在单源题上够用；多跳题上它本身 PGR **−0.196**，比不用 cache 还差，只有付费修复（CacheBlend 重算 17% payload、LegoLink 不到 0.5%、attention calibration）拉回到 0.39–0.46。压缩类方法没有一个格子显著赢过免费对齐，SnapKV 在出生上下文里 PGR 0.77/0.69/0.82，错位拼接后掉到 0.57/0.17/−0.08；直接拼接 agent 报告 PGR **−0.82**。换一个 checkpoint 写 cache，训练无关方法几乎不动（≤0.06），训练过的 adapter 最多掉 0.135，失败形态是流畅的答案配错的实体。
主板只有一个未具名的 8B 模型，Llama-3.1-8B-Instruct 与一个 4B 只复现模式不比数字；每子集 N=100，最小可检差异约 0.10 PGR；输入上限 29K；论文里的 pip 包与仓库链接还是占位符，PyPI 今天查不到。
*适读对象：在 RAG 或多 agent 服务里做非前缀 KV 复用、或准备给复用的 cache 上压缩的人。*
解说：暂无人写解说
三个社区各自发表、各自计分的 KV 修复方法，第一次放到同一把尺子下，给出的是类级别的结论，能直接拿去做决策。位置对齐免费且够用，除非题目要同时用多个来源；压缩在复用场景下只会亏；训练过的修复换 checkpoint 就坏。验证记录见附录。

## 硬件

### HBFSim: Fast and Faithful Simulation of High-Bandwidth Flash Under Real GPU Execution

2026-09-09 · [arXiv 2609.09800](https://arxiv.org/abs/2609.09800) · 【论文】【仅摘要】
High-Bandwidth Flash 把 NAND 堆进加速器封装，位于 HBM 之下一层，规范 2026-08-03 发布，首批推理器件预计 2027 年初送样。HBFSim 改写 PTX、门控 kernel 启动，把 HBF 的时序、容量、热效应加到真实 GPU 上跑的真实负载：六个校准点与实测器件一致，零不安全启动，未改动的 vLLM 0.15.1 跑 Qwen3-30B-A3B 返回与基线相同的 token id；快路径 **2 秒**对详细路径 44 秒。
仅摘要；「与实测器件一致」指校准用的现有器件，HBF 本身还没有硅，容量与放置决策的结论要等真器件。
*适读对象：在做推理机内存层级规划、评估 HBM 之下再加一层的人。*

## 模型

### Good Pretraining, Bad SFT: Checkpoint Quality Across the Training Stack

Aleph Alpha · 2026-09-08 · [arXiv 2609.08966](https://arxiv.org/abs/2609.08966) · 【论文】【全文】
30B MoE（3B 激活）、7.5T token 预训练，同一条下游流水线（100B 中训 + 100B 长上下文 + 10B SFT）跑三个起点。COOLDOWN 在最后 800B token 做学习率退火，每一项预训练指标都更好（验证 loss 1.648 对 1.734，预训练聚合 0.440 对 0.415），SFT 后聚合却是 **0.247 对 0.360**。差距主要来自 HumanEval+ 从 64.6% 崩到 4.9%，去掉它只差 0.016。中训后的排名与最终排名相关只有 r=0.47，长上下文后升到 0.88，但仍分不出这三个起点。高斯扰动后保留 90% 分数的比例（solution density），GSM8K 上 CONSTANT 27%、MERGE 13%、COOLDOWN 0%。
一个模型家族、每设置一个种子；COOLDOWN 扫了 27 个配置而 CONSTANT 和 MERGE 各只跑一次，方向不受影响，幅度会；COOLDOWN 的失败主要是答到 32k 上限停不下来，作者自承这放大了差距；无代码无权重。
*适读对象：做多阶段训练、按预训练 loss 或 benchmark 选起点 checkpoint 的人。*
解说：暂无人写解说

### Quantization Amplifies Determinism, Not Bias: Scale-Dependent Behavioral Effects of Serving-Time Weight Compression

单作者 Dachi Kurtskhalia · 2026-09-07 · [arXiv 2609.07901](https://arxiv.org/abs/2609.07901) · 【论文】【仅摘要】
Qwen3-8B/14B/32B 各跑 W4A16 AWQ、W8A16 FP8-Marlin、bf16，硬件软件采样固定，约 71,000 条按 prompt 和 seed 配对的补全，分析分三波预注册进版本控制。8B 上 int4 让输出收窄：同一场景两次采样推荐同一品牌的概率 **+5.1pp**（Holm p=.023，重跑 +4.4pp），词汇多样性 TTR −0.011；14B 和 32B 上集中度不显著，出现风格漂移（破折号率 +0.46 和 +0.61 每千词）。刻板印象方向的预注册检验在所有尺寸都是零结果。
仅摘要；一个模型家族、两套自制 prompt 电池；NeurIPS 2026 workshop 在审。
*适读对象：用 4-bit 服务小模型做推荐、生成类任务的人；做「量化无损」审计、只看准确率的人。*

## 软件系统

### KVShareArena

[arXiv 2609.10266](https://arxiv.org/abs/2609.10266) · 【论文】【全文】
即本周只读一篇，本线第一名。

### Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding

EMNLP 2026 · 2026-09-08 · [arXiv 2609.09338](https://arxiv.org/abs/2609.09338) · 【论文】【仅摘要】
drafter 通常只对一个目标模型的窄分布训练，workload 一变接受率就崩。Osprey 把现成的小预训练模型剪成浅 backbone，做目标无关的 next-token 预训练，再用词表对齐、零初始化 QKV 扩展和目标 logit 蒸馏适配到每个目标。一个 backbone 跨目标复用：Qwen3-8B 平均接受长度 **+16.1%**，Llama-3.3-70B +21.2%，MiniMax-M2.5 229B +22.7%（tokens/s +17.5%），最大增益在域外和多语言数据上。
仅摘要；接受长度不是端到端加速比，只有 M2.5 给了 tokens/s；论文写的仓库 LeanModels/Osprey 今天 GitHub API 查不到。
*适读对象：投机解码上线后发现生产流量和 drafter 的训练分布对不上、接受率往下掉的人。*

### Miles v0.1: Production-Level Post-Training

RadixArk · 2026-09-08 · [arXiv 2609.08368](https://arxiv.org/abs/2609.08368) · 【论文】【仅摘要】
slime 的生产化后继。SGLang 做 rollout，Megatron-LM 和 FSDP 两套训练后端，三种权重同步传输；全参 RL 之外支持 LoRA RL、on-policy 蒸馏、SFT、true-on-policy 对齐，并扩展到扩散模型。案例是 GLM-5.2 744B-A40B 在 **64 张 GB300** 上全异步 agentic RL（32 张 rollout、32 张训练），前 30 步中位步时 263 秒，rollout 权重平均落后 1.7 步，prefix cache 命中 96%。
内容 8 月 18 日已在 LMSYS 博客发过（当时写的是约 4.5 分钟一步），arXiv 版是整理稿；只报告前 30 步，没有收敛曲线；仓库 Apache-2.0、2,740 星、09-10 仍在推送。
*适读对象：要在 Blackwell 上做万亿级 MoE 异步 RL 的人。*
解说：[LMSYS 博客（作者侧）](https://www.lmsys.org/blog/2026-08-18-miles-v0-1/)

## 工程方法

### IB2: A Protocol for Measuring Enterprise AI Systems by Serving Route, Not Model Identifier

Iterate.ai · 2026-09-09 · [arXiv 2609.10494](https://arxiv.org/abs/2609.10494) · 【论文】【全文】
企业买的是 endpoint 不是 checkpoint。作者审计的 18 个基准全按模型标识打分，没有一个能区分模型答错和路由拒绝。同一份 Qwen3.6-27B 权重，两条 FP8 路由跑完 128 题各得 **26.12 和 62.25**，事后才发现一条把 13 张图的请求卡在 4 张上限，另一条号称 262,144 token 输出实际在 32,768 处截断；Qwen3.8-27B 换一条 serving arm，同一 revision 从 77.38 走到 82.54。把失败请求计入分母后，点估计的排序会变。
作者全部来自 Iterate.ai，语料封存不可复核，每配置只跑一次没有 run-to-run 方差；那两条路由的能力缺口是事后回溯出来的，不是预注册排除；仓库 IterateAI/IBIB 今天 404。
*适读对象：给采购写评测报告，或在多家 provider 之间比同一个开源模型的人。*
解说：暂无人写解说

### Benchmark Scores Are Pipeline-Dependent: A Reliability Audit of Cybersecurity LLM Benchmarks

2026-09-08 · [arXiv 2609.08765](https://arxiv.org/abs/2609.08765) · 【论文】【仅摘要】
8 个网络安全基准、10 个模型，把基准建模成测量流水线，找出 15 种系统性失败模式。单个流水线选项能让一个模型的分数动**超过 80 个百分点**；两对语义相近的任务因为评测约定不兼容给出不同排名；在保留任务语义、统一流水线选项的 harness 下，10 个模型里 9 个至少在一个基准上移动 3 名以上。
仅摘要；只覆盖网络安全基准，80 个百分点是最极端的一个选项。
*适读对象：把公开 leaderboard 当采购依据的人；自己写评测 harness 的人。*

## 工程实践与博客

**本周值得一读的实践**：vLLM x AgentX。三条直觉上对、端到端测量下错的教训，作者自己贴了出来。

### vLLM x AgentX: Optimizing for Real-World Agentic Serving

vLLM 团队（Inferact 主导） · 2026-09-08 · [原文](https://vllm.ai/blog/2026-09-08-vllm-agentx) · 【一方博客】
AgentX 是 SemiAnalysis 用 300 万美元真实 agentic coding 轨迹做的公开基准（中位 43 轮、中位输入 142K、输出 444、前缀命中率 >96%、44% 会话带子 agent）。vLLM 在上面的最优点：DeepSeek V4 Pro 12 张 GB300 服务 256 并发，P90 交互 58.3 tok/s 时 **83K** 总 token 每 GPU 秒；MiniMax M3 两张 B300 74.2 tok/s、70K；Kimi K3 16 张 GB300 62.7 tok/s、11.8K。`--long-prefill-token-threshold 512` 让 DeepSeek V4 Pro 在 B300 上吞吐 +93%、P90 交互 2.3×，代价是长请求 TTFT 变高。三条负面：PP 在热轮次上填不满流水线；DCP 在 Kimi K3 上赢 TP8，在 DeepSeek V4 上只打平 DEP；按负载均衡路由输给 session 粘性路由，因为 KV 迁移不免费。
「比 Opus 5 API 便宜 14.6×–106×」一边按理论完美缓存命中算 API 价、一边算 GPU TCO，口径不同；所有数字都是 vLLM 自己在 AgentX 上调出的最优配置，好在 dashboard 公开、harness 是 Apache-2.0。
*适读对象：在 GB300 或 B300 上给 agent 流量服务 MoE 大模型的人；正在选并行策略的人。*

### Inside the megakernel serving engine for North Mini Code

Cohere（Xiaochun Tong 等） · 2026-09-08 · [原文](https://cohere.com/blog/megakernels) · 【一方博客】
第一个围绕 decode megakernel 建的完整服务系统，支持 continuous batching、paged attention、ragged 序列、OpenAI 兼容端点和工具调用。单张 H100、North Mini Code（30B-A3B，BF16）：bs=1 时 **292 tok/s**，占带宽上限（约 470）的 62%，vLLM 185 tok/s；端到端 1.25–1.41×（AIME 1.41×、SciCode 1.37×、LiveCodeBench 1.28×）。整个 kernel 是一个 CUDA 文件，不用编译器。
基线是 vLLM v0.24 配 FA3 和 Triton MoE 后端、关掉 prefill、用合成 KV；1.58× 是 bs=1 的纯 decode 数，端到端只有 1.25–1.41×；自家模型用的 parallel transformer 层结构，作者自承这种结构从 megakernel 获益比多数架构大。仓库 cohere-ai/cohere-megakernel，Apache-2.0，75 星。
*适读对象：小 batch、低延迟 decode 场景（本地 coding agent）的人；想知道 megakernel 到底难不难写的人。*

### Benchmarking Qwen3.8 27B quantizations: 4-bit holds up, 1-bit collapses

Piotr Migdał（Quesma） · 2026-08-26（09-08 上 HN 首页） · [原文](https://quesma.com/blog/qwen38-27b-quantizations-benchmarked/) · 【工业博客】
Unsloth GGUF 的 Q8_0、Q4_K_M、UD-Q2_K_XL、UD-IQ1_S 在 GPQA Diamond、IFBench、Terminal-Bench 2.1 上对 BF16。**Q4_K_M（17 GB）三个基准上与 BF16 无可测差异**，Terminal-Bench 也复现了官方数；2-bit 在 GPQA 略降、Terminal-Bench 明显降，同一批解出的任务上多写约四分之一的 token；1-bit 在 GPQA 上接近随机，xhigh 推理更差，因为经常跑到预算耗尽返回空答案。
llama.cpp 用 8 月 16 日构建；Unsloth 8 月 19 日替换了 v2 文件，测过的文件已经拿不到；Q8_0 在 Terminal-Bench 上漏跑靠插值；KV cache 全程 F16，没测 KV 量化。约 3,000 美元 Modal（L40S、H100、H200）。
*适读对象：在 24 GB 卡上跑 27B 的人；看到「8-bit 也变笨」的抱怨想验证的人。*
解说：[HN 132 评论](https://news.ycombinator.com/item?id=49611128)

### Modernizing complex legacy code with AI agents

Mistral · 2026-09-09 · [原文](https://mistral.ai/news/legacy-code-modernization) · 【一方博客】
帮一家欧洲能源运营商把 Fortran 77 油藏模拟器迁到 C++，首个 sprint 做核心 **4 万行**（全库 30 万行），无测试集无集中文档。三次尝试：全自主（一个子程序一个 agent 跑一周）得到换了语法的 Fortran；planner、coder、tester、reviewer 四角色质量上去了，但卡住时没人解；最后是人操作 coder、tester、reviewer 工作流按模块推进，模块控制在 1 万行 Fortran 以内。动手前先建数值一致性 harness：Fortran 侧导出状态快照，C++ 侧加载校验；再用 caller-callee 树派上百个 agent 写文档。
无成本、时间、缺陷率数字；产品植入（Vibe CLI、Mistral OCR）；只完成核心部分。方法本身（parity harness 先行、按调用树切模块、人做检查点）可独立复现。
*适读对象：做代码迁移或现代化项目、在纠结给 agent 多大自主权的人。*

简条目：

- **Deltafin: Kimi K3 (2.8T) on a MacBook Pro** · argonautlabsai · [仓库](https://github.com/argonautlabsai/deltafin) · 【上游变更】【仅摘要】 · M5 Max 128 GB 上以约 1 token/s 跑完整 Kimi K3，权重从四块 SSD 流式加载，不剪枝不跳专家。
- **Pretraining progress is mostly coming from data** · Dwarkesh Patel、Jerry Han · [原文](https://www.dwarkesh.com/p/pretraining-progress-is-mostly-data) · 【工业博客】【仅摘要】 · 用 2019–2025 各年的公开模型配方和数据语料交叉训练（最高 1e19 FLOPs），数据侧带来 12.0× 算力效率、模型侧 3.7×，两者基本可加。
- **Exploring Speculative Decoding in vLLM on AMD GPUs** · vLLM 团队 · [原文](https://vllm.ai/blog/2026-08-23-speculative-decoding-amd-gpus) · 【一方博客】【仅摘要】 · MI300X 和 MI355X 上测五种起草方式（原生 MTP、Gemma 4 MTP、EAGLE-3、DFlash、DSpark），结论是收益随模型家族、draft checkpoint、负载和接受率变化。
- **GPT-6 Astra, Looped Transformers, and Hidden Reasoning** · Sebastian Raschka · [原文](https://magazine.sebastianraschka.com/p/gpt-6-astra-looped-transformers-and) · 【工业博客】【仅摘要】 · 第三方对 Astra 的循环 transformer 传闻做梳理，附近期 looped transformer 论文。

## 资讯

- NSA、CISA、FBI 联合通告 AA26-251A 点名 DeepSeek、月之暗面、阿里、MiniMax、阶跃、智谱自 2024 年底起对美国前沿模型做「工业规模蒸馏」，建议美国厂商检测异常账号、对疑似蒸馏请求悄悄改答、跨厂商共享情报 · CISA · [通告](https://www.cisa.gov/news-events/cybersecurity-advisories/aa26-251a) · 【资讯】
- Mistral 完成 30 亿欧元 D 轮，投后估值超 210 亿欧元，三星领投，钱明说用于扩算力训更大模型 · Mistral · [公告](https://mistral.ai/news/mistral-makes-sovereign-open-weight-ai-to-frontier/) · 【资讯】
- Paul Christiano 加入 OpenAI Foundation 董事会与安全与安保委员会，兼任 OpenAI Group PBC 董事会无投票权观察员，保留 CAISI 职务 · OpenAI · [公告](https://openai.com/index/paul-christiano-joins-openai-foundation-board) · 【资讯】
- 面壁开源 MiniCPM5-2B（2.52B 稠密、131K 上下文、Apache 2.0，vLLM 与 SGLang day-0）并开源背后的 RL 训练框架 Meshy（推理、rollout、训练拆成独立服务，Apache 2.0） · OpenBMB · [模型](https://huggingface.co/openbmb/MiniCPM5-2B) · [Meshy](https://github.com/OpenBMB/Meshy) · 【资讯】
- 蚂蚁百灵开源 Ling-3.0-flash-VL：124B 总参 5.5B 激活的原生多模态 MoE，42 层 KDA 加 Gated MLA 混合注意力，BF16 与 FP8 权重，MIT 许可 · inclusionAI · [模型](https://huggingface.co/inclusionAI/Ling-3.0-flash-VL) · 【资讯】
- OpenRouter 上线美国区域内路由：`us.openrouter.ai` 在美国境内解密、只发给美国 provider，无可用 provider 直接 404；DeepSeek V4 Pro、Kimi K3、GLM 5.2 通过 Baseten、Fireworks、Azure 在美国境内可用 · OpenRouter · [公告](https://openrouter.ai/blog/announcements/us-in-region-routing/) · 【资讯】
- OpenAI 公开支持按能力分级的强制性联邦安全监管，并背书四项已过加州议会的法案（SB 813、AB 1405、SB 1119、AB 1864） · OpenAI · [原文](https://openai.com/index/ai-policy-window) · 【资讯】

部分资讯经 AIHOT 聚合发现，链接均指向原始出处。

## X 上的讨论

- vLLM 里 DSpark 投机解码终于能和流水线并行一起用，推动者是 Kimi K3 的 2.8T 参数 · @SemiAnalysis_ · [原帖](https://x.com/SemiAnalysis_/status/2097445137521524787)
- AMD 不到 19 天靠软件把 vLLM 在 MI355X 上跑 MiniMax M3 agentic 负载的性能提了 11 倍，主要是长上下文 attention 算子 · @SemiAnalysis_ · [原帖](https://x.com/SemiAnalysis_/status/2097007346421531008)
- TPUv7 的 SparseCore 负责把各专家的 token 聚成连续组，TensorCore 只做矩阵乘，MoE 输入重排提 12% 吞吐；配 TorchTPU 外部推理栈，InferenceX 同口径下每美元性能比 Blackwell Ultra 高 50% · @SemiAnalysis_ · [原帖](https://x.com/SemiAnalysis_/status/2097490954907275409) · [TorchTPU 帖](https://x.com/SemiAnalysis_/status/2097309231082807795)
- Perplexity 已把大量推理迁到 NVLink Blackwell，下一步 Vera Rubin · @AravSrinivas · [原帖](https://x.com/AravSrinivas/status/2097372049559969973)
- Meta-Zenith 无人干预跑 111 轮试验，把 Qwen3.8-27B-NVFP4 在单张 RTX 5090 上的吞吐提了 63.5%（18 种设置几何均值），65K 上下文 4.1×，工具调用质量不变 · @ii_posts · [原帖](https://x.com/ii_posts/status/2097621235920191555)

## 延伸阅读 · 2026-09-29 补充

本节是此次编辑新增的背景阅读，材料原始日期见各条。它们不计入原扫描的论文、实践和快讯数量，也不改写当期判断。博客已阅读相关正文，但没有在本轮复跑实验或全部通过实践四项核验。

### 确定性推理：为什么 temperature 0 仍会变

Thinking Machines Lab / Horace He · 2025-09-10 · [博客原文](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/) · 【一方博客】【背景阅读】

文章从浮点加法顺序讲到 batch invariance：同一 kernel 在相同输入上可以逐位重现，但请求的批次形状变了，归约路径也可能变化。服务端的并发负载决定批大小，用户端便会看到不同输出。这里要区分“同一程序重复运行”与“请求换一个批次仍得到同样结果”。

这份作者侧解释适合和本期的测量研究对读。固定随机种子与贪心解码覆盖不了批次变化；核查一次回归时，还需要记录服务并发和 kernel 路径。博客中的具体实现与实验属于其发表时的版本，不据此保证现在任意推理服务的确定性。

### Kimi K3 的 DSpark：接受长度之外，还要读训练数据通路

vLLM 团队 · 2026-09-15 · [博客原文](https://vllm.ai/blog/2026-09-15-kimi-k3-dspark) · 【一方博客】【背景阅读】

这篇工程记录补上了起草模型怎样训练、怎样交付的过程。草稿模型一次提出多个 token，目标模型批量验证；DSpark 在并行起草后增加轻量的顺序修正与置信度估计。已发布 Kimi K3 drafter 每轮提出八个 token，九类任务的宏平均接受长度为 4.11，数学任务为 6.42，领域差异不能忽略。

训练链路用 Mooncake 传输目标模型的 hidden states，让推理和训练部署在不同节点并独立扩容。原文给出 GB300 环境与启动命令，但镜像示例使用 latest，图注的节点分组与正文也不完全一致；本轮作为已读背景材料收录，尚未完成版本及拓扑的四项复核。数学上的单流速度不能直接当作工具调用负载的收益。

### X 原帖补充

以下链接已经核对原始页面的作者与帖子文本；只作讨论线索，不作为独立实验证据。

**SemiAnalysis：把扩展域与专家并行一起比较**

@SemiAnalysis_ · 2026-09-11 · [X 原帖](https://x.com/SemiAnalysis_/status/2098238630015705267)

原帖强调 GB300 NVL72 的节点内扩展域与宽专家并行之间的关系。它适合提示下一轮比较应关注拓扑和专家分布。帖子中的性价比倍率仍需固定流量、利用率和成本口径，本次不把它写成采购结论。

## 落选池

- **Accuracy is Not Enough: A Divergence-Based Approach to Evaluate Fidelity Loss in Quantized LLMs** · 零样本准确率在逐级量化下非单调，掩盖了对 BF16 的分布偏离；用 token 决策边界上的 JSD、TVD 量信息损失 · [arXiv 2609.07664](https://arxiv.org/abs/2609.07664)
- **When Auditors Fabricate** · Gemini 3.0 Pro 找 150 篇论文里 450 处植入错误：单篇 50%、小批 60%、大批 **2.8%**，大批时会编造不存在的错误，而非弃权 · [arXiv 2609.09696](https://arxiv.org/abs/2609.09696)
- **A Layered Analysis of Disagreement and Answer Quality in Multi-Agent LLM Debate** · 750 场辩论，语气从友好到敌对让报告的一致率差 50.4 个百分点，回复文本是否真的反驳要单独量 · [arXiv 2609.08016](https://arxiv.org/abs/2609.08016)
- **Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training** · NVIDIA，drafter 与策略在线共训，CP 下扩展 zigzag ring attention 支持分支注意力，PP 下 TapChannel 跨阶段传特征，最高 122B、256K · [arXiv 2609.07108](https://arxiv.org/abs/2609.07108)
- **Q2D-Web** · Perplexity 的检索基准：190M 网页、69,721 条 agent 改写查询、三套相关性判定，附公开榜 · [arXiv 2609.08887](https://arxiv.org/abs/2609.08887)

## 判断账本动态

本期新增 1 条、印证 6 条、弱印证 1 条。J8 维持【存疑】。

![本期体量](assets/2026-09-10-weekly/volume.svg)

![判断账本关系](assets/2026-09-10-weekly/judgments.svg)

- **J19 新增**：量化的「无损」只在任务准确率这一层成立；行为层（输出集中度、风格、过程 token 数）会先于准确率变化，模型越小越明显。来源：Quantization Amplifies Determinism、账本里已有的 QSpec，落选池的 Accuracy is Not Enough 和 Quesma 实测作辅助。
- **J1 印证**：Osprey 把「加速比要带负载分布」推到投机解码的 drafter：接受率是训练分布的函数，域外和多语言上先崩。vLLM x AgentX 的 512 token 预填充上限（吞吐 +93%、长请求 TTFT 变差）是同一件事的 SLO 版本（一方博客，辅助证据）。
- **J8 弱印证，不改状态**：KVShareArena 的跨 checkpoint 实验里，训练无关的修复几乎不动，贴着某个 checkpoint 训出来的 adapter 换 checkpoint 就掉，失败还是静默的。
- **J10 印证**：Miles v0.1 的 arXiv 日期比 LMSYS 博客晚三周，Good Pretraining, Bad SFT 是「预训练指标选错起点」的负面结果样板。
- **J12 印证**：vLLM x AgentX 给了两条生产侧样本，DCP 与 DEP 的胜负随 scale-up 域大小翻转，按负载均衡路由输给 session 粘性路由（一方博客，辅助证据）。
- **J13 印证**：Benchmark Scores Are Pipeline-Dependent 把「仪器」从模型判断扩到整条评测流水线：一个选项动 80 个百分点，统一流水线后 10 个模型 9 个换名次。
- **J15 印证**：IB2 从「共享 endpoint 上同名模型不冻结」推到「路由的能力包络是测量对象的一部分」：图片数上限、输出截断、工具调用解析器，哪一个都能让同一份权重的分数差出一倍多。
- **J16 印证**：KVShareArena 里更多 cache 不是单调有益，收益符号由任务是否需要多源、以及修复机制决定；不修的 cache 比不用还差。

![跨期趋势](assets/2026-09-10-weekly/trend.svg)

## 附录 · 验证记录

### KVShareArena（arXiv 2609.10266）

1. 预印本时间线：v1，2026-09-09 首投，无历史版本。两位作者，机构未在 HTML 版署名。
2. 数据采集窗口 vs 发表：Retrieved Evidence 赛道用 LongBench v1 的三个 QA 子集加 FRAMES（钉在 2026 年 Wikipedia 快照上，作为变体标注），Agent Reports 赛道是作者构造的报告流水线；每子集 N=100，SHA256 冻结，固定种子，输入上限 29K token。准入判据、方法规格、读数规则在跑之前写好并提交；LLM 评分走「先提交判定、再开参考答案」的审计链。
3. 代码仓库状态：论文写「pip install kvsharearena」并给仓库、榜单、数据集三个链接，但正文里都是 `[repo link]` 占位符；PyPI 查 `kvsharearena` 返回 404，GitHub 搜索 0 个仓库。作者称在官方服务栈里发现并修了两个上游缺陷（分隔符处理让 cache blending 静默失效、RoPE scaling 被拦截），补丁随代码发布，目前无法核对。
4. 基线公平性：全部方法按机制分九类，跑官方实现或过「机制门」的移植版；KVPacket 和 Block-Attention 按官方配方自训（后者 8.2 GPU 小时）。对比基线是免费位置对齐，配对 bootstrap 95% CI，差异低于分辨率报为平手。主板 8B 模型未具名，第二家族 Llama-3.1-8B-Instruct 和一个 4B 只复现模式方向、不比数字，两处显著性判定在板间闪烁但方向不翻。
5. 适用边界：多源 QA 与 agent 报告，不覆盖代码或长生成；per-row 排名建立在一个 8B 上，作者自己给的反例是 LegoLink 的零重算端点在确认模型上赢、主模型上输；跨 checkpoint 只覆盖同架构、同 tokenizer、同 RoPE base 的兄弟模型。许可 CC BY 4.0；关键图是 Figure 3 的四面板 PGR 对重算比例散点，正文数字已够，没嵌。

### IB2（arXiv 2609.10494）

1. 预印本时间线：v1，2026-09-09 首投，42 页。名字 IB2 是 Iterate Business Intelligence Benchmark 的缩写，协议公开、语料封存。
2. 数据采集窗口 vs 发表：采样参数 2026-07-23 冻结，同日第一个完整运行开始；R11（DeepInfra FP8）2026-07-24、R12（CoreWeave FP8）07-26；十条判据的绑定门 08-13 才首次完整签署，晚于 R11/R12，所以那两条路由的能力缺口是回溯发现，只有 Provider P 是前瞻绑定。厂商服务条款审核日期 08-31 和 09-07。
3. 代码仓库状态：论文说方法、schema、runner 接口、合成一致性样例和审计账本会发布在 github.com/IterateAI/IBIB，Apache-2.0；今天该地址 404，GitHub 搜索 0 个仓库。语料、任务库、金标和非公开运行证据明确不发布。
4. 基线公平性：十一个系统（三个 GPT-5.6 端点、两个 Anthropic 操作点、三个 Qwen、Kimi K3、Muse Glimmer 30B、一个 GLM 组合系统），每配置只跑一次，串行并发 1。作者自承四条主要威胁：厂商利益冲突（基准是对自家系统建的，十一个第三方系统是唯一的留出集）、七个套件里四个饱和、单次运行无法识别 run-to-run 方差（领先两名差 0.97 分，区间宽 6.4 分）、评测包络（13 张图、25 个工具、>32,768 token 输出）是作者的设计选择不是测出来的负载分布。55 个两两区间未做多重比较校正，作者自己指出前三档的切分不可信，只认「前九、Qwen3.5-122B-A10B、GLM 组合」三组。
5. 适用边界：结论是「按模型名打分的基准无法报告路由能力」这个可报告性论点，不是任何具体排名；那 5.16 分的 serving-arm 差是接入方式、harness 代际、工具调用解析器和路由的联合效应，作者明说分不开。适用于企业采购场景下的多 provider 对比，不适用于生产部署（无检索、无人在环、无多用户状态）。许可 CC BY 4.0，未嵌图。

### Good Pretraining, Bad SFT（arXiv 2609.08966）

1. 预印本时间线：v1，2026-09-08 首投，5 页正文加附录，Aleph Alpha 五位作者，无 HTML 版。
2. 数据采集窗口 vs 发表：一个 30B-A3B MoE 的 7.5T token 预训练，CONSTANT 与 COOLDOWN 共享前 6.7T；下游流水线固定为 100B 中训（8k）、100B 长上下文（64k）、10B 对话 SFT（64k），各阶段重置优化器并重新 warmup。评测用作者自家 eval 框架，预训练期用补全式基准，SFT 后用六个对话式基准（AIME、DAPO、Skywork、IFBench、HumanEval+、GPQA）。
3. 代码仓库状态：无代码、无权重、无训练日志发布。
4. 基线公平性：作者自己列出的不对称：COOLDOWN 扫了 9 个中训/长上下文学习率组合、27 个含 SFT 的配置，CONSTANT 和 MERGE 各只跑一次且沿用 COOLDOWN 的最优调度；27 个 COOLDOWN 配置里最好的 0.294 仍低于未调的 0.360 和 0.363，所以翻转方向成立，幅度和 CONSTANT–MERGE 的先后可能变。每设置一个种子。
5. 适用边界：一个模型家族；COOLDOWN 的失败主要是 SFT 后答案跑到 32k 上限（AIME 100%、GPQA 99% 触顶），只取首个代码块能把 HumanEval+ 从 7.3% 救到 61.0%，说明能力在、停不下来；solution density 只在 GSM8K 和 MBPP 两题上测，作者明说不主张因果。许可 CC BY-NC-SA 4.0，关键图是 Figure 1 的扰动分布，未嵌。

### vLLM x AgentX（vllm.ai）

1. 第一方还是转述：vLLM 团队第一方，Inferact 主导，NVIDIA 和 AMD 协作；基准和 dashboard 由 SemiAnalysis 独立运营，harness 仓库 SemiAnalysisAI/agentx-harness（Apache-2.0，09-01 仍在推送）。
2. 可验证数字：三组模型、卡型、并发、TPGS、P90 交互全部给出，每条都链到 InferenceX dashboard 上的运行记录；调度参数的效果（+93%、2.3×）限定在 DeepSeek V4 Pro 于 B300 上。成本对比一侧是 GPU TCO、一侧是按理论完美缓存命中折算的 Opus 5 API 价，作者也写了这是「服务成本不是模型质量」。
3. 时间戳与版本：09-08 发布，引用的 PR 编号（#46188、#45444、#45659、#47317 等）可查；「Kimi K3 博客」为其前作。「数字是今天的」这句话本身就在提醒会变。
4. 营销动机：有，vLLM 展示自身；但基准是第三方的、结果公开可复现，且负面教训（PP、DCP、负载均衡）是自己贴出来的，保留为详条目。

### Cohere megakernel（cohere.com）

1. 第一方：Cohere 工程团队，三位署名作者。
2. 可验证数字：单张 H100（132 SM）、North Mini Code 30B-A3B BF16、bs=1 292 tok/s、SoL 约 470、vLLM 185；端到端表格分基准给出总时长、token 数、吞吐和倍数。代码 cohere-ai/cohere-megakernel，Apache-2.0，09-04 建仓、09-08 最后推送。
3. 时间戳与版本：基线 vLLM v0.24（FA3 attention、Triton MoE 后端、prefill 关闭、合成 KV）；vLLM 换 MoE 后端或开 CUDA graph 后差距可能不同，文中未测。
4. 营销动机：有，服务自家模型且模型结构对 megakernel 有利；方法（单文件 CUDA、统一 ABI、host 侧静态调度加设备侧 work stealing）可独立复现，保留。

### Quesma 量化实测（quesma.com）

1. 第一方还是转述：作者本人实测，非转述。
2. 可验证数字：四档量化、三个基准、三档推理强度都给了分数和 Wilson 95% 区间；BF16 结果与官方一致；Terminal-Bench 2.1 用 89 题、3 小时超时、98k 上下文。花费约 3,000 美元。
3. 时间戳与版本：llama.cpp 8 月 16 日构建；Unsloth v2 量化文件 8 月 19 日被替换，测过的文件已不可得；1-bit 用的是 v3。文章 8 月 26 日发，HN 9 月 8 日才上首页。
4. 营销动机：无产品推广。缺口是 Q8_0 在 Terminal-Bench 上没跑、KV cache 未测量化。

### Mistral 遗留代码迁移（mistral.ai）

1. 第一方：Mistral 自述项目。
2. 可验证数字：4 万行（全库 30 万行）、模块上限约 1 万行 Fortran、上百个文档 agent；无成本、工时、缺陷率、返工率。
3. 时间戳与版本：09-09 发布，未说明使用的模型版本与 Vibe CLI 版本。
4. 营销动机：有，Vibe CLI、Mistral OCR、文档库都是自家产品。三条方法结论（parity harness 先行、文档先行、人做检查点的结构化工作流）不依赖产品，保留为详条目，但按「过程叙事无数字」的水分读。
