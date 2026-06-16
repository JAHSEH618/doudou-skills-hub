---
name: viral-ai-blog-writing
description: Use when writing AI tech blog posts that need to go viral on X/Twitter or WeChat. Executes multi-agent workflow with research (8-10 searches + case verification), writing (24 AI patterns avoided), review (content 100 + humanizer-zh 50), and polish (independent agents per round, ≥45 score required). v2.0.
---

# Viral AI Blog Writing

为 X 和微信写出爆火的 AI 技术博文。强制多 agent 协作，从调研到交付全流程质量控制。

## 工作流程

**Phase 1: Research（调研）** - 独立调研 agent
- 8-10 次网络搜索：X 平台特点、微信 AI 检测机制、主题最新案例
- 验证真实案例：必须有明确使用方、项目名、数据
- 输出结构化 insights（JSON schema 强制）

**Phase 2: Writing（撰写）** - 独立写作 agent
- 基于 insights 创作初稿（2500-4000 字）
- 内嵌 24 种 AI 模式规避逻辑
- 标题 12-16 词 + 2.7 秒 hook + 代码示例

**Phase 3: Review（评审）** - 独立评审 agent
- 内容质量评分（100 分制，70 分及格）
- Humanizer-zh 评估（50 分制，45 分及格）
- 24 种 AI 模式逐项检测

**Phase 4: Polish（润色）** - 每轮创建独立润色 agent
- 如果 humanizer-zh <45 分，启动迭代润色
- 每轮创建新的 polish agent（`polish-round-1`, `polish-round-2`...）
- 最多 3 轮，每轮针对具体 AI 模式改写

## 质量门槛

- ✅ 内容质量 ≥70/100
- ✅ Humanizer-zh ≥45/50
- ✅ 24 种 AI 模式检测 + 修复
- ✅ 真实案例验证（无虚构）

## 使用方法

```
请用 viral-ai-blog-writing 撰写关于"${topic}"的博文
```

示例：
```
请用 viral-ai-blog-writing 撰写关于"Claude Code 动态工作流实战"的博文
```

## Humanizer-zh 完整内化

