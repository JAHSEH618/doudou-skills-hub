---
name: init-scale
description: 在原生 /init 之后补齐大型代码库的导航层——搜索面收缩(permissions.deny)、LSP 正确性层、codegraph 发现层(条件安装)、模块分片 CLAUDE.md 与跨仓共性分发、codebase map、折旧基线与新鲜度 hook。只要用户在 monorepo、多模块工程、多仓并排工作区或多语言仓库里抱怨 Claude 定位代码慢、上下文烧得快、grep 噪音大、lint/test 超时,或想"配置一下这个大仓",都应使用本 skill——即使用户没提 init-scale 这个名字。参数 sync = 仅同步跨仓共性标记块。
argument-hint: "[sync | 留空引导式全量]"
---

# init-scale:大仓导航层(引导式)

本 skill 的每一步都动真实环境——装二进制、改共享文件、写 settings。所以采用引导式:**先无声看清现状,一次提问定范围,探索后把要做的一切摊成一张总提案请用户确认,然后连续执行不再打断**。用户的确认成本要一次付清,不能让确认变成十几次打断。

## 不变原则(全程适用)

1. **幂等**:每步先探测现状,已满足就跳过并说明。重跑永远安全——重跑就是断点续跑,没有单独的断点管理。
2. **自动化边界在"出错是否可见"**:出错会报错的(装二进制)直接做;出错静默的(ignore 规则、改共享文件)必须经过提案确认;需要 sudo 的只给命令不动手。
3. 修改已有文件先备份到工作区根 `.claude/init-scale-backup/<日期>/`,以 diff 呈现。
4. 收尾必须输出:写入/修改文件清单 + before/after 对比。

## Phase 0 — 无声体检(不问任何问题)

先探测,后开口。逐项检查并记录状态表:

- 工作区根 CLAUDE.md 存在?其中有 `claude-config-baseline` 块?(有 = 重跑场景)
- `.claude/settings.json` 已有 deny 规则?
- 各语言 LSP:插件启用 + 二进制在 PATH?(探测约束见 [references/lsp.md](references/lsp.md),jdtls 类只能 `which` 不能试运行)
- codegraph:`which codegraph` + 本工作区 `.codegraph/` 存在?
- 模块分片 CLAUDE.md、shared-conventions.md、codebase-map、新鲜度 hook 各自存在?

分支:
- `$ARGUMENTS` = `sync` → 直接执行 [references/sharding.md](references/sharding.md) 的「sync 子流程」,跳过其余全部。
- 根 CLAUDE.md 不存在 → 告知先跑原生 `/init`(本 skill 是增量层),询问是否代跑。
- 全部就绪 → 报告"导航层完整,无事可做",建议到期跑 `/config-audit`,结束。

## Phase 1 — 开场与定范围(第一次提问)

先打印简短 primer(首次用户需要知道这些词是什么):

> 大仓导航层分四件事:**搜索面收缩**(把构建产物/第三方代码排出 Claude 视野)、**LSP**(符号级精确导航,重构安全的判决层)、**codegraph**(可选,架构问答的发现层)、**分片 CLAUDE.md**(每模块自己的说明 + 跨仓共性的统一分发)。

然后展示 Phase 0 状态表(✓ 已就绪 / ✗ 缺失),并用 AskUserQuestion 问(可同轮问两题):

- **Q1 范围**:「补齐全部缺失项(推荐)」/「我逐项挑选」(multiSelect 追问)/「只看提案,先不执行」
- **Q2 探索占比**(仅当 codegraph 未装且规模落在灰区,判定阈值见 [references/codegraph.md](references/codegraph.md)):你的工作里"理解/探索代码"占比高吗?——这是唯一代码里查不到的判定轴,所以才问。

## Phase 2 — 探索(只读,不写任何东西)

并行子代理探索,汇总为提案的原料:

- 基线测量:源文件总数;选一个常见符号记录 grep 命中数(Phase 5 对比用)
- 模块切分:识别边界(workspace 配置 / pom modules / 并排 git 仓),多仓并排工作区显式标记——它改变分发方式
- ignore 候选三来源采集(带证据:文件数/体积/判断依据)
- 语言清单与间接层信号(Feign/RPC 注解、route、多语言桥)

探索面细节与子代理输出契约(JSON schema):[references/exploration.md](references/exploration.md)。已装 codegraph 时子代理先问图再选择性读文件,控制上下文消耗。

## Phase 3 — 总提案(引导式的核心时刻)

把 Phase 0 缺口 × Phase 1 范围 × Phase 2 证据合成**一张分区提案**,以普通文本完整打印,每项一行:动作、证据、目标文件、⚠️ 标记(静默失明类:deny 规则、共享文件改动)。示例形态:

> 这是我准备做的:
> - **[排除]** 12,400 个文件进 deny(target/、node_modules/,证据:构建产物+gitignore 交集)⚠️
> - **[LSP]** 装 jdtls(brew)+ jdtls-lsp 插件 —— Java 无正确性层
> - **[codegraph]** 不装:1,800 文件但无跨服务间接层,收益不足
> - **[分片]** 7 个仓各建 CLAUDE.md;A 类共性 4 条进 master 渲染 ⚠️
> - **[map]** 跳过:目录名自解释
> - **[hook]** 装新鲜度检查(用户级,自 scoping)⚠️

然后**一次** AskUserQuestion:「照这个执行吗?」选项:全部执行 / 去掉部分(multiSelect 追问)/ 只存档方案不执行。不用 preview 字段——提案已在上文可见。

## Phase 4 — 执行(依赖序,边做边验,只在必要处再开口)

顺序:deny → LSP → codegraph → 分片+标记块 → map → baseline+hook。每项:做 → 验证 → 一行结果。执行时按需读取:

| 项 | 读 | 内含 |
|---|---|---|
| 排除 | [references/ignore.md](references/ignore.md) | deny 格式、剔除规则、分组确认、写后验证 |
| LSP | [references/lsp.md](references/lsp.md) | 三层体检、运行时查 marketplace、探测坑、会话边界 |
| codegraph | [references/codegraph.md](references/codegraph.md) | 判定阈值、接线审计(必摘 prompt-hook)、试用期登记、铁律模板 |
| 分片/map | [references/sharding.md](references/sharding.md) | 归并规则、冲突处理、标记块格式、sync、map 两半 |
| 基线/hook | [references/baseline-hook.md](references/baseline-hook.md) | baseline 块格式、hook 脚本模板与安装 |

执行中仅三类情况再开口:后缀被多插件注册要二选一、标记块被手改要裁决、需要 sudo。新装插件本会话认不到不算失败——是会话边界,记入收尾"重启后重跑即从验证续跑"。

## Phase 5 — 收尾

输出四件事:① before/after(文件数、grep vs LSP/图命中);② 文件清单与备份位置;③ 重启才生效的项;④ 待办——各仓 commit 分片文件、codegraph 试用期到期日、下次 /config-audit 时间。
