# Phase 2 探索细节

## 基线测量(价值证明的前半段)

- 源文件总数(未排除前)
- 选一个仓内常见函数名,记录 `grep -rnw` 命中数与涉及文件数
- 存入内存,Phase 5 与 LSP/图的命中数对比

## 模块切分(自顶向下,只识别不写内容)

识别来源:workspace/多模块配置(pom `<modules>`、pnpm-workspace、go.work)、并排的独立 git 仓(逐目录测 `.git`)、服务目录惯例。产出模块清单:名称、路径、语言、是否独立 git 仓。

- 递归深度限 2(工作区根 + 模块层)。更深的差异后续用 `.claude/rules/` + paths frontmatter 表达,不再铺 CLAUDE.md——文件层级越深人越难维护,折旧审查扫描面越大。
- **多仓并排工作区(根不是 git 仓)显式标记**:它决定 Phase 4 分片走三层分发(见 sharding.md);单 git 仓 monorepo 退化为两层。

## 模块探索子代理(并行,每模块一个)

只凭本地证据,**不读根 CLAUDE.md**——避免被已有内容锚定,归并时根文件是要被重新推导的残差,不是基线。

已装 codegraph 时:先 `codegraph files` / `codegraph query` 拿符号清单和模块间依赖,再选择性读文件——N 个子代理全文读文件会把上下文灌爆。

采集面:

- 构建/测试/lint 命令,**限定到本模块作用域的版本**(防全仓跑超时),记实际命令不要猜
- 偏离语言默认的风格约定
- 地雷、必需 env、前置条件
- 对外暴露面:本模块被哪些模块依赖(A 类共性的原料)

## 输出契约(强制——归并靠它机械对齐)

每条候选一个 JSON 对象:

```json
{"type": "command|convention|gotcha", "content": "...", "evidence": "文件路径:行", "confidence": "high|medium|low"}
```

没有这个契约,7 个代理用各自措辞描述同一条约定,归并就只能凭感觉。

## ignore 候选采集(三来源,每组附证据)

1. 惯例目录:node_modules/ target/ dist/ build/ .gradle/ vendor/ 等,实测文件数与体积
2. .gitignore 交集——只作线索不照搬(两个方向都有反例,见 ignore.md)
3. 生成物标头:文件头含 `@generated` / `DO NOT EDIT` 的目录

## 间接层信号(codegraph 判定的输入)

扫描:`@FeignClient` / RPC 客户端注解、route→handler 注解(@GetMapping 等大规模存在)、多语言桥(JNI/RN bridge)。这些是 grep 和 LSP 都难覆盖、唯独结构图能给的边。
