# 2026-10-22 研究笔记

## 运行上下文
- 06:29 定时 run（d7f1ea0448ec）因工具调用迭代上限在研究阶段截断：arXiv 主窗 783 + 补窗 523 = 1306 篇（2610.24921–2610.28632，全部新于账本最大 2610.23818，零重叠，合并去重）、exa 四线 12×8=96 条（期间修复 scripts/exa_api.py 的 category 字段 bug，重跑验证）、必看博客 37/37 全文读完——均已完成落盘；报告撰写与发布链路未开始。
- 主会话直接复用落盘产物完成报告与发布链路（未重抓）：stats/三图/两账本于 2026-10-22 由主会话补写。

## 来源缺口
- OpenAI 博客：全文 403（Cloudflare 全域不可达），窗口内 10 条全部降级 RSS 摘要（含 Patch the Planet、OpenAI 模型上线 Google Cloud）；证据链记于 candidates.json 的 errors。
- anthropic-engineering feed 解析失败，窗口内 2 篇手动补抓：GRAFT（10-19，上期已覆盖，不重推）、攻击面缩减（10-20）。后者无全文缓存，撰写依据为 web 搜索的第一方核对 + cron 档案；493 / 17,000 / 3,842 / 162 / 94 / 68 / 4500 行 / 16% 各数字逐一对照搜索结果核验。
- 解说线：lookup×3 + exa×3 封顶，结果全为自动聚合站（arxivsignals、papers.cool 等），按硬规则 16 不收；zot.news 的 KV-Surgeon 第三方解读同为聚合站，仅内部记录。
- X 线：x_hot / x_by_account 记于 candidates.json，无符合硬规则 11 条目（flash = 0）。

## 落选池（2）
- System X · arXiv 2610.25456：窗口内，初疑属 harness 论证群，复核为 KV 决策模型，不在本期论证内，不凑数。
- Shopify Sidekick 分工架构（GTC Berlin 演讲转述）：原谈日期早于本期窗口，记入「继续阅读」。
