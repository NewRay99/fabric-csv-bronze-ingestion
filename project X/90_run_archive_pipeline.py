# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "known_lakehouses": [
# META         {
# META           "id": "d286fa39-f255-4ba7-a982-32cb69362ef7"
# META         }
# META       ],
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770"
# META     }
# META   },
# META   "spark_compute": {
# META     "compute_id": "/trident/default",
# META     "session_options": {
# META       "conf": {
# META         "spark.synapse.nbs.session.timeout": "7200000"
# META       }
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 90 — Archive pipeline runner
#
# Run the archive-to-Gold sequence in one controlled order. Each child notebook remains independently runnable for recovery.

# CELL ********************

# Archive replays can process several complete monthly extracts. Two hours
# prevents the runner from terminating 02a_archive_silver at the old 30-minute limit.
NOTEBOOK_TIMEOUT_SECONDS = 7200
print(
    f"Child notebook timeout: {NOTEBOOK_TIMEOUT_SECONDS:,} seconds "
    f"({NOTEBOOK_TIMEOUT_SECONDS / 60:.0f} minutes)"
)
STOP_ON_ERROR = True
JOB_RUN_ID = ""  # Optional caller-supplied ID; generated when blank.

# Optional guarded single-month rebuild controls forwarded to Archive Silver.
PROCESS_ONLY = ""  # YYYY-MM; blank processes the normal archive range.
RESET_MONTH_MONITORING = False
CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY = False
CONFIRM_PROCESS_ONLY_RESET = ""  # Must be RESET YYYY-MM, or RESET ALL when PROCESS_ONLY is blank.

ARCHIVE_STEPS = [
    ("00_setup_cfg", {}),
    ("00_archive_load", {}),
    ("01a_cfg_schema_capture_archive", {}),
    # Archive Silver runs its DQ and Gold-fact child steps. Dimensions are
    # deliberately deferred to the final explicit step below.
    ("02a_archive_silver", {
        "RUN_GOLD_DIMENSIONS_AT_MONTH_END": False,
        "PROCESS_ONLY": PROCESS_ONLY,
        "RESET_MONTH_MONITORING": RESET_MONTH_MONITORING,
        "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY": CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY,
        "CONFIRM_PROCESS_ONLY_RESET": CONFIRM_PROCESS_ONLY_RESET,
    }),
    ("05_gold_dimensions", {}),
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run ./99_common_library

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import uuid
from datetime import datetime

from notebookutils import mssparkutils

PIPELINE_NAME = "90_run_archive_pipeline"
JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())
started_at = datetime.utcnow()
results = []
def record_step(step_sequence, notebook_name, status, step_started,
                child_result=None, error_message=None):
    merge_monitor_row(
        "monitoring.cfg_job_step_run",
        (JOB_RUN_ID, step_sequence, notebook_name, step_started,
         None if status == "RUNNING" else datetime.utcnow(), status,
         child_result[:4000] if child_result else None,
         error_message[:4000] if error_message else None, datetime.utcnow()),
        "job_run_id string,step_sequence int,notebook_name string,started_at timestamp,ended_at timestamp,status string,child_result string,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence",
    )


# Setup is deliberately first: it creates or upgrades the two orchestration
# monitor tables before this runner writes its first status record.
setup_name, setup_parameters = ARCHIVE_STEPS[0]
setup_started = datetime.utcnow()
print(f"JOB_RUN_ID={JOB_RUN_ID}")
print(f"=== START {setup_name} ===")
try:
    setup_result = mssparkutils.notebook.run(
        setup_name, NOTEBOOK_TIMEOUT_SECONDS,
        {**setup_parameters, "JOB_RUN_ID": JOB_RUN_ID},
    )
except Exception:
    # Monitoring tables may not yet exist, so Fabric's notebook error is the
    # authoritative failure record for a failed setup bootstrap.
    raise

merge_monitor_row(
    "monitoring.cfg_job_run",
    (JOB_RUN_ID, PIPELINE_NAME, started_at, None, "RUNNING", 1, 0, None,
     datetime.utcnow()),
    "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
    "target.job_run_id = source.job_run_id",
)
record_step(1, setup_name, "SUCCESS", setup_started, str(setup_result))
results.append((setup_name, "SUCCESS", str(setup_result)))
print(f"=== SUCCESS {setup_name} ===")

try:
    for step_sequence, (notebook_name, parameters) in enumerate(ARCHIVE_STEPS[1:], start=2):
        step_started = datetime.utcnow()
        print(f"=== START {notebook_name}; JOB_RUN_ID={JOB_RUN_ID} ===")
        record_step(step_sequence, notebook_name, "RUNNING", step_started)
        try:
            result = mssparkutils.notebook.run(
                notebook_name, NOTEBOOK_TIMEOUT_SECONDS,
                {**parameters, "JOB_RUN_ID": JOB_RUN_ID},
            )
            result_text = str(result)
            record_step(step_sequence, notebook_name, "SUCCESS", step_started,
                        child_result=result_text)
            results.append((notebook_name, "SUCCESS", result_text))
            print(f"=== SUCCESS {notebook_name} ===")
        except Exception as exc:
            error_text = str(exc)[:4000]
            record_step(step_sequence, notebook_name, "FAILED", step_started,
                        error_message=error_text)
            results.append((notebook_name, "FAILED", error_text))
            print(f"=== FAILED {notebook_name}: {error_text} ===")
            if STOP_ON_ERROR:
                raise
finally:
    failed = [name for name, status, _ in results if status == "FAILED"]
    succeeded = sum(1 for _, status, _ in results if status == "SUCCESS")
    status = "FAILED" if failed else "SUCCESS"
    error_message = f"Failed notebook(s): {failed}" if failed else None
    merge_monitor_row(
        "monitoring.cfg_job_run",
        (JOB_RUN_ID, PIPELINE_NAME, started_at, datetime.utcnow(), status,
         succeeded, len(failed), error_message, datetime.utcnow()),
        "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id",
    )

failed = [name for name, status, _ in results if status == "FAILED"]
print(
    f"Archive pipeline {status}; JOB_RUN_ID={JOB_RUN_ID}; "
    f"started={started_at.isoformat()}; results={results}"
)
if failed:
    raise RuntimeError(f"Archive pipeline failed notebook(s): {failed}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
