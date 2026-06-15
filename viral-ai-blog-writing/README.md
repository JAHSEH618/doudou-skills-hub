# Viral AI Blog Writing

写爆火AI技术博文的多agent workflow。

## 特点

- 强制多agent（Research → Writing → Review → Polish），无法跳过
- 5-8次网络搜索，收集2026年爆文模式
- 完全内化[Humanizer-zh](https://github.com/op7418/Humanizer-zh)（24种模式 + 5维评分）
- 双重验证（内容≥70分 + Humanizer-zh≥45分）
- 自动迭代润色（最多3轮）

## 快速开始

```bash
请用 viral-ai-blog-writing 撰写关于"AI Agent在代码审查中的应用"的博文
```

## Workflow执行流程

```
Phase 1: Research (调研)          ~5分钟
├─ 5-8次网络搜索
├─ X平台2026爆文特点
├─ 微信公众号流行模式
└─ 主题最新进展和案例

Phase 2: Writing (写作)           ~5分钟
├─ 基于research insights
├─ 内嵌humanizer-zh 24种模式规避
├─ 标题12-16词 + 2.7秒hook
└─ 2500-4000字，含代码示例

Phase 3: Review (评审)            ~3分钟
├─ 内容质量评分（100分制）
├─ Humanizer-zh评估（50分制）
├─ 24种AI模式检测
└─ 具体改进建议

Phase 4: Polish (润色)            ~5-10分钟
├─ 如果humanizer-zh <45分
├─ 迭代润色（最多3轮）
└─ 直到≥45分或达到最大轮数
```

总耗时 15-25 分钟。

## Humanizer-zh内化

基于 https://github.com/op7418/Humanizer-zh

### 24种AI写作模式检测

**内容模式**：过度强调意义、-ing式分析、宣传语言、模糊归因

**语言模式**：AI高频词（此外、然而、至关重要等）、系动词回避、否定排比、三段式法则

**风格模式**：破折号/粗体过度使用

### 5维度评分（50分制，45分及格）

| 维度 | 说明 |
|------|------|
| 直接性（10分） | 直接陈述事实，无绕圈宣告 |
| 节奏（10分） | 句子长度变化，长短交错 |
| 信任度（10分） | 尊重读者智慧，不过度解释 |
| 真实性（10分） | 像真人说话，有个性观点 |
| 精炼度（10分） | 紧凑有力，无冗余赘述 |

## 输出示例

```json
{
  "article": "完整博文markdown",
  "metadata": {
    "quality_gates": {
      "content_quality": "✅ PASS (85/100)",
      "humanizer_score": "✅ PASS (47/50)",
      "overall": "✅ ALL PASS"
    },
    "polish": {
      "iterations": 2,
      "initial_score": 42,
      "final_score": 47
    },
    "review": {
      "ai_patterns_found": ["检测到的具体AI模式"]
    }
  }
}
```

## 文件结构

```
viral-ai-blog-writing/
├── README.md         # 本文档
├── SKILL.md          # 用户文档（触发器）
└── workflow.js       # 可执行workflow
```

## 技术实现

- Workflow tool - 强制执行pipeline
- Schema-driven agents - 结构化输出
- 内化humanizer-zh - 不依赖外部skill调用
- 自动迭代 - 评分<45分自动润色

## 开发过程

基于TDD方法论（RED-GREEN-REFACTOR）：

1. RED阶段 - Baseline测试，发现agent会忽略文档skill
2. GREEN阶段 - 创建可执行workflow
3. REFACTOR阶段 - 内化humanizer-zh，完善评分机制

开发文档在本地 `.skill-development/` 目录（不上传git）。

## 适用场景

适合：
- AI技术深度博文
- X和微信平台
- 需要去AI味
- 实战案例 + 代码

不适合：
- 快速短文（overhead大）
- 非技术内容
- 不在乎AI痕迹

## 版本信息

- Version: 1.0.0
- Date: 2026-06-15
- Based on: [Humanizer-zh](https://github.com/op7418/Humanizer-zh)
- License: MIT

## 贡献

欢迎提issue或PR。

特别感谢：
- [Humanizer-zh](https://github.com/op7418/Humanizer-zh) - 核心去AI味逻辑
- Superpowers - TDD方法论
