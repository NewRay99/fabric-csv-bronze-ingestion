"""
Local simulation test for 04_gold_model 02 03.ipynb.

Fabricates 3 months of Silver-layer data (referral_aud, referral_provider,
offer, ipa, referral_event_log) that mimics what the bronze->silver formatter
and the archive replay would produce: new referrals each month plus in-month
updates, spread across multiple months. Then runs the gold model SQL logic
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

WAREHOUSE = os.path.abspath("_gold_sim_warehouse")
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

referrals = []   # referral_aud rows (audit: one row per revision)
providers = []   # referral_provider
offers = []      # offer
ipas = []        # ipa
events = []      # referral_event_log

rev_counter = {}
event_id = 0
provider_ids = [uuid.uuid4() for _ in range(3)]
home_ids = [uuid.uuid4() for _ in range(5)]

def add_referral(created, required_start, status="open"):
    rid = str(uuid.uuid4())
    rev_counter[rid] = 0
    rev_counter[rid] += 1
    referrals.append(dict(id=uuid.uuid4(), rev=rev_counter[rid], revtype=0,
        referral_id=rid, placement_type_code="FOSTER",
        required_start_date=required_start, response_required_by_date=required_start - timedelta(days=2),
        created_timestamp=ts(created), modified_timestamp=ts(created),
        created_by=str(uuid.uuid4()), modified_by=str(uuid.uuid4()), status="open",
        export_date=ts(created)))
    return rid

def add_event(rid, when, etype="STATUS"):
    global event_id
    event_id += 1
    events.append(dict(event_id=event_id, referral_id=rid, event_type=etype,
        event_message="sim", event_username="sim", event_timestamp=ts(when, 10),
        sequence_number=event_id, created_by="sim", created_timestamp=ts(when, 10),
        export_date=ts(when, 10)))

def add_offer(rid, when, status="pending"):
    rp = str(uuid.uuid4())
    providers.append(dict(referral_provider_id=rp, referral_id=rid,
        provider_id=random.choice(provider_ids), is_excluded=False, is_declined=False,
        created_by="sim", modified_by="sim", is_cancelled=False, is_closed=False,
        is_spot=False, export_date=ts(when)))
    oid = str(uuid.uuid4())
    offers.append(dict(offer_id=oid, referral_provider_id=rp, offer_status=status,
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
add_event(r1, jan); o1 = add_offer(r1, date(2025,1,11), "accepted"); add_ipa(r1, o1, date(2025,1,11), date(2025,1,12))
r2 = add_referral(date(2025,1,12), date(2025,1,20))  # offer but no ipa -> open
add_event(r2, date(2025,1,12)); add_offer(r2, date(2025,1,13), "pending")
r3 = add_referral(date(2025,1,15), date(2025,2,10))  # planned, closes in Feb
add_event(r3, date(2025,1,15))
r4 = add_referral(date(2025,1,20), date(2025,1,21))  # critical, no offer -> overdue
add_event(r4, date(2025,1,20))
r5 = add_referral(date(2025,1,25), date(2025,3,1))   # planned, placed after target in Mar
add_event(r5, date(2025,1,25))

# --- Month 2 (Feb): 4 new + updates to month-1 referrals ---
feb = date(2025, 2, 5)
r6 = add_referral(feb, date(2025,2,6))               # critical placed by target
add_event(r6, feb); o6 = add_offer(r6, date(2025,2,6), "accepted"); add_ipa(r6, o6, date(2025,2,6), date(2025,2,6))
r7 = add_referral(date(2025,2,10), date(2025,2,25))  # high, open
add_event(r7, date(2025,2,10))
r8 = add_referral(date(2025,2,12), date(2025,3,15))  # planned
add_event(r8, date(2025,2,12))
r9 = add_referral(date(2025,2,20), date(2025,2,22))  # critical, closed without placement in Mar
add_event(r9, date(2025,2,20))
# in-month update: close r3 (created Jan) -> new audit revision in Feb
rev_counter[r3] += 1
referrals.append(dict(id=uuid.uuid4(), rev=rev_counter[r3], revtype=1,
    referral_id=r3, placement_type_code="FOSTER", required_start_date=date(2025,2,10),
    response_required_by_date=date(2025,2,8), created_timestamp=ts(date(2025,1,15)),
    modified_timestamp=ts(date(2025,2,15), 14), created_by=uuid.uuid4(), modified_by=uuid.uuid4(),
    status="completed", export_date=ts(date(2025,2,15), 14)))
add_event(r3, date(2025,2,15), "CLOSE")

# --- Month 3 (Mar): 3 new + updates ---
mar = date(2025, 3, 5)
r10 = add_referral(mar, date(2025,3,6))
add_event(r10, mar); o10 = add_offer(r10, date(2025,3,6), "accepted"); add_ipa(r10, o10, date(2025,3,6), date(2025,3,6))
r11 = add_referral(date(2025,3,10), date(2025,3,30))
add_event(r11, date(2025,3,10))
r12 = add_referral(date(2025,3,12), date(2025,4,1))
add_event(r12, date(2025,3,12))
# r5 placed after target (IPA issued after required_start_date 2025-03-01)
o5 = add_offer(r5, date(2025,3,3), "accepted"); add_ipa(r5, o5, date(2025,3,3), date(2025,3,5))
# r9 closed without placement in Mar
rev_counter[r9] += 1
referrals.append(dict(id=uuid.uuid4(), rev=rev_counter[r9], revtype=1,
    referral_id=r9, placement_type_code="FOSTER", required_start_date=date(2025,2,22),
    response_required_by_date=date(2025,2,20), created_timestamp=ts(date(2025,2,20)),
    modified_timestamp=ts(date(2025,3,10), 14), created_by=uuid.uuid4(), modified_by=uuid.uuid4(),
    status="cancelled", export_date=ts(date(2025,3,10), 14)))
add_event(r9, date(2025,3,10), "CLOSE")

print(f"Fabricated: {len(referrals)} referral_aud rows, {len(providers)} providers, "
      f"{len(offers)} offers, {len(ipas)} ipas, {len(events)} events")

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

write(mkdf(referrals), "slv_referral_aud")
write(mkdf(providers), "slv_referral_provider")
write(mkdf(offers), "slv_offer")
write(mkdf(ipas), "slv_ipa")
write(mkdf(events), "slv_referral_event_log")
print("Silver tables written")

GOLD_FACT_SQL = open("_gold_fact_sql.sql", encoding="utf-8").read()

def run_gold(as_of):
    as_of_sql = f"DATE '{as_of.isoformat()}'"
    spark.sql(GOLD_FACT_SQL.format(AS_OF_SQL=as_of_sql))
    snapshot = spark.table("gold.fact_referral").select(
        F.lit(as_of).cast("date").alias("SnapshotDate"),
        "ReferralID", "CurrentStatus", "PlacementUrgencyBand", "RequiredPlacementDate",
        "IsOpen", "HasOffer", "OfferCount", "DaysOpen", "DaysWithoutActivity",
        "DaysPastRequiredDate", "PlacedByRequiredDate", "RequiredPlacementDateOutcome")
    snap_table = "gold.fact_referral_snapshot"
    if not spark.catalog.tableExists(snap_table):
        snapshot.write.format("delta").mode("overwrite").saveAsTable(snap_table)
    else:
        from delta.tables import DeltaTable
        t = DeltaTable.forName(spark, snap_table)
        (t.alias("t").merge(snapshot.alias("s"),
            "t.SnapshotDate = s.SnapshotDate AND t.ReferralID = s.ReferralID")
            .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
    return spark.table("gold.fact_referral")

results = {}
for me in MONTHS:
    df = run_gold(me)
    results[me] = df
    n = df.count()
    print(f"\n=== Gold as-of {me}: {n} referrals ===")
    df.groupBy("RequiredPlacementDateOutcome").count().orderBy("RequiredPlacementDateOutcome").show(truncate=False)
    df.groupBy("PlacementUrgencyBand").count().orderBy("PlacementUrgencyBand").show(truncate=False)

print("\n=== VALIDATION ===")
failures = []
def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond: failures.append(msg)

jan_df = results[date(2025,1,31)]
r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12 = map(str,[r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12])
out = {row.ReferralID: row for row in jan_df.collect()}
check(out[r1].RequiredPlacementDateOutcome == "Placed by target", "r1 placed by target (Jan)")
check(out[r1].PlacedByRequiredDate == True, "r1 PlacedByRequiredDate true")
check(out[r4].RequiredPlacementDateOutcome == "Open overdue", "r4 open overdue (Jan, required 1/21 < 1/31)")
check(out[r4].DaysPastRequiredDate == 10, f"r4 10 days past required (got {out[r4].DaysPastRequiredDate})")
check(out[r2].HasOffer == True and out[r2].IsOpen == True, "r2 has offer and open")
# r1: created 1/10, required 1/12 -> 2 days -> High (Critical needs <=1)
check(out[r1].PlacementUrgencyBand == "High", f"r1 urgency High (2 days, got {out[r1].PlacementUrgencyBand})")
# r2: created 1/12, required 1/20 -> 8 days -> Planned (Medium needs <=7)
check(out[r2].PlacementUrgencyBand == "Planned", f"r2 urgency Planned (8 days, got {out[r2].PlacementUrgencyBand})")
check(out[r5].PlacementUrgencyBand == "Planned", "r5 urgency Planned")

feb_df = results[date(2025,2,28)]
out_f = {row.ReferralID: row for row in feb_df.collect()}
check(out_f[r3].IsOpen == False, "r3 closed in Feb")
check(out_f[r3].RequiredPlacementDateOutcome == "Closed without placement", "r3 closed without placement")
check(out_f[r6].RequiredPlacementDateOutcome == "Placed by target", "r6 placed by target (Feb)")
check(out_f[r4].RequiredPlacementDateOutcome == "Open overdue", "r4 still open overdue (Feb)")
check(feb_df.count() == 9, f"Feb has 9 referrals (got {feb_df.count()})")

mar_df = results[date(2025,3,31)]
out_m = {row.ReferralID: row for row in mar_df.collect()}
check(mar_df.count() == 12, f"Mar has 12 referrals (got {mar_df.count()})")
check(out_m[r5].RequiredPlacementDateOutcome == "Placed after target", "r5 placed after target (IPA 3/3 > required 3/1)")
check(out_m[r5].PlacedByRequiredDate == False, "r5 PlacedByRequiredDate false")
check(out_m[r9].RequiredPlacementDateOutcome == "Closed without placement", "r9 closed without placement (Mar)")
check(out_m[r10].RequiredPlacementDateOutcome == "Placed by target", "r10 placed by target (Mar)")

snap = spark.table("gold.fact_referral_snapshot")
snap_dates = sorted(row.SnapshotDate for row in snap.select("SnapshotDate").distinct().collect())
check(snap_dates == MONTHS, f"snapshot has 3 month-end dates {snap_dates}")
check(snap.count() == 5 + 9 + 12, f"snapshot total rows {snap.count()} == 26")

spark.sql("""CREATE OR REPLACE VIEW gold.vw_kpi_referral_board_summary AS
SELECT AsOfDate, PlacementUrgencyBand, RequiredPlacementDateOutcome,
  COUNT(DISTINCT ReferralID) AS ReferralCount,
  SUM(CASE WHEN IsOpen THEN 1 ELSE 0 END) AS OpenReferralCount,
  SUM(CASE WHEN IsOpen AND RequiredPlacementDate < AsOfDate THEN 1 ELSE 0 END) AS OpenOverdueCount,
  SUM(CASE WHEN PlacedByRequiredDate THEN 1 ELSE 0 END) AS PlacedByRequiredDateCount,
  SUM(CASE WHEN HasOffer THEN 1 ELSE 0 END) AS ReferralsWithOfferCount,
  PERCENTILE_APPROX(DaysToIPA, 0.5) AS MedianDaysToIPA,
  SUM(COALESCE(EstimatedWeeklyCost, 0)) AS EstimatedWeeklyCost
FROM gold.fact_referral
GROUP BY AsOfDate, PlacementUrgencyBand, RequiredPlacementDateOutcome""")
kpi = spark.table("gold.vw_kpi_referral_board_summary")
check(kpi.count() > 0, "KPI board summary view returns rows")

print("\n" + ("ALL CHECKS PASSED" if not failures else f"{len(failures)} FAILURES"))
spark.stop()
sys.exit(1 if failures else 0)
