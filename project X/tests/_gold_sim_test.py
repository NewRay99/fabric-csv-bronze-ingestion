"""
Local simulation test for 04_gold_model.py.

Fabricates 3 months of flattened Silver-layer data (referral, referral_enrichment,
referral_person, referral_closure_reason_summary) that mimics what the Silver
materialisations and the archive replay would produce: new referrals each month
plus in-month updates, spread across multiple months. The enrichment rows are
derived from fabricated referral_provider/offer/ipa records using the GLD-009 /
GLD-011 business rules, so the simulation also exercises the propagated
is_open / is_awaiting_offer / is_spot flags. Then runs the gold model SQL logic
against it for each month-end as-of date and validates the output.
"""
import os, sys, uuid, random
sys.setrecursionlimit(100000)
from datetime import date, datetime, timedelta

os.environ["JAVA_HOME"] = r"C:\Program Files\Eclipse Adoptium\jre-17.0.20.8-hotspot"
os.environ["HADOOP_HOME"] = r"C:\hadoop"
os.environ["PATH"] = r"C:\hadoop\bin;" + os.environ.get("PATH", "")
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip
from pyspark.sql import functions as F

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
WAREHOUSE = os.path.join(TEST_ROOT, "_gold_sim_warehouse")
builder = (SparkSession.builder.master("local[2]")
    .appName("gold-sim")
    .config("spark.sql.warehouse.dir", WAREHOUSE)
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.driver.memory", "2g"))
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
print("Spark", spark.version, "started")

random.seed(42)
MONTHS = [date(2025, 1, 31), date(2025, 2, 28), date(2025, 3, 31)]  # 3 month-ends

def ts(d, h=9, m=0):
    return datetime(d.year, d.month, d.day, h, m)

referrals = []   # flattened referral rows, including later versions for test coverage
providers = []   # referral_provider (feeds the fabricated enrichment)
offers = []      # offer (feeds the fabricated enrichment)
ipas = []        # ipa (feeds the fabricated enrichment)
cancel_reasons = []
decline_reasons = []
persons = []     # referral_person
closures = []    # referral_closure_reason_summary

provider_ids = [uuid.uuid4() for _ in range(3)]
home_ids = [uuid.uuid4() for _ in range(5)]

def add_referral(created, required_start, status="open", is_spot=False):
    rid = str(uuid.uuid4())
    referrals.append(dict(
        referral_id=rid, placement_type="FOSTER", is_spot=is_spot,
        required_start_date=required_start, response_required_by_date=required_start - timedelta(days=2),
        referral_created_date=ts(created), referral_modified_date=ts(created),
        referral_created_by=str(uuid.uuid4()), referral_updated_by=str(uuid.uuid4()), referral_status=status,
        export_date=ts(created)))
    persons.append(dict(person_id=str(uuid.uuid4()), referral_id=rid, child_index=0))
    return rid

def add_offer(rid, when, status="pending"):
    rp = str(uuid.uuid4())
    providers.append(dict(referral_provider_id=rp, referral_id=rid,
        provider_id=random.choice(provider_ids), is_excluded=False, is_declined=False,
        created_by="sim", modified_by="sim", created_date=ts(when, 9),
        modified_date=ts(when, 9), is_cancelled=False, is_closed=False,
        is_spot=False, export_date=ts(when)))
    oid = str(uuid.uuid4())
    offers.append(dict(offer_id=oid, referral_provider_id=rp, referral_id=rid,
        offer_status=status,
        provider_home_id=random.choice(home_ids), id_number="ID"+str(random.randint(1,999)),
        category=1, estimated_start_date=when + timedelta(days=7),
        core_weekly_fee=800.0, includes_education=False, education_weekly_fee=None,
        child_summary_needs="sim", offer_date=ts(when, 11), last_modified_date=ts(when, 12),
        decline_reason_other=None, decline_reason=None, can_edit_offer=True,
        withdraw_reason=None, offer_type="standard", category_code="A",
        export_date=ts(when, 12)))
    return oid

def add_ipa(rid, oid, when, admission):
    ipas.append(dict(ipa_id=str(uuid.uuid4()), offer_id=oid, referral_id=rid,
        placement_admission_date=admission, costs_total_weekly_fee=950.0,
        created_datetime=ts(when, 8), updated_datetime=ts(when, 8),
        status="issued", export_date=ts(when, 8)))

# --- Month 1 (Jan): 5 new referrals ---
jan = date(2025, 1, 10)
r1 = add_referral(jan, date(2025, 1, 12))            # critical, placed by target
o1 = add_offer(r1, date(2025,1,11), "accepted"); add_ipa(r1, o1, date(2025,1,11), date(2025,1,12))
r2 = add_referral(date(2025,1,12), date(2025,1,20))  # offer but no ipa -> open
add_offer(r2, date(2025,1,13), "pending")
# GLD-013: two extra distinct provider assignments (no offers) -> multiple providers
for extra_pid in provider_ids[1:]:
    providers.append(dict(referral_provider_id=str(uuid.uuid4()), referral_id=r2,
        provider_id=extra_pid, is_excluded=False, is_declined=False,
        created_by="sim", modified_by="sim", created_date=ts(date(2025,1,14), 9),
        modified_date=ts(date(2025,1,14), 9), is_cancelled=False, is_closed=False,
        is_spot=False, export_date=ts(date(2025,1,14))))
r3 = add_referral(date(2025,1,15), date(2025,2,10))  # planned, closes in Feb
r4 = add_referral(date(2025,1,20), date(2025,1,21))  # critical, no offer -> overdue
r5 = add_referral(date(2025,1,25), date(2025,3,1))   # planned, placed after target in Mar

# --- Month 2 (Feb): 4 new + updates to month-1 referrals ---
feb = date(2025, 2, 5)
r6 = add_referral(feb, date(2025,2,6))               # critical placed by target
o6 = add_offer(r6, date(2025,2,6), "accepted"); add_ipa(r6, o6, date(2025,2,6), date(2025,2,6))
# GLD-014: the referral-level source flag is stale/false while the linked
# provider assignment is spot.  The Gold fact must use the provider value.
r7 = add_referral(date(2025,2,10), date(2025,2,25), is_spot=False)
providers.append(dict(referral_provider_id=str(uuid.uuid4()), referral_id=r7,
    provider_id=random.choice(provider_ids), is_excluded=False, is_declined=False,
    created_by="sim", modified_by="sim", created_date=ts(date(2025,2,10), 9),
    modified_date=ts(date(2025,2,10), 9), is_cancelled=False, is_closed=True,
    is_spot=True, export_date=ts(date(2025,2,10))))
r8 = add_referral(date(2025,2,12), date(2025,3,15))  # planned
r9 = add_referral(date(2025,2,20), date(2025,2,22))  # critical, closed without placement in Mar
# in-month update: close r3 (created Jan) -> new flattened version in Feb
referrals.append(dict(
    referral_id=r3, placement_type="FOSTER", is_spot=False,
    required_start_date=date(2025,2,10),
    response_required_by_date=date(2025,2,8), referral_created_date=ts(date(2025,1,15)),
    referral_modified_date=ts(date(2025,2,15), 14), referral_created_by=uuid.uuid4(), referral_updated_by=uuid.uuid4(),
    referral_status="completed", export_date=ts(date(2025,2,15), 14)))
closures.append(dict(referral_id=r3, closed_referral_reason_bucket="Closed/Withdrawn"))

# --- Month 3 (Mar): 3 new + updates ---
mar = date(2025, 3, 5)
r10 = add_referral(mar, date(2025,3,6))
o10 = add_offer(r10, date(2025,3,6), "accepted"); add_ipa(r10, o10, date(2025,3,6), date(2025,3,6))
r11 = add_referral(date(2025,3,10), date(2025,3,30))
r12 = add_referral(date(2025,3,12), date(2025,4,1))
# r5 placed after target (IPA issued after required_start_date 2025-03-01)
o5 = add_offer(r5, date(2025,3,3), "accepted"); add_ipa(r5, o5, date(2025,3,3), date(2025,3,5))
# r9 closed without placement in Mar
referrals.append(dict(
    referral_id=r9, placement_type="FOSTER", is_spot=False,
    required_start_date=date(2025,2,22),
    response_required_by_date=date(2025,2,20), referral_created_date=ts(date(2025,2,20)),
    referral_modified_date=ts(date(2025,3,10), 14), referral_created_by=uuid.uuid4(), referral_updated_by=uuid.uuid4(),
    referral_status="cancelled", export_date=ts(date(2025,3,10), 14)))
closures.append(dict(referral_id=r9, closed_referral_reason_bucket="Cancelled"))

print(f"Fabricated: {len(referrals)} flattened referral rows, {len(providers)} providers, "
      f"{len(offers)} offers, {len(ipas)} ipas")

# --- Derive silver.referral_enrichment rows (mirrors 03_silver_business_rules) ---
CLOSED_STATUSES = {"CLOSED", "CANCELLED", "WITHDRAWN", "COMPLETED"}
latest_export = max(r["export_date"] for r in referrals).date()
current = {}
for row in referrals:
    key = row["referral_id"]
    if key not in current or (row["referral_modified_date"], row["export_date"]) > (
            current[key]["referral_modified_date"], current[key]["export_date"]):
        current[key] = row

enrichment = []
for rid, r in current.items():
    rps = [p for p in providers if p["referral_id"] == rid]
    rp_ids = {p["referral_provider_id"] for p in rps}
    r_offers = [o for o in offers if o["referral_provider_id"] in rp_ids]
    r_ipas = [i for i in ipas if i["referral_id"] == rid]
    live = any(not p["is_closed"] and not p["is_declined"]
               and not p["is_excluded"] and not p["is_cancelled"] for p in rps)
    engaged = any(not p["is_cancelled"] and not p["is_closed"]
                  and not p["is_excluded"] for p in rps)
    status = (r["referral_status"] or "").upper()
    response_date = r["response_required_by_date"]
    in_window = response_date is not None and response_date >= latest_export
    # GLD-009 business rule
    is_open = (status in ("OPEN", "UNDER_OFFER")
               and (live or status == "UNDER_OFFER" or (status == "OPEN" and in_window)))
    # GLD-011 business rule
    is_awaiting_offer = status == "OPEN" and (engaged or in_window)
    activity = ([r["referral_modified_date"]] if r["referral_modified_date"] > r["referral_created_date"] else [])
    activity += [o["offer_date"] for o in r_offers] + [o["last_modified_date"] for o in r_offers]
    activity += [i["created_datetime"] for i in r_ipas] + [i["updated_datetime"] for i in r_ipas]
    accepted = [o for o in r_offers if o["offer_status"] in ("accepted", "approved", "selected", "offer_successful")]
    enrichment.append(dict(
        referral_id=rid,
        referral_created_date=r["referral_created_date"],
        cnt_offer_made=len(r_offers),
        unique_homes_offered=len({o["provider_home_id"] for o in r_offers}),
        estimated_weekly_cost=sum(i["costs_total_weekly_fee"] for i in r_ipas) if r_ipas else None,
        first_action_date=min(activity) if activity else None,
        first_offer_date=min((o["offer_date"] for o in r_offers), default=None),
        offer_accepted_date=min((o["last_modified_date"] for o in accepted), default=None),
        ipa_issued_date=min((i["created_datetime"] for i in r_ipas), default=None),
        referral_closed_date=(r["referral_modified_date"] if status in CLOSED_STATUSES else None),
        last_activity_date=max(activity) if activity else r["referral_modified_date"],
        first_provider_seen_date=min((p["export_date"] for p in rps), default=None),
        is_not_seen_by_providers=not rps,
        ipa_placement_admission_date=min(
            (ts(i["placement_admission_date"]) if isinstance(i["placement_admission_date"], date)
             and not isinstance(i["placement_admission_date"], datetime)
             else i["placement_admission_date"] for i in r_ipas), default=None),
        ipa_2_signatures=False,
        ipa_last_signature_date=None,
        ipa_due_diligence_min_review_date=None,
        is_open=is_open,
        is_awaiting_offer=is_awaiting_offer,
        # GLD-014: fact_referral has one row per referral, so any spot
        # provider assignment makes the referral spot.
        is_spot=any(bool(p["is_spot"]) for p in rps),
        # GLD-013: distinct providers assigned to the referral
        provider_assignment_count=len({p["provider_id"] for p in rps}),
    ))

spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")

def write(df, name):
    df.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable(f"silver.{name}")

import json as _json
def clean(rows):
    # PySpark cannot infer uuid.UUID; convert to str
    out = []
    for r in rows:
        out.append({k: (str(v) if isinstance(v, uuid.UUID) else v) for k, v in r.items()})
    return out

_tmp_dirs = []
def mkdf(rows):
    # Avoid cloudpickle recursion on Python 3.14 by writing JSON and reading it back
    data = clean(rows)
    d = os.path.abspath(f"_sim_{uuid.uuid4().hex}")
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "part.json"), "w", encoding="utf-8") as f:
        for r in data:
            f.write(_json.dumps(r, default=str) + "\n")
    _tmp_dirs.append(d)
    return spark.read.json("file:///" + d.replace("\\", "/"))

