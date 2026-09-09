"""Generate the KPI-01..117 as-is -> Gold requirement mapping section for
04_Data_and_Reporting/KPI_Reference_Guide.md.

Joins the parsed as-is KPI inventory (C:/tmp/kpi_rows.json) with the settled
Gold disposition for each KPI (from GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md and
GOLD_DAX_FIELD_COVERAGE_AUDIT.md rev 3).
"""
import json
import re

rows = json.load(open("C:/tmp/kpi_rows.json", encoding="utf-8"))

# kpi_num -> (gold objects, gold measure / disposition note, status)
# status: C = covered, A = alias, X = proxy, R = retired, B = blocked
M = {
    1: ("`fact_referral`", "Total Referrals", "C"),
    2: ("`fact_referral` + `fact_offer`", "Referrals With an Offer", "C"),
    3: ("`fact_referral` + `fact_offer`", "Referrals Awaiting Offer", "C"),
    4: ("`fact_referral[person_id]` → `dim_person[gender_clean]` (GLD-006/007)", "Male Referrals", "C"),
    5: ("`fact_referral[person_id]` → `dim_person[gender_clean]`", "Female Referrals", "C"),
    6: ("`fact_referral[person_id]` → `dim_person[gender_clean]`", "Other Gender Referrals", "C"),
    7: ("`fact_referral[person_id]` → `dim_person[gender_clean]`", "Total Gendered Referrals", "C"),
    8: ("`fact_referral` + `dim_date`", "Referrals Not Yet Closed (Created in Period)", "C"),
    9: ("`fact_referral` + `fact_offer` + `dim_date`", "Referrals With Offers (Created in Period)", "C"),
    10: ("`fact_referral` + `fact_offer` + `dim_date`", "Offer Receipt Rate (Created in Period)", "C"),
    11: ("`fact_offer`", "Providers Who Made Offers", "C"),
    12: ("`fact_offer`", "Offers Submitted", "A"),
    13: ("`fact_offer` + `fact_referral`", "Average Offers per Referral Under Offer", "C"),
    14: ("`fact_offer`", "Average Offers per Provider (Under Offer Referrals)", "C"),
    15: ("`fact_offer` + `dim_offer_status`", "Successful Offers (Under Offer Referrals)", "C"),
    16: ("`fact_offer` + `dim_offer_status`", "Unsuccessful Offers", "C"),
    17: ("`fact_offer` + `dim_offer_status`", "Offers in Draft", "C"),
    18: ("`fact_offer` + `dim_offer_status`", "Pending Offers (Under Offer Referrals)", "C"),
    19: ("`fact_referral` + `fact_referral_provider`", "Active Referrals With Provider Engagement", "C"),
    20: ("`fact_referral` + `fact_referral_provider`", "Active Referral Engagement Rate", "C"),
    21: ("`fact_referral` + `fact_referral_provider`", "Active Referrals With Provider Engagement", "A"),
    22: ("`fact_referral` + `fact_referral_provider`", "Active Awaiting Offers Without Engagement", "A"),
    23: ("`fact_referral` + `dim_date`", "Referrals Created This Month", "A"),
    24: ("`fact_referral` + `dim_date`", "Referrals Created This Financial Year", "A"),
    25: ("`fact_offer`", "Offers Submitted", "A"),
    26: ("`fact_referral`", "Total Referrals + `fact_referral[placement_type_required]` visual dimension", "A"),
    27: ("`fact_offer`", "Spot Offers", "C"),
    28: ("`fact_offer`", "Offers Submitted", "A"),
    29: ("`fact_referral` + `dim_referral_status`", "Referrals Currently Active", "C"),
    30: ("`fact_referral` + `fact_offer`", "Referrals Under Offer", "C"),
    31: ("`fact_referral` + `dim_referral_status`", "Closed or Cancelled Referrals", "C"),
    32: ("`fact_referral` + `fact_offer`", "Referrals Awaiting Offer", "A"),
    33: ("`fact_referral` + `fact_offer`", "Referrals With an Offer", "A"),
    34: ("`fact_referral`", "Closed Referrals + `fact_referral[referral_closure_reason]` visual dimension", "C"),
    35: ("`fact_offer`", "Offers on Referrals Under Offer", "C"),
    36: ("—", "Retired — internal CALCULATETABLE helper; Gold relationship graph + TREATAS make it unnecessary", "R"),
    37: ("`fact_offer`", "Offers per Provider (Under Offer Referrals)", "C"),
    38: ("`fact_offer` (framework flag)", "Framework Offers (Under Offer Referrals)", "C"),
    39: ("—", "Retired — internal scoped-table helper (see KPI-36)", "R"),
    40: ("`dim_provider_home`", "Provider Homes Registered", "C"),
    41: ("`dim_provider`", "Providers Registered", "C"),
    42: ("`dim_provider` + `dim_provider_home`", "Providers - Fostering", "C"),
    43: ("`dim_provider` + `dim_provider_home`", "Providers - Residential", "C"),
    44: ("`dim_provider` + `dim_provider_home`", "Providers - Supported Accommodation", "C"),
    45: ("`dim_provider` + `bridge_provider_framework` + `dim_framework`", "Framework Providers", "C"),
    46: ("`dim_provider` + `bridge_provider_framework`", "Non-Framework Providers", "C"),
    47: ("`dim_provider` + `bridge_provider_framework`", "Is Non Framework Provider (row helper)", "C"),
    48: ("—", "Retired — depended on report-view axis tables; rebuild with field parameters over `dim_provider_home[service_type]` if needed", "R"),
    49: ("`dim_provider_home`", "Residential Homes", "C"),
    50: ("`dim_provider_home`", "Supported Accommodation Homes", "C"),
    51: ("`dim_provider` + `dim_provider_home`", "Providers - Fostering", "A"),
    52: ("—", "Retired — depended on `rpt_provider_fostering` report-view table (see KPI-48)", "R"),
    53: ("`fact_offer`", "Draft Offers With No Activity Since Creation", "C"),
    54: ("`fact_offer`", "Draft Offers With Activity Since Creation", "C"),
    55: ("`fact_offer`", "Draft Offers Missing Dates", "C"),
    56: ("`fact_offer`", "Draft Offers With Activity Since Creation", "A"),
    57: ("`fact_offer`", "Draft Offers Stalled 7+ Days", "C"),
    58: ("`fact_offer`", "Draft Offers Stalled 14+ Days", "C"),
    59: ("`fact_offer`", "Average Days in Draft", "C"),
    60: ("`fact_offer`", "Oldest Draft Age Days", "C"),
    61: ("`fact_offer`", "Offers in Draft", "A"),
    62: ("`fact_offer`", "Draft Offers With No Activity %", "C"),
    63: ("`fact_offer`", "Draft Offers Stalled 14+ Days", "A"),
    64: ("—", "Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands", "R"),
    65: ("`fact_offer`", "Pending Offers 15-29 Days", "C"),
    66: ("`fact_offer`", "Pending Offers 30+ Days", "C"),
    67: ("`fact_offer`", "Pending Offers 0-7 Days", "C"),
    68: ("`fact_offer`", "Pending Offers 8-14 Days", "C"),
    69: ("`fact_offer` + `fact_referral_provider`", "Providers With Pending Offers 30+ Days", "C"),
    70: ("`fact_offer`", "Pending Offers 8-14 Days", "A"),
    71: ("`fact_offer`", "Pending Offers 15-29 Days", "A"),
    72: ("`fact_offer`", "Pending Offers 30+ Days", "A"),
    73: ("`fct_ipa`", "IPA Exists (row helper)", "C"),
    74: ("—", "Blocked — no IPA-grain signature status; use the referral-grain IPA funnel instead", "B"),
    75: ("—", "Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it", "R"),
    76: ("`fct_ipa`", "IPAs Created", "C"),
    77: ("—", "Blocked — IPA-grain signed flags (`signed_by_local_authority` / `signed_by_provider`) not in Gold; use [Referrals With Fully Signed IPA]", "B"),
    78: ("`fact_referral` (`ipa_issued_date`, `ipa_2_signatures`)", "Referrals With IPA Pending Signature — referral-grain proxy for IPAs Pending Completion", "X"),
    79: ("`fact_offer` ⟕ `fct_ipa`", "Offers Awaiting IPA Creation", "C"),
    80: ("—", "Blocked — no IPA-grain signature status (see KPI-77)", "B"),
    81: ("`fact_offer` ⟕ `fct_ipa`", "Is Awaiting IPA Creation (row helper)", "C"),
    82: ("—", "Blocked — no IPA-grain signature status (see KPI-77)", "B"),
    83: ("`fact_offer` ⟕ `fct_ipa`", "Accepted Offer to IPA Conversion %", "C"),
    84: ("`fact_offer` ⟕ `fct_ipa`", "Offers Still to Progress to IPA %", "C"),
    85: ("—", "Blocked — IPA-grain completion rate needs signed flags; referral-grain [IPA Signature Completion Rate] is the supported proxy", "B"),
    86: ("—", "Blocked — as KPI-85", "B"),
    87: ("`fact_referral[gold_modelled_at]`", "Gold Model Last Refreshed", "A"),
    88: ("`fact_offer[source_export_date]`", "Latest Offer Source Export", "A"),
    89: ("—", "Retired — Gold `fact_offer` is already deduplicated to the latest state per offer", "R"),
    90: ("`fact_referral_provider`", "Referrals With Multiple Provider Assignments", "C"),
    91: ("`fact_referral` (`required_start_date` vs created date)", "Emergency Referrals", "C"),
    92: ("`fact_referral`", "Emergency Placement Rate", "C"),
    93: ("`fact_referral`", "Planned Referrals", "C"),
    94: ("`fact_referral`", "Visual split using [Emergency Referrals] and [Planned Referrals]; no separate measure", "C"),
    95: ("—", "Blocked — `fact_referral[region]` is null until a reliable source supplies it", "B"),
    96: ("—", "Blocked — as KPI-95", "B"),
    97: ("`dim_provider` QA flag columns", "Providers With QA Flags", "C"),
    98: ("—", "Blocked — no QA flag-type dimension to unpivot in Gold", "B"),
    99: ("`dim_provider_home` ⟕ `dim_provider`", "QA Flagged Homes", "C"),
    100: ("`dim_provider_submission_document`", "Documents Expiring Next 30 Days", "C"),
    101: ("`dim_provider_submission_document`", "Documents Expired", "C"),
    102: ("—", "Blocked — no expected-document set in Gold to test completeness against", "B"),
    103: ("—", "Blocked — as KPI-102", "B"),
    104: ("`dim_provider[provider_status]`", "Providers Pending Onboarding / Providers Approved (provider_status split)", "C"),
    105: ("—", "Blocked — no decline-reason history in active Gold", "B"),
    106: ("—", "Blocked — no framework-change history in active Gold", "B"),
    107: ("`fct_ipa[estimated_weekly_cost]`", "Estimated Active Weekly Cost — estimate, not signed-only actuals", "X"),
    108: ("—", "Blocked — no payment method / payment facts in Gold", "B"),
    109: ("—", "Blocked — no payment lifecycle facts in Gold", "B"),
    110: ("`fact_referral_lifecycle_event`", "Provider Messages Sent — lifecycle-event proxy for volume only; no response-time or unread analysis", "X"),
    111: ("—", "Blocked — no message response-time facts in Gold", "B"),
    112: ("—", "Blocked — no message-status facts in Gold", "B"),
    113: ("`fact_referral_lifecycle_event`", "Referral Lifecycle Events — derived roll-up, not the source audit log", "X"),
    114: ("`fact_referral` IPA fields", "IPA Signature Completion Rate — referral-grain proxy", "X"),
    115: ("—", "Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure", "B"),
    116: ("`dim_provider[provider_status]`", "Providers Pending Onboarding", "C"),
    117: ("`dim_provider[provider_status]`", "Provider Onboarding Success Rate", "C"),
}

