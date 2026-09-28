# 发布：GitHub + GitHub Pages

2026-09-28 起，用户将发布方式改为 GitHub + GitHub Pages。仓库工作区只是生成、查重与提交的工作副本；不再复制到桌面或 iCloud Obsidian vault，也不维护两处本地索引。

## 位置

- 仓库：https://github.com/JAHSEH618/doudou-skills-hub
- 阅读站：https://jahseh618.github.io/doudou-skills-hub/
- 源报告：`paper-radar/reports/YYYY-MM-DD.md`；同日多模式用有意义的后缀。
- 资源：`paper-radar/reports/assets/<日期或同名后缀>/`，相对链接保持一致。
- 账本：`paper-radar/state/seen-papers.md` 与 `judgments.md`。

## 一次发布

1. 写报告、图表、统计并更新两个账本；只提交与本次雷达相关的改动，保留其他在途工作。
2. 安装依赖：`python3 -m pip install -r paper-radar/site/requirements.txt`。运行 `python3 paper-radar/scripts/build_site.py` 和 `python3 paper-radar/scripts/check_site.py _site`；生成目录 `_site/` 不入库。
3. 审查提交，确认没有密钥、私人资料或未经许可转载的全文。候选审计只保留必要来源元数据。
4. 按用户已授权的发布范围提交并推送；仓库要求 PR 时走 PR，不绕过保护规则。PR 说明写清最终行为及验证。
5. 默认分支 `master` 的报告变化触发 `.github/workflows/paper-radar-pages.yml`；PR 只构建检查，默认分支才发布。
6. 等待工作流成功，打开本期网页并检查图表。正文和图表都在线可读才算发布成功。失败时给 GitHub 原文链接并说明 Pages 状态，不能把已推送说成已上线。
7. 对话给本期网页、历史索引和 GitHub 原文链接，加一句论文/实践/资讯体量，不贴全文。

## 站点和元数据

静态 HTML 从 Markdown 构建，无浏览器 JavaScript 依赖；索引自动扫描 reports 和 stats.json。文章保留目录与来源标注，支持手机、深色主题和打印。只发布报告目录及两个账本，不复制技能库其他模块。

新报告建议 YAML frontmatter 保留 type、title、mode、window、paper_count、practice_count（详）、practice_abstract_count、news_count、created、updated、tags；旧报告无 frontmatter 也可构建。

不再扫描桌面 PDF 库或新增本机 PDF 路径，历史报告原有文本保留。
