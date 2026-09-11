from notebook_loader import load_notebook as read_notebook
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path(__file__).resolve().with_name("_gold_fact_sql.sql")
notebook = read_notebook(ROOT / "04_gold_model.py")
source = "".join(notebook["cells"][4]["source"])
start = source.find('spark.sql(f"""') + len('spark.sql(f"""')
end = source.rfind('""")')
body = source[start:end].strip() + "\n"
OUTPUT.write_text(body, encoding="utf-8")
print("written", len(body), "chars to", OUTPUT)
