# Requirement KPI and provider document source changes

Saved-source change SEM-004, 18 October 2026. See [implementation, limitations and acceptance](../../../client%20documentation/04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

The `after` files are a reviewable delta against the exact latest local WIP baseline in the manifest. They contain report/model definitions only. The original active WIP folder is locally ignored; this package prevents source changes from being lost from Git review. It does not replace the repository ZIP.

Run `python "project X/tools/apply_requirement_dashboard_additions.py"` from the repository root for a read-only baseline check. Add `--apply` to install only the named files, saving a backup. A mismatched baseline is refused; an already applied file is accepted. Reopen the project and refresh calculated metadata before using `acceptance.dax`. Runtime and client acceptance remain pending.
