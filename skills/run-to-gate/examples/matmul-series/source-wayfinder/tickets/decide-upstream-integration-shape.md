# Decide upstream integration and PR shape

Label: `wayfinder:grilling`
Mode: HITL
Status: blocked
Blocked by: Freeze the delivery baseline and repository contract; Confirm community-task deliverables and upstream submission path; Choose the shared operator architecture boundary; Lock the implementation proof and acceptance-test plan

## Question

Should the five operators land as one coordinated PR or a staged sequence, and what shared infrastructure changes (headers, CMake, common kernels/helpers, tests, docs) are allowed in each stage so review and rollback remain tractable without duplicating implementation?

The resolution must produce the final integration boundary that `/to-spec` will encode.
