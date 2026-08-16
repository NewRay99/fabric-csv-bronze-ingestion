import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).resolve().with_name("_gold_fact_sql.sql")
notebook = json.loads((ROOT / "04_gold_model 02 03.ipynb").read_text(encoding="utf-8"))
source = "".join(notebook["cells"][4]["source"])
start = source.find('spark.sql(f"""') + len('spark.sql(f"""')
end = source.rfind('""")')
body = source[start:end].strip() + "\n"
OUTPUT.write_text(body, encoding="utf-8")
print("written", len(body), "chars to", OUTPUT)
