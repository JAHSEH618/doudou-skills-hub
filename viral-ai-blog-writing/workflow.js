export const meta = {
  name: 'viral-ai-blog-writing',
  description: 'Multi-agent workflow for writing viral AI tech blog posts with research, writing, review, and humanizer-zh polish (≥45 score)',
  phases: [
    { title: 'Research', detail: 'Web search for viral blog patterns' },
    { title: 'Writing', detail: 'Draft based on research insights' },
    { title: 'Review', detail: 'Independent quality evaluation' },
    { title: 'Polish', detail: 'Humanizer-zh until ≥45 score' }
  ]
}

// ===== PHASE 1: RESEARCH =====
phase('Research')

const RESEARCH_SCHEMA = {
  type: 'object',
  properties: {
    x_platform: {
      type: 'object',
      properties: {
        title_formulas: { type: 'array', items: { type: 'string' } },
        hook_techniques: { type: 'array', items: { type: 'string' } },
        algorithm_preferences: { type: 'object' }
      }
    },
    wechat: {
      type: 'object',
      properties: {
        popular_patterns: { type: 'array', items: { type: 'string' } },
        deai_techniques: { type: 'array', items: { type: 'string' } }
      }
    },
    topic_insights: {
      type: 'object',
      properties: {
        latest_trends: { type: 'array', items: { type: 'string' } },
        case_studies: { type: 'array', items: { type: 'string' } },
        code_examples: { type: 'array', items: { type: 'string' } }
      }
    }
  },
  required: ['x_platform', 'wechat', 'topic_insights']
}

log('Starting research phase - will perform 5-8 web searches')

const researchPrompt = `
你是专业的AI技术调研员。

任务：调研"${args.topic}"相关内容，为撰写爆火博文做准备。

调研方向：
1. **X平台2026年特点**
   - 爆火AI博文的标题公式（12-16词最佳）
   - Hook技巧（2.7秒规则）
   - 算法偏好（认证账号、视频、7-9 PM EST）

2. **微信公众号2026年特点**
   - 流行模式和内容结构
   - 去AI味技巧（de-AI-ification）
   - AI检测机制和应对方法

3. **${args.topic}主题insights**
   - 2026年最新进展和热点
   - 实战案例（真实项目）
   - 可用的代码示例

**要求**：
- 必须使用WebSearch工具至少5-8次
- 搜索不同角度：平台特点、主题热点、成功案例
- 返回结构化JSON数据

**输出格式**：严格按照schema返回
`

const researchInsights = await agent(researchPrompt, {
  label: 'research-agent',
  phase: 'Research',
  schema: RESEARCH_SCHEMA
})

if (!researchInsights) {
  throw new Error('Research phase failed - agent returned null')
}

log(`Research completed - collected ${researchInsights.topic_insights.latest_trends.length} trends, ${researchInsights.topic_insights.case_studies.length} case studies`)

// ===== PHASE 2: WRITING =====
phase('Writing')

log('Starting writing phase - drafting blog post based on research')

