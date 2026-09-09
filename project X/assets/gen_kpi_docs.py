"""Generate the KPI calculation inventory for the As-Is Assessment Report and
the requirement-ID mapping for the Gold KPI Reference Guide."""
import json
import re

rows = json.load(open("/tmp/kpi_rows.json", encoding="utf-8"))

SECTION_TITLES = {
    "1": "Section 1 — Referral Volume KPIs",
    "2": "Section 2 — Provider Activity",
    "3": "Section 3 — Time-based",
    "4": "Section 4 — Spot vs Framework",
    "5": "Section 5 — Referral Offers",
    "6": "Section 6 — Provider Registry",
    "7": "Section 7 — Draft/Pending Offers",
    "8": "Section 8 — IPA Measures",
    "9": "Section 9 — Other Measures",
    "10": "Section 10 — New Outstanding Measures (functional-gap closure)",
}


def section_of(cells):
    if len(cells) > 7 and cells[7]:
        m = re.search(r"Section (\d+)", cells[7])
        if m:
            return m.group(1)
    return "10"  # Section 10 table has no trailing section column


def esc(text):
    return text.replace("|", "\\|") if text else text


# ---------- As-Is appendix ----------
groups = {}
for k, cells in rows.items():
    groups.setdefault(section_of(cells), []).append(cells)

out = []
out.append("### 4.7 KPI Calculation Inventory (As-Is)")
out.append("")
out.append(
    "The table below is the complete as-is KPI inventory for the V13.1 pilot "
    "dashboard: every KPI with its functional requirement IDs (from the WMPP "
    "Functional Specification), source tables, calculation logic and Power BI "
    "measure name. It is ported from "
    "`Supplementary/02_01_As_Is_KPI.md` so that the assessment report is "
    "self-contained; the supplementary copy remains the historic original."
)
out.append("")
out.append("#### 4.7.1 Table mapping — Silver-era model to Gold-era objects (as assessed)")
out.append("")
out.append("| Model table | Source | Schema definition table | Functional area |")
out.append("|---|---|---|---|")
table_map = [
    ("fact_referral_offer", "referral_provider", "referral.referral_provider", "Referral → Provider mapping"),
    ("fact_offer", "offer", "offer.offer", "Provider offers"),
    ("fact_ipa", "ipa", "ipa.ipa", "Individual Placement Agreements"),
    ("fact_referral", "referral", "referral.referral", "Referral header"),
    ("dim_provider", "provider", "provider.provider", "Provider master"),
    ("dim_provider_home", "provider_home", "provider.provider_home", "Provider homes"),
    ("dim_provider_framework", "provider_framework", "provider.provider_framework", "Provider-framework link"),
    ("fact_referral_person", "person", "referral.person", "Child demographics"),
    ("fact_referral_category", "referral_category", "referral.referral_category", "Referral categories"),
    ("fact_provider_message", "referral_provider_message", "referral.referral_provider_message", "Inter-party messages"),
    ("fact_referral_gender", "person", "referral.person", "Gender aggregation"),
    ("fact_referral_event_log", "referral_event_log", "referral.referral_event_log", "Audit trail"),
    ("dim_s3_file_metadata", "s3_file_metadata", "document.s3_file_metadata", "Document metadata"),
    ("dim_provider_document", "provider_document", "provider.provider_document", "Provider docs"),
    ("dim_submission_documents", "submission_documents", "provider.submission_documents", "Onboarding docs"),
    ("fact_referral_provider_decline_reason", "referral_provider_decline_reason", "referral.referral_provider_decline_reason", "Decline reasons"),
    ("dim_offer_status", "offer (derived)", "offer.offer", "Offer status lookup"),
]
for t in table_map:
    out.append("| " + " | ".join(t) + " |")
out.append("")
out.append(
    "> These are the table names used by the assessed V13.1 model. They are "
    "**not** the active notebook-created Gold v02 objects — see "
    "`04_Data_and_Reporting/KPI_Reference_Guide.md` for the current mapping."
)
out.append("")
out.append("#### 4.7.2 KPI inventory by report section")

HEADER = ("| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |",
          "|---|---|---|---|---|---|---|")
for sec in sorted(groups, key=int):
    out.append("")
    out.append(f"##### {SECTION_TITLES[sec]}")
    out.append("")
    out.extend(HEADER)
    for cells in sorted(groups[sec], key=lambda c: int(c[0].split("-")[1])):
        padded = cells + [""] * (7 - len(cells))
        kpi, reqs, desc, reqdesc, tables, calc, pbi = padded[:7]
        out.append("| " + " | ".join(esc(x) for x in (kpi, reqs, desc, reqdesc, tables, calc, pbi)) + " |")

out.append("")
out.append("#### 4.7.3 Inventory summary")
out.append("")
out.append("| Category | Existing KPIs | New KPIs | Total |")
out.append("|---|---:|---:|---:|")
summary = [
    ("Referral Volume", "10", "4 (emergency/planned)", "14"),
    ("Provider Activity", "12", "0", "12"),
    ("Timebased", "2", "0", "2"),
    ("Spot vs Framework", "3", "0", "3"),
    ("Referral Offers", "12", "1 (decline reasons)", "13"),
    ("Provider Registry", "13", "3 (QA flags, due diligence)", "16"),
    ("Draft/Pending", "20", "0", "20"),
    ("IPA Measures", "14", "3 (finance, signatures)", "17"),
    ("Out-of-Region", "1", "2 (out-of-region, rate)", "3"),
    ("Document Compliance", "0", "4 (expiry, blocked, rate)", "4"),
    ("Messaging", "0", "3 (response, unread)", "3"),
    ("Audit Trail", "0", "2 (events, signatures)", "2"),
    ("Onboarding", "0", "2 (pipeline, success)", "2"),
    ("Finance", "0", "3 (fees, payment, status)", "3"),
]
for s in summary:
    out.append("| " + " | ".join(s) + " |")
out.append("| **Total** | **90** (existing) | **27** (new) | **117** |")
out.append("")

open("/tmp/appendix_asis.md", "w", encoding="utf-8").write("\n".join(out))
print("appendix lines:", len(out))