本 workflow 完全内化了 [Humanizer-zh](https://github.com/op7418/Humanizer-zh) 的核心逻辑，无需外部 skill 调用。

### 24 种 AI 写作模式（逐项检测 + 修复）

**内容模式（6 种）**

1. **过度强调意义** - "作为...的证明"、"标志着"、"见证了"、"至关重要的"、"为...奠定基础"
2. **夸大知名度** - 过度列举媒体来源、粉丝数，无实质信息
3. **-ing 式肤浅分析** - "突出/强调...的特点"、"反映/象征...的理念"、"培养/促进..."
4. **宣传式语言** - "充满活力的"、"丰富的"、"令人叹为观止的"、"无缝"、"赋能"、"驱动"
5. **模糊归因** - "专家认为"、"研究表明"（无具体来源）
6. **提纲式结构** - "尽管其...面临若干挑战..."、"挑战与未来展望"

**语言模式（6 种）**

7. **AI 高频词** - 此外、然而、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的
8. **系动词回避** - 用"作为/充当"代替简单的"是"
9. **否定式排比** - "不仅...而且..."、"这不仅仅是...而是..."
10. **三段式过度使用** - 强行分成三组（改为 2 项或 4 项）
11. **刻意换词** - 过度使用同义词避免重复
12. **虚假范围** - "从 X 到 Y"但两者不在有意义尺度上

**风格模式（6 种）**

13. **破折号过度使用** - 频繁使用 — 做戏剧性停顿
14. **粗体过度使用** - 机械地用粗体强调（如 **此外**）
15. **内联标题列表** - 项目符号以粗体标题 + 冒号开头
16. **标题大小写** - 标题中所有主要词大写（中文不适用）
17. **表情符号装饰** - 用表情符号装饰标题和内容
18. **弯引号** - 使用 "" 而非 ""（中文用 「」或 ""）

**交流模式（6 种）**

19. **协作痕迹** - "希望这对您有帮助"、"当然！"、"请告诉我"
20. **知识截止免责** - "截至 [日期]"、"基于可用信息"
21. **谄媚语气** - "好问题！"、"您说得完全正确"
22. **填充短语** - "为了实现这一目标"、"值得注意的是"、"可以看到"
23. **过度限定** - "可以潜在地可能被认为"
24. **通用积极结论** - "未来看起来光明"、"激动人心的时代"

### 5 维度评分（50 分制）

| 维度 | 评分标准 | 满分 |
|------|----------|------|
| **直接性** | 直截了当陈述 vs 绕圈宣告铺垫 | 10 |
| **节奏** | 长短句交错变化 vs 机械重复句式 | 10 |
| **信任度** | 简洁明了表达 vs 过度解释说明 | 10 |
| **真实性** | 自然流畅口语 vs 机械生硬 AI 腔 | 10 |
| **精炼度** | 紧凑有力无赘述 vs 大量冗余废话 | 10 |
| **及格线** | **45 分**（低于 45 分自动润色） | **50** |

### 人性化写作原则（积极做到）

✅ **有观点** - 对技术做判断，不只罗列
- ❌ "这个技术提供了多种功能"
- ✅ "这个技术解决了 X 问题，但 Y 场景下不够"

✅ **变化节奏** - 长短句混合
- 短句制造冲击："问题来了。"
- 长句展开细节："当时系统已经运行了三个月..."

✅ **第一人称** - 适当用"我"、"我们"
- ✅ "我在项目中发现..."
- ❌ "本文将探讨..."

✅ **具体细节** - 用真实数据替代抽象描述
- ❌ "显著提升了性能"
- ✅ "响应时间从 2 秒降到 300ms"

✅ **允许不完美** - 承认局限和复杂性
- ✅ "这个方案在大流量时会有问题"
- ❌ "这个方案完美解决了所有问题"

✅ **口语化** - 像说话一样写
- ✅ "问题来了"、"这很麻烦"
- ❌ "值得注意的是"、"综上所述"

## 2026 爆文写作模式（基于真实调研）

### X 平台特点

**标题公式**
- 12-16 词最佳（CTR 高 37%）
- 包含数字、动词、痛点
- 年份标注："(2026)"、"in 2026"
- 示例："I tested 7 AI coding tools in 2026 — here's what actually works"

**Hook 技巧（2.7 秒规则）**
- 问题先行："你正在为 AI 工具付费 $20/月...每份初稿听起来像机器人"
- 反直觉开场："大多数技术人不想听这个。但事实相反。"
- 成本量化："每年 $40 亿的损失"来自糟糕的技术文档

**内容结构**
1. Hook 开头（2.7 秒内抓住注意力）
2. 问题陈述（具体痛点）
3. 为什么重要（成本 / 影响）
4. 现有局限（承认复杂性）
5. 你的方法（3-5 步骤，每步 <8 词）
6. 实战案例（真实项目 + 数据）
7. 结果影响（转化对比：之前 vs 之后）
8. 行动号召（清晰下一步）

**发布时机**
- 黄金时段：7-9 PM EST
- 2-3 个 trending hashtags
- 认证账号优先

### 微信公众号特点

**2026 年最大挑战：AI 检测限流**
- AI 生成内容被检测后会限流
- 文章阅读量大幅下降
- 需要"降 AI 率"才能避免惩罚

**去 AI 味策略**
- 工作流优化：2 分钟 AI 初稿 + 人工润色
- 双指标管理：查重率 + AIGC 率
- 真实性验证：案例必须有明确来源

**内容偏好**
- 自然表达，口语化
- 有个性，有观点
- 承认局限，不夸大

### 10 种病毒式写作框架

**TIPS** - 提供可执行建议
- 5+ 条具体 tips，每条 <10 词
- 示例："5 tips to debug faster: 1) 先看日志 2) 隔离变量..."

**STATS** - 数据支撑
- 百分比 + 来源 + 年份
- 示例："88% 的营销人员每天使用 AI（2026）"

**STEPS** - 分步指南
- 5 步骤，每步 <8 词
- 示例："如何优化性能：1) 分析瓶颈 2) 缓存热点..."

**LESSONS** - 从失败中学习
- 失败故事 + 3 个 insights
- 示例："我的服务挂了 6 小时。3 个教训：..."

**BENEFITS** - 身份转化
- 行动 → 具体结果
- 示例："每天写测试 → 你变成可信赖的开发者"

**REASONS** - 解释动机
- 3+ 情感化理由
- 示例："3 个理由开始用 TDD：1) 睡得更香..."

**MISTAKES** - 常见错误
- 5 个错误，每个 5 词描述
- 示例："5 个新手错误：1) 跳过单元测试..."

**EXAMPLES** - 真实案例
- 3 个真实例子 + 结果
- ⚠️ **必须验证**：必须有明确使用方、项目名、可查证数据
- ❌ 错误："某创业公司使用后效率提升 300%"（无名称）
- ✅ 正确："Stripe 使用 Claude Code 后 PR review 时间从 4 小时降到 45 分钟（2025 工程博客）"

**QUESTIONS** - 处理疑问
- 5 个问题 + 每个 10 词答案
- 示例："'AI 会取代程序员吗？' 不会，但会改变工作方式。"

**STORIES** - 个人经历
- 100 词故事 + 1 情感 + 1 教训
- 示例："我盯着报错看了 2 小时。沮丧。教训：先休息再 debug。"

### 代码示例要求

✅ **必须做到**
- 可运行（读者能直接复制执行）
- 有注释（解释关键决策）
- 解释 WHY 不只是 HOW（为什么这样设计）
- 来自真实场景（不是教科书示例）

✅ **示例对比**

❌ 错误：
```python
# 处理数据
data = process(input)
result = analyze(data)
```

✅ 正确：
```python
# 为什么用流式处理：数据量可能超过内存（实际遇到过 10GB 日志文件）
def process_stream(file_path):
    for chunk in read_chunks(file_path, size=1024):
        yield parse(chunk)  # 逐块处理，避免 OOM
```

## 实施要求（执行时必须遵守）

### Agent 独立性（NO EXCEPTIONS）

**必须使用独立 agent**

✅ 正确 - 每个阶段独立 agent：
```javascript
// Phase 1: Research agent
const research = await agent(researchPrompt, {
  label: 'research-agent',
  phase: 'Research',
  schema: RESEARCH_SCHEMA
})

// Phase 2: Writing agent
const draft = await agent(writingPrompt, {
  label: 'writing-agent',
  phase: 'Writing'
})

// Phase 3: Review agent
const review = await agent(reviewPrompt, {
  label: 'review-agent',
  phase: 'Review',
  schema: REVIEW_SCHEMA
})

// Phase 4: Polish agents - 每轮创建新 agent
const polished1 = await agent(polishPrompt, {
  label: 'polish-round-1',  // 注意：每轮不同名称
  phase: 'Polish'
})

const polished2 = await agent(polishPrompt, {
  label: 'polish-round-2',  // 第二轮创建新 agent
  phase: 'Polish'
})
```

❌ 错误 - 单 agent 或复用：
```javascript
// ❌ 单个 agent 完成所有工作
const result = await agent("调研、写作、评审一起完成")

// ❌ 调研和写作在同一个 agent
const draft = await agent("先调研再写作")

// ❌ 润色轮次复用同一个 agent
for (let i = 0; i < 3; i++) {
  polished = await agent(polishPrompt, {
    label: 'polish-agent'  // ❌ 名称相同
  })
}
```

### 调研 Agent 要求

**必须网络搜索（8-10 次）**

覆盖领域：
- X 平台特点（2-3 次搜索）
- 微信 AI 检测机制（1-2 次搜索）
- 主题最新进展（3-4 次搜索）
- 真实案例验证（2-3 次搜索）

**真实案例验证标准**

✅ 可以使用：
- 有明确公司 / 项目名称
- 有可查证的数据或来源
- 示例："Stripe 工程博客（2025）提到 PR review 时间从 4 小时降到 45 分钟"

❌ 不可使用：
- "某创业公司"、"一家科技公司"
- "效率提升 300%"（无来源）
- "Sarah from Marketing"（虚构角色）

### Review Agent 要求

**双重评分（都必须通过）**

1. **内容质量（100 分制）**
   - 标题吸引力（10 分）
   - Hook 效果（15 分）
   - 技术深度（20 分）
   - 实战价值（20 分）
   - 代码质量（15 分）
   - 可读性（10 分）
   - 平台适配（10 分）
   - **及格线：70 分**

2. **Humanizer-zh（50 分制）**
   - 直接性（10 分）
   - 节奏（10 分）
   - 信任度（10 分）
   - 真实性（10 分）
   - 精炼度（10 分）
   - **及格线：45 分**

**24 种 AI 模式逐项检测**

Review agent 必须逐项检查 24 种模式，发现的模式记录在 `ai_patterns_found` 数组中。

### Polish Agent 要求

**每轮创建独立 agent**

```javascript
let polishIterations = 0
const MAX_POLISH_ITERATIONS = 3

while (finalScore < 45 && polishIterations < MAX_POLISH_ITERATIONS) {
  polishIterations++
  
  // 每轮创建新的 agent，名称不同
  const polished = await agent(polishPrompt, {
    label: `polish-round-${polishIterations}`,  // ✅ 动态名称
    phase: 'Polish'
  })
  
  // 重新评估
  const evalResult = await agent(reEvalPrompt, {
    label: `eval-round-${polishIterations}`,    // ✅ 评估也用新 agent
    phase: 'Polish'
  })
}
```

**针对性改写**

每轮润色必须：
- 基于 Review 发现的具体 AI 模式
- 针对性改写（不是泛泛润色）
- 重新评估 humanizer-zh 分数

## 输出格式

```json
{
  "article": "完整博文 markdown",
  "metadata": {
    "topic": "主题",
    "workflow_version": "2.0.0",
    "phases_completed": 4,
    "research": {
      "trends_count": 8,
      "cases_count": 4,
      "verified_examples": [
        {
          "name": "Stripe",
          "metric": "PR review time: 4h → 45min",
          "source": "Stripe Engineering Blog 2025"
        }
      ]
    },
    "review": {
      "content_score": 85,
      "humanizer_score": 42,
      "ai_patterns_found": [
        "模式7: AI高频词 - '此外'出现3次",
        "模式9: 否定排比 - '不仅...而且...'",
        "模式13: 破折号过度使用 - 8处"
      ]
    },
    "polish": {
      "initial_score": 42,
      "final_score": 47,
      "iterations": 2,
      "agents_created": [
        "polish-round-1",
        "polish-round-2",
        "eval-round-1",
        "eval-round-2"
      ],
      "passed": true
    },
    "quality_gates": {
      "content_quality": "✅ PASS (85/100)",
      "humanizer_score": "✅ PASS (47/50)",
      "overall": "✅ ALL PASS"
    }
  }
}
```

## 常见错误与红色警报

### ❌ 错误 1：Agent 复用或不独立

**问题**：单个 agent 完成多个阶段，或润色轮次复用同一 agent
```javascript
// ❌ 错误
const result = await agent("调研、写作、评审一起完成")
for (let i = 0; i < 3; i++) {
  polished = await agent(prompt, {label: 'polish-agent'})  // 名称相同
}
```

**正确**：每个阶段独立 agent，润色每轮创建新 agent
```javascript
// ✅ 正确
const research = await agent(researchPrompt, {label: 'research-agent'})
const draft = await agent(writingPrompt, {label: 'writing-agent'})
const review = await agent(reviewPrompt, {label: 'review-agent'})
const polished1 = await agent(polishPrompt, {label: 'polish-round-1'})
const polished2 = await agent(polishPrompt, {label: 'polish-round-2'})
```

### ❌ 错误 2：跳过网络搜索

**问题**："我已经了解主题"直接开始写作
**正确**：调研 agent 必须进行 8-10 次网络搜索，获取 2026 年最新数据

### ❌ 错误 3：使用虚构案例

**问题**：
- "某创业公司使用后效率提升 300%"
- "Sarah from Marketing 说..."
- "一家科技公司的实践"

**正确**：必须有明确名称 + 可查证来源
- "Stripe 工程博客（2025）：PR review 时间从 4 小时降到 45 分钟"
- "Anthropic Claude Code 文档：支持 1M context"

### ❌ 错误 4：忽略评分门槛

**问题**：humanizer-zh 评分 44 分就交付
**正确**：必须 ≥45 分，<45 时自动启动润色迭代

### ❌ 错误 5：泛泛润色

**问题**：润色时只说"改进文本"
**正确**：针对 Review 发现的具体 AI 模式改写
- 发现"模式 7: AI 高频词 - '此外'出现 3 次" → 删除或替换为"同时"、"另外"
- 发现"模式 13: 破折号过度使用" → 减少破折号，改用句号或逗号

### 🚨 Red Flags - 立即停止，重新开始

如果发现以下情况，说明执行有误：

- ❌ 只用一个 agent 完成所有工作
- ❌ 没有进行网络搜索（Research agent）
- ❌ 没有检测 24 种 AI 模式（Review agent）
- ❌ 评分 <45 但不重新润色
- ❌ 写作 agent 同时做评审
- ❌ 跳过调研直接写作
- ❌ 润色轮次 agent 名称相同
- ❌ 案例没有明确名称或来源

## 技术实现细节

**Workflow Tool**
- 使用 `pipeline()` 模式（非 `parallel()`）
- Schema-driven agents（结构化输出）
- 自动迭代润色直到 ≥45 分

**文件位置**
- SKILL.md：用户文档（触发器）
- workflow.js：可执行 workflow
- README.md：开发文档

**版本信息**
- Version: 2.0.0
- Last Updated: 2026-06-16
- Based on: [Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- License: MIT

## 参考资源

**Humanizer-zh**
- GitHub: https://github.com/op7418/Humanizer-zh
- 24 种 AI 写作模式 + 5 维评分系统

**调研来源**
- [AI Technical Blog Writing Best Practices](https://www.eesel.ai/blog/ai-technical-blog-writing)
- [How to Write Authentic Technical Posts](https://aiagentssimplified.substack.com/p/how-to-write-an-authentic-technical)
- [10 Viral Writing Frameworks](https://sifuyik.substack.com/p/10-viral-writing-style)
- [Long-Form AI Blogs Without Slop](https://resources.opencraftai.com/blog/how-to-write-long-form-blogs-with-ai-without-sounding-like-slop-2026-guide/)

**微信 AI 检测**
- [2026 公众号降 AI 率方案](https://www.cnblogs.com/jiangai/p/19710755)
- [微信 AIGC 检测应对策略](https://www.cnblogs.com/jiangai/p/19699362)