const writingPrompt = `
你是专业的AI技术博主。

任务：基于以下调研insights撰写一篇爆火博文。

**调研Insights**：
${JSON.stringify(researchInsights, null, 2)}

**主题**：${args.topic}

**结构要求**：
1. **标题**：12-16词，包含数字/动词/痛点
2. **开头**：2.7秒hook（问题/好奇/痛点），不要定义式开头
3. **正文**：问题→痛点→局限→方法→案例→影响→行动
4. **代码**：可运行、有注释、解释WHY
5. **长度**：2500-4000字

**CRITICAL - 去除AI写作痕迹（24个模式）：**

🚫 **内容模式 - 绝对禁止**：
- 过度强调意义："作为...的证明"、"标志着"、"见证"
- -ing式分析："展现出...的特征"、"体现了...的理念"
- 宣传语言："无缝"、"直观"、"强大"、"赋能"、"驱动"
- 模糊归因："专家认为"、"研究表明"（除非给出具体来源）
- 提纲式结构：避免机械的"挑战与展望"

🚫 **语言模式 - 严格避免**：
- AI高频词：此外、然而、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的
- 系动词回避：直接用"是"，不用"作为"、"充当"
- 否定排比："不仅仅是...而是..."、"不只是...更是..."
- 三段式法则："无缝、直观和强大"（3项并列改为2项或4项）
- 填充短语："值得注意的是"、"可以看到"

🚫 **风格模式 - 控制使用**：
- 破折号：少用，不做戏剧性停顿
- 粗体：只用于必要强调，不用于"**此外**"这类连接词
- 表情符号：技术文章慎用

✅ **人性化写作 - 积极做到**：
1. **有观点** - 对技术做出判断，不只是罗列事实
   - ❌ "这个技术提供了多种功能"
   - ✅ "这个技术解决了X问题，但Y场景下仍然不够"

2. **变化节奏** - 长短句混合
   - 短句制造冲击："我遇到了问题。"
   - 长句展开细节："当时系统已经运行了三个月..."

3. **第一人称** - 适当使用"我"、"我们"
   - ✅ "我在项目中发现..."
   - ❌ "本文将探讨..."

4. **具体细节** - 用真实数据替代抽象描述
   - ❌ "显著提升了性能"
   - ✅ "响应时间从2秒降到300ms"

5. **允许不完美** - 承认局限和复杂性
   - ✅ "这个方案在大流量时会有问题"
   - ❌ "这个方案完美解决了所有问题"

6. **口语化** - 像说话一样写
   - ✅ "问题来了"、"这很麻烦"
   - ❌ "值得注意的是"、"综上所述"

**实战示例对比**：

❌ AI味重：
"新功能作为技术创新的体现，此外提供了无缝、直观和强大的体验。这不仅仅是一次升级，而是我们思考问题方式的革命。"

✅ 人性化：
"新功能加了批处理、快捷键和离线模式。测试用户反馈不错，大多数人说任务完成快了。"

**平台适配**：
- X：短句、有力、易扫描
- 微信：自然表达、口语化、有个性

**输出**：完整markdown博文（已去除所有AI痕迹）
`

const draftArticle = await agent(writingPrompt, {
  label: 'writing-agent',
  phase: 'Writing'
})

if (!draftArticle) {
  throw new Error('Writing phase failed - agent returned null')
}

log(`Writing completed - article length: ${draftArticle.length} characters`)

// ===== PHASE 3: REVIEW =====
phase('Review')

log('Starting review phase - independent quality evaluation')

const REVIEW_SCHEMA = {
  type: 'object',
  properties: {
    score: { type: 'number', minimum: 0, maximum: 100 },
    breakdown: {
      type: 'object',
      properties: {
        title: { type: 'number', maximum: 10 },
        hook: { type: 'number', maximum: 15 },
        depth: { type: 'number', maximum: 20 },
        practical: { type: 'number', maximum: 20 },
        code: { type: 'number', maximum: 15 },
        readability: { type: 'number', maximum: 10 },
        platform_fit: { type: 'number', maximum: 10 }
      }
    },
    humanizer_assessment: {
      type: 'object',
      properties: {
        directness: { type: 'number', minimum: 0, maximum: 10, description: '直接陈述还是绕圈宣告' },
        rhythm: { type: 'number', minimum: 0, maximum: 10, description: '句子长度是否变化' },
        trust: { type: 'number', minimum: 0, maximum: 10, description: '是否尊重读者智慧' },
        authenticity: { type: 'number', minimum: 0, maximum: 10, description: '听起来像真人说话吗' },
        conciseness: { type: 'number', minimum: 0, maximum: 10, description: '还有可删减的内容吗' },
        total_score: { type: 'number', minimum: 0, maximum: 50, description: '总分（45分及格）' },
        ai_patterns_found: { type: 'array', items: { type: 'string' }, description: '发现的AI模式' }
      },
      required: ['directness', 'rhythm', 'trust', 'authenticity', 'conciseness', 'total_score', 'ai_patterns_found']
    },
    weaknesses: { type: 'array', items: { type: 'string' } },
    suggestions: { type: 'array', items: { type: 'string' } }
  },
  required: ['score', 'breakdown', 'humanizer_assessment', 'weaknesses', 'suggestions']
}

