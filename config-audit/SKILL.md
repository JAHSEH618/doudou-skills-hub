---
name: config-audit
description: 复审 Claude Code 配置是否已被模型进步淘汰——找出为绕过旧模型限制而写、如今反而削弱新模型的规则/skill/hook,裁决试用期工具(如 codegraph)的去留,校验 codebase map 与跨仓共性标记块。在重大模型发布后、SessionStart 新鲜度提醒出现时、或距上次审查 3-6 个月时运行。
disable-model-invocation: true
---

# config-audit:配置折旧复审

核心论点:**配置是折旧资产**。为绕过模型限制写的规则会随模型变强从拐杖变成手铐(例:「重构拆成单文件改动」曾防止弱模型跨文件崩溃,现在纯粹削弱协调编辑能力)。折旧速度由模型迭代决定,不由代码决定。工具同理。

审查次序刻意安排为**先机械后判断**:机械校验免费且客观,先跑完把确定的问题摆上桌,再做需要判断和打扰用户的部分。

## Phase 0 — 机械校验(免费,先跑,不问)

从工作区根 CLAUDE.md 读 `claude-config-baseline` 块(date / model / workaround-rules / tools-on-trial / quarantine)。没有 baseline:告知需先跑 /init-scale,或现场补建(逐条问已有规则"当初为什么写")。

然后跑四项客观检查:

1. baseline 距今天数;当时 model vs 当前 model(换代 = 重点审查信号)
2. codebase map:列出的目录还存在?顶层有未记录新目录?结构事实半边可从 manifest/图重新推导比对
3. 跨仓标记块:各仓 hash 与 master 一致?不一致且非已知版本 = 被手改
4. LSP/插件健康:配置的 server 二进制还在 PATH?后缀注册有无新冲突?

**扫描范围:master(shared-conventions.md)与根文件,不扫各仓渲染拷贝。**

## Phase 1 — 呈现与定范围

打印 Phase 0 发现摘要(每项一行,✓/✗)。AskUserQuestion 问审查范围:「全面审查(推荐)」/「只修机械校验发现的问题」/「只裁决到期的试用期/隔离项」。

## Phase 2 — 规则三分类(需要判断的部分)

逐条过 workaround-rules、CLAUDE.md 正文、skills、hooks;baseline 之外来历不明的规则按"无法判断"处理:

- **项目事实**(命令、约定、地雷——编码的是项目而非模型缺陷)→ 保留
- **已被模型能力覆盖** → 提议删除,附一句理由
- **无法判断** → 进 quarantine:移入 baseline 的 quarantine 段并从生效位置注释掉,观察 2-4 周(记 until 日期)。到期没人喊疼 → 下次删除;出了问题 → 恢复并改标为项目事实。**用可逆的观察替代不可靠的单次 A/B 对比**——观察免费,误删的排查很贵。拿不准一律倾向 quarantine。

## Phase 3 — 试用期工具裁决

对 tools-on-trial 到期项,按登记的 criteria 问用户实际体验(codegraph:探索类问题变快了吗?出现过错误调用边吗?)。留 → 转正并登记下次复审日期;去 → 执行卸载(codegraph:`codegraph uninit` + `npm rm -g @colbymchenry/codegraph` + 清理 MCP 注册与 permissions.allow)。

## Phase 4 — 产出

diff 提案逐条一行理由,AskUserQuestion 确认后执行。手改标记块的裁决:收编进 master 或回退,不静默覆盖。所有删除先备份到 `.claude/init-scale-backup/<日期>/`。更新 baseline(date 刷新、model 记当前、quarantine/trial 推进)。收尾报告:删/隔离/保留各几条,下次建议审查时间。

## 约束

本 skill 仅由用户触发(disable-model-invocation)——改共享配置是有副作用的维护动作,不该被模型自主发起。
