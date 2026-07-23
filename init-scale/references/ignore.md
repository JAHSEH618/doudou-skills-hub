# 搜索面收缩(permissions.deny)

## 写入目标

**`.claude/settings.json` 的 `permissions.deny`,格式 `Read(./path/**)`。** `.claudeignore` 机制不存在(已在二进制里证实为 0 命中),不要写那个文件——写了就是一个没人读的静默无效文件,恰好是最危险的失败模式。

## 为什么这一步必须用户确认

ignore 写错**不报任何错**:Claude 只是从此看不见那些文件,然后给出错误答案,用户无法把错误归因到几个月前的一条规则。静默失明型配置必须过人。且机器拿不到关键信息:「这个 vendor 目录有没有本地补丁」「这些生成代码是不是团队的 API 面」只有用户知道——确认不是流程礼貌,是在补机器拿不到的信息。

## gitignore ≠ claude ignore(两个方向都有反例)

| gitignore 有、但 Claude 该看 | 版本控制里有、但 Claude 不必看 |
|---|---|
| 生成的 API stubs(protobuf/OpenAPI client) | 入库的 vendor 代码 |
| lockfile(查版本用) | 大体积测试快照/fixture |

## 剔除规则(看似该排、实则不能排)

- **承载 API 面的生成代码**:排掉即对整个调用面失明,最危险的误排
- **敏感文件(.env、密钥)**:不进 deny,单独提示用户——ignore 不是安全边界,权限机制才是

## 确认 UX

分组呈现,每组一行证据:「target/ —— 12,400 个文件,Maven 构建产物,已在 .gitignore」。AskUserQuestion(multiSelect)一次批量确认,高置信组默认勾选。绝不逐文件问——确认成本必须一次付清。

## 写后验证(不验证 = 没做)

对一个只存在于被排除目录中的字符串跑 Grep,确认返回空。报告排除文件数与占仓库比例。
