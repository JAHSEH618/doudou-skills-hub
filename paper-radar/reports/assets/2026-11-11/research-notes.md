# 2026-11-11 研究笔记

## 运行信息

- 运行方式：cron 每日推送（周扫流程），窗口 2026-11-02 → 2026-11-11（9 天 ≤ 10 天，不扩容）。
- 上次周扫日期 2026-11-02（账本头部）；2026-11-09 的一次运行被宿主机出站网络故障中断，只留下 `reports/assets/2026-11-09/` 空目录，无报告——本次 9 天窗口是连带的补扫。
- 11-02 期报告在本地存在但未进仓库（仓库 HEAD 停在 2026-10-30），与本期同一次 push 补档。
- 主题：一致性（kernel/数值/上下文失配）。8 篇论文（全文 3 + 摘要 5）、14 条工程实践（详 6 + 简 8）、资讯 8、快讯 8。

## 信源缺口与降级（披露）

1. **exa 不可用**：`scripts/exa_api.py` 所有查询返回 **402 NO_MORE_CREDITS**（`exa-papers.jsonl` 为空）。按硬规则 3 已向用户披露，禁止静默降级。替代检索：arXiv 官方 API（`export.arxiv.org`，四线 12 个关键词簇 × submittedDate 窗口，见 `arxiv-candidates.json`，窗口内 370 篇，去重后 55 篇候选人工初筛）+ 内置 web_search（无 key 免费档，用于补 arXiv 池外的真实论文与 URL 定位）。
2. **AIHot 只覆盖近 7 天**：窗口前 2 天（11-02/11-03）的资讯靠 HN 高分帖与网页搜索渠道补，报告导言已声明。
3. **fetch_sources.py scan 首扫 8 个 feed URL 报错**（瞬时故障）：**rescan 后 errors 为空**，rescan 版 candidates.json 为权威；rescan 比首扫多 5 个窗口内条目（其中 1 条 SGLang-TorchTPU 相关信号不在 rescan 池，未采用）。
4. **anthropic.com/engineering 页面改版**（文章移到新版卡片布局），重写 `fetch_sources.py` 的 `scrape_anthropic_engineering()`（按 `<article class="nUeDbq_article">` 切分），解析 24 条，窗口内 1 条（11-06 The components of agent memory）。
5. **arXiv 全文通道**：`arxiv.org/html/<id>v1` 对 2611.04887 与 2611.06828 缺节；ar5iv 对这两篇只返回 abs 页；最终经 `arxiv.org/pdf/` 提取 PDF 全文（两篇合计 25,900 字）完成全文核验。arXiv API 摘要仍是元数据权威来源。
6. web_search 与 web_extract 并用，未单独依赖任一通道。
7. openai.com 两条资讯链接（GPT-6 Cyber、收购 Pierre）在 link audit 中为 403（bot 出口受限），已用 web_extract 独立通道核对页面标题与内容一致，按硬规则 6 标注为「受限但已核对」，不算失效也不算审计通。

## 候选池（rescan 版 candidates.json）

- AIHot 热点：134 条（7 天窗口）
- HN：2 条（均为 Agent memory 主题高分帖）
- blog_feeds 窗口内：87 条，分源如下
  - claude.dev（必看）2：Fable 5.2 多智能体 → 详；「Which Claude model should you build with?」（11-09）→ 过滤，模型选型营销指南，无可核验工程数字
  - anthropic-engineering（必看）1：agent memory → 详
  - vLLM（必看）5：Zero Mismatch/REINFORCE Zero → 详；Kinference → 详；Stable ABI → 简；VeRL-Omni v0.3.0 → 简；Kimi K3.1 Pro day-0 → 简
  - Hugging Face（必看）11：HOPE 专家剪枝 → 简；其余 10 条过滤（Hub 账单/Decision Models/Nemotron-Personas 数据集/ToyBlocks 机器人/ASR 排行榜/Phonon TTS/Dharma Field/Palette/CWE-bench v2/Transformers 集成合同——产品、数据集或四线外；CWE-bench v2 进落选池）
  - OpenAI（必看）32：GPT-6 Cyber → 资讯；收购 Pierre → 资讯；其余 30 条过滤（客户案例 ×10、产品发布 4、人事 2、安全系列 5、教育/医疗内容营销、wet-lab agent 测量与「A thousand fewer paths to root」未全文读，前者进落选池）
  - DeepMind（必看）5：Gemini 4 Carbon → 资讯；AlphaProof Code → 资讯；Gemini Robotics 2.5/Gemini Omni 1.2 Flash/Antigravity 化学信息学 → 过滤（四线外或未全文读）
  - NVIDIA Developer（必看）25：Attribution → 详（页面正文日期 2026-11-02，RSS 标 11-03，以页面为准）；NeMo 失败转测试 → 简；Reshard → 简；Snapshot → 简；CUDA 13.5 → 资讯；其余 20 条过滤（产品/营销/四线外；Agent Substrate、Automated Workload Recovery 命中四线但未全文读，进落选池；Nemotron 3.5 Super VL 属模型发布，资讯配额 8/8 已满，留待下期）
  - PyTorch（必看）4：Muse Spark on TPU v7 → 简；CFP/KVCache Meetup/Ray SIG → 过滤（活动与社区治理）
  - 被动组：Together AI 2（Together Compiler、Polymorphic Inference，11-04，命中推理线，简条目配额 8/8 已满，进落选池）；Qwen/Raschka/Huyen/Weng 窗口内 0 条

