# LSP 正确性层(主动安装)

LSP 是三层导航里的**判决层**:编译器级的 findReferences / goToImplementation,重构安全的唯一可信来源。grep 是字面匹配,codegraph 是启发式图——两者都只能提供线索。

## 三层体检(按 Phase 2 的语言清单逐语言做)

1. **插件层**:该语言插件是否已启用?查官方 marketplace(`claude-plugins-official`,13 个 LSP 插件)与用户已添加的第三方 marketplace(如 `claude-code-lsps`)。**语言→插件映射运行时读 marketplace 清单,不要依赖任何硬编码表**——硬编码表本身就是会折旧的配置。
   - 坑:插件的 `lspServers` 配置可能**内联在 marketplace.json 里**,插件目录只有 LICENSE 和 README。判断"是否已配置"不能只看插件目录。
2. **二进制层**:`.lsp.json`/清单里的 `command` 是否在 PATH?缺则用包管理器装(brew/npm/pip/rustup)。需要 sudo 的只给命令,报给用户。
3. **冲突层**:同一后缀被多个插件注册?(例:typescript-lsp 与 vtsls 都抢 `.ts`)Claude Code 只用一个,另一个白占配置——让用户二选一停掉。

## 探测约束(实测踩过的坑)

- **jdtls 等 JVM 系 server 探测只能 `which`,绝不能试运行**:`jdtls --version` 会启动整个 JVM 挂住等 stdin,120 秒超时。
- jdtls 首次请求慢是正常的(要导入 Maven/Gradle 工程,插件配了 120s startupTimeout),不要当故障处理。

## 验证(幂等收尾)

跑 `LSP documentSymbol` 探测一个该语言源文件:

- **通** → 对基线测量用过的符号跑 grep vs `findReferences` 命中数对比,报数量差给用户——这就是本层的价值证明,不做对比不算配完。
- **不通且本步刚装过插件** → 不是失败,是**会话边界**:LSP 服务器注册表在会话启动时构建,中途装的插件不热加载。告知用户"已装好,重启会话后重跑 /init-scale 会自动从验证续跑"(幂等保证已装项直接跳过)。
