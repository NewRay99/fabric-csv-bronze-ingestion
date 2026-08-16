# Fabric configuration files

Deploy these files to the configured Fabric Lakehouse location, normally
`Files/cfg_files/`:

- `schema_definition.csv` — approved column, type, PK, and FK contract;
- `dq_rule_definition.csv` — additional data-quality rules;
- `schema drift.xlsx` — review workbook comparing captured schemas.

The notebooks do not read these files from the Git repository at runtime. The
repository copy is the controlled source that must be published to Fabric.

