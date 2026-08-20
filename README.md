# BCT — Fabric CSV ingestion

This repository contains the BCT implementation of the
West Midlands Placement Portal (WMPP) data platform in Microsoft Fabric.

The active client implementation is under [`project X`](project%20X/). The
repository-level `scripts`, `references`, and `SKILL.md` retain reusable
ingestion material; they are not the production WMPP notebook chain.

## Repository layout

| Location | Purpose |
|---|---|
| `project X/` | Active BCT Fabric notebooks and project assets |
| `project X/client documentation/` | Client-facing discovery, design, governance, and operations documentation |
| `project X/change tracking/` | ETL issue/change history kept separate from client design documents |
| `project X/configuration/` | Version-controlled schema and DQ configuration deployed to Fabric Files |
| `project X/tests/` | Portable static regression checks and Spark simulation harness |
| `archive/` | Superseded layouts and versions retained for recovery/reference |
| `scripts/` | Reusable or supporting ingestion scripts |
| `references/` | Generic Fabric reference material |

Start with [`project X/README.md`](project%20X/README.md).
