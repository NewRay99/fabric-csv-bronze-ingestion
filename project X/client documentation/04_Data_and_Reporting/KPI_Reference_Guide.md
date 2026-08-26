# KPI Reference Guide — Active Gold semantic model

This is the authoritative KPI reference for the notebook-created Gold model.
Do not create a new KPI against Bronze, Silver, an extracted v15 table, or a
retired Gold object.

## Naming convention

All active Gold table and column names are lower-case `snake_case`, matching
Silver. The IPA fact is `gold.fct_ipa`; the retired `gold.fact_placement`
object is removed by the Gold model deployment.

| Role | Active Gold table | Grain | Key |
| --- | --- | --- | --- |
| Current referral | `gold.fact_referral` | One current row per referral | `referral_id` |
| Historic referral state | `gold.fact_referral_snapshot` | One referral per reporting snapshot | `snapshot_date`, `referral_id` |
| Offer | `gold.fact_offer` | One offer | `offer_id` |
| IPA | `gold.fct_ipa` | One IPA | `ipa_id` |
| Provider response | `gold.fact_referral_provider` | One referral-provider assignment | `referral_provider_id` |
| Lifecycle evidence | `gold.fact_referral_lifecycle_event` | One derived event | `event_id` |

The active supporting tables are `gold.dim_date`, `gold.dim_provider`,
`gold.dim_provider_home`, `gold.dim_framework`,
`gold.dim_framework_category`, `gold.dim_placement_type`,
`gold.dim_referral_status`, `gold.dim_provider_submission_document`,
`gold.bridge_provider_framework`, and `gold.bridge_provider_sic_code`.

## Semantic-model build rules

Import only the active tables above. Create single-direction relationships from
`fact_referral[referral_id]` to the referral keys on `fact_offer`, `fct_ipa`,
and `fact_referral_provider`. Use inactive role-playing date relationships for
creation, required-placement, IPA-issued and closure dates. Keep
`fact_referral_snapshot` separate from current-state facts and use its
`snapshot_date` for historic trends.

## Requirement mapping

| KPI area | Requirement IDs | Active evidence |
| --- | --- | --- |
| Referral status, target, responsiveness and snapshot trend | R24, R51–R53, R69 | Referral and snapshot facts |
| Offer submission, decision and acceptance | R28, R29, R36, R51 | Offer fact |
| Digitised IPA, current IPA and cost analysis | R35, R51, R62, R71 | `fct_ipa` and referral IPA fields |
| Provider assignment and decline analysis | R25, R28, R51, R54 | Referral-provider fact |

## DAX implementation

Copy-ready DAX, the v15 reconciliation, required relationships, and the
measures that cannot yet be recreated are in
[Gold Semantic Model DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md).

## Source limitations

`estimated_weekly_cost` is an estimate, not an invoice or actual payment.
`region`, `complexity_band`, actual placement dates/cost, duration and end
reason remain null until a reliable source supplies them. A measure should not
turn those nulls into invented business values.