write(mkdf(referrals), "referral")
write(spark.createDataFrame([], "referral_id string, framework_category_id int"), "referral_category")
write(spark.createDataFrame([], "referral_id string, location string, location_match_status string, "
                           "location_is_default boolean, location_requires_review boolean"), "referral_location")
write(mkdf(enrichment), "referral_enrichment")
write(mkdf(persons), "referral_person")
write(mkdf(closures), "referral_closure_reason_summary")
write(mkdf(providers), "referral_provider")
write(mkdf(offers), "offer")
# Keep both reason-event sources present. The response rule uses their
# timestamps conservatively and does not require a reason on every assignment.
r2_response_provider = next(
    offer["referral_provider_id"] for offer in offers if offer["referral_id"] == r2
)
cancel_reasons.append(dict(
    referral_provider_id=r2_response_provider,
    created_date=ts(date(2025, 1, 14), 10),
    export_date=ts(date(2025, 1, 14), 10),
))
decline_reasons.append(dict(
    referral_provider_id=r2_response_provider,
    created_date=ts(date(2025, 1, 15), 10),
    export_date=ts(date(2025, 1, 15), 10),
))
write(mkdf(cancel_reasons), "referral_provider_cancel_reason")
write(mkdf(decline_reasons), "referral_provider_decline_reason")
print("Silver tables written")

