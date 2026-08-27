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

## Gold-only KPI contract

Every published referral KPI must reference a field in an active Gold fact,
dimension or bridge table imported into the semantic model. `bronze.*`,
`silver.*`, retired facts and legacy model tables are lineage evidence only and
must never appear in a published DAX expression. A source marked as available
in Bronze or Silver is therefore **not** KPI-ready until the required field is
deliberately promoted into Gold. The source-coverage worksheet in
`configuration/Dashboard Legend.xlsx` records this distinction in its **KPI
DAX eligibility** column.

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

Provider Messages Sent =
CALCULATE (
    [Referral Lifecycle Events],
    'fact_referral_lifecycle_event'[event_type] = "ProviderMessageSent"
)

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
| KPI-73–76, 79, 83–84, 107, 110 and 113 | IPA volume/cost, accepted-offer conversion, provider-message volume proxy and lifecycle-activity measures. |
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
| KPI-108–109 and KPI-111–112 | No payment, invoice, detailed provider-message or message-status facts. `Provider Messages Sent` is supported as a lifecycle-event proxy only. |
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

## Legacy v15 full-library port

This section reconciles **all 153 measures** extracted from the legacy
`SM WMPP v15.zip` semantic model (`_Measures` table, TMDL) against the Gold
build guide. Disposition:

| Disposition | Count | Meaning |
| --- | ---: | --- |
| Already covered (identical or alias) | 59 | Served by a measure in the sections above |
| Newly ported in this revision | 62 | Copy-ready Gold DAX below (76 definitions; MoM stacks completed to a consistent 5-measure pattern) |
| Retired report-construct helpers | 15 | Not recreated; reasons listed below |
| Blocked by missing Gold source fields | 17 | Added to the do-not-recreate list |
| **Total legacy v15 measures** | **153** | |

Every ported measure references active Gold tables only. No `bronze.*`,
`silver.*`, `fact_placement`, `fact_referral_offer`, `dim_referral`,
`dim_offer_status`, or `LocalDateTable` reference survives the port.

### Month-on-month card variance and indicator family

Every v15 KPI card ships with a previous-month companion, an absolute
variance, a month-on-month percentage, and arrow/colour indicator measures.
The legacy model defined these inconsistently (some cards lack the MoM %
member); the port completes every card to the same five-measure stack.

All stacks use the active `dim_date[date]` to
`fact_referral[referral_created_date]` relationship, so no
`USERELATIONSHIP` is required. The stack pattern is:

```DAX
<Base> Previous Month = CALCULATE ( [<Base>], DATEADD ( 'dim_date'[date], -1, MONTH ) )
<Base> Variance = [<Base>] - [<Base> Previous Month]
<Base> MoM % = DIVIDE ( [<Base> Variance], [<Base> Previous Month] )
<Base> Variance Indicator = IF ( [<Base> Variance] > 0, "▲", IF ( [<Base> Variance] < 0, "▼", "–" ) )
<Base> Variance Indicator Color = IF ( [<Base> Variance] > 0, "green", IF ( [<Base> Variance] < 0, "red", "grey" ) )
```

Copy-ready stacks for every legacy KPI card:

