# 折旧基线与新鲜度 hook

## 为什么需要 baseline

配置是折旧资产:为绕过当前模型/工具限制写的规则,会随模型变强从拐杖变成手铐。折旧审查(config-audit)需要知道**每条规则当初为什么存在**——不显式记录,三个月后没人说得清哪条该删。

## baseline 块格式(工作区根 CLAUDE.md 末尾,机器可读)

```
<!-- claude-config-baseline
date: <今天>
model: <当前模型 ID>
workaround-rules:      # 为绕过当前模型/工具限制而写的规则,每条附一句"为什么"
  - "<规则>: <当初原因>"
tools-on-trial:        # 试用期工具
  - codegraph: installed=<日期> trial-until=<+7天> criteria="探索变快?错边出现?"
quarantine: []         # config-audit 隔离观察中的规则(格式: 规则 | until=<日期>)
-->
```

## 新鲜度 hook(SessionStart,用户级,一个 hook 服务所有工作区)

hook 是确定性 shell,秒级预算,没有 LLM——所以它只做机械检测与提醒;判断与修改归 config-audit skill。这正是 hook 与 skill 的正确分工:该自动的用 hook,要判断的用 skill。

脚本放 `~/.claude/hooks/config-freshness.sh`,**自 scoping**:从 cwd 向上找含 `claude-config-baseline` 的 CLAUDE.md,找不到静默退出(毫秒级,全局挂载无感)。找到则查四项:

1. baseline date 距今 > 90 天?
2. codebase-map 列的目录还存在?顶层有 map 未记录的新目录?
3. 各仓标记块 hash 与 master 一致?
4. tools-on-trial / quarantine 有到期项?

**任一命中输出一行提醒(如「[config-freshness] 配置 112 天未审;map 2 目录失效 → 建议 /config-audit」),全部通过绝对静默。** SessionStart 的 stdout 注入每次会话上下文——一个每天喊"一切正常"的 hook 本身就是上下文污染。

## 安装流程

写 hook 前调用 `update-config` skill(args 以 `[hooks-only]` 开头)加载 hooks schema 与验证流:构造 → pipe-test → 写入 settings → `jq -e` 校验。hook 写入用户 settings 前需用户确认(在 Phase 3 总提案里已标 ⚠️,若用户当时已勾选则直接执行)。
