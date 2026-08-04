Processing archive batch 2026-06-30
OK archived.archived_additional_fee -> silver.slv_additional_fee @ 2026-06-30: 120 rows
FAILED archived.archived_framework_category @ 2026-06-30: No schema contract for archived.archived_framework_category
OK archived.archived_holding_company -> silver.slv_holding_company @ 2026-06-30: 606 rows
FAILED archived.archived_ipa @ 2026-06-30: An error occurred while calling o8382.saveAsTable.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 567.0 failed 4 times, most recent failure: Lost task 0.3 in stage 567.0 (TID 5043) (vm-89243710 executor 2): org.apache.spark.SparkException: [TASK_WRITE_FAILED] Task failed while writing rows to abfss://fefdb483-d26c-4bd9-9a4f-0c41cc786770@onelake.dfs.fabric.microsoft.com/d286fa39-f255-4ba7-a982-32cb69362ef7/Tables/silver/slv_ipa.
	at org.apache.spark.sql.errors.QueryExecutionErrors$.taskFailedWhileWritingRowsError(QueryExecutionErrors.scala:777)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.executeTask(DeltaFileFormatWriter.scala:621)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.$anonfun$executeWrite$4(DeltaFileFormatWriter.scala:387)
	at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
	at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
	at org.apache.spark.scheduler.Task.run(Task.scala:141)
	at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:636)
	at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
	at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:95)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:639)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
	at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: org.apache.spark.SparkUpgradeException: [INCONSISTENT_BEHAVIOR_CROSS_VERSION.PARSE_DATETIME_BY_NEW_PARSER] You may get a different result due to the upgrading to Spark >= 3.0:
Fail to parse '2026-05-19 08:51:41.0' in the new parser. You can set "spark.sql.legacy.timeParserPolicy" to "LEGACY" to restore the behavior before Spark 3.0, or set to "CORRECTED" and treat it as an invalid datetime string.
	at org.apache.spark.sql.errors.ExecutionErrors.failToParseDateTimeInNewParserError(ExecutionErrors.scala:54)
	at org.apache.spark.sql.errors.ExecutionErrors.failToParseDateTimeInNewParserError$(ExecutionErrors.scala:48)
	at org.apache.spark.sql.errors.ExecutionErrors$.failToParseDateTimeInNewParserError(ExecutionErrors.scala:218)
	at org.apache.spark.sql.catalyst.util.DateTimeFormatterHelper$$anonfun$checkParsedDiff$1.applyOrElse(DateTimeFormatterHelper.scala:142)
	at org.apache.spark.sql.catalyst.util.DateTimeFormatterHelper$$anonfun$checkParsedDiff$1.applyOrElse(DateTimeFormatterHelper.scala:135)
	at scala.runtime.AbstractPartialFunction.apply(AbstractPartialFunction.scala:38)
	at org.apache.spark.sql.catalyst.util.Iso8601TimestampFormatter.parse(TimestampFormatter.scala:195)
	at org.apache.spark.sql.catalyst.expressions.GeneratedClass$GeneratedIteratorForCodegenStage3.processNext(Unknown Source)
	at org.apache.spark.sql.execution.BufferedRowIterator.hasNext(BufferedRowIterator.java:43)
	at org.apache.spark.sql.execution.WholeStageCodegenEvaluatorFactory$WholeStageCodegenPartitionEvaluator$$anon$1.hasNext(WholeStageCodegenEvaluatorFactory.scala:43)
	at org.apache.spark.sql.execution.datasources.FileFormatDataWriter.writeWithIterator(FileFormatDataWriter.scala:121)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.$anonfun$executeTask$3(DeltaFileFormatWriter.scala:603)
	at org.apache.spark.util.Utils$.tryWithSafeFinallyAndFailureCallbacks(Utils.scala:1398)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.executeTask(DeltaFileFormatWriter.scala:611)
	... 12 more
Caused by: java.time.format.DateTimeParseException: Text '2026-05-19 08:51:41.0' could not be parsed, unparsed text found at index 19
	at java.base/java.time.format.DateTimeFormatter.parseResolved0(DateTimeFormatter.java:2049)
	at java.base/java.time.format.DateTimeFormatter.parse(DateTimeFormatter.java:1874)
	at org.ap
OK archived.archived_ipa_child -> silver.slv_ipa_child @ 2026-06-30: 8 rows
FAILED archived.archived_ipa_child_support_needs @ 2026-06-30: No schema contract for archived.archived_ipa_child_support_needs
FAILED archived.archived_offer @ 2026-06-30: An error occurred while calling o9034.saveAsTable.
: org.apache.spark.SparkException: Job aborted due to stage failure: Task 0 in stage 767.0 failed 4 times, most recent failure: Lost task 0.3 in stage 767.0 (TID 7163) (vm-89243710 executor 2): org.apache.spark.SparkException: [TASK_WRITE_FAILED] Task failed while writing rows to abfss://fefdb483-d26c-4bd9-9a4f-0c41cc786770@onelake.dfs.fabric.microsoft.com/d286fa39-f255-4ba7-a982-32cb69362ef7/Tables/silver/slv_offer.
	at org.apache.spark.sql.errors.QueryExecutionErrors$.taskFailedWhileWritingRowsError(QueryExecutionErrors.scala:777)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.executeTask(DeltaFileFormatWriter.scala:621)
	at org.apache.spark.sql.delta.files.DeltaFileFormatWriter$.$anonfun$executeWrite$4(DeltaFileFormatWriter.scala:387)
	at org.apache.spark.scheduler.ResultTask.runTask(ResultTask.scala:93)
	at org.apache.spark.TaskContext.runTaskWithListeners(TaskContext.scala:166)
	at org.apache.spark.scheduler.Task.run(Task.scala:141)
	at org.apache.spark.executor.Executor$TaskRunner.$anonfun$run$4(Executor.scala:636)
	at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally(SparkErrorUtils.scala:64)
	at org.apache.spark.util.SparkErrorUtils.tryWithSafeFinally$(SparkErrorUtils.scala:61)
	at org.apache.spark.util.Utils$.tryWithSafeFinally(Utils.scala:95)
	at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:639)
	at java.base/java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1128)
	at java.base/java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:628)
	at java.base/java.lang.Thread.run(Thread.java:829)
Caused by: org.apache.spark.SparkUpgradeException: [INCONSISTENT_BEHAVIOR_CROSS_VERSION.PARSE_DATETIME_BY_NEW_PARSER] You may get a different result due to the upgrading to Spark >= 3.0:
Fail to parse '2026-06-05 09:28:43.959135' in the new parser. You can set "spark.sql.legacy.timeParserPolicy" to "LEGACY" to restore the behavior before Spark 3.0, or set to "CORRECTED" and treat it as an invalid datetime string.
	at org.apache.spark.sql.errors.ExecutionErrors.failToParseDateTimeInNewParserError(ExecutionErrors.scala:54)
	at org.apache.spark.sql.errors.ExecutionErrors.failToParseDateTimeInNewParserError$(ExecutionErrors.scala:48)
	at org.apache.spark.sql.errors.ExecutionErrors$.failToParseDateTimeInNewParserError(ExecutionErrors.scala:218)
	at org.apache.spark.sql.catalyst.util.DateTimeFormatterHelper$$anonfun$checkParsedDiff$1.applyOrElse(DateTimeFormatterHelper.scala:142)
	at 