```DAX

-- Legacy card: Total Referrals
Total Referrals Previous Month =
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Total Referrals Variance =
[Total Referrals] - [Total Referrals Previous Month]

Total Referrals MoM % =
DIVIDE ( [Total Referrals Variance], [Total Referrals Previous Month] )

Total Referrals Variance Indicator =
IF ( [Total Referrals Variance] > 0, "▲", IF ( [Total Referrals Variance] < 0, "▼", "–" ) )

Total Referrals Variance Indicator Color =
IF ( [Total Referrals Variance] > 0, "green", IF ( [Total Referrals Variance] < 0, "red", "grey" ) )

-- Legacy card: Open Referral
Open Referrals Previous Month =
CALCULATE ( [Open Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Open Referrals Variance =
[Open Referrals] - [Open Referrals Previous Month]

Open Referrals MoM % =
DIVIDE ( [Open Referrals Variance], [Open Referrals Previous Month] )

Open Referrals Variance Indicator =
IF ( [Open Referrals Variance] > 0, "▲", IF ( [Open Referrals Variance] < 0, "▼", "–" ) )

Open Referrals Variance Indicator Color =
IF ( [Open Referrals Variance] > 0, "green", IF ( [Open Referrals Variance] < 0, "red", "grey" ) )

-- Legacy card: Closed Referrals (by Reason)
Closed Referrals Previous Month =
CALCULATE ( [Closed Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Closed Referrals Variance =
[Closed Referrals] - [Closed Referrals Previous Month]

Closed Referrals MoM % =
DIVIDE ( [Closed Referrals Variance], [Closed Referrals Previous Month] )

Closed Referrals Variance Indicator =
IF ( [Closed Referrals Variance] > 0, "▲", IF ( [Closed Referrals Variance] < 0, "▼", "–" ) )

Closed Referrals Variance Indicator Color =
IF ( [Closed Referrals Variance] > 0, "green", IF ( [Closed Referrals Variance] < 0, "red", "grey" ) )

-- Legacy card: Referrals With Offers
Referrals With an Offer Previous Month =
CALCULATE ( [Referrals With an Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals With an Offer Variance =
[Referrals With an Offer] - [Referrals With an Offer Previous Month]

Referrals With an Offer MoM % =
DIVIDE ( [Referrals With an Offer Variance], [Referrals With an Offer Previous Month] )

Referrals With an Offer Variance Indicator =
IF ( [Referrals With an Offer Variance] > 0, "▲", IF ( [Referrals With an Offer Variance] < 0, "▼", "–" ) )

Referrals With an Offer Variance Indicator Color =
IF ( [Referrals With an Offer Variance] > 0, "green", IF ( [Referrals With an Offer Variance] < 0, "red", "grey" ) )

-- Legacy card: Active Referrals Awaiting Offers
Referrals Awaiting Offer Previous Month =
CALCULATE ( [Referrals Awaiting Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Awaiting Offer Variance =
[Referrals Awaiting Offer] - [Referrals Awaiting Offer Previous Month]

Referrals Awaiting Offer MoM % =
DIVIDE ( [Referrals Awaiting Offer Variance], [Referrals Awaiting Offer Previous Month] )

Referrals Awaiting Offer Variance Indicator =
IF ( [Referrals Awaiting Offer Variance] > 0, "▲", IF ( [Referrals Awaiting Offer Variance] < 0, "▼", "–" ) )

Referrals Awaiting Offer Variance Indicator Color =
IF ( [Referrals Awaiting Offer Variance] > 0, "green", IF ( [Referrals Awaiting Offer Variance] < 0, "red", "grey" ) )

-- Legacy card: Active Referrals Under Offer
Referrals Under Offer Previous Month =
CALCULATE ( [Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Under Offer Variance =
[Referrals Under Offer] - [Referrals Under Offer Previous Month]

Referrals Under Offer MoM % =
DIVIDE ( [Referrals Under Offer Variance], [Referrals Under Offer Previous Month] )

Referrals Under Offer Variance Indicator =
IF ( [Referrals Under Offer Variance] > 0, "▲", IF ( [Referrals Under Offer Variance] < 0, "▼", "–" ) )

Referrals Under Offer Variance Indicator Color =
IF ( [Referrals Under Offer Variance] > 0, "green", IF ( [Referrals Under Offer Variance] < 0, "red", "grey" ) )

-- Legacy card: Referrals Currently Active
Referrals Currently Active Previous Month =
CALCULATE ( [Referrals Currently Active], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Currently Active Variance =
[Referrals Currently Active] - [Referrals Currently Active Previous Month]

Referrals Currently Active MoM % =
DIVIDE ( [Referrals Currently Active Variance], [Referrals Currently Active Previous Month] )

Referrals Currently Active Variance Indicator =
IF ( [Referrals Currently Active Variance] > 0, "▲", IF ( [Referrals Currently Active Variance] < 0, "▼", "–" ) )

Referrals Currently Active Variance Indicator Color =
IF ( [Referrals Currently Active Variance] > 0, "green", IF ( [Referrals Currently Active Variance] < 0, "red", "grey" ) )

-- Legacy card: Referrals Cancelled/Closed
Closed or Cancelled Referrals Previous Month =
CALCULATE ( [Closed or Cancelled Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Closed or Cancelled Referrals Variance =
[Closed or Cancelled Referrals] - [Closed or Cancelled Referrals Previous Month]

Closed or Cancelled Referrals MoM % =
DIVIDE ( [Closed or Cancelled Referrals Variance], [Closed or Cancelled Referrals Previous Month] )

Closed or Cancelled Referrals Variance Indicator =
IF ( [Closed or Cancelled Referrals Variance] > 0, "▲", IF ( [Closed or Cancelled Referrals Variance] < 0, "▼", "–" ) )

Closed or Cancelled Referrals Variance Indicator Color =
IF ( [Closed or Cancelled Referrals Variance] > 0, "green", IF ( [Closed or Cancelled Referrals Variance] < 0, "red", "grey" ) )

-- Legacy card: Active Referral Engagement Rate
Active Referral Engagement Rate Previous Month =
CALCULATE ( [Active Referral Engagement Rate], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Active Referral Engagement Rate Variance =
[Active Referral Engagement Rate] - [Active Referral Engagement Rate Previous Month]

Active Referral Engagement Rate MoM % =
DIVIDE ( [Active Referral Engagement Rate Variance], [Active Referral Engagement Rate Previous Month] )

Active Referral Engagement Rate Variance Indicator =
IF ( [Active Referral Engagement Rate Variance] > 0, "▲", IF ( [Active Referral Engagement Rate Variance] < 0, "▼", "–" ) )

Active Referral Engagement Rate Variance Indicator Color =
IF ( [Active Referral Engagement Rate Variance] > 0, "green", IF ( [Active Referral Engagement Rate Variance] < 0, "red", "grey" ) )

-- Legacy card: Total Offers Made (Active Referrals Under Offer)
Offers on Referrals Under Offer Previous Month =
CALCULATE ( [Offers on Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Offers on Referrals Under Offer Variance =
[Offers on Referrals Under Offer] - [Offers on Referrals Under Offer Previous Month]

Offers on Referrals Under Offer MoM % =
DIVIDE ( [Offers on Referrals Under Offer Variance], [Offers on Referrals Under Offer Previous Month] )

Offers on Referrals Under Offer Variance Indicator =
IF ( [Offers on Referrals Under Offer Variance] > 0, "▲", IF ( [Offers on Referrals Under Offer Variance] < 0, "▼", "–" ) )

Offers on Referrals Under Offer Variance Indicator Color =
IF ( [Offers on Referrals Under Offer Variance] > 0, "green", IF ( [Offers on Referrals Under Offer Variance] < 0, "red", "grey" ) )

-- Legacy card: Total Referrals That Received Offers
Offer Receipt Rate (Created in Period) Previous Month =
CALCULATE ( [Offer Receipt Rate (Created in Period)], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Offer Receipt Rate (Created in Period) Variance =
[Offer Receipt Rate (Created in Period)] - [Offer Receipt Rate (Created in Period) Previous Month]

Offer Receipt Rate (Created in Period) MoM % =
DIVIDE ( [Offer Receipt Rate (Created in Period) Variance], [Offer Receipt Rate (Created in Period) Previous Month] )

Offer Receipt Rate (Created in Period) Variance Indicator =
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "▲", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "▼", "–" ) )

Offer Receipt Rate (Created in Period) Variance Indicator Color =
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "green", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "red", "grey" ) )

```

