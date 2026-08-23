# Skills 技能库

把实际干活时摸索出来的套路固化下来。每个技能的硬规则基本都来自一次真实翻车。

| 技能 | 一句话 | 触发方式 |
|---|---|---|
| [paper-radar](#paper-radar) | AI 工程化论文雷达，周扫 + 定向捞 + 单篇验证 | 自动 / `/paper-radar` |
| [ai-backend-resume-screening](#ai-backend-resume-screening) | AI 后端开发简历筛选（从严版） | 自动 |
| [init-scale](#init-scale) | 大型代码库导航层配置 | `/init-scale` |
| [config-audit](#config-audit) | Claude Code 配置折旧复审 | `/config-audit`（仅手动） |

## 快速开始

```bash
# 1. 克隆到任意位置
git clone https://github.com/JAHSEH618/doudou-skills-hub.git ~/CodeSpace/skills

# 2. 软链你要用的技能（推荐——仓库一更新就生效，改动也会回流）
ln -s ~/CodeSpace/skills/paper-radar ~/.claude/skills/paper-radar

# 或者复制一份（跟仓库脱钩，两边会各自漂移）
cp -r ~/CodeSpace/skills/paper-radar ~/.claude/skills/
```

别直接 `git clone` 进 `~/.claude/skills`——那个目录通常已经有别的技能了，克隆会失败；就算是空的，之后也没法只更新其中一个。

装好后直接跟 Claude Code 说任务就行，会自动触发（`config-audit` 除外，它只能手动调）。

---

## 技能列表

### paper-radar

AI 工程化论文雷达。为个人技术认知服务，**不做**「你们能不能落地」的业务过滤——每篇标注「谁该读」，把适用性判断留给读者。

**三种模式**：
- **周扫**（`/paper-radar`）：四条固定线全扫——硬件 / 模型 / 软件系统 / 工程方法，每线必报，没货也要写「本线无值得推的」
- **定向**（`/paper-radar agent记忆`）：按主题临时收窄，不改常驻范围
- **单篇验证**（`/paper-radar 验证 <arXiv链接>`）：对指定论文走全文验证检查单

**核心约束**：
- 主动调用 exa MCP 多角度搜，不用内置 WebSearch 替代；exa 不可用必须在报告开头声明降级
- 严格只收论文，工业工程博客一律不进清单（只能进判断账本作辅助证据）
- 每条必带可点击链接，强制标注【全文】/【仅摘要】；首推 2–3 篇必须全文验证
- 详条目 ≤8 篇（丰收周可声明扩容到 12），报告开头强制「本周只读一篇」

**两个自持账本**（这是本技能最值钱的部分）：
- `state/seen-papers.md`：去重账本，已推不重发，防改名重投
- `state/judgments.md`：跨论文判断账本，持续生长，可被新证据标【存疑】

**用法**：
```bash
/paper-radar                        # 周扫
/paper-radar agent记忆              # 定向
/paper-radar 验证 <arXiv链接>       # 单篇验证
```

详细文档：[paper-radar/SKILL.md](paper-radar/SKILL.md)

---

### ai-backend-resume-screening

AI 后端开发简历筛选（从严版）。

**能做什么**：
- 分层筛选（硬门槛 → 能力门槛 → 加分项）
- AI 灌水检测（基于 humanizer-zh），识别用 AI 美化或编造的经历
- 自动去重（本地 `checked.md`，已筛过不重复推送）
- 等级评定（初级 / 中级 / 高级）

**画像要点**：招的是**传统项目借助 AI 提效的后端**，不是 RAG / 大模型应用 / Agent 开发工程师——项目主体是后者的按画像错位处理。AI coding 工具实证和 SDD/TDD 是必过门槛。

具体阈值（年龄、工龄、学历、放宽机制）以 SKILL.md 为准，这里不复述——写两处必然漂移。

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

### init-scale

大型代码库导航层配置（引导式）。原生 `/init` 之后的增量层——`/init` 让 Claude 知道项目，init-scale 让 Claude 在大仓里找得到东西。

**能做什么**：
- 引导式流程：无声体检 → 一次提问定范围 → 只读探索 → 一张总提案确认 → 连续执行
- 搜索面收缩（`permissions.deny`，提案确认制，写后验证）
- LSP 正确性层主动安装（三层体检：插件 / 二进制 / 后缀冲突）
- codegraph 发现层条件安装（按仓库规模 + 间接层自动判定，试用期管制）
- 模块分片 CLAUDE.md + 跨仓共性标记块分发（多仓并排工作区适用）
- 折旧基线 + SessionStart 新鲜度 hook

**核心原则**：
- 幂等：重跑即断点续跑，已就绪项自动跳过
- 自动化边界在「出错是否可见」：会报错的直接做，静默失明的必须确认
- 三层导航铁律：发现用 codegraph（线索），判决用 LSP（事实），字面用 grep

**用法**：
```bash
# 在大仓 / monorepo / 多仓工作区根目录
/init-scale

# 仅同步跨仓共性标记块
/init-scale sync
```

适用场景：monorepo、多模块工程、多仓并排工作区、多语言仓库；或 Claude 定位代码慢、上下文烧得快、lint/test 超时的时候。

详细文档：[init-scale/SKILL.md](init-scale/SKILL.md)（细节按阶段下沉在 [init-scale/references/](init-scale/references/)）

---

### config-audit

Claude Code 配置折旧复审。init-scale 的配套技能——核心论点：**配置是折旧资产**，为绕过旧模型限制写的规则会随模型变强从拐杖变成手铐。

**能做什么**：
- 机械校验先行（免费客观）：baseline 陈旧度、模型换代、codebase map 失真、跨仓标记块手改检测、LSP / 插件健康
- 规则三分类：项目事实（保留）/ 已被模型能力覆盖（提议删）/ 无法判断（进 quarantine 隔离观察 2–4 周）
- 试用期工具裁决（如 codegraph 的去留）
- 用可逆的观察替代不可靠的单次 A/B 对比

**触发时机**：重大模型发布后、SessionStart 新鲜度提醒出现时、或距上次审查 3–6 个月。**仅限手动触发**（`disable-model-invocation`）——改共享配置是有副作用的维护动作。

**用法**：
```bash
/config-audit
```

依赖 init-scale 写入的 `claude-config-baseline` 块；没有 baseline 时会引导现场补建。

详细文档：[config-audit/SKILL.md](config-audit/SKILL.md)

---

## 技能结构

```
skill-name/
├── SKILL.md          # 技能主文档，必需（frontmatter + 正文）
├── references/       # 细节下沉，按需读取（init-scale、简历筛选有）
├── scripts/          # 确定性脚本，把机械活从模型手里拿走（简历筛选有）
├── assets/           # 模板、产物（简历筛选有）
└── state/ reports/   # 技能自持的账本与产出（paper-radar 有）
```

只有 `SKILL.md` 是必需的，其余按技能实际需要加。SKILL.md 的 frontmatter：

```markdown
---
name: skill-name
description: 这个技能做什么 + 什么时候该用它
---
```

`description` 决定技能会不会被触发——它是 Claude 唯一拿来跟用户请求做匹配的东西，所以「什么时候用」必须写进去，不能只写「做什么」。

---

## 关于这些技能的取舍

里面的阈值和规则是我按自己踩的坑定的，不是通用最佳实践。

用之前看看是否符合你的场景。结构性的东西（分层门槛、否决规则、账本机制）建议保留，具体数值随意改——改完记得改的是 `SKILL.md`，README 里不复述这类会漂移的细节就是为了这个。

---

## 许可证

MIT License，随便用。

---

## 贡献

欢迎提 issue 或 PR。觉得有用的话给个 ⭐️。
