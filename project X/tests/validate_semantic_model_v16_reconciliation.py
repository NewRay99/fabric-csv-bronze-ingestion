"""Validate the repeatable v16 semantic-model reconciliation contract."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "reports/current/SM WMPP v16 updated/SM_WMPP_v16.SemanticModel/definition"
REPORT = ROOT / "reports/current/SM WMPP v16 updated/SM_WMPP_v16.Report/definition"
GOLD = (ROOT / "04_gold_model.py").read_text(encoding="utf-8-sig")
DIMENSIONS = (ROOT / "05_gold_dimensions.py").read_text(encoding="utf-8-sig")
SETUP = (ROOT / "00_setup_cfg.py").read_text(encoding="utf-8-sig")

assert MODEL.is_dir(), "Reconciled v16 semantic model is missing"
model = (MODEL / "model.tmdl").read_text(encoding="utf-8-sig")
relationships = (MODEL / "relationships.tmdl").read_text(encoding="utf-8-sig")
tables = {path.stem: path.read_text(encoding="utf-8-sig")
          for path in (MODEL / "tables").glob("*.tmdl")}

assert "__PBI_TimeIntelligenceEnabled = 0" in model
assert "LocalDateTable_" not in model and "DateTableTemplate_" not in model
assert not list((MODEL / "tables").glob("LocalDateTable_*.tmdl"))
assert not list((MODEL / "tables").glob("DateTableTemplate_*.tmdl"))
assert "variation Variation" not in "\n".join(tables.values())
assert "bothDirections" not in relationships
assert "mode: directQuery" not in "\n".join(tables.values())

required_tables = {
    "dim_snapshot_month", "bridge_provider_home_framework_category",
    "fact_provider_kpi_monthly", "fact_referral_global_summary",
    "dim_security_scope", "sec_user_scope_access", "bridge_referral_scope",
}
assert required_tables <= tables.keys()
for table_name in required_tables:
    assert f"ref table {table_name}" in model

assert "fact_referral_snapshot.snapshot_month_start" in relationships
assert "toColumn: dim_snapshot_month.month_start" in relationships
assert "fact_referral_snapshot.referral_id\n\ttoColumn: fact_referral.referral_id" not in relationships
assert "fact_referral.placement_type_required" in relationships
assert "fact_referral_snapshot.placement_type_required" in relationships

role = MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
assert role.exists()
role_text = role.read_text(encoding="utf-8-sig")
assert "USERPRINCIPALNAME" in role_text
assert "tablePermission fact_referral" in role_text
assert "tablePermission fact_referral_snapshot" in role_text
assert "tablePermission fact_provider_kpi_monthly" in role_text
assert "fact_referral_global_summary" not in role_text

measures = tables["_Measures"]
for required_measure in {
    "Open Referrals at Snapshot", "Active Provider Response Rate at Snapshot",
    "Provider Response Rate", "Provider Offer Conversion Rate",
    "Provider Target Placement Rate", "Provider Average Response Hours",
    "Offers in Draft (Under Offer Referrals)",
    "Spot Offers (Under Offer Referrals)",
    "Successful Offers (Under Offer Referrals)",
}:
    assert re.search(rf"^\tmeasure '{re.escape(required_measure)}'", measures, re.MULTILINE)

report_text = "\n".join(
    path.read_text(encoding="utf-8-sig") for path in REPORT.rglob("*.json")
)
assert "Referral Closure Reason Summary_old" not in report_text
assert '"Entity": "dim_referral"' not in report_text
assert '"Property": "Closed Referral Reason Bucket"' not in report_text
assert report_text.count('"Property": "referral_closure_reason"') >= 23

for expected in {
    "snapshot_month_start", "snapshot_rule_version", "has_provider_response",
    "CREATE OR REPLACE TABLE gold.fact_referral_global_summary",
    "CREATE OR REPLACE TABLE gold.fact_provider_kpi_monthly",
}:
    assert expected in GOLD
assert "gold.bridge_provider_home_framework_category" in DIMENSIONS
assert "gold.dim_snapshot_month" in DIMENSIONS
assert "monitoring.cfg_security_scope" in SETUP
assert "monitoring.cfg_user_scope_access" in SETUP
assert "monitoring.cfg_referral_scope" in SETUP

print(f"PASS reconciled v16 model: {len(tables)} tables, RLS, snapshots and report bindings")
