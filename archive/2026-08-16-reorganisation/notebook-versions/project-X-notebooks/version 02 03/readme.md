

errors with 

## first errors
i am refactoring the repeatable code accross the notebooks using 99_common_library 02 03.ipynb
```
cfg_result = mssparkutils.notebook.run(
                CFG_NOTEBOOK_NAME,
                NOTEBOOK_TIMEOUT_SECONDS,
                {"AUDIT_TABLE": "{AUDIT_TABLE}"}
            )
```
error is
```
Py4JJavaError
An error occurred while calling o5280.throwExceptionIfHave. : com.microsoft.spark.notebook.msutils.NotebookExecutionException: name 'TIME_PARSER_POLICY' is not defined ---------------------------------------------------------------------------NameError Traceback
```
could you fix this


## next error
next error with 02a_archive_silver 02 03
```
ValueError
No schema contract for archived.archived_provider_sic_codes
```
i know that the schema_definition.csv is not 100% accurate and is missing some contracts (tables) entirely.. these should throw errors in the load only flag them in the cfg log tables and quietly continue to the next contract/table

# next error 
there are csv files with date as their filenames... example YYYY-MM-DD.csv 2026-06-29.csv

these were meant to go into a table with a schema like so
correlation_id
commit_date
event_subject_name
user_id
user_name
entity_type
entity_id
property_name
change_type
old_value
new_value


obviously dont have an export date.. shouls i create a seperate notebook to havle these ??? or exlude them completely asd they dont have a export_date field


