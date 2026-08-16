# Notebook regression checks

The `validate_*.py` files perform portable static checks on the active notebooks
and configuration contract. Run them from the `project X` folder or adjust the
working directory/path assumptions if required.

`_gold_sim_test.py` requires PySpark/Delta dependencies and may need to run in a
compatible Spark environment. End-to-end notebook orchestration remains a
Fabric acceptance test.

