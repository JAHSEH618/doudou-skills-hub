# 发布：GitHub + GitHub Pages

2026-09-28 起，用户将发布方式改为 GitHub + GitHub Pages。仓库工作区只是生成、查重与提交的工作副本；不再复制到桌面或 iCloud Obsidian vault，也不维护两处本地索引。

## 位置

- 仓库：https://github.com/JAHSEH618/doudou-skills-hub
- 阅读站：https://jahseh618.github.io/doudou-skills-hub/
- 用户口头的「gitbook」指本站，与 dankoe 翻译站共用此称呼——按内容消歧：雷达报告进这里，译文文章进 dankoe-zh 仓库。
- 源报告：`paper-radar/reports/YYYY-MM-DD.md`；同日多模式用有意义的后缀。
- 资源：`paper-radar/reports/assets/<日期或同名后缀>/`，相对链接保持一致。
- 账本：`paper-radar/state/seen-papers.md` 与 `judgments.md`。

## 一次发布

1. 写报告、图表、统计并更新两个账本；只提交与本次雷达相关的改动，保留其他在途工作。
2. 先运行 `python3 paper-radar/scripts/audit_links.py`，复核目标标题、X 原帖与受限项，并更新仓库审计记录。再安装依赖：`python3 -m pip install -r paper-radar/site/requirements.txt`。运行 `python3 paper-radar/scripts/build_site.py` 和 `python3 paper-radar/scripts/check_site.py _site`；生成目录 `_site/` 不入库。
3. 审查提交，确认没有密钥、私人资料或未经许可转载的全文。候选审计只保留必要来源元数据。
4. 按用户已授权的发布范围提交并推送；仓库要求 PR 时走 PR，不绕过保护规则。PR 说明写清最终行为及验证。
5. 默认分支 `master` 的报告变化触发 `.github/workflows/paper-radar-pages.yml`；PR 只构建检查，默认分支才发布。
6. 等待工作流成功，打开本期网页并检查图表。正文和图表都在线可读才算发布成功。失败时给 GitHub 原文链接并说明 Pages 状态，不能把已推送说成已上线。
7. 对话给本期网页、历史索引和 GitHub 原文链接，加一句论文/实践/资讯体量，不贴全文。

**定时运行的预算纪律**：commit/push/Actions 验证是迭代预算耗尽时最先被挤掉的步骤。仓库同步完成后**立即** commit + push，把剩余迭代留给 Actions 验证与页面检查；定时任务提示词里已固定提交身份（`user.name`/`user.email`），不要花迭代跑 `git log` 看提交风格。若一次运行死在了推送之前，按其最终响应里列出的「未完成」清单补完剩余步骤后自行验证外部状态（Actions success、页面 200）再汇报。

## 发布坑（2026-10-20 实测）

- 账本（judgments.md / seen-papers.md）条目里**禁止用非 URL 的 markdown 链接**，如 `[SDCs in the Wild](OSDI '26，独立印证：…)`——构建器会把括号内容当相对路径生成 `<a href>`，check_site.py 必报 `missing`。无 URL 的旁证用纯文本：`OSDI '26《SDCs in the Wild》（独立印证：…）`。
- cron 跑死在推送之前时：主会话可直接复用磁盘产物收尾，不重跑后台（研究产物都在 `reports/assets/<日期>/`）。收尾顺序：写报告 → 更新两个账本 → 同步 `reports/` + `state/` 到 doudou-skills-hub 仓库工作区 → `render_charts.py <assets目录>` → `audit_links.py` → `build_site.py` + `check_site.py _site` → commit + push（作者身份 `了可以 <60974244+JAHSEH618@users.noreply.github.com>`，与往期一致）→ 等 Actions success + 页面与 SVG 资源 200 再汇报。

## 站点和元数据

静态 HTML 从 Markdown 构建，无浏览器 JavaScript 依赖；索引自动扫描 reports 和 stats.json。文章保留目录与来源标注，支持手机、深色主题和打印。只发布报告目录及两个账本，不复制技能库其他模块。

每次构建需有 `site/link-audit.json`，检查记录只随仓库提交，不输出到阅读站。完整研究笔记存于 `reports/assets/<日期>/research-notes.md`，构建时同样排除。新报告的 YAML frontmatter 保留 description、supplement_blogs、supplement_x，以及 type、title、mode、window、paper_count、practice_count（详）、practice_abstract_count、news_count、created、updated、tags；旧报告无 frontmatter 也可构建。

不再扫描桌面 PDF 库或新增本机 PDF 路径，历史报告原有文本保留。
