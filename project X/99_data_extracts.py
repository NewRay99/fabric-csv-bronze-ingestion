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
# META         "spark.synapse.nbs.session.timeout": "1200000"
# META       }
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Bronze data-extractor
#
# Extracts the data config files

# PARAMETERS CELL ********************

BRONZE_SCHEMA = "bronze"
CONTRACT_TABLE = ["cfg_schema_drift_definition"
, "cfg_data_domain"
, "cfg_schema_definition_candidate"
, "cfg_schema_contract_column"
, "cfg_archived_schema_live"
, "cfg_bronze_schema_live"
, "cfg_gold_lineage_mapping"
, "cfg_referential_exception"
, "cfg_silver_export_load"
, "cfg_silver_load_control"
, "cfg_table_load_metric"
]
OVERWRITE_FILES = True

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

from datetime import datetime, timezone
from uuid import uuid4

RUN_ID = str(uuid4())
PROFILED_AT = datetime.now(timezone.utc)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

for _table in CONTRACT_TABLE:
    full_name = f"monitoring.{_table}"
    _CSV_PATH = f"/lakehouse/default/Files/cfg_extracts/{_table}.csv"
    if not spark.catalog.tableExists(full_name):
        raise RuntimeError(f"Schema contract table does not exist: {full_name}")
    df= spark.table(full_name)
    pdf = df.toPandas()

    pdf.to_csv(_CSV_PATH, index=False)
    print(f"table exported: {full_name} written to {_CSV_PATH}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import shutil
from notebookutils import mssparkutils

_EXTRACT_NAME = "cfg_extracts"
_RAW_PATH = "/lakehouse/default/Files/cfg_extracts"
_ZIP_PATH = f"/lakehouse/default/Files/cfg_files/{_EXTRACT_NAME}"
_ONELAKE_PATH = f"Files/cfg_files/{_EXTRACT_NAME}.zip"
# zip locally
shutil.make_archive(
    _ZIP_PATH, "zip", _RAW_PATH
)

#verify file is in onelake
mssparkutils.fs.ls(_ONELAKE_PATH)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
