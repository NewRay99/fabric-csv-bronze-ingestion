# Gold semantic model DAX build guide

## Purpose

Use this guide to build the replacement Power BI semantic model over the
active notebook-created Gold database. It was reconciled against:

- `SM WMPP v15.zip` — legacy business-report measures;
- `SM WMPP Mission Control.zip` — operational monitoring report; and
- `reports/mission-control/mission-control-measures.dax` — monitoring-only
  measures.

The Mission Control measures remain a separate monitoring model because they
use `monitoring.cfg_*` tables, not referral Gold facts. The v15 measures must
be recreated only from the active Gold tables listed below; do not retain a
legacy table in the new semantic model just to preserve a measure name.

## Import and relationship instructions

Import `fact_referral`, `fact_referral_snapshot`, `fact_offer`, `fct_ipa`,
`fact_referral_provider`, and the active `dim_*` / `bridge_*` tables. Their
columns are lower-case `snake_case`.

Create these active relationships:

| From | To | Cardinality / direction | Status |
| --- | --- | --- | --- |
| `fact_referral[referral_id]` | `fact_offer[referral_id]` | One-to-many, single direction | Active |
| `fact_referral[referral_id]` | `fct_ipa[referral_id]` | One-to-many, single direction | Active |
| `fact_referral[referral_id]` | `fact_referral_provider[referral_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `fact_offer[provider_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `fact_referral_provider[provider_id]` | One-to-many, single direction | Active |
| `dim_provider_home[provider_home_id]` | `fact_offer[home_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `dim_provider_home[provider_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `bridge_provider_framework[provider_id]` | One-to-many, single direction | Active |
| `dim_provider_home[provider_home_id]` | `dim_provider_submission_document[home_id]` | One-to-many, single direction | Active |

Use `dim_date[date]` as the Date table. Keep the relationships to
`fact_referral[referral_created_date]` and
`fact_referral_snapshot[snapshot_date]` active only in the relevant model or
use inactive role-playing relationships for the remaining dates. Do not create
an active `fact_offer[offer_id]` to `fct_ipa[accepted_offer_id]` relationship
when it creates an ambiguous route; use `USERELATIONSHIP` in a specific
conversion measure instead.

## Copy-ready DAX

Create the measures below in a dedicated `_measures` table. They refer only to
the new Gold model.

```DAX
Total Referrals = DISTINCTCOUNT ( 'fact_referral'[referral_id] )

Open Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Closed Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = FALSE () )

Referrals With an Offer =
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )

Referrals Awaiting Offer =
CALCULATE (
    [Total Referrals],
    'fact_referral'[is_open] = TRUE (),
    'fact_referral'[has_offer] = FALSE ()
)

Referrals Without Provider Assignment =
CALCULATE ( [Total Referrals], 'fact_referral'[is_not_seen_by_providers] = TRUE () )

Open Overdue Referrals =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE ()
            && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
            && 'fact_referral'[required_placement_date] < 'fact_referral'[as_of_date]
    )
)

Referrals Placed by Required Date =
CALCULATE ( [Total Referrals], 'fact_referral'[placed_by_required_date] = TRUE () )

Placement Target Hit Rate =
DIVIDE (
    [Referrals Placed by Required Date],
    CALCULATE (
        [Total Referrals],
        FILTER (
            'fact_referral',
            NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
                && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
        )
    )
)

Median Days to First Action =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_action] ) ),
    'fact_referral'[days_to_first_action]
)

Median Days to First Offer =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_offer] ) ),
    'fact_referral'[days_to_first_offer]
)

Median Days to IPA =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_ipa] ) ),
    'fact_referral'[days_to_ipa]
)

Open Referrals Stalled 7+ Days =
CALCULATE (
    [Total Referrals],
    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[days_without_activity] >= 7 )
)
```

```DAX
Offers Submitted = DISTINCTCOUNT ( 'fact_offer'[offer_id] )

Accepted Offers =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( 'fact_offer'[offer_status] ) IN { "accepted", "approved", "selected", "offer_successful" }
    )
)

Offers with a Decision =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_decision_date] ) )
)

Offer Acceptance Rate = DIVIDE ( [Accepted Offers], [Offers with a Decision] )

Average Offers per Referral = DIVIDE ( [Offers Submitted], [Referrals With an Offer] )

Offers in Draft =
CALCULATE ( [Offers Submitted], LOWER ( 'fact_offer'[offer_status] ) = "draft" )

Draft Offers Stalled 7+ Days =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( 'fact_offer'[offer_status] ) = "draft"
            && DATEDIFF ( 'fact_offer'[offer_reviewed_date], TODAY (), DAY ) >= 7
    )
)

IPAs Created = DISTINCTCOUNT ( 'fct_ipa'[ipa_id] )

Active IPAs =
CALCULATE ( [IPAs Created], 'fct_ipa'[is_placement_closed] = FALSE () )

Estimated Active Weekly Cost =
CALCULATE (
    SUM ( 'fct_ipa'[estimated_weekly_cost] ),
    'fct_ipa'[is_placement_closed] = FALSE ()
)

Average Estimated Weekly Cost — Confirmed Referrals =
AVERAGEX (
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
            && NOT ISBLANK ( 'fact_referral'[estimated_weekly_cost] )
    ),
    'fact_referral'[estimated_weekly_cost]
)

Provider Assignments = DISTINCTCOUNT ( 'fact_referral_provider'[referral_provider_id] )

Provider Declines =
CALCULATE ( [Provider Assignments], 'fact_referral_provider'[is_declined] = TRUE () )

Provider Decline Rate = DIVIDE ( [Provider Declines], [Provider Assignments] )
```

```DAX
Snapshot Referrals = DISTINCTCOUNT ( 'fact_referral_snapshot'[referral_id] )

Open Referrals at Snapshot =
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open] = TRUE () )

Closed Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    FILTER (
        'fact_referral_snapshot',
        NOT ISBLANK ( 'fact_referral_snapshot'[referral_closed_date] )
            && 'fact_referral_snapshot'[referral_closed_date] < 'fact_referral_snapshot'[snapshot_date] + 1
    )
)

Referrals with IPA at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    FILTER (
        'fact_referral_snapshot',
        NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
            && 'fact_referral_snapshot'[ipa_issued_date] < 'fact_referral_snapshot'[snapshot_date] + 1
    )
)

Open Overdue Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    'fact_referral_snapshot'[required_placement_date_outcome] = "Open overdue"
)

Open On-Track Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    'fact_referral_snapshot'[required_placement_date_outcome] = "Open on track"
)

Open Referral Rate at Snapshot = DIVIDE ( [Open Referrals at Snapshot], [Snapshot Referrals] )

Placement Rate at Snapshot = DIVIDE ( [Referrals with IPA at Snapshot], [Snapshot Referrals] )
```

## Additional legacy KPI ports

The following measures complete the **supported** portion of the historical
KPI library. They use active Gold fields only. Measures with similar historic
names can be renamed in the semantic model after the totals have been
reconciled.

### Referral, provider engagement and planning

```DAX
Referrals Created This Month =
CALCULATE ( [Total Referrals], DATESMTD ( 'dim_date'[date] ) )

Referrals Created Previous Month =
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referral Volume Month on Month =
[Total Referrals] - [Referrals Created Previous Month]

Referral Volume Month on Month % =
DIVIDE ( [Referral Volume Month on Month], [Referrals Created Previous Month] )

Referrals Created This Financial Year =
VAR financial_year_start =
    DATE ( YEAR ( TODAY () ) - IF ( MONTH ( TODAY () ) < 4, 1, 0 ), 4, 1 )
RETURN
    CALCULATE (
        [Total Referrals],
        DATESBETWEEN ( 'dim_date'[date], financial_year_start, TODAY () )
    )

Referrals Currently Active =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Referrals Under Offer =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Closed or Cancelled Referrals =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "closed", "cancelled", "withdrawn", "completed" }
    )
)

Active Referrals With Provider Engagement =
CALCULATE (
    [Total Referrals],
    'fact_referral'[is_open] = TRUE (),
    'fact_referral'[has_offer] = TRUE ()
)

Active Referral Engagement Rate =
DIVIDE ( [Active Referrals With Provider Engagement], [Referrals Currently Active] )

Active Awaiting Offers With Engagement =
CALCULATE (
    [Total Referrals],
    'fact_referral'[is_open] = TRUE (),
    'fact_referral'[has_offer] = TRUE ()
)

Active Awaiting Offers Without Engagement =
CALCULATE (
    [Total Referrals],
    'fact_referral'[is_open] = TRUE (),
    'fact_referral'[has_offer] = FALSE ()
)

Emergency Referrals =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[referral_created_date] )
            && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
            && DATEDIFF (
                'fact_referral'[referral_created_date],
                'fact_referral'[required_placement_date],
                DAY
            ) = 0
    )
)

Planned Referrals =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[referral_created_date] )
            && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
            && DATEDIFF (
                'fact_referral'[referral_created_date],
                'fact_referral'[required_placement_date],
                DAY
            ) > 0
    )
)

Emergency Placement Rate = DIVIDE ( [Emergency Referrals], [Total Referrals] )

Referrals With Multiple Provider Assignments =
COUNTROWS (
    FILTER (
        VALUES ( 'fact_referral_provider'[referral_id] ),
        CALCULATE ( DISTINCTCOUNT ( 'fact_referral_provider'[provider_id] ) ) > 1
    )
)
```

Use `fact_referral[referral_closure_reason]`,
`fact_referral[placement_type_required]`, `fact_referral[priority]` and
`fact_referral[complexity_band]` directly as visual dimensions with the
appropriate referral count measure. This ports the legacy closed-reason and
placement-type visual logic without creating redundant measures.

### Offer, spot/framework and draft/pending-offer portfolio

```DAX
Non-Draft Offers =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) <> "draft" )
)

Pending Offers =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "pending" )
)

Unsuccessful Offers =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
            IN { "declined", "rejected", "withdrawn", "offer_unsuccessful", "offer_withdrawn" }
    )
)

Offers With Recorded Rejection Reason =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[rejection_reason] ) )
)

Providers Who Made Offers =
CALCULATE (
    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
    FILTER (
        'fact_offer',
        NOT (
            LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
                IN { "draft", "withdrawn", "offer_withdrawn" }
        )
    )
)

Average Offers per Provider =
DIVIDE ( [Non-Draft Offers], [Providers Who Made Offers] )

Average Offers per Referral Under Offer =
DIVIDE (
    CALCULATE (
        [Non-Draft Offers],
        FILTER (
            'fact_referral',
            LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
                IN { "under_offer", "under offer", "offer" }
        )
    ),
    [Referrals Under Offer]
)

Offers on Referrals Under Offer =
CALCULATE (
    [Non-Draft Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Spot Offers =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home'[is_spot] = TRUE () )

Non-Spot Offers =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home'[is_spot] = FALSE () )

Spot Offer Rate = DIVIDE ( [Spot Offers], [Non-Draft Offers] )

Draft Offers With No Activity Since Creation =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && 'fact_offer'[offer_submitted_date] = 'fact_offer'[offer_reviewed_date]
    )
)

Draft Offers With Activity Since Creation =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && 'fact_offer'[offer_reviewed_date] > 'fact_offer'[offer_submitted_date]
    )
)

Draft Offers Missing Dates =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && (
                ISBLANK ( 'fact_offer'[offer_submitted_date] )
                    || ISBLANK ( 'fact_offer'[offer_reviewed_date] )
            )
    )
)

Draft Offers Stalled 14+ Days =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && DATEDIFF (
                COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
                TODAY (), DAY
            ) >= 14
    )
)

Average Days in Draft =
AVERAGEX (
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && NOT ISBLANK ( 'fact_offer'[offer_submitted_date] )
    ),
    DATEDIFF ( 'fact_offer'[offer_submitted_date], TODAY (), DAY )
)

Oldest Draft Age Days =
MAXX (
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && NOT ISBLANK ( 'fact_offer'[offer_submitted_date] )
    ),
    DATEDIFF ( 'fact_offer'[offer_submitted_date], TODAY (), DAY )
)

Draft Offers With No Activity % =
DIVIDE ( [Draft Offers With No Activity Since Creation], [Offers in Draft] )

Pending Offers 0-7 Days =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_offer',
        DATEDIFF (
            COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
            TODAY (), DAY
        ) <= 7
    )
)

Pending Offers 8-14 Days =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_offer',
        VAR age_days = DATEDIFF (
            COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
            TODAY (), DAY
        )
        RETURN age_days >= 8 && age_days <= 14
    )
)

Pending Offers 15-29 Days =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_offer',
        VAR age_days = DATEDIFF (
            COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
            TODAY (), DAY
        )
        RETURN age_days >= 15 && age_days <= 29
    )
)

Pending Offers 30+ Days =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_offer',
        DATEDIFF (
            COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
            TODAY (), DAY
        ) >= 30
    )
)

Providers With Pending Offers 30+ Days =
CALCULATE (
    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "pending"
            && DATEDIFF (
                COALESCE ( 'fact_offer'[offer_reviewed_date], 'fact_offer'[offer_submitted_date] ),
                TODAY (), DAY
            ) >= 30
    )
)

Latest Offer Source Export = MAX ( 'fact_offer'[source_export_date] )
```

Use `fact_offer[offer_status]`, `fact_offer[offer_type]`,
`fact_offer[rejection_reason]`, and `dim_provider[provider_name]` as visual
dimensions for the historic offer-status, decline-reason and provider ranking
tables.

### Provider register, framework, QA and documentation

```DAX
Provider Homes Registered = DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] )

Providers Registered = DISTINCTCOUNT ( 'dim_provider'[provider_id] )

Providers - Fostering =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
    'dim_provider_home'[service_type] = "Fostering"
)

Providers - Residential =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
    'dim_provider_home'[service_type] = "Residential"
)

Providers - Supported Accommodation =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
    'dim_provider_home'[service_type] = "Supported Accommodation"
)

Residential Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Residential" )

Supported Accommodation Homes =
CALCULATE (
    [Provider Homes Registered],
    'dim_provider_home'[service_type] = "Supported Accommodation"
)

Fostering Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Fostering" )

Framework Providers = DISTINCTCOUNT ( 'bridge_provider_framework'[provider_id] )

Non-Framework Providers =
COUNTROWS (
    EXCEPT (
        VALUES ( 'dim_provider'[provider_id] ),
        VALUES ( 'bridge_provider_framework'[provider_id] )
    )
)

Providers With QA Flags =
CALCULATE ( [Providers Registered], 'dim_provider'[qa_flag] = TRUE () )

QA Flagged Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[qa_flag] = TRUE () )

Providers Pending Onboarding =
CALCULATE (
    [Providers Registered],
    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "pending" )
)

Providers Approved =
CALCULATE (
    [Providers Registered],
    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "approved" )
)

Provider Onboarding Success Rate = DIVIDE ( [Providers Approved], [Providers Registered] )

Provider Submission Documents =
DISTINCTCOUNT ( 'dim_provider_submission_document'[document_id] )

Documents Expiring Next 30 Days =
CALCULATE (
    [Provider Submission Documents],
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] >= TODAY ()
            && 'dim_provider_submission_document'[expiry_date] <= TODAY () + 30
    )
)

Documents Expired =
CALCULATE (
    [Provider Submission Documents],
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
    )
)

Provider Homes With Expired Documents =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_submission_document'[home_id] ),
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
    )
)
```

### IPA, cost and referral-lifecycle measures

Create an inactive `dim_date[date]` to `fct_ipa[ipa_issued_date]`
relationship and use `USERELATIONSHIP` (or make it active only on an IPA
report page) for the issued-date time-intelligence measures below.

```DAX
IPAs Issued This Month =
CALCULATE (
    [IPAs Created],
    USERELATIONSHIP ( 'dim_date'[date], 'fct_ipa'[ipa_issued_date] ),
    DATESMTD ( 'dim_date'[date] )
)

Closed IPAs =
CALCULATE ( [IPAs Created], 'fct_ipa'[is_placement_closed] = TRUE () )

Average Active IPA Weekly Cost =
DIVIDE ( [Estimated Active Weekly Cost], [Active IPAs] )

Total IPA Weekly Cost = SUM ( 'fct_ipa'[estimated_weekly_cost] )

Accepted Offers With IPA =
VAR ipa_offer_ids =
    FILTER (
        VALUES ( 'fct_ipa'[accepted_offer_id] ),
        NOT ISBLANK ( 'fct_ipa'[accepted_offer_id] )
    )
RETURN
    CALCULATE ( [Accepted Offers], TREATAS ( ipa_offer_ids, 'fact_offer'[offer_id] ) )

Offers Awaiting IPA Creation =
VAR accepted_offer_ids =
    CALCULATETABLE (
        VALUES ( 'fact_offer'[offer_id] ),
        FILTER (
            'fact_offer',
            LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
                IN { "accepted", "approved", "selected", "offer_successful" }
        )
    )
VAR ipa_offer_ids =
    FILTER (
        VALUES ( 'fct_ipa'[accepted_offer_id] ),
        NOT ISBLANK ( 'fct_ipa'[accepted_offer_id] )
    )
RETURN
    COUNTROWS ( EXCEPT ( accepted_offer_ids, ipa_offer_ids ) )

Accepted Offer to IPA Conversion % =
DIVIDE ( [Accepted Offers With IPA], [Accepted Offers] )

Offers Still to Progress to IPA % = 1 - [Accepted Offer to IPA Conversion %]

Referrals With Fully Signed IPA =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
            && 'fact_referral'[ipa_2_signatures] = TRUE ()
    )
)

IPA Signature Completion Rate =
DIVIDE ( [Referrals With Fully Signed IPA], [Referrals with IPA] )

Referral Lifecycle Events =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[event_id] )

Referrals With Lifecycle Activity =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[referral_id] )

Average Lifecycle Events per Referral =
DIVIDE ( [Referral Lifecycle Events], [Referrals With Lifecycle Activity] )

Gold Model Last Refreshed = MAX ( 'fact_referral'[gold_modelled_at] )
```

`Accepted Offers With IPA` deliberately uses `TREATAS` rather than an active
fact-to-fact relationship. This avoids an ambiguous relationship path while
still using the stable `fct_ipa[accepted_offer_id]` key.

## Legacy v15 reconciliation

| Historic KPI groups now portable | Use the measures above / visual dimensions |
| --- | --- |
| KPI-01–03, 08–10, 19–24, 29–39, 87–90 | Referral, offer, provider-engagement, time, closure reason, status, assignment overlap and export measures. |
| KPI-11–18, 25–28, 53–72 | Provider activity, offer portfolio, spot/non-spot, draft and pending age measures. |
| KPI-40–52, 97, 99–101, 104, 116–117 | Provider/home register, framework coverage, QA flags, document expiry and onboarding measures. |
| KPI-73–76, 79, 83–84, 107 and 113 | IPA volume/cost, accepted-offer conversion and lifecycle-activity measures. |
| KPI-114 and KPI-115 | Referral-level IPA-signature and lifecycle-event **proxies** are supplied; they are not like-for-like IPA-signature or referral-update measures. |
| KPI-91–94 | Emergency/planned referral measures using created and required-placement dates. |

| Do not recreate yet | Missing active-Gold field or grain |
| --- | --- |
| KPI-04–07 | No child gender field in the active Gold referral fact. |
| KPI-77–78, 80–82, 85–86, 114 | No IPA-grain signature status; `ipa_2_signatures` is a referral-level proxy only. |
| KPI-95–96 | `fact_referral[region]` is not populated; provider geography is not a safe referral-region substitute. |
| KPI-98 | Only one provider/home QA flag is published, not the historic flag-type breakdown. |
| KPI-102–103 | The current document fact has no documented expected-document set or blocking outcome, so compliance cannot be calculated. |
| KPI-105–106 | No referral-level decline-reason or framework-change history fact. Use offer rejection reasons only. |
| KPI-108–112 | No payment, invoice, provider-message or message-status facts. |
| KPI-115 | No durable referral update timestamp; lifecycle events provide the supported activity measure. |
| Child support needs and referral categories | No active Gold dimension/fact at the required analysis grain. |

For any unsupported item, add the missing Gold fact/dimension first; do not
point DAX at Bronze, Silver, or a legacy imported table as a workaround.

## Deployment checklist

1. Run `04_gold_model.ipynb`, which publishes snake-case fact fields, retires
   `fact_placement`, and creates `fct_ipa`.
2. Run `05_gold_dimensions.ipynb`, which publishes snake-case dimension and
   bridge fields.
3. Refresh the Lakehouse semantic model and remove old imported tables.
4. Create the active relationships, then add the DAX above.
5. Reconcile totals by `referral_id`, `offer_id`, `ipa_id`, and
   `referral_provider_id` before rebuilding visual pages.
