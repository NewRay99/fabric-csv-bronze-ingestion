
00_archive_load 02 03

## new issue

df = spark.read.format("csv").option("header","true").load("Files/archive_unzipped/2026-07-30/provider_framework.csv")
display(df.select("export_date").distinct())
--Results
2026-06-30 00:00:00



df = spark.sql("SELECT distinct  export_date FROM LH_BCT_WMPP.silver.slv_provider_framework LIMIT 1000")
display(df)
--Results
2026-07-30


[DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_referral_provider_decline_reason for 2026-08-03
FAILED Files/archive_unzipped/2026-08-03/referral_provider_decline_reason.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_referral_provider_cancel_reason for 2026-08-04
FAILED Files/archive_unzipped/2026-08-04/referral_provider_cancel_reason.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_provider_submission_docs for 2026-07-30
FAILED Files/archive_unzipped/2026-07-30/provider_submission_docs.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_referral_person_support_needs for 2026-07-30
FAILED Files/archive_unzipped/2026-07-30/referral_person_support_needs.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_holding_company for 2026-08-03
FAILED Files/archive_unzipped/2026-08-03/holding_company.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_referral_provider_decline_reason for 2026-08-05
FAILED Files/archive_unzipped/2026-08-05/referral_provider_decline_reason.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'
Deleted legacy export-date rows from archived.archived_provider_education_provision for 2026-05-30
FAILED Files/archive_unzipped/2026-05-30/provider_education_provision.csv: [DELTA_FAILED_TO_MERGE_FIELDS] Failed to merge fields 'export_date' and 'export_date'…

these arent coming from the source extracts...
FAILED bronze.ref_KPI_Definition: bronze.ref_KPI_Definition has no export_date; rerun 01_bronze_get_latest first
FAILED bronze.ref_KPI_RID_linkage: bronze.ref_KPI_RID_linkage has no export_date; rerun 01_bronze_get_latest first
FAILED bronze.ref_RID: bronze.ref_RID has no export_date; rerun 01_bronze_get_latest first
FAILED bronze.ref_Table_Lineage: bronze.ref_Table_Lineage has no export_date; rerun 01_bronze_get_latest first
OK bronze.referral -> silver.slv_referral @ 2026-08-15 00:00:00: 599 rows
create a new notebook call it common_util.ipynb and add these tables in a list array so that this 02_silver_formatter 02 03.ipynb any any other ETL notebooks can explucde them from the process
