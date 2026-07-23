# Skills 技能库

把实际干活时摸索出来的套路固化下来。

## 快速开始

```bash
# 克隆到 Claude Code 技能目录
git clone https://github.com/JAHSEH618/doudou-skills-hub.git ~/.claude/skills

# 或单独安装某个技能
cp -r ai-backend-resume-screening ~/.claude/skills/
```

装好后直接跟 Claude Code 说任务就行，会自动触发。

---

## 技能列表

### ai-backend-resume-screening

AI 后端开发简历筛选（从严版）。

**能做什么**：
- 分层筛选（硬门槛 → 能力门槛 → 加分项）
- AI 灌水检测（基于 humanizer-zh）
- 自动去重（本地 `checked.md`）
- 等级评定（初级/中级/高级）

**筛选标准**：
- 必须有 Cursor/Claude Code/Codex 实证
- 必须用过 SDD/TDD 工程化
- Agent 应用真实落地加 10 分
- 底线：工龄≤10年、本科及以上、年龄≤30

**用法**：
```bash
# 单份简历
请筛选这份简历：[附上内容或路径]

# 批量筛选
请筛选 ./AI开发-0615/ 目录下的所有简历

# 生成评分表
请为 AI 后端开发岗位生成评分表
```

详细文档：[ai-backend-resume-screening/SKILL.md](ai-backend-resume-screening/SKILL.md)

---

### viral-ai-blog-writing

写爆火 AI 技术博文的多 agent workflow。基于 TDD 开发，完全内化 [Humanizer-zh](https://github.com/op7418/Humanizer-zh)。

**特点**：
- 强制多 agent（Research → Writing → Review → Polish）
- 5-8次网络搜索，收集2026年爆文模式
- 内化 Humanizer-zh（24种AI模式 + 5维评分）
- 双重验证（内容≥70分 + humanizer-zh≥45分）
- 自动迭代润色到达标

**用法**：
```bash
请用 viral-ai-blog-writing 撰写关于"AI Agent在代码审查中的应用"的博文
```

**效果**：
- X平台：12-16词标题、2.7秒hook、易扫描
- 微信：去AI味、自然表达、口语化
- 技术深度：实战案例 + 可运行代码 + WHY解释
- Humanizer-zh≥45分（50分制）

耗时 15-25 分钟（自动执行）

详细文档：[viral-ai-blog-writing/README.md](viral-ai-blog-writing/README.md)

---

### init-scale

大型代码库导航层配置(引导式)。原生 `/init` 之后的增量层——`/init` 让 Claude 知道项目,init-scale 让 Claude 在大仓里找得到东西。

**能做什么**:
- 引导式流程:无声体检 → 一次提问定范围 → 只读探索 → 一张总提案确认 → 连续执行
- 搜索面收缩(permissions.deny,提案确认制,写后验证)
- LSP 正确性层主动安装(三层体检:插件/二进制/后缀冲突)
- codegraph 发现层条件安装(按仓库规模+间接层自动判定,试用期管制)
- 模块分片 CLAUDE.md + 跨仓共性标记块分发(多仓并排工作区适用)
- 折旧基线 + SessionStart 新鲜度 hook(配置是折旧资产,3-6 个月复审)

**核心原则**:
- 幂等:重跑即断点续跑,已就绪项自动跳过
- 自动化边界在"出错是否可见":会报错的直接做,静默失明的必须确认
- 三层导航铁律:发现用 codegraph(线索),判决用 LSP(事实),字面用 grep

**用法**:
```bash
# 在大仓/monorepo/多仓工作区根目录
/init-scale

# 仅同步跨仓共性标记块
/init-scale sync
```

适用场景:monorepo、多模块工程、多仓并排工作区、多语言仓库;或 Claude 定位代码慢、上下文烧得快、lint/test 超时的时候。

详细文档:[init-scale/SKILL.md](init-scale/SKILL.md)(细节按阶段下沉在 [init-scale/references/](init-scale/references/))

---

### config-audit

Claude Code 配置折旧复审。init-scale 的配套技能——核心论点:**配置是折旧资产**,为绕过旧模型限制写的规则会随模型变强从拐杖变成手铐。

**能做什么**:
- 机械校验先行(免费客观):baseline 陈旧度、模型换代、codebase map 失真、跨仓标记块手改检测、LSP/插件健康
- 规则三分类:项目事实(保留)/ 已被模型能力覆盖(提议删)/ 无法判断(进 quarantine 隔离观察 2-4 周)
- 试用期工具裁决(如 codegraph 的去留)
- 用可逆的观察替代不可靠的单次 A/B 对比

**触发时机**:重大模型发布后、SessionStart 新鲜度提醒出现时、或距上次审查 3-6 个月。仅限手动触发(`disable-model-invocation`)——改共享配置是有副作用的维护动作。

**用法**:
```bash
/config-audit
```

依赖 init-scale 写入的 `claude-config-baseline` 块;没有 baseline 时会引导现场补建。

详细文档:[config-audit/SKILL.md](config-audit/SKILL.md)

---

## 技能结构

```
skill-name/
├── SKILL.md              # 技能主文档
├── README.md             # 快速入门（可选）
├── workflow.js           # Workflow脚本（workflow类型）
├── references/           # 参考文档（标准、判定逻辑）
└── assets/               # 资源文件（模板、工具）
```

SKILL.md 格式：
```markdown
---
name: skill-name
description: 什么时候用这个技能
---

# 技能名称
...
```

---

## 开发文档

想了解开发过程的话，看 `.skill-development/` 目录（本地保留，不上传git）：

```
.skill-development/
├── completion-report.md              # 完成报告
├── final-summary.md                  # 最终总结
├── green-test-analysis.md            # GREEN阶段测试分析
├── progress-log.md                   # 开发进度日志
└── ...                               # 其他开发文档
```

记录了基于 TDD 的完整过程（RED-GREEN-REFACTOR）：
- Baseline测试和问题发现
- 方案设计和验证
- 迭代优化
- 关键决策依据

---

## 关于标准

这些标准是我基于实际踩的坑定的。

用之前看看是否符合你的场景，阈值可以自己调。核心逻辑（分层门槛、否决规则）建议保持，具体分值和放宽条件随意改。

---

## 许可证

MIT License，随便用。

---

## 贡献

欢迎提 issue 或 PR。觉得有用的话给个⭐️。