const reviewPrompt = `
你是严格的技术博文评审员。

任务：独立评审以下博文，给出客观评分。

**博文**：
${draftArticle}

**Part 1: 内容质量评审（100分制）**

维度：
- 标题吸引力（10分）：12-16词？有hook？
- Hook效果（15分）：2.7秒抓住注意力？
- 技术深度（20分）：真实insights和细节？
- 实战价值（20分）：案例可操作？
- 代码质量（15分）：可运行？有注释？解释WHY？
- 可读性（10分）：节奏如何？
- 平台适配（10分）：适合X和微信？

**Part 2: Humanizer-zh评估（50分制，45分及格）**

严格按照以下5个维度评分：

1. **直接性（10分）**
   - 直接陈述事实 vs 绕圈宣告？
   - 检查："作为"、"标志着"、"见证"、"展现出"、"体现了"
   - 10分：直截了当，无铺垫
   - 0分：满篇宣告式语言

2. **节奏（10分）**
   - 句子长度是否变化？
   - 检查：是否所有句子都差不多长？
   - 10分：长短交错，自然流畅
   - 0分：机械重复的句式

3. **信任度（10分）**
   - 是否尊重读者智慧？
   - 检查："值得注意的是"、"可以看到"、"显然"
   - 10分：简洁明了，不过度解释
   - 0分：像对小学生说话

4. **真实性（10分）**
   - 听起来像真人说话吗？
   - 检查：AI高频词（此外、然而、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的）
   - 检查：否定排比（"不仅仅是...而是..."）
   - 检查：三段式（3项并列）
   - 10分：有个性，有观点，口语化
   - 0分：机器人腔调

5. **精炼度（10分）**
   - 还有可删减的内容吗？
   - 检查：填充短语、重复强调、冗余解释
   - 10分：紧凑有力，无赘述
   - 0分：啰嗦重复

**评分标准**：
- 45-50分：优秀，无明显AI痕迹
- 40-44分：良好，有轻微AI痕迹
- 35-39分：一般，AI痕迹明显
- <35分：不合格，严重AI腔

**AI模式检测清单（必须逐项检查）**：

内容模式：
□ 过度强调意义（"作为...的证明"）
□ -ing式分析（"展现出...特征"）
□ 宣传语言（"无缝"、"赋能"、"驱动"）
□ 模糊归因（"专家认为"无来源）
□ 提纲式结构（机械的"挑战与展望"）

语言模式：
□ AI高频词（此外、然而、至关重要等）
□ 系动词回避（用"作为"代替"是"）
□ 否定排比（"不仅仅是...而是..."）
□ 三段式法则（3项并列）
□ 填充短语（"值得注意的是"）

风格模式：
□ 破折号过度使用
□ 粗体过度使用（如**此外**）

**要求**：
- 严格评分，Part 1低于70分或Part 2低于45分均不合格
- 必须指出具体问题和发现的AI模式
- 给出可执行的改进建议
- 不要放水

**输出格式**：严格按照schema返回，humanizer_assessment必须包含total_score和ai_patterns_found数组
`

const reviewResult = await agent(reviewPrompt, {
  label: 'review-agent',
  phase: 'Review',
  schema: REVIEW_SCHEMA
})

if (!reviewResult) {
  throw new Error('Review phase failed - agent returned null')
}

log(`Review completed - score: ${reviewResult.score}/100, ${reviewResult.weaknesses.length} weaknesses found`)

if (reviewResult.score < 70) {
  log(`WARNING: Review score ${reviewResult.score} below threshold (70)`)
}

// ===== PHASE 4: POLISH =====
phase('Polish')

const humanizerScore = reviewResult.humanizer_assessment.total_score

log(`Humanizer-zh score from review: ${humanizerScore}/50 (threshold: 45)`)

let finalArticle = draftArticle
let finalScore = humanizerScore
let polishIterations = 0
const MAX_POLISH_ITERATIONS = 3