> The legacy `Provider Contact Referral` card family (6 measures) is
> **not** ported: there is no `contact_made` field anywhere in the
> active Gold layer. See the blocked list below.


### Created-in-period measures

These replace the legacy `USERELATIONSHIP(dim_date[Date],
dim_referral[referral_date_only])` pattern; the Gold active relationship
already filters on `referral_created_date`.

```DAX
Referrals Not Yet Closed (Created in Period) =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Referrals With Offers (Created in Period) =
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )

Offer Receipt Rate (Created in Period) =
DIVIDE ( [Referrals With Offers (Created in Period)], [Total Referrals] )
```

> `Offer Receipt Rate (Created in Period)` ports the legacy measure named
> `Total Referrals That Received Offers`, which despite its name returns a
> ratio, not a count.

### Under-offer referral offer portfolio

The legacy model scoped offer measures to referrals in `UNDER_OFFER` status
through a chain of `CALCULATETABLE`/`TREATAS` helper measures. In Gold the
active `fact_referral` to `fact_offer` relationship makes this a single
cross-table filter, matching the existing `Offers on Referrals Under Offer`
pattern.

```DAX
Draft Offers on Referrals Under Offer =
CALCULATE (
    [Offers in Draft],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Pending Offers on Referrals Under Offer =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Successful Offers on Referrals Under Offer =
CALCULATE (
    [Accepted Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Unsuccessful Offers on Referrals Under Offer =
CALCULATE (
    [Unsuccessful Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Spot Offers on Referrals Under Offer =
CALCULATE (
    [Spot Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Framework Offers on Referrals Under Offer =
CALCULATE (
    [Non-Spot Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Providers With Offers on Referrals Under Offer =
CALCULATE (
    [Providers Who Made Offers],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Average Offers per Provider - Under Offer =
DIVIDE (
    [Offers on Referrals Under Offer],
    [Providers With Offers on Referrals Under Offer]
)

Draft Offers With No Activity - Under Offer Referrals =
CALCULATE (
    [Draft Offers With No Activity Since Creation],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)

Draft Offers Stalled 14+ Days - Under Offer Referrals =
CALCULATE (
    [Draft Offers Stalled 14+ Days],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "under_offer", "under offer", "offer" }
    )
)
```

