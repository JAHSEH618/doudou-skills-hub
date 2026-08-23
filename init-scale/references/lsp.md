# LSP 正确性层(主动安装)

LSP 是三层导航里的**判决层**:编译器级的 findReferences / goToImplementation,重构安全的唯一可信来源。grep 是字面匹配,codegraph 是启发式图——两者都只能提供线索。

## 四层体检(按 Phase 2 的语言清单逐语言做)

1. **插件层**:该语言插件是否已启用?查官方 marketplace(`claude-plugins-official`,13 个 LSP 插件)与用户已添加的第三方 marketplace(如 `claude-code-lsps`)。**语言→插件映射运行时读 marketplace 清单,不要依赖任何硬编码表**——硬编码表本身就是会折旧的配置。
   - 坑:插件的 `lspServers` 配置可能**内联在 marketplace.json 里**,插件目录只有 LICENSE 和 README。判断"是否已配置"不能只看插件目录。
2. **二进制层**:`.lsp.json`/清单里的 `command` 是否在 PATH?缺则用包管理器装(brew/npm/pip/rustup)。需要 sudo 的只给命令,报给用户。
3. **依赖层(二进制在 PATH 只是必要条件,远不是充分条件)**:LSP 的判决能力建立在它能解析出完整 classpath / 模块图之上。依赖拿不到时它**不报错、不退出**,只退化成语法解析器——这是本层最危险的失败形态,详见「验证」一节。逐语言查:私有制品库需要凭据或内网吗?本地仓里是真构件还是失败标记(Maven 看 `~/.m2/repository` 下有没有 `.jar`,只有 `.lastUpdated` = 从没成功过)?工程构建过吗?
   - 修不了的(需内网/VPN/凭据)不要硬修,写进 CLAUDE.md 当已知缺陷,并**据此下调铁律强度**——见「验证」的降级措辞。
4. **冲突层**:同一后缀被多个插件注册?**先读各插件声明的后缀集合做差集,再下结论——不要凭插件名假设它们等价。** 实测 typescript-lsp 与 vtsls:重叠的 6 个后缀 vtsls 赢,但 vtsls 没声明 `.mts`/`.cts`,这两个漏给了 typescript-lsp。**它们是分工不是冲突,按"二选一"停掉任意一个都会静默丢覆盖。**
   - 真正重叠的部分谁赢**只能实测**:对该后缀发一次 LSP 请求,然后 `ps ax -o command= | grep -E '<server-a>|<server-b>'` 看谁被拉起来。
   - 只有当一方的后缀集合是另一方的**真子集**时,停掉子集方才是安全的。

## 探测约束(实测踩过的坑)

- **任何 LSP server 二进制一律只 `which`,绝不试运行**——包括加 `--version`。它们是 server,拿到 stdin 就等协议帧,不会退出。实测挂住并耗掉 120 秒超时的:`jdtls --version`(启整个 JVM)、`tsserver --version`(输出一个 `Content-Length:` 帧头然后等)。版本号要么从包管理器查(`npm ls -g`、`brew list --versions`),要么从插件清单读,不要问二进制本身。
  - 例外:少数带 CLI 前端的(`vtsls --version`、`typescript-language-server --version`)会正常退出。但**分不清就别试**——猜错的代价是 120 秒,猜对省不下什么。
- jdtls 首次请求慢是正常的(要导入 Maven/Gradle 工程,插件配了 120s startupTimeout),不要当故障处理。

## 验证(幂等收尾)

**`documentSymbol` 通过不构成验证通过——它是本层最容易上当的假绿灯。** 语法解析不需要 classpath,所以依赖全解析不了的 jdtls 照样能把符号列得整整齐齐,看起来完全健康;而同一时刻 `findReferences` 恒返回空。实测原文:`X.java is not on the classpath of project Y, only syntax errors are reported`。

必须用**已知答案的符号**校准判决层,而不是问"有没有响应":

1. 从 Phase 2 基线测量挑一个 grep 命中数明确的符号(最好是几十个引用量级的)。
2. 跑 `findReferences`,拿返回数和 grep 数对照。
3. 判读:
   - **数量同量级(LSP 略少于 grep,因为 grep 含注释/字符串/同名类)** → 判决层是活的。把差值报给用户,这就是本层的价值证明。
   - **返回 0 或个位数,而 grep 有几十上百** → **判决层是死的**,不要因为 `documentSymbol` 通了就宣布配好。回到「依赖层」查根因。
   - **不通且本步刚装过插件** → 不是失败,是**会话边界**:LSP 服务器注册表在会话启动时构建,中途装的插件不热加载。告知用户"已装好,重启会话后重跑 /init-scale 会自动从验证续跑"(幂等保证已装项直接跳过)。

### 判决层是死的时候,铁律必须降级

这时**绝不能**把标准措辞「重构前用 LSP findReferences 判决」写进 CLAUDE.md——那等于给了一把读数恒为 0 的尺子,Claude 会据此把活代码判成死代码。比没有 LSP 更危险。

改写成:

> **LSP 的空结果当前不是证据。** `findReferences` / `goToImplementation` 因 <根因> 恒返回空;`documentSymbol` 正常返回会让它看起来是活的。修好之前,不要用 LSP 的空结果论证任何东西可以删改。当前判定只能靠 codegraph 发现 + grep 交叉验证 + 人工确认。

同时在 baseline 块登记为 `workaround-rules` 并注明**修好后必须删除此条**——这类规则是为绕过环境缺陷而写的,环境修好后它就从保护变成枷锁,会长期压制一个已经可用的判决层。修复步骤属一次性流程,放模板/文档文件里,不要占根 CLAUDE.md 的常驻上下文。