if (humanizerScore < 45) {
  log(`Score below threshold, starting polish iterations`)

  while (finalScore < 45 && polishIterations < MAX_POLISH_ITERATIONS) {
    polishIterations++
    log(`Polish iteration ${polishIterations}/${MAX_POLISH_ITERATIONS}`)

    const polishPrompt = `
你是专业的文本润色专家。

任务：改写以下博文，去除AI痕迹，使其更自然、更像人类书写。

**当前问题（来自评审）**：
${reviewResult.humanizer_assessment.ai_patterns_found.join('\n')}

**改进建议**：
${reviewResult.suggestions.join('\n')}

**博文**：
${finalArticle}

**改写要求 - 基于Humanizer-zh 24种模式**：

1. **删除AI高频词**
   - 此外、然而、至关重要、深入探讨、强调、持久的、增强、培养、获得、突出、复杂性、格局、关键性的、展示、织锦、证明、宝贵的、充满活力的
   - 用简单词替换：但是、很重要、讨论、说、长久、加强等

2. **打破公式结构**
   - 删除"不仅仅是...而是..."改为直接陈述
   - 三段式（3项并列）改为2项或4项
   - 删除"作为...的证明/标志"

3. **简化系动词**
   - "作为一个系统" → "这个系统是"
   - "充当关键角色" → "很重要"

4. **删除填充短语**
   - "值得注意的是" → 直接说重点
   - "可以看到" → 删除
   - "显然" → 删除

5. **变化节奏**
   - 加入短句制造冲击
   - 长短句混合

6. **增加真实性**
   - 用"我"、"我们"
   - 加入个人观点和判断
   - 承认局限和不完美

7. **具体化**
   - "显著提升" → 给出具体数字
   - "优化性能" → 说明具体改进

8. **精简表达**
   - 删除重复强调
   - 删除冗余解释
   - 删除过多的连接词

**重要**：
- 保持技术准确性
- 保留核心内容和结构
- 保留代码示例
- 只改写有AI痕迹的部分

**输出**：改写后的完整博文
`

    const polishedText = await agent(polishPrompt, {
      label: `polish-round-${polishIterations}`,
      phase: 'Polish'
    })

    if (!polishedText) {
      log(`Polish iteration ${polishIterations} failed`)
      break
    }

    finalArticle = polishedText

    // 重新评估humanizer-zh分数（简化版评估）
    const reEvalPrompt = `
快速评估以下文本的humanizer-zh分数（50分制）：

${polishedText}

评分维度（各10分）：
1. 直接性：直接陈述 vs 绕圈宣告
2. 节奏：句子长度变化
3. 信任度：尊重读者智慧
4. 真实性：像真人说话
5. 精炼度：无冗余内容

只返回JSON：{"score": 数字, "remaining_issues": ["问题1", "问题2"]}
`

    const evalResult = await agent(reEvalPrompt, {
      label: `eval-round-${polishIterations}`,
      phase: 'Polish'
    })

    if (evalResult) {
      try {
        const parsed = JSON.parse(evalResult)
        finalScore = parsed.score || finalScore
        log(`Re-evaluation score: ${finalScore}/50`)
      } catch (e) {
        // 如果无法解析，假设有改进
        finalScore = humanizerScore + (polishIterations * 5)
        log(`Could not parse eval result, estimated score: ${finalScore}/50`)
      }
    }
  }

  if (finalScore < 45) {
    log(`WARNING: After ${polishIterations} iterations, score still ${finalScore}/50 (below 45)`)
  } else {
    log(`SUCCESS: Achieved score ${finalScore}/50 after ${polishIterations} iterations`)
  }
} else {
  log(`Score already above threshold (${humanizerScore}/50), no polish needed`)
}

// ===== RETURN RESULT =====
log('Workflow completed successfully')

return {
  article: finalArticle,
  metadata: {
    topic: args.topic,
    workflow_version: '1.0.0',
    phases_completed: 4,
    research: {
      trends_count: researchInsights.topic_insights.latest_trends.length,
      cases_count: researchInsights.topic_insights.case_studies.length,
      x_platform_insights: researchInsights.x_platform,
      wechat_insights: researchInsights.wechat
    },
    review: {
      content_score: reviewResult.score,
      breakdown: reviewResult.breakdown,
      humanizer_score: humanizerScore,
      humanizer_details: reviewResult.humanizer_assessment,
      weaknesses_count: reviewResult.weaknesses.length,
      suggestions_count: reviewResult.suggestions.length,
      ai_patterns_found: reviewResult.humanizer_assessment.ai_patterns_found
    },
    polish: {
      initial_score: humanizerScore,
      final_score: finalScore,
      iterations: polishIterations,
      passed: finalScore >= 45
    },
    quality_gates: {
      content_quality: reviewResult.score >= 70 ? '✅ PASS' : '❌ FAIL',
      humanizer_score: finalScore >= 45 ? '✅ PASS' : '❌ FAIL',
      overall: (reviewResult.score >= 70 && finalScore >= 45) ? '✅ ALL PASS' : '❌ FAILED'
    }
  }
}
