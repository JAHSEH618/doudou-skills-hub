# Skills 技能库

这是一个用于 Claude Code CLI 的自定义技能（Skills）仓库，包含专业领域的结构化工作流和评估框架。

## 📋 目录

- [什么是 Skills](#什么是-skills)
- [已收录技能](#已收录技能)
- [安装与使用](#安装与使用)
- [技能结构](#技能结构)
- [贡献指南](#贡献指南)

## 什么是 Skills

Skills 是 Claude Code 的可复用工作流程模块，用于：

- **标准化专业评估流程**：将复杂的多步骤判定逻辑固化为可执行的框架
- **提高工作一致性**：确保每次评估使用相同的标准和方法论
- **加速重复任务**：通过预定义的检查清单和判定规则，快速完成常见任务
- **知识沉淀与复用**：将领域专家的经验转化为可传承的结构化文档

## 已收录技能

### 🎯 ai-backend-resume-screening

**AI 后端开发工程师简历筛选（从严版）**

用于筛选「AI 后端开发工程师」岗位的简历与候选人评估。提供分层筛选标准，区分「进化型 AI 编程开发」和「传统手写搬砖」候选人。

**核心特性：**

- **分层门槛体系**
  - 硬门槛：工龄 ≤10 年、学历本科及以上、年龄 ≤30
  - 必过能力门槛：AI coding 工具实证（Cursor/Claude Code/Codex）、SDD/TDD 工程化
  - 优先加分项：Agent 应用真实落地（最高 +10 分）、金融/电商经验、AI 全栈能力

- **等级评定**
  - 通过者评定为：初级开发 / 中级 / 高级
  - 输出格式：`dir-name-score-等级`

- **AI 灌水核验**
  - 基于 `humanizer-zh` 检测简历真实性
  - 区分「AI 润色」与「AI 编造经历」
  - 风险分级：🟢低 / 🟡中 / 🔴高

- **去重机制**
  - 本地 `checked.md` 记录已筛简历
  - 批量/跨批次自动去重，避免重复推送

**适用场景：**

- 简历初筛、候选人打分
- 等级评定、面试预判
- 制作评分表/评分卡
- 简历真实性核验

**详细文档：** [ai-backend-resume-screening/SKILL.md](ai-backend-resume-screening/SKILL.md)

## 安装与使用

### 方式一：本地安装（推荐）

1. 克隆本仓库到本地：

```bash
git clone https://github.com/your-username/skills.git ~/.claude/skills
```

2. 在 Claude Code CLI 中使用技能：

```bash
claude
# 在对话中直接描述任务，相关技能会自动触发
# 或者明确调用：/skill ai-backend-resume-screening
```

### 方式二：单个技能安装

将特定技能目录复制到 Claude Code 的技能目录：

```bash
cp -r ai-backend-resume-screening ~/.claude/skills/
```

### 使用示例

**简历筛选：**

```
# 单份简历评估
请筛选这份简历：[附上简历内容或路径]

# 批量筛选
请筛选 ./AI开发-0615/ 目录下的所有简历

# 生成评分表
请为 AI 后端开发岗位生成一份可交互的评分表
```

## 技能结构

每个技能遵循标准目录结构：

```
skill-name/
├── SKILL.md              # 技能主文档（包含 frontmatter 和使用说明）
├── references/           # 参考文档目录
│   ├── screening-criteria.md    # 筛选标准
│   └── ai-writing-integrity-check.md  # AI 写作真实性检测
└── assets/               # 资源文件目录
    └── scoring-rubric.html      # 评分表模板
```

**SKILL.md frontmatter 格式：**

```markdown
---
name: skill-name
description: 技能简短描述，说明核心功能和触发场景
---
```

## 贡献指南

欢迎贡献新技能或改进现有技能！

### 贡献流程

1. Fork 本仓库
2. 创建特性分支：`git checkout -b feature/new-skill`
3. 按照[技能结构](#技能结构)组织文件
4. 确保 SKILL.md 包含完整的 frontmatter 和使用说明
5. 提交变更：`git commit -am 'Add: 新技能名称'`
6. 推送分支：`git push origin feature/new-skill`
7. 提交 Pull Request

### 技能编写规范

1. **明确触发场景**：在 description 中清晰说明何时使用该技能
2. **结构化判定逻辑**：将复杂流程拆解为可执行的步骤
3. **提供参考文档**：将详细标准放在 `references/` 目录
4. **输出格式标准化**：定义清晰的输出格式，便于后续处理
5. **中文优先**：技能文档和输出使用中文

## 许可证

MIT License

## 联系方式

- Issues: [提交问题或建议](https://github.com/your-username/skills/issues)
- Discussions: [参与讨论](https://github.com/your-username/skills/discussions)

---

**注意：** 本仓库中的技能基于特定业务场景设计，使用前请根据实际需求调整标准和阈值。