> Legacy `Draft Offer Count (Under Offer Referrals)` and `Offers per Provider
> (Under Offer Referrals)` are exact duplicates of `Draft Offers on Referrals
> Under Offer` and `Offers on Referrals Under Offer`; they are not recreated
> as separate measures.

### IPA signature funnel (referral-level proxies)

The legacy funnel (`IPA Created`, `IPA Completed`, `IPAs Pending Completion`,
`IPA Created to Completion %`, `Successful Offers to IPA Completed %`) read
`fact_ipa[signed_by_provider]` and `fact_ipa[signed_by_local_authority]`.
Gold has no IPA-grain signature fields, so the funnel is ported at referral
grain using the existing `ipa_2_signatures` proxy. Like-for-like IPA-grain
signature measures remain blocked (see the do-not-recreate list).

`Referrals With IPA` also closes a dangling dependency: `IPA Signature
Completion Rate` already references it, but it was never defined.

```DAX
Referrals With IPA =
CALCULATE (
    [Total Referrals],
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[ipa_issued_date] ) )
)

Referrals With IPA Pending Signature =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
            && COALESCE ( 'fact_referral'[ipa_2_signatures], FALSE () ) = FALSE ()
    )
)

IPA Signature Pending Rate =
DIVIDE ( [Referrals With IPA Pending Signature], [Referrals With IPA] )
```

### Snapshot target measures

`fact_referral_snapshot` carries every `fact_referral` column including
`placed_by_required_date`, so the legacy target-at-snapshot pair ports
directly. Legacy `Referrals with Placement at Snapshot` is a name alias of
the existing `Referrals with IPA at Snapshot`.

```DAX
Referrals Placed by Target at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    'fact_referral_snapshot'[placed_by_required_date] = TRUE ()
)

Target Hit Rate at Snapshot =
DIVIDE (
    [Referrals Placed by Target at Snapshot],
    CALCULATE (
        [Snapshot Referrals],
        FILTER (
            'fact_referral_snapshot',
            NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
                && NOT ISBLANK ( 'fact_referral_snapshot'[required_placement_date] )
        )
    )
)
```

### Row-level visual helpers

Legacy per-row Yes/No flags used on the IPA funnel and provider registry
pages. These evaluate in a single-row visual context (`SELECTEDVALUE`); they
are not aggregation measures.

```DAX
Is Non Framework Provider =
IF ( CALCULATE ( COUNTROWS ( 'bridge_provider_framework' ) ) = 0, 1, 0 )

IPA Exists =
VAR current_offer = SELECTEDVALUE ( 'fact_offer'[offer_id] )
RETURN
    IF (
        CALCULATE (
            COUNTROWS ( 'fct_ipa' ),
            TREATAS ( { current_offer }, 'fct_ipa'[accepted_offer_id] )
        ) > 0,
        "Yes",
        "No"
    )

Is Awaiting IPA Creation =
VAR current_offer = SELECTEDVALUE ( 'fact_offer'[offer_id] )
VAR accepted_offers =
    CALCULATETABLE (
        VALUES ( 'fact_offer'[offer_id] ),
        FILTER (
            'fact_offer',
            LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
                IN { "accepted", "approved", "selected", "offer_successful" }
        )
    )
VAR ipa_offers =
    CALCULATETABLE (
        VALUES ( 'fct_ipa'[accepted_offer_id] ),
        FILTER ( 'fct_ipa', NOT ISBLANK ( 'fct_ipa'[accepted_offer_id] ) )
    )
RETURN
    IF ( current_offer IN EXCEPT ( accepted_offers, ipa_offers ), 1, 0 )
```

> Legacy `Is IPA Completed`, `Is IPA Pending` and `Is In Accepted KPI` need
> IPA-grain signature flags and stay blocked; use the referral-grain proxy
> measures above instead.


### Legacy-to-Gold alias map

These legacy measures are already satisfied by an existing Gold measure
under a different name; rename visuals at reconciliation time, do not
recreate.