## 阅读与核验记录

- 全文验证检查单 3 篇：FourSight 2611.04887、Systolic 2611.06828、PACE 2611.10240（PDF 全文，时间线/基线/硬件边界逐项过）。
- 摘要级 5 篇：RAG poisoning 2611.04264、OPD 2611.08453、TIM/OPD 容忍度 2611.11450、BitDecoding-FP4 2611.09825、Twice as Fast 2611.04380。
- 一方/工业博客原文全读 6 篇详条目：vLLM Zero Mismatch（含 REINFORCE Zero 对照，GitHub `hijkzzz/REINFORCE-Zero`，NVIDIA 10 人，不在 arXiv）、Anthropic agent memory、Claude Fable 5.2、Kinference、Apple MIPS（`machinelearning.apple.com/research/faster-retrieval`，11-05；对应论文 ICML 2026，arXiv 2603.08001，代码 apple/ml-amips）、NVIDIA Attribution。
- 关键数字 5 轮 Python 上下文核验（Stainless 53%/54→61%/48%、ZM 2.4×、PACE 97%/42%、D3 定义更正版：逐更新对 token 求平均的 w−1−log w，w 为重要性权重；vLLM commit hash 不可验证已从正文删除）。
- X 快讯 8 条全部经 `fetch_sources.py x`（oEmbed）验证（18 帖 + 2 帖重验）。
- 解说：FourSight 找到合格第三方人写解读 1 条（liuzhao09.github.io，2026-11-05）；其余论文与实践无合格解说，只记于此不写占位。
- 许可证：FourSight CC BY-NC-ND（不嵌图）；Systolic/RAG/OPD CC BY 4.0（可嵌）；PACE 未声明（按保守不嵌）；本期正文未嵌任何论文原图。

## 判断账本联动

- 印证 6 条：J1（Twice as Fast + Apple MIPS 1.9× 条件集）、J14（BitDecoding-FP4 + Zyphra MI355X）、J16（PACE：保留什么与放在哪两个独立变量）、J18（RAG 投毒：写入准入与检索边界是防线）、J19（FourSight：FP4 误差集中性前提）、J29（Systolic：亚二次注意力效率实现受限）。
- 新增 1 条：J30「失配是一级变量」（OPD 2611.11450 摘要级主证据 + REINFORCE Zero/Zero Mismatch 一方博客辅助证据，含边界说明）。
- 单篇孤立结论不进账本（RAG poisoning、Twice as Fast 的多数发现已按印证并入 J18/J1）。

## 落选池（≤5，仅标题 + 一句话 + 链接）

1. The Intrusion Pathway（arXiv 2611.07778，NVIDIA 等，11-05）——非证据上下文经稀疏「intrusion heads」入侵下游任务，mask 级 knockout 约 10 头恢复 57% 掉点；9 天窗口上限 8 篇让位。代码 `https://github.com/dk4248/the-intrusion-pathway`，解说 alphaXiv/ithome 可达。
2. Agent Substrate: Advancing Kubernetes for Agents at Scale（NVIDIA Dev，11-10）——agent 编排基础设施，命中软件系统线，未全文读。
3. Keep Distributed Training Running with Automated Workload Recovery（NVIDIA Dev，11-03）——容错线，未全文读。
4. CWE-bench v2（Hugging Face，11-03）——安全 benchmark 更新，工程方法线，未全文读。
5. Measuring how AI agents handle everyday wet-lab science（OpenAI，11-06）——agent 实测研究，工程方法线，未全文读。

另：Together Compiler（together.ai，11-04，推理编译，命中软件系统线）——超出落选池 5 条上限，仅记于此：`https://www.together.ai/blog`（当期两条）。Nemotron 3.5 Super VL（NVIDIA，11-09，模型发布，资讯配额满）：`https://developer.nvidia.com/blog`。

## 统计

- 见 `stats.json` 与三张图（volume/judgments/trend）。
- 外链审计：`site/link-audit.json`（audit_links.py）。
- 检索审计：`search-audit.json`。
