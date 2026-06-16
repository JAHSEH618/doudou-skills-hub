# Viral AI Blog Writing

为 X 和微信写出爆火的 AI 技术博文。强制多 agent 协作 workflow。

## 特点

- ✅ **强制多 agent**（Research → Writing → Review → Polish），每轮独立
- ✅ **8-10 次网络搜索**，收集 2026 年最新爆文模式 + 真实案例验证
- ✅ **完全内化 [Humanizer-zh](https://github.com/op7418/Humanizer-zh)**（24 种模式 + 5 维评分）
- ✅ **双重验证**（内容 ≥70 分 + Humanizer-zh ≥45 分）
- ✅ **独立 polish agents**（每轮创建新 agent，最多 3 轮）
- ✅ **无虚构案例**（所有案例必须有明确名称 + 来源）

## 快速开始

```bash
请用 viral-ai-blog-writing 撰写关于"Claude Code 动态工作流实战"的博文
```

## Workflow 执行流程

```
Phase 1: Research (调研)          ~5 分钟
├─ 8-10 次网络搜索
├─ X 平台 2026 特点（标题公式、Hook 技巧）
├─ 微信 AI 检测机制（限流惩罚、降 AI 率策略）
├─ 主题最新进展和热点
└─ 真实案例验证（必须有名称 + 数据 + 来源）

Phase 2: Writing (写作)           ~5 分钟
├─ 基于 research insights
├─ 内嵌 24 种 AI 模式规避逻辑
├─ 标题 12-16 词 + 2.7 秒 hook
├─ 2500-4000 字，含代码示例
└─ 只使用 verified_cases（无虚构）

Phase 3: Review (评审)            ~3 分钟
├─ 内容质量评分（100 分制，70 分及格）
├─ Humanizer-zh 评估（50 分制，45 分及格）
├─ 24 种 AI 模式逐项检测
└─ 具体改进建议

Phase 4: Polish (润色)            ~5-10 分钟
├─ 如果 humanizer-zh <45 分
├─ 每轮创建独立 polish agent（polish-round-1, polish-round-2...）
├─ 每轮创建独立 eval agent（eval-round-1, eval-round-2...）
└─ 最多 3 轮，针对具体 AI 模式改写
```

总耗时 15-25 分钟。

## Humanizer-zh 完整内化

基于 https://github.com/op7418/Humanizer-zh

### 24 种 AI 写作模式检测

**内容模式（6 种）**：过度强调意义、夸大知名度、-ing 式分析、宣传语言、模糊归因、提纲式结构

**语言模式（6 种）**：AI 高频词（此外、然而、至关重要等）、系动词回避、否定排比、三段式法则、刻意换词、虚假范围

**风格模式（6 种）**：破折号 / 粗体过度使用、内联标题列表、标题大小写、表情符号装饰、弯引号

**交流模式（6 种）**：协作痕迹、知识截止免责、谄媚语气、填充短语、过度限定、通用积极结论

### 5 维度评分（50 分制，45 分及格）

| 维度 | 说明 |
|------|------|
| 直接性（10 分） | 直接陈述事实，无绕圈宣告 |
| 节奏（10 分） | 句子长度变化，长短交错 |
| 信任度（10 分） | 尊重读者智慧，不过度解释 |
| 真实性（10 分） | 像真人说话，有个性观点 |
| 精炼度（10 分） | 紧凑有力，无冗余赘述 |

## 2026 爆文写作模式（基于真实调研）

**X 平台特点**
- 标题 12-16 词（CTR 高 37%）+ 年份标注 "(2026)"
- Hook 2.7 秒规则（问题先行 / 反直觉 / 成本量化）
- 内容结构：Hook → 问题 → 为什么重要 → 局限 → 方法（3-5 步，每步 <8 词）→ 案例 → 结果 → 行动
- 发布时机：7-9 PM EST，2-3 个 trending hashtags

**微信公众号特点**
- **最大挑战**：AI 检测限流（AIGC 率检测）
- **策略**：降 AI 率、双指标管理（查重 + AIGC）
- **内容偏好**：自然表达、有个性、承认局限

**10 种病毒式写作框架**
- TIPS, STATS, STEPS, LESSONS, BENEFITS, REASONS, MISTAKES, EXAMPLES, QUESTIONS, STORIES

## 输出示例

```json
{
  "article": "完整博文 markdown",
  "metadata": {
    "workflow_version": "2.0.0",
    "quality_gates": {
      "content_quality": "✅ PASS (85/100)",
      "humanizer_score": "✅ PASS (47/50)",
      "overall": "✅ ALL PASS"
    },
    "research": {
      "search_count": 9,
      "verified_cases": [
        {
          "name": "Stripe",
          "metric": "PR review: 4h → 45min",
          "source": "Stripe Engineering Blog 2025"
        }
      ]
    },
    "polish": {
      "iterations": 2,
      "agents_created": ["polish-round-1", "polish-round-2", "eval-round-1", "eval-round-2"],
      "initial_score": 42,
      "final_score": 47
    },
    "agents_created": ["research-agent", "writing-agent", "review-agent", "polish-round-1", "polish-round-2", "eval-round-1", "eval-round-2"]
  }
}
```

## 文件结构

```
viral-ai-blog-writing/
├── README.md         # 本文档
├── SKILL.md          # 用户文档（触发器 + 完整实施指南）
└── workflow.js       # 可执行 workflow
```

## 技术实现

- **Workflow tool** - 强制执行 pipeline
- **Schema-driven agents** - 结构化输出（JSON）
- **内化 humanizer-zh** - 不依赖外部 skill 调用
- **独立 polish agents** - 每轮创建新 agent（动态名称）
- **自动迭代** - 评分 <45 分自动润色

## 核心改进（v2.0）

### 相比 v1.0 的提升

1. **调研深度**：5-8 次搜索 → 8-10 次搜索
2. **案例验证**：允许模糊案例 → 强制真实案例验证（名称 + 数据 + 来源）
3. **Agent 独立性**：可能复用 → 强制每轮创建新 agent
4. **Humanizer-zh**：部分内化 → 完全内化 24 种模式
5. **行文优化**：基于真实调研（eesel AI、AI Agents Simplified、Opencraft AI 等）

### 基于的调研来源

- [AI Technical Blog Writing Best Practices](https://www.eesel.ai/blog/ai-technical-blog-writing)
- [How to Write Authentic Technical Posts](https://aiagentssimplified.substack.com/p/how-to-write-an-authentic-technical)
- [10 Viral Writing Frameworks](https://sifuyik.substack.com/p/10-viral-writing-style)
- [Long-Form AI Blogs Without Slop](https://resources.opencraftai.com/blog/how-to-write-long-form-blogs-with-ai-without-sounding-like-slop-2026-guide/)
- [微信 2026 公众号降 AI 率方案](https://www.cnblogs.com/jiangai/p/19710755)

## 适用场景

✅ **适合**：
- AI 技术深度博文
- X 和微信平台
- 需要去 AI 味
- 实战案例 + 代码

❌ **不适合**：
- 快速短文（overhead 大）
- 非技术内容
- 不在乎 AI 痕迹

## 版本信息

- **Version**: 2.0.0
- **Date**: 2026-06-16
- **Based on**: [Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- **License**: MIT

## 贡献

欢迎提 issue 或 PR。

特别感谢：
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh) - 核心去 AI 味逻辑
- [blader/humanizer](https://github.com/blader/humanizer) - 原始英文版本
- Superpowers - TDD 方法论
- 2026 年优秀 AI 技术博文调研来源
