# 容器与 JVM

容器中的 JVM 运行在 cgroup 限制下。调优不能只看 `-Xmx`，还要考虑进程 RSS、CPU quota、线程数、native 内存和容器 OOMKill 行为。

## 容器感知

- JDK 8u191+、JDK 10+ 对 cgroup 支持更完善，早期版本可能按宿主机资源计算默认堆和 GC 线程数。
- JDK 9/10 之后常用 `-XX:+UseContainerSupport`，多数新版本默认开启。
- 可用 `-XshowSettings:system`、`-XshowSettings:vm` 或 `jcmd <pid> VM.info` 确认 JVM 识别到的 CPU 和内存限制。
- cgroup v1 和 v2 的指标路径不同，排查时要确认运行时和基础镜像支持情况。

### cgroup 常见指标

- cgroup v1 常见路径包括 `memory.usage_in_bytes`、`memory.limit_in_bytes`、`cpu.cfs_quota_us`、`cpu.cfs_period_us`。
- cgroup v2 常见路径包括 `memory.current`、`memory.max`、`cpu.max`、`memory.events`。
- Kubernetes 中还应结合 Pod limit、request、QoS、重启次数和事件判断。

## 内存组成

容器 RSS 通常包含：

- Java 堆：受 `-Xmx` 或 `MaxRAMPercentage` 影响。
- 元空间：类元数据和 ClassLoader 相关内存。
- 直接内存：NIO、Netty、Unsafe、JNI 分配。
- 线程栈：线程数乘以 `-Xss`，还包括 native thread 结构开销。
- 代码缓存：JIT 编译后的机器码。
- GC native 内存：卡表、记忆集、标记位图、线程本地结构等。
- JVM 自身和 JNI 库：解释器、编译器、符号、内部结构和第三方 native 库。
- mmap 和 page cache：文件映射、JAR、日志、临时文件等可能影响 RSS 或容器内存压力。

## 参数建议

- 固定堆大小时，`-Xmx` 不应接近容器 limit，需要给非堆内存留余量。
- 使用百分比参数时，明确 `InitialRAMPercentage`、`MaxRAMPercentage` 和容器 limit 的关系。
- 高线程服务要核算 `线程数 * -Xss`，线程池不是越大越安全。
- Netty 或大量 NIO 场景应显式规划 `-XX:MaxDirectMemorySize`，并监控池化直接内存。
- 容器 CPU limit 较小时，过多 GC 线程或 JIT 编译线程会和业务线程争抢 CPU。

### 内存预算示例

- 如果容器 limit 是 2GB，不能简单设置 `-Xmx2g`。
- 需要预留元空间、直接内存、线程栈、代码缓存、GC native 内存、JVM 本体、JNI 库和诊断文件空间。
- 一个常见起点是堆占 limit 的 50% 到 70%，再根据线程数、直接内存和实际 RSS 调整。
- Netty 大量使用直接内存或线程数很多时，堆比例应更保守。

## CPU Quota 影响

- JVM 会根据可用处理器数量决定 GC 线程、JIT 编译线程和 ForkJoinPool 并行度。
- CPU quota 很低但线程很多时，应用容易出现延迟尖刺、GC 并发阶段追不上和安全点等待变长。
- 可用 `-XX:ActiveProcessorCount=<n>` 明确 JVM 看到的处理器数量，适合容器识别不准确或需要隔离并行度的场景。
- 延迟敏感服务要同时看 CPU throttling、GC pause、safepoint 和请求延迟。

## Kubernetes 注意点

- request 决定调度和 QoS，limit 决定 cgroup 上限。
- memory limit 过小会导致 OOMKill，CPU limit 过小会导致 throttling 和延迟抖动。
- Burstable Pod 在节点内存压力下比 Guaranteed 更容易被驱逐。
- JVM 自适应堆按 limit 计算时，如果 limit 远大于 request，实际节点压力仍可能影响稳定性。

## OOMKill 与 Java OOM

| 类型 | 表现 | 处理方向 |
| --- | --- | --- |
| Java OOM | JVM 抛出 `OutOfMemoryError`，可能生成 heap dump | 根据异常类型排查堆、元空间、直接内存或线程 |
| 容器 OOMKill | 进程直接退出，通常没有 Java 异常栈 | 查容器事件、RSS、limit、非堆内存和 page cache |
| 系统 OOM | 节点内存压力导致进程被 kill | 查节点事件、宿主机 dmesg、Pod QoS 和资源超卖 |

## 观测指标

- JVM：heap used/committed/max、metaspace、direct buffer、thread count、GC pause、allocation rate。
- 进程：RSS、VMS、fd 数、线程数、native memory、CPU 使用率。
- 容器：memory.current、memory.max、oom_kill、cpu throttled time、CPU quota。
- 系统：节点内存、swap、page cache、IO 等待、负载和调度延迟。

## 发布和镜像注意点

- 基础镜像的 libc、时区、字体、证书和 DNS 配置可能影响 Java 行为。
- Alpine/musl 镜像体积小，但部分 native 库、诊断工具和性能特征可能不同。
- 生产镜像建议保留必要诊断工具或提供 sidecar/debug 镜像路径。
- 容器内 heap dump 和 JFR 文件可能很大，要预留磁盘空间并避免写爆临时目录。
