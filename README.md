# Skills 技能库

我的个人工作沉淀，把实际干活时摸索出来的套路固化成可复用的技能。

## 为什么写这个

招人时筛简历是件烦人的事。看多了就会发现模式：哪些信号靠谱，哪些是灌水，什么人能真正干活。但每次筛选都要重新想一遍这套逻辑，很容易因为手感不同漏掉关键点。

所以我把这套标准写死了。从严版意味着我宁可错过一些人，也不想招错。门槛定得比市面上高——AI coding 工具实证、SDD/TDD 工程化，这两项必须有。Agent 应用真实落地是最高加分项。

这个仓库就是干这个用的。

## 目前有什么

### ai-backend-resume-screening

简历筛选用的。专门针对 AI 后端开发这个岗位，标准比一般的高。

**筛什么：**
- 必须会用 Cursor/Claude Code/Codex 这类专业编程工具写代码（不是 ChatGPT 网页版）
- 必须用过 SDD/TDD 工程化工具（OpenSpec、Superpowers 之类）
- Agent 应用真实落地是最高加分（+10 分），但只认生产环境和真实用户，Demo 不算

**硬门槛：**
- 工龄 ≤10 年（超了直接淘汰）
- 本科及以上（专科淘汰）
- 年龄 ≤30（大厂或强 AI 落地经历可以放宽到 35）

**输出：**
- 通过者按项目经验评级：初级开发/中级/高级
- 格式：`dir-name-score-等级`

**AI 灌水识别：**
用 humanizer-zh 检测简历真实性。关键是区分「用 AI 润色」和「用 AI 编造经历」——前者没问题，后者扣 12 分。风险分级：🟢低 / 🟡中 / 🔴高。

**去重：**
本地 `checked.md` 记录筛过的简历，批量时自动跳过。

详细文档：[ai-backend-resume-screening/SKILL.md](ai-backend-resume-screening/SKILL.md)

## 怎么用

克隆到 Claude Code 的技能目录：

```bash
git clone https://github.com/JAHSEH618/doudou-skills-hub.git ~/.claude/skills
```

然后在 Claude Code 里直接说任务，技能会自动触发。也可以明确调用：

```bash
# 单份简历
请筛选这份简历：[附上内容或路径]

# 批量筛选
请筛选 ./AI开发-0615/ 目录下的所有简历

# 生成评分表
请为 AI 后端开发岗位生成评分表
```

单个技能也可以单独装：

```bash
cp -r ai-backend-resume-screening ~/.claude/skills/
```

## 技能目录结构

```
skill-name/
├── SKILL.md              # 技能主文档
├── references/           # 参考文档（具体标准、判定逻辑）
└── assets/               # 资源文件（模板、工具）
```

SKILL.md 开头要有 frontmatter：

```markdown
---
name: skill-name
description: 什么时候用这个技能
---
```

## 关于标准

这些技能里的标准是我自己定的，基于实际踩过的坑。用之前最好看看是不是符合你的场景，阈值可以自己调。

核心逻辑（分层门槛、否决规则）建议保持，具体分值和放宽条件可以改。

MIT License，随便用。
