# Realistic user prompt

我接了 CANN 2026 社区任务“矩阵乘系列算子开发”，附件里有任务书和官方自测脚本。

目标是在 **Atlas A2（ascend910b3 / arch22）** 上，基于 Ascend C 为 `ops-blas` 完成以下 5 个 complex64 BLAS Level-3 算子：

- `aclblasCHEMM`
- `aclblasCHER2K`
- `aclblasCHERK`
- `aclblasCSYMM`
- `aclblasCSYRK`

最终需要：功能和标准 BLAS/cuBLAS 语义对齐；官方泛化精度用例通过；性能达到任务书要求（NPU 耗时不超过 A100 的 1.25 倍）；提交设计文档、自测代码、自测报告和待验收代码，并最终向 `cann/ops-blas` 的 experimental/目标目录发起 PR。

仓库最近变化较快，我不确定应该复用哪些现有实现、复杂数怎样在 A2 上做高性能矩阵计算、五个算子是否应该共享 kernel，以及随包测试与当前 upstream 是否完全一致。

请使用 Wayfinder：先不要写生产代码，先把所有会阻塞实现和验收的关键决策画成 decision map，直到可以无歧义地转成 spec 和 implementation tickets。