assert len(M) == 117, len(M)

STATUS_LABEL = {
    "C": "✅ Covered",
    "A": "🔁 Alias",
    "X": "⚠️ Proxy",
    "R": "🗄 Retired",
    "B": "❌ Blocked",
}

def esc(text):
    return text.replace("|", "\\|") if text else text

out = []
out.append("### Full KPI-to-requirement mapping (KPI-01–117)")
out.append("")
out.append(
    "The table below maps every as-is KPI from the V13.1 assessment "
    "([§4.7 of the As-Is Assessment Report](../02_Assessment_and_Requirements/As_Is_Assessment_Report.md#47-kpi-calculation-inventory-as-is), "
    "ported from `Supplementary/02_01_As_Is_KPI.md`) to the **active Gold "
    "semantic model**, including the GLD-005–008 additions (`dim_person`, "
    "`dim_offer_status`, provider-home contact fields, `person_id` on "
    "`fact_referral`). Copy-ready DAX for each covered measure is in the "
    "[DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md); field-level "
    "evidence is in the [Field Coverage Audit](GOLD_DAX_FIELD_COVERAGE_AUDIT.md)."
)
out.append("")
out.append("Status legend: **✅ Covered** — active Gold measure; **🔁 Alias** — "
           "served by an existing Gold measure under a different name (rename "
           "the visual, do not recreate); **⚠️ Proxy** — supported at a "
           "different grain or with estimated logic, caveat applies; "
           "**🗄 Retired** — report-construct helper, deliberately not "
           "recreated; **❌ Blocked** — required field/grain missing from Gold, "
           "do not point DAX at Bronze, Silver or legacy tables.")
