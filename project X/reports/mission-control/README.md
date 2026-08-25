# WMPP ETL Operations Control Tower

`index.html` is a grey-and-white interactive wireframe for the Power BI report.
It documents the required pages, visual hierarchy and drill paths; its sample
values are illustrative, not sourced data.

`mission-control-measures.dax` contains the DAX measure definitions. Import
the `monitoring` reporting views and configuration tables using the semantic
model names stated at the top of that file.

The additional referral, offer, placement, provider-response and snapshot DAX
measures enabled by `04_gold_model` are held in
`client documentation/04_Data_and_Reporting/KPI_Reference_Guide.md`.

Create two distinct ETL pages. Apply the following page filter to every
job-based visual and drillthrough path respectively:

- **Live pipeline:** `pipeline_name = "90_run_live_pipeline"`
- **Archive pipeline:** `pipeline_name = "90_run_archive_pipeline"`

The archive page additionally uses `export_date` and `snapshot_date` from the
archive controls. Do not include those archive batch metrics on the live page.

Use `monitoring.vw_job_run_summary` as the job-run hub, related one-to-many by
`job_run_id` to job step, data-quality, schema-drift, table-load-metric and
referential-exception facts. Use single-direction filtering from Job Run to
child facts. Cast timestamp fields to dates in Power Query for page-level date
relationships.

The report must state that table/column lifecycle events and true
insert/update/delete counts are not currently captured by the ETL. Do not
derive them from snapshot overwrite counts.
