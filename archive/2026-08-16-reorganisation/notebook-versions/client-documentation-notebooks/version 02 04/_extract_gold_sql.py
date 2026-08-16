import json
nb = json.load(open(r"04_gold_model 02 03.ipynb", encoding="utf-8"))
src = "".join(nb["cells"][4]["source"])
# strip the leading `spark.sql(f"""` and trailing `""")`
start = src.find('spark.sql(f"""') + len('spark.sql(f"""')
end = src.rfind('""")')
body = src[start:end].strip() + "\n"
open("_gold_fact_sql.sql", "w", encoding="utf-8").write(body)
print("written", len(body), "chars")
print("HEAD:", body[:120])
print("TAIL:", body[-120:])
