# Wayfinder Map — Atlas A2 complex64 matrix-multiply series

Label: `wayfinder:map`

## Destination

形成一份**已清除关键决策歧义、可直接交给 `/to-spec` 的实现路线**：在 Atlas A2 / arch22 上为 ops-blas 实现 CHEMM、CHER2K、CHERK、CSYMM、CSYRK，满足标准 BLAS/cuBLAS 语义、当前 ops-blas 工程规范、社区精度标准和任务书的 0.8×A100 性能门槛，并明确最终验收交付与上游 PR 路径。

到达本 map 终点时，不要求生产代码已实现；要求**实现者不再需要做架构级、接口级、测试标准级或验收流程级决策**。

## Notes

- Domain: Ascend C / CANN ops-blas / BLAS Level-3 / complex64 / Atlas A2 (ascend910b3, arch22).
- Wayfinder rule: **plan, don't do**. 本 map 不写生产 kernel；清图后交给 `/to-spec → /to-tickets → implement`。
- Target hardware from task book: Atlas A2 training series. arch35/Ascend 950 is useful only as reference, not a delivery target unless destination is later redrawn.
- Treat the task book as semantic authority for required operator behavior, but reconcile it with the exact CANN/ops-blas baseline selected for delivery.
- The provided test bundle is evidence, not automatically the current repo contract: it contains paths/commands that appear older than the current upstream repository structure.
- Current upstream is changing quickly; freeze a baseline before implementation.
- Precision must use the current ecological mixed-tolerance standard rather than silently preserving outdated local test conventions.

## Decisions so far

<!-- Empty by design at charting time. A Wayfinder charting session resolves no tickets. -->

## Not yet specified

- Exact A2 kernel micro-architecture and tile sizes after the viable complex-matmul path is settled.
- Whether the five operators converge on one generalized internal engine, two families (MM vs rank-k), or several specialized kernels after code-reuse and performance tradeoffs are understood.
- Exact materialization/fusion strategy for symmetric/Hermitian reconstruction after memory-traffic and Cube/AIV constraints are quantified.
- Detailed performance-iteration plan (which bottleneck to attack first) until an initial architecture and cost model are selected.
- Exact implementation ticket slicing and tracer-bullet order; this belongs downstream after this map clears.
- Final design-document section contents and screenshots; their structure depends on the frozen implementation/test contract.

## Out of scope

- Ascend 950 / arch35 production support for these five operators.
- FP16/BF16/complex128 variants.
- Batched/strided-batched variants not required by the task book.
- Redesigning unrelated ops-blas public APIs or repository-wide test infrastructure.
- Replacing the upstream community workflow or changing official acceptance thresholds.
- Implementing production code inside Wayfinder.

## Frontier

Open, unblocked, unclaimed tickets:

1. [Freeze the delivery baseline and repository contract](tickets/freeze-delivery-baseline.md) — `wayfinder:grilling`
2. [Reconcile the supplied acceptance bundle with the current precision standard](tickets/reconcile-acceptance-bundle.md) — `wayfinder:research`
3. [Establish the Atlas A2 complex64 compute capability envelope](tickets/a2-complex-compute-envelope.md) — `wayfinder:research`
4. [Confirm community-task deliverables and upstream submission path](tickets/confirm-delivery-path.md) — `wayfinder:research`

Blocked tickets are listed in `dependencies.md`.