GOLD_FACT_SQL = open(os.path.join(TEST_ROOT, "_gold_fact_sql.sql"), encoding="utf-8").read()

def run_gold(as_of):
    as_of_sql = f"DATE '{as_of.isoformat()}'"
    spark.sql(GOLD_FACT_SQL.format(
        AS_OF_SQL=as_of_sql,
        GOLD_JOB_RUN_ID="gold-simulation",
    ))
    snapshot = spark.table("gold.fact_referral").select(
        F.lit(as_of).cast("date").alias("snapshot_date"),
        "referral_id", "current_status", "placement_urgency_band", "required_placement_date",
        "is_open", "is_awaiting_offer", "is_spot", "has_offer", "offer_count", "days_open",
        "provider_assignment_count", "provider_responded_count", "has_provider_response",
        "first_provider_response_date", "is_emergency_placement", "is_open_overdue",
        "days_without_activity", "days_past_required_date", "placed_by_required_date",
        "required_placement_date_outcome")
    snap_table = "gold.fact_referral_snapshot"
    if not spark.catalog.tableExists(snap_table):
        snapshot.write.format("delta").mode("overwrite").saveAsTable(snap_table)
    else:
        from delta.tables import DeltaTable
        t = DeltaTable.forName(spark, snap_table)
        (t.alias("t").merge(snapshot.alias("s"),
            "t.snapshot_date = s.snapshot_date AND t.referral_id = s.referral_id")
            .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
    return spark.table("gold.fact_referral")

results = {}
for me in MONTHS:
    df = run_gold(me)
    results[me] = df
    n = df.count()
    print(f"\n=== Gold as-of {me}: {n} referrals ===")
    df.groupBy("required_placement_date_outcome").count().orderBy("required_placement_date_outcome").show(truncate=False)
    df.groupBy("placement_urgency_band").count().orderBy("placement_urgency_band").show(truncate=False)

print("\n=== VALIDATION ===")
failures = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: failures.append(msg)

jan_df = results[date(2025,1,31)]
r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12 = map(str,[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
out = {row.referral_id: row for row in jan_df.collect()}
check(out[r1].required_placement_date_outcome == "Placed by target", "r1 placed by target (Jan)")
check(out[r1].placed_by_required_date == True, "r1 placed_by_required_date true")
check(out[r4].required_placement_date_outcome == "Open overdue", "r4 open overdue (Jan, required 1/21 < 1/31)")
check(out[r4].days_past_required_date == 10, f"r4 10 days past required (got {out[r4].days_past_required_date})")
check(out[r2].has_offer == True and out[r2].is_open == True, "r2 has offer and open (live provider branch)")
check(out[r2].has_provider_response == True, "r2 has qualifying provider response evidence")
check(out[r2].is_awaiting_offer == True, "r2 awaiting offer (open with engaged provider)")
# GLD-013: pushed-down referral-grain columns
check(out[r2].provider_assignment_count >= 2,
      f"r2 has multiple provider assignments (got {out[r2].provider_assignment_count})")
check(out[r2].is_open_overdue == True, "r2 open overdue (open, required 1/20 < as-of 1/31)")
check(out[r2].is_emergency_placement == False, "r2 not emergency (8-day lead)")
check(out[r1].provider_assignment_count == 1, "r1 single provider assignment")
check(out[r3].is_open_overdue == False, "r3 not open overdue (required 2/10 >= as-of 1/31)")
# GLD-009: r4 has no provider engagement and its response window (1/19) closed
# before the latest export (3/10), so the original business rule says NOT open.
check(out[r4].is_open == False, "r4 not open under GLD-009 rule (no engagement, expired response window)")
check(out[r4].is_awaiting_offer == False, "r4 not awaiting offer")
# r1: created 1/10, required 1/12 -> 2 days -> High (Critical needs <=1)
check(out[r1].placement_urgency_band == "High", f"r1 urgency High (2 days, got {out[r1].placement_urgency_band})")
# r2: created 1/12, required 1/20 -> 8 days -> Planned (Medium needs <=7)
check(out[r2].placement_urgency_band == "Planned", f"r2 urgency Planned (8 days, got {out[r2].placement_urgency_band})")
check(out[r5].placement_urgency_band == "Planned", "r5 urgency Planned")

feb_df = results[date(2025,2,28)]
out_f = {row.referral_id: row for row in feb_df.collect()}
check(out_f[r3].is_open == False, "r3 closed in Feb")
check(out_f[r3].is_awaiting_offer == False, "r3 not awaiting offer (completed)")
check(out_f[r3].required_placement_date_outcome == "Closed without placement", "r3 closed without placement")
check(out_f[r6].required_placement_date_outcome == "Placed by target", "r6 placed by target (Feb)")
check(out_f[r4].required_placement_date_outcome == "Open overdue", "r4 still open overdue (Feb)")
check(feb_df.count() == 9, f"Feb has 9 referrals (got {feb_df.count()})")
# GLD-014: r7 has a false referral source flag but a true provider flag.
check(out_f[r7].is_spot == True, "r7 is_spot true from referral_provider (GLD-014)")
check(out_f[r6].is_spot == False, "r6 is_spot false")
# GLD-009: r7 has no provider engagement and its response window (2/23) expired
check(out_f[r7].is_open == False, "r7 not open under GLD-009 rule (spot, no engagement, expired window)")

mar_df = results[date(2025,3,31)]
out_m = {row.referral_id: row for row in mar_df.collect()}
check(mar_df.count() == 12, f"Mar has 12 referrals (got {mar_df.count()})")
check(out_m[r5].required_placement_date_outcome == "Placed after target", "r5 placed after target (IPA 3/3 > required 3/1)")
check(out_m[r5].placed_by_required_date == False, "r5 placed_by_required_date false")
check(out_m[r9].required_placement_date_outcome == "Closed without placement", "r9 closed without placement (Mar)")
check(out_m[r9].is_open == False, "r9 not open (cancelled)")
check(out_m[r10].required_placement_date_outcome == "Placed by target", "r10 placed by target (Mar)")
# GLD-009: r12 is OPEN with response window (3/30) on/after latest export (3/10)
check(out_m[r12].is_open == True, "r12 open under GLD-009 rule (inside response window)")
check(out_m[r12].is_awaiting_offer == True, "r12 awaiting offer (open, inside response window)")

snap = spark.table("gold.fact_referral_snapshot")
snap_dates = sorted(row.snapshot_date for row in snap.select("snapshot_date").distinct().collect())
check(snap_dates == MONTHS, f"snapshot has 3 month-end dates {snap_dates}")
check(snap.count() == 5 + 9 + 12, f"snapshot total rows {snap.count()} == 26")

spark.sql("""CREATE OR REPLACE VIEW gold.vw_kpi_referral_board_summary AS
SELECT as_of_date, placement_urgency_band, required_placement_date_outcome,
  COUNT(DISTINCT referral_id) AS referral_count,
  SUM(CASE WHEN is_open THEN 1 ELSE 0 END) AS open_referral_count,
  SUM(CASE WHEN is_open AND required_placement_date < as_of_date THEN 1 ELSE 0 END) AS open_overdue_count,
  SUM(CASE WHEN placed_by_required_date THEN 1 ELSE 0 END) AS placed_by_required_date_count,
  SUM(CASE WHEN has_offer THEN 1 ELSE 0 END) AS referrals_with_offer_count,
  PERCENTILE_APPROX(days_to_ipa, 0.5) AS median_days_to_ipa,
  SUM(COALESCE(estimated_weekly_cost, 0)) AS estimated_weekly_cost
FROM gold.fact_referral
GROUP BY as_of_date, placement_urgency_band, required_placement_date_outcome""")
kpi = spark.table("gold.vw_kpi_referral_board_summary")
check(kpi.count() > 0, "KPI board summary view returns rows")

print("\n" + ("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILURES"))
spark.stop()
sys.exit(1 if failures else 0)
