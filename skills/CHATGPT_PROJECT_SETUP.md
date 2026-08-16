# ChatGPT Project Setup

## Recommended project

- **Name:** BCT — Fabric & Power BI Engineering
- **Icon:** database or chart
- **Colour:** BCT blue/purple
- **Memory:** Project-only memory, especially if the project will be shared
- **Purpose:** Long-running engineering and documentation workspace for the WMPP
  Fabric Lakehouse and Power BI solution

## Project instructions

Paste the complete contents of `PROJECT_INSTRUCTIONS.md` into **Project
settings → Project instructions**.

## Initial project sources

Upload these foundation files first:

1. `SOUL.md`
2. `PROJECT_STATE.md`
3. project `README.md`
4. client-documentation `README.md`
5. `HLD.md`
6. `TFD.md`
7. `FFD.md`
8. `NOTEBOOK_RUNBOOK.md`
9. `ETL_ISSUE_AND_CHANGE_LOG.md`
10. `SEMANTIC_MODEL_CHANGELOG.md`
11. `schema_definition.csv`
12. `dq_rule_definition.csv`
13. current KPI/measure catalogue and requirements source

Add current notebooks, TMDL/PBIP definitions, and test assets only as needed for
the active task or where the plan's file limit permits. Prefer current sources
over archives.

## Recommended first chats

1. **Project control and documentation** — maintain state, decisions, README,
   HLD, TFD, FFD, runbooks, and change logs.
2. **Fabric/PySpark engineering** — notebook design, schema, DQ, archive replay,
   Gold, tests, and performance.
3. **Power BI semantic model and DAX** — TMDL, relationships, RLS, KPIs,
   measures, and regression evidence.
4. **KPI reconciliation and acceptance** — baseline mapping, stakeholder
   decisions, UAT, and sign-off evidence.

## Important limitation

A ChatGPT Project can use uploaded files and its project memory, but an uploaded
copy is not a live synchronisation of the local `H:` repository. After ChatGPT
edits a document, save/download the revised file into the repository and upload
the new version to the project, or connect an approved cloud source. Keep Git
and the controlled repository as the authoritative version history.