out.append("")
out.append("| KPI | Req IDs | As-is KPI (V13.1) | Active Gold object(s) | Gold measure / disposition | Status |")
out.append("|---|---|---|---|---|---|")

counts = {"C": 0, "A": 0, "X": 0, "R": 0, "B": 0}
for n in range(1, 118):
    kpi_id = f"KPI-{n:02d}"
    cells = rows[kpi_id]
    reqs = cells[1]
    desc = cells[2]
    objects, disp, st = M[n]
    counts[st] += 1
    out.append("| " + " | ".join(esc(x) for x in
               (kpi_id, reqs, desc, objects, disp, STATUS_LABEL[st])) + " |")

out.append("")
out.append("#### Disposition summary")
out.append("")
out.append("| Status | Count | Meaning |")
out.append("|---|---:|---|")
out.append(f"| ✅ Covered | {counts['C']} | Active Gold measure computes the KPI |")
out.append(f"| 🔁 Alias | {counts['A']} | Existing Gold measure under a different name; rename the visual |")
out.append(f"| ⚠️ Proxy | {counts['X']} | Supported at a different grain or with estimated logic |")
out.append(f"| 🗄 Retired | {counts['R']} | v15 report-construct helper, not recreated |")
out.append(f"| ❌ Blocked | {counts['B']} | Missing Gold field/grain; add the data first |")
total = sum(counts.values())
out.append(f"| **Total** | **{total}** | KPI-01–117 |")
out.append("")
out.append(
    "> **Gender measures (KPI-04–07)** were blocked in earlier revisions and "
    "are now covered: `gold.dim_person[gender_clean]` joins to "
    "`fact_referral[person_id]` (GLD-006/GLD-007). **Offer-status measures** "
    "filter through `gold.dim_offer_status` (GLD-008) rather than hard-coded "
    "status strings."
)

open("C:/tmp/gold_kpi_map.md", "w", encoding="utf-8").write("\n".join(out))
print("lines:", len(out), "counts:", counts, "total:", total)