| Legacy v15 measure | Gold measure |
| --- | --- |
| Open Referral | Open Referrals |
| Referrals This Month | Referrals Created This Month |
| Referrals This FY | Referrals Created This Financial Year |
| Referrals With Offers / Referrals With One or More Offers | Referrals With an Offer |
| Active Referrals Awaiting Offers | Referrals Awaiting Offer |
| Active Referrals Under Offer | Referrals Under Offer |
| Referrals Cancelled/Closed | Closed or Cancelled Referrals |
| Closed Referrals (by Reason) | Closed Referrals + `fact_referral[referral_closure_reason]` visual dimension |
| Active Awaiting Offers (Engaged) | Active Referrals With Provider Engagement |
| Active Awaiting Offers (No Engagement) | Active Awaiting Offers Without Engagement |
| Offer Count / Total Offers Made Historically / (NEW)Total Offers Made / Latest Offer Status Count | Offers Submitted (Gold `fact_offer` holds the latest state per offer) |
| Placement Type Totals (Visual) | Total Referrals + `fact_referral[placement_type_required]` visual dimension |
| Offers At Risk (8-14 Days) | Pending Offers 8-14 Days |
| Offers Outside Timeframe (15-30 Days) | Pending Offers 15-29 Days |
| Critical Offers (30+ Days) | Pending Offers 30+ Days |
| Provider with Offers over 30+ Days | Providers With Pending Offers 30+ Days |
| Draft No Activity 7+ Days | Draft Offers Stalled 7+ Days |
| Drafts With No Activity 14+ Days | Draft Offers Stalled 14+ Days |
| Draft Offers Updated After Creation | Draft Offers With Activity Since Creation |
| Draft With No Activity Since Creation (%) | Draft Offers With No Activity % |
| Latest Export per Offer | Latest Offer Source Export |
| Dashboard Last Refreshed: | Gold Model Last Refreshed |
| Average Active Weekly Cost | Average Active IPA Weekly Cost |
| Overlap Referrals | Referrals With Multiple Provider Assignments |
| Fostering Providers | Providers - Fostering |
| NON Framework Providers | Non-Framework Providers |
| Total Offers Made (Active Referrals Under Offer) | Offers on Referrals Under Offer |
| Avg Offers per Referral Under Offer | Average Offers per Referral Under Offer |
| IPA Created (successful offers with IPA) | Accepted Offers With IPA |
| IPAs Created | IPAs Created (identical name) |
| Offers Still to Progress to IPA | Offers Awaiting IPA Creation |
| Referrals with Placement at Snapshot | Referrals with IPA at Snapshot |
| IPA Completed / IPA Created to Completion % / Successful Offers to IPA Completed % | Referral-grain proxies: Referrals With Fully Signed IPA, IPA Signature Completion Rate |

### Retired report-construct helpers

These legacy measures exist only to drive v15 report navigation or SCD
latest-export logic. They are deliberately **not** recreated in the Gold
model.

| Legacy v15 measure | Why retired |
| --- | --- |
| Accepted Offers Base / Accepted Offers (Scoped Table) / Offer IDs (Under Offer Referrals) | Internal `CALCULATETABLE` helpers; the Gold relationship graph and `TREATAS` patterns make them unnecessary |
| KPI Tooltip Style 1 | Reads the `ref_KPI` functional-spec metadata table, which is not a Gold object; re-import `ref_KPI` as a static table if the tooltip page is rebuilt |
| Directory Summary Count / Fostering Chart Count | Depend on the `Directory Summary Axis` and `rpt_provider_fostering` report-view tables; rebuild with field parameters over `dim_provider_home[service_type]` |
| Pending Offers by Age Bucket | Depended on the disconnected `Draft Age Band Table`; the four pending-age measures cover the same bands |
| Latest Export per Offer / Latest Offer Status Count | Gold `fact_offer` is already deduplicated to the latest state per offer |
| Dashboard Last Refreshed: | Superseded by Gold Model Last Refreshed (`gold_modelled_at`) |

### Additional blocked legacy measures

These rows extend the do-not-recreate list above; they must not be pointed
at Bronze, Silver or legacy tables.

| Do not recreate yet | Missing active-Gold field or grain |
| --- | --- |
| Provider Contact Referral card family (6 measures: base, Previous Month, Variance, MoM %, Indicator, Indicator Color) | No provider-contact flag (legacy `dim_referral[contact_made]`) anywhere in the active Gold referral fact. `is_not_seen_by_providers` is an offer-visibility flag, not a safe substitute. |
| Female / Male / Other / Total Gendered Referrals | Already covered by the KPI-04-07 entry: no child gender field in the active Gold referral fact. |
| Is IPA Completed / Is IPA Pending / Is In Accepted KPI | Already covered by the KPI-77-86 entry: no IPA-grain signature status. Use the referral-grain proxies instead. |
