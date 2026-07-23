# codegraph 发现层(条件安装)

codegraph 是预计算结构索引(tree-sitter 图 + SQLite),定位是三层导航里的**发现层**:架构问答、影响面、入口发现一次调用出结果。它**不是**正确性来源——Spring DI/反射场景实测存在假阴性(impl 方法报"No callers"但实际经接口注入被调)与错误归因(同前缀方法混淆)。

## 装不装:从已采集数据推导,不让用户自估仓库大小

| 条件 | 判定 |
|---|---|
| 排除后源文件数 ≥ 2000 | 强推荐 |
| 500–2000 且存在跨服务间接层(Feign/RPC、route→handler、多语言桥) | 推荐 |
| < 500 | 不装(小仓 grep+read 已够快,常驻 watcher 不划算) |

唯一问用户的轴:探索/理解类工作占比(Phase 1 的 Q2)。占比低 → 灰区一律不装。语言折扣:Spring/反射重不改变装不装,改变铁律措辞强度(见文末模板)。

## 安装与接线

```
npm i -g @colbymchenry/codegraph
codegraph init          # 在工作区根
```

**接线只用 MCP/CLI 按需模式,绝不用 prompt-hook。** 流程:

1. 记录 `~/.claude/settings.json` 快照
2. `codegraph install --target=claude --yes`
3. **diff 审计它写了什么**。已知它会写三样:MCP 注册(保留)、`permissions.allow: mcp__codegraph__*`(保留)、**全局 UserPromptSubmit hook `codegraph prompt-hook`——必须摘除**:它对每条 prompt 无差别注入图上下文并附"treat as already read"指令,实测把纯讨论 prompt 灌进 13.6KB 无关符号,直接违反常驻上下文极瘦原则。

通用规则:**任何第三方安装器跑完都要 diff settings 文件**——安装器写的东西经常超出它声称的范围。

## 试用期登记(写进 baseline,见 baseline-hook.md)

```
codegraph: installed=<日期> trial-until=<+7天> criteria="探索类问题明显变快?出现过错误调用边?"
```

到期由 config-audit 按 criteria 问用户实际体验裁决去留。它的收益随模型变强而缩窄(模型自身导航越强收益越小),按折旧配置对待——不是基础设施,是登记在册、定期重审、随时可扔的效率插件。卸载:`codegraph uninit` + `npm rm -g @colbymchenry/codegraph` + 清理 MCP 注册与 permissions.allow,零沉没。

## 使用注意

- bare-name 查询会把同名符号的调用者**合并返回**,用 `"Class.method"` 限定
- MCP 中途接线本会话不生效,重启后可用;CLI(`codegraph explore/callers/impact`)即装即用

## 铁律模板(Phase 4 写入 B 类/根文件;Spring/反射重的仓库用重措辞版)

> 代码导航分三层:**发现用 codegraph**(架构问答、影响面,输出是线索不是事实),**判决用 LSP**(重构前 findReferences/goToImplementation,编译器级),**字面用 grep**(字符串、日志、注释)。铁律:codegraph 报「无调用者」不构成可安全修改的证据——本仓库 DI/反射场景实测出现过假阴性与错误归因,动手前必须 LSP 复核。
