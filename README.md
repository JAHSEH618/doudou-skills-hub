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
