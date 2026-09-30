# WMPP semantic model measure catalogue

Inventory reviewed 30 September 2026 from the saved **SM WMPP v16 updated WIP** model. There are 58 model tables and 366 measures across seven measure containers. This includes formatting, interaction and compatibility helpers. The Dashboard Legend contains 144 curated business entries, including 35 additions to its previous 109-entry catalogue. Presence is not evidence of successful refresh or UAT.

See [current status and limits](WMPP_CURRENT_STATUS.md) and [requirement reassessment](WMPP_REQUIREMENT_REASSESSMENT.md). Names below are exact model names so users can locate their definitions.

| Measure container | Definitions |
| --- | --- |
| _Design Measures | 18 |
| _Explore Measures | 12 |
| _Journey Interaction | 23 |
| _Journey Measures | 41 |
| _Measures | 259 |
| _Provider Detail Measures | 6 |
| _Story Measures | 7 |

## Source model objects

Gold imports and local selector/reference/calculated tables are distinguished; 58 is not the count of warehouse tables.

| Model table | Kind | Source | Key or grain |
| --- | --- | --- | --- |
| _Design Measures | Measure container | Local empty import partition | See model columns and source definition |
| _Explore Measures | Measure container | Local empty import partition | See model columns and source definition |
| _Journey Interaction | Measure container | Local empty import partition | See model columns and source definition |
| _Journey Measures | Measure container | Local empty import partition | See model columns and source definition |
| _Measures | Measure container | Local empty import partition | See model columns and source definition |
| _Provider Detail Measures | Measure container | Local empty import partition | See model columns and source definition |
| _Story Measures | Measure container | Local empty import partition | See model columns and source definition |
| bridge_provider_framework | Gold import | gold.bridge_provider_framework | See model columns and source definition |
| bridge_provider_home_framework_category | Gold import | gold.bridge_provider_home_framework_category | See model columns and source definition |
| bridge_provider_sic_code | Gold import | gold.bridge_provider_sic_code | See model columns and source definition |
| bridge_referral_framework_category | Gold import | gold.bridge_referral_framework_category | referral_id + framework_category_id |
| bridge_referral_scope | Gold import | gold.bridge_referral_scope | See model columns and source definition |
| Dashboard Metric Selector | Local model table | Calculated or embedded import | See model columns and source definition |
| Days to Target | Local model table | Calculated or embedded import | See model columns and source definition |
| dim_category | Gold import | gold.dim_framework_category | See model columns and source definition |
| dim_date | Gold import | gold.dim_date | See model columns and source definition |
| dim_framework | Gold import | gold.dim_framework | See model columns and source definition |
| dim_framework_category | Gold import | gold.dim_framework_category | See model columns and source definition |
| dim_offer_status | Gold import | gold.dim_offer_status | See model columns and source definition |
| dim_person | Gold import | gold.dim_person | person_id |
| dim_placement_type | Gold import | gold.dim_placement_type | See model columns and source definition |
| dim_provider | Gold import | gold.dim_provider | provider_id |
| dim_provider_home | Gold import | gold.dim_provider_home | provider_home_id |
| dim_provider_submission_document | Gold import | gold.dim_provider_submission_document | See model columns and source definition |
| dim_referral_provider_message | Gold import | gold.dim_referral_provider_message | message_id |
| dim_referral_provider_reject_reason | Gold import | gold.dim_referral_provider_reject_reason | reject_reason_id |
| dim_security_scope | Gold import | gold.dim_security_scope | See model columns and source definition |
| dim_snapshot_month | Gold import | gold.dim_snapshot_month | See model columns and source definition |
| Directory Summary Axis | Local model table | Calculated or embedded import | See model columns and source definition |
| Draft Age Band Table | Local model table | Calculated or embedded import | See model columns and source definition |
| fact_ipa | Gold import | gold.fact_ipa | ipa_id |
| fact_offer | Gold import | gold.fact_offer | offer_id |
| fact_provider_kpi_monthly | Gold import | gold.fact_provider_kpi_monthly | See model columns and source definition |
| fact_referral | Gold import | gold.fact_referral | referral_id |
| fact_referral_global_summary | Gold import | gold.fact_referral_global_summary | See model columns and source definition |
| fact_referral_lifecycle_event | Gold import | gold.fact_referral_lifecycle_event | event_id |
| fact_referral_provider | Gold import | gold.fact_referral_provider | referral_provider_id |
| fact_referral_snapshot | Gold import | gold.fact_referral_snapshot | snapshot_date + referral_id |
| Fostering Axis | Local model table | Calculated or embedded import | See model columns and source definition |
| gold referral_journey_flow | Gold import | gold.referral_journey_flow | See model columns and source definition |
| gold rpt_kpi_referral_board_summary | Gold import | gold.rpt_kpi_referral_board_summary | See model columns and source definition |
| Journey Detail Selection | Local model table | Calculated or embedded import | See model columns and source definition |
| Journey Provider Selection | Local model table | Calculated or embedded import | See model columns and source definition |
| KPI Selector | Local model table | Calculated or embedded import | See model columns and source definition |
| Offer Category | Local model table | Calculated or embedded import | See model columns and source definition |
| Offer Journey Stage | Local model table | Calculated or embedded import | See model columns and source definition |
| Open Referral Age | Local model table | Calculated or embedded import | See model columns and source definition |
| Placement Window | Local model table | Calculated or embedded import | See model columns and source definition |
| ref_KPI | Local model table | Calculated or embedded import | See model columns and source definition |
| ref_KPI_RID_Linkage | Local model table | Calculated or embedded import | See model columns and source definition |
| ref_RID | Local model table | Calculated or embedded import | See model columns and source definition |
| Referral Breakdown | Local model table | Calculated or embedded import | See model columns and source definition |
| Referral Category | Local model table | Calculated or embedded import | See model columns and source definition |
| Referral Map Points | Local model table | Calculated or embedded import | See model columns and source definition |
| Referral Metric | Local model table | Calculated or embedded import | See model columns and source definition |
| sec_user_scope_access | Gold import | gold.sec_user_scope_access | See model columns and source definition |
| Snapshot Window | Local model table | Calculated or embedded import | See model columns and source definition |
| Target Status | Local model table | Calculated or embedded import | See model columns and source definition |

## Design Measures

Definition: [_Design Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Design%20Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Snapshot Window Months | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Snapshot Window Anchor | — | Other model calculation | Referral Snapshots |
| Snapshot Month In Window | — | Other model calculation | Referral Snapshots |
| Current Referral As Of | — | Other model calculation | Overall Performance, Provider & Placement Supply, Target & Urgency Performance, WMPP Homepage |
| Critical Overdue Referrals | GOLD-KPI-144 | Catalogue business measure | Overall Performance |
| Critical Target Hit Rate | — | Other model calculation | Target & Urgency Performance |
| Referrals Due in Reporting Period | — | Other model calculation | Target & Urgency Performance |
| Referrals Due This As Of Month | — | Other model calculation | Target & Urgency Performance |
| Open Referrals Due in 3 Days | — | Other model calculation | Target & Urgency Performance |
| Average Days Early | — | Other model calculation | Target & Urgency Performance |
| Homes Offered | GOLD-KPI-143 | Catalogue business measure | Provider & Placement Supply |
| Median Offered Weekly Cost | — | Other model calculation | Provider & Placement Supply |
| Provider Median Days to First Offer | — | Other model calculation | Provider & Placement Supply |
| Open Referrals by Target Status | — | Other model calculation | Overall Performance, Target & Urgency Performance |
| Open Referrals by Days to Target | — | Other model calculation | Target & Urgency Performance |
| Open Referrals by Age | — | Other model calculation | Target & Urgency Performance |
| Cohort Placement Within Window | — | Other model calculation | Target & Urgency Performance |
| Offer Journey Count | — | Other model calculation | Provider & Placement Supply |

## Explore Measures

Definition: [_Explore Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explore%20Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Referrals | — | Other model calculation | Referral Geography |
| Category-aware open referrals | — | Other model calculation | Referral Geography |
| Awaiting offer | — | Other model calculation | Referral Geography |
| Under offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Completed IPAs | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Mapped referrals | — | Other model calculation | Referral Explorer, Referral Geography |
| Location review | — | Other model calculation | Referral Geography |
| Median preferred-city distance km | GOLD-KPI-142 | Catalogue business measure | Offer Locations |
| Offers with preferred-city distance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers without preferred-city distance | — | Other model calculation | Offer Locations |
| Preferred-city distance coverage | GOLD-KPI-141 | Catalogue business measure | Offer Locations |

## Journey Interaction

Definition: [_Journey Interaction.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey%20Interaction.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Rail referrals 1 | — | Other model calculation | Referral Explorer |
| Rail referral circle 1 | — | Display or filter helper | Referral Explorer |
| Rail referrals 2 | — | Other model calculation | Referral Explorer |
| Rail referral circle 2 | — | Display or filter helper | Referral Explorer |
| Rail referrals 3 | — | Other model calculation | Referral Explorer |
| Rail referral circle 3 | — | Display or filter helper | Referral Explorer |
| Rail referrals 4 | — | Other model calculation | Referral Explorer |
| Rail referral circle 4 | — | Display or filter helper | Referral Explorer |
| Rail referrals 5 | — | Other model calculation | Referral Explorer |
| Rail referral circle 5 | — | Display or filter helper | Referral Explorer |
| Rail referrals 6 | — | Other model calculation | Referral Explorer |
| Rail referral circle 6 | — | Display or filter helper | Referral Explorer |
| Rail referral summary | — | Other model calculation | Referral Explorer |
| Rail provider circle 1 | — | Display or filter helper | Provider Explorer |
| Rail provider circle 2 | — | Display or filter helper | Provider Explorer |
| Rail provider circle 3 | — | Display or filter helper | Provider Explorer |
| Rail provider circle 4 | — | Display or filter helper | Provider Explorer |
| Rail provider circle 5 | — | Display or filter helper | Provider Explorer |
| Rail provider row visible | — | Display or filter helper | Provider Explorer |
| Rail provider cohort label | — | Display or filter helper | Provider Explorer |
| Rail provider selected metric | — | Display or filter helper | Provider Explorer |
| Rail activity row visible | — | Display or filter helper | Referral Detail (Drillthrough) |
| Rail activity caption | — | Display or filter helper | Referral Detail (Drillthrough) |

## Journey Measures

Definition: [_Journey Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey%20Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Journey referrals 1 | GOLD-KPI-123 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 2 | GOLD-KPI-124 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 3 | GOLD-KPI-125 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 4 | GOLD-KPI-126 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 5 | GOLD-KPI-127 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 6 | GOLD-KPI-128 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 7 | GOLD-KPI-129 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referrals 8 | GOLD-KPI-130 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey referral reconciliation | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Journey referral exceptions | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Journey selected stage | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey current position | — | Other model calculation | Referral Detail (Drillthrough) |
| Journey next action | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Journey detail evidence 1 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 1 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 1 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail evidence 2 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 2 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 2 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail evidence 3 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 3 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 3 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail evidence 4 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 4 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 4 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail evidence 5 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 5 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 5 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail evidence 6 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey detail label 6 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey detail colour 6 | — | Display or filter helper | Referral Detail (Drillthrough) |
| Journey provider stage | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Journey providers 0 | GOLD-KPI-131 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey providers 1 | GOLD-KPI-132 | Catalogue business measure | Provider Explorer |
| Journey providers 2 | GOLD-KPI-133 | Catalogue business measure | Provider Explorer |
| Journey providers 3 | GOLD-KPI-134 | Catalogue business measure | Provider Explorer |
| Journey providers 5 | GOLD-KPI-135 | Catalogue business measure | Provider Explorer |
| Journey providers 4 | — | Other model calculation | Provider Explorer |
| Journey provider label | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Journey providers both signed | GOLD-KPI-136 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Journey provider coverage | — | Other model calculation | Provider Explorer |

## Measures

Definition: [_Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Total Referrals | GOLD-KPI-001 | Catalogue business measure | Historic, Overall Performance, Referral Explorer, Referrals |
| Referrals Awaiting Offer | GOLD-KPI-005 | Catalogue business measure | Historic, Offers Overview, Referrals, Requirement Matrix Overview |
| No. Providers Who Made Offers | — | Other model calculation | Historic, Offers Overview, Requirement Matrix Overview |
| Avg Offers per Provider (Under Offer) | — | Other model calculation | Historic, Offers Overview, Requirement Matrix Overview |
| Successful Offers on Referrals Under Offer | — | Other model calculation | Historic, IPA Overview, Offers Overview |
| Unsuccessful Offers (Under Offer Referrals) | — | Other model calculation | Historic, Offers Overview |
| Offers in Draft | GOLD-KPI-019 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers (Under Offer Referrals) | — | Other model calculation | Historic, Offers Overview |
| Male Referrals | GOLD-KPI-110 | Catalogue business measure | Referrals |
| Female Referrals | GOLD-KPI-111 | Catalogue business measure | Referrals |
| Other Gender Referrals | GOLD-KPI-112 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Total Gendered Referrals | GOLD-KPI-113 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Homes Registered | GOLD-KPI-076 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers Registered | GOLD-KPI-077 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active | GOLD-KPI-041 | Catalogue business measure | Historic, Offers Overview, Referrals, Requirement Matrix Overview |
| Closed or Cancelled Referrals | GOLD-KPI-043 | Catalogue business measure | Historic, Referrals |
| Draft No Activity Since Creation (Under Offer Referrals) | — | Other model calculation | Draft Offers |
| Draft Offers With Activity Since Creation | GOLD-KPI-064 | Catalogue business measure | Draft Offers |
| Draft Offers Missing Dates | GOLD-KPI-065 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Drafts No Activity 14+ Days (Under Offer Referrals) | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Average Days in Draft | GOLD-KPI-067 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Oldest Draft Age Days | GOLD-KPI-068 | Catalogue business measure | Draft Offers |
| Draft Offer Count (Under Offer Referrals) | — | Other model calculation | Draft Offers, Historic, Offers Overview |
| Providers - Fostering | GOLD-KPI-078 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers - Residential | GOLD-KPI-079 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers - Supported Accommodation | GOLD-KPI-080 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Framework Providers | GOLD-KPI-084 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Non-Framework Providers | GOLD-KPI-085 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Is Non Framework Provider | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Directory Summary Count | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Residential Homes | GOLD-KPI-081 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Supported Accommodation Homes | GOLD-KPI-082 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers 15-29 Days | GOLD-KPI-072 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers 30+ Days | GOLD-KPI-073 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers 0-7 Days | GOLD-KPI-070 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers 8-14 Days | GOLD-KPI-071 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Not Yet Closed (Created in Period) | — | Other model calculation | Referrals |
| Referrals With Offers (Created in Period) | — | Other model calculation | Historic, Referrals |
| Total Referrals That Received Offers (Ratio) | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals With Provider Engagement | GOLD-KPI-044 | Catalogue business measure | Offers Overview, Referrals |
| Active Referral Engagement Rate | GOLD-KPI-045 | Catalogue business measure | Offers Overview, Referrals |
| Active Awaiting Offers With Engagement | GOLD-KPI-046 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Active Awaiting Offers Without Engagement | GOLD-KPI-047 | Catalogue business measure | Referrals |
| Offers per Provider (Under Offer Referrals) | — | Other model calculation | Offers Overview |
| Spot Offers | GOLD-KPI-060 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Framework Offers (Under Offer Referrals) | — | Other model calculation | Offers Overview |
| IPA Exists | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Is In Accepted KPI | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| IPA Completed | GOLD-KPI-114 | Catalogue business measure | IPA Overview, Referral Explorer |
| IPAs Pending Completion | GOLD-KPI-115 | Catalogue business measure | IPA Overview, Referral Detail (Drillthrough), Referral Explorer (Original) |
| Offers Awaiting IPA Creation | GOLD-KPI-100 | Catalogue business measure | IPA Overview |
| Is IPA Pending | — | Other model calculation | IPA Overview, Referral Detail (Drillthrough), Referral Explorer (Original) |
| Is Awaiting IPA Creation | — | Other model calculation | IPA Overview |
| Is IPA Completed | — | Other model calculation | IPA Overview, Referral Detail (Drillthrough), Referral Explorer (Original) |
| Accepted Offer to IPA Conversion % | GOLD-KPI-101 | Catalogue business measure | IPA Overview |
| IPA Created to Completion % | — | Other model calculation | IPA Overview |
| Successful Offers to IPA Completed % | — | Other model calculation | IPA Overview |
| Open Referrals Previous Month | — | Other model calculation | Draft Offers, IPA Overview, Offers Overview, Referrals, Requirement Matrix Overview |
| Closed Referrals Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Open Referrals MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed Referrals MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referral | — | Other model calculation | Referrals |
| Provider Contact Referral Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referrals MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed Referrals Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Closed Referrals Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Open Referrals Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referral Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Open Referrals Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referral Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Closed Referrals Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Open Referrals Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referral Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Cancelled/Closed Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With an Offer Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Total Offers Made Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Cancelled/Closed Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Cancelled/Closed Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With an Offer Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Total Offers Made Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals With an Offer Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Total Offers Made Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Total Offers Made Variance Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Total Referrals That Received Offers Previous Month | — | Other model calculation | Referrals |
| Total Referrals That Received Offers Variance | — | Other model calculation | Referrals |
| Total Referrals That Received Offers Variance Indicator Color | — | Display or filter helper | Referrals |
| Total Referrals Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Total Referrals Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Total Referrals Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Total Referrals Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referrals Awaiting Offers Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals Under Offer Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals Awaiting Offers Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals Awaiting Offers Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referrals Awaiting Offers Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referrals Under Offer Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals Under Offer Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referrals Under Offer Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referral Engagement Rate Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referral Engagement Rate Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referral Engagement Rate Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referral Engagement Rate Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| KPI Tooltip Style 1 | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Snapshot Referrals | GOLD-KPI-028 | Catalogue business measure | Overall Performance, Referral Snapshots, Referrals |
| Open Referrals at Snapshot | GOLD-KPI-029 | Catalogue business measure | Referral Snapshots |
| Closed or Cancelled Referrals at Snapshot | — | Other model calculation | Overall Performance, Referral Snapshots, Referrals |
| Active Referrals Awaiting Offers at Snapshot | — | Other model calculation | Referral Snapshots |
| Active Referrals Under Offer at Snapshot | — | Other model calculation | Referral Snapshots, Referrals |
| Referrals With an Offer at Snapshot | — | Other model calculation | Referrals |
| Total Offers at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Contact Referrals at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Referrals With Provider Response at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Active Provider Response Rate at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed Referrals at Snapshot | GOLD-KPI-030 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Open On-Track Referrals at Snapshot | GOLD-KPI-033 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Placed by Target at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Open Overdue Referrals | GOLD-KPI-007 | Catalogue business measure | Target & Urgency Performance |
| Open Referral Rate at Snapshot | GOLD-KPI-034 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Placement Rate at Snapshot | GOLD-KPI-035 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Target Hit Rate at Snapshot | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Estimated Active Weekly Cost | GOLD-KPI-023 | Catalogue business measure | Overall Performance |
| IPAs Created | GOLD-KPI-021 | Catalogue business measure | IPA Overview |
| Open Referrals | GOLD-KPI-002 | Catalogue business measure | Overall Performance, Referral Detail (Drillthrough), Referral Explorer (Original) |
| Referrals with IPA at Snapshot | GOLD-KPI-031 | Catalogue business measure | Referral Snapshots |
| Closed Referrals | GOLD-KPI-003 | Catalogue business measure | Referral Detail (Drillthrough), Referral Explorer (Original), Referrals |
| Referrals With an Offer | GOLD-KPI-004 | Catalogue business measure | Historic |
| Referrals Without Provider Assignment | GOLD-KPI-006 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Placed by Required Date | GOLD-KPI-008 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Placement Target Hit Rate | GOLD-KPI-009 | Catalogue business measure | Overall Performance, Target & Urgency Performance |
| Median Days to First Action | GOLD-KPI-010 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Median Days to First Offer | GOLD-KPI-011 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Median Days to IPA | GOLD-KPI-012 | Catalogue business measure | Overall Performance |
| Open Referrals Stalled 7+ Days | GOLD-KPI-013 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Offers Submitted | GOLD-KPI-014 | Catalogue business measure | Historic, Offer Locations, Overall Performance, Provider & Placement Supply, Referral Explorer |
| Accepted Offers | GOLD-KPI-015 | Catalogue business measure | Overall Performance, Provider & Placement Supply |
| Average Offers per Referral | GOLD-KPI-018 | Catalogue business measure | Provider & Placement Supply |
| Active IPAs | GOLD-KPI-022 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Average Estimated Weekly Cost — Confirmed Referrals | GOLD-KPI-024 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Open Overdue Referrals at Snapshot | GOLD-KPI-032 | Catalogue business measure | Referral Snapshots |
| Referrals Created This Month | GOLD-KPI-036 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Created Previous Month | GOLD-KPI-037 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referral Volume Month on Month | GOLD-KPI-038 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referral Volume Month on Month % | GOLD-KPI-039 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Created This Financial Year | GOLD-KPI-040 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer | GOLD-KPI-042 | Catalogue business measure | Historic, Offers Overview, Referrals |
| Emergency Referrals | GOLD-KPI-048 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Planned Referrals | GOLD-KPI-049 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Emergency Placement Rate | GOLD-KPI-050 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Non-Draft Offers | GOLD-KPI-052 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers | GOLD-KPI-053 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Unsuccessful Offers on Referrals Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Providers Who Made Offers | GOLD-KPI-056 | Catalogue business measure | Provider & Placement Supply |
| Average Offers per Referral Under Offer | GOLD-KPI-058 | Catalogue business measure | Historic, Offers Overview, Requirement Matrix Overview |
| Average Offers per Provider | GOLD-KPI-057 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer | GOLD-KPI-059 | Catalogue business measure | Offers Overview, Requirement Matrix Overview |
| Non-Spot Offers | GOLD-KPI-061 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Fostering Homes | GOLD-KPI-083 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers With QA Flags | GOLD-KPI-086 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| QA Flagged Homes | GOLD-KPI-087 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers Pending Onboarding | GOLD-KPI-088 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Providers Approved | GOLD-KPI-089 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Onboarding Success Rate | GOLD-KPI-090 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| IPAs Issued This Month | GOLD-KPI-095 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Closed IPAs | GOLD-KPI-096 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Average Active IPA Weekly Cost | GOLD-KPI-097 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Total IPA Weekly Cost | GOLD-KPI-098 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Accepted Offers With IPA | GOLD-KPI-099 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Offers Still to Progress to IPA % | GOLD-KPI-102 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals With Fully Signed IPA | GOLD-KPI-103 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| IPA Signature Completion Rate | GOLD-KPI-104 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals With IPA | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Gold Model Last Refreshed | GOLD-KPI-108 | Catalogue business measure | Draft Offers, IPA Overview, Offer Locations, Offers Overview, Overall Performance, Provider & Placement Supply, Provider Detail (Drillthrough), Provider Explorer, Referral Detail (Drillthrough), Referral Explorer, Referral Geography, Referrals, Requirement Matrix Overview, Target & Urgency Performance, WMPP Homepage |
| Total Referrals MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With an Offer MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With an Offer Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Awaiting Offer Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Awaiting Offer Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Awaiting Offer MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Awaiting Offer Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Awaiting Offer Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Under Offer Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals Currently Active Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Closed or Cancelled Referrals Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed or Cancelled Referrals Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed or Cancelled Referrals MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Closed or Cancelled Referrals Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Closed or Cancelled Referrals Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Active Referral Engagement Rate MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Offers on Referrals Under Offer Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Draft Offers on Referrals Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Pending Offers on Referrals Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Spot Offers on Referrals Under Offer | — | Other model calculation | Offers Overview |
| Framework Offers on Referrals Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Providers With Offers on Referrals Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Average Offers per Provider - Under Offer | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With IPA Pending Signature | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| IPA Signature Pending Rate | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offers with a Decision | GOLD-KPI-016 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Offer Acceptance Rate | GOLD-KPI-017 | Catalogue business measure | Provider & Placement Supply |
| Draft Offers Stalled 7+ Days | GOLD-KPI-020 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals With Multiple Provider Assignments | GOLD-KPI-051 | Catalogue business measure | Offers Overview, Referrals |
| Offers With Recorded Rejection Reason | GOLD-KPI-055 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Spot Offer Rate | GOLD-KPI-062 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Draft Offers With No Activity Since Creation | GOLD-KPI-063 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Draft Offers Stalled 14+ Days | GOLD-KPI-066 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Draft Offers With No Activity % | GOLD-KPI-069 | Catalogue business measure | Draft Offers |
| Providers With Pending Offers 30+ Days | GOLD-KPI-074 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Submission Documents | GOLD-KPI-091 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Documents Expiring Next 30 Days | GOLD-KPI-092 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Documents Expired | GOLD-KPI-093 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Homes With Expired Documents | GOLD-KPI-094 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referral Lifecycle Events | GOLD-KPI-105 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Referrals With Lifecycle Activity | GOLD-KPI-106 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Average Lifecycle Events per Referral | GOLD-KPI-107 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Messages Sent | GOLD-KPI-109 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) Previous Month | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) Variance | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) MoM % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) Variance Indicator | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Offer Receipt Rate (Created in Period) Variance Indicator Color | — | Display or filter helper | No direct visual binding found; may be a DAX dependency |
| Draft Offers With No Activity - Under Offer Referrals | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Draft Offers Stalled 14+ Days - Under Offer Referrals | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Unsuccessful Offers | GOLD-KPI-054 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Latest Offer Source Export | GOLD-KPI-075 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Assignments | GOLD-KPI-025 | Catalogue business measure | Referral Explorer |
| Provider Declines | GOLD-KPI-026 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Decline Rate | GOLD-KPI-027 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Pending Offers Missing or Future Date | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| IPAs Signed by Provider | GOLD-KPI-116 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| IPAs Signed by Local Authority | GOLD-KPI-117 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Accepted Offers Linked to IPA % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Pending Offers 15–30 Days | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Drafts No Activity 14+ Days | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Drafts With No Activity Since Creation (Under Offer) % | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Other Referrals | — | Other model calculation | Referrals |
| Provider Response Opportunities | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Qualifying Responses | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Provider Response Rate | GOLD-KPI-137 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Offer Conversion Rate | GOLD-KPI-139 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Target Placement Rate | GOLD-KPI-140 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Provider Average Response Hours | GOLD-KPI-138 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Lifetime Placement Cost | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Total Lifetime Cost | — | Other model calculation | Overall Performance |
| Previous Snapshot Referrals | — | Other model calculation | Referrals |
| Last Snapshot Date | — | Other model calculation | No direct visual binding found; may be a DAX dependency |
| Referrals With Offers (Created in Period) % | — | Other model calculation | Referrals |

## Provider Detail Measures

Definition: [_Provider Detail Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Provider%20Detail%20Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Provider explorer matching homes | — | Other model calculation | Provider Explorer |
| Provider detail profile rows | — | Display or filter helper | Provider Detail (Drillthrough) |
| Provider detail home rows | — | Display or filter helper | Provider Detail (Drillthrough) |
| Provider detail assignment rows | — | Display or filter helper | Provider Detail (Drillthrough) |
| Provider detail offer rows | — | Display or filter helper | Provider Detail (Drillthrough) |
| Provider detail message rows | — | Display or filter helper | Provider Detail (Drillthrough) |

## Story Measures

Definition: [_Story Measures.tmdl](../../reports/client-deliverables/WMPP%20v16/SM%20WMPP%20v16%20updated%20WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story%20Measures.tmdl).

| Measure | Catalogue ID | Role | Direct visual bindings |
| --- | --- | --- | --- |
| Matching referrals | GOLD-KPI-122 | Catalogue business measure | Referral Explorer |
| Detail referral selected | — | Display or filter helper | Referral Detail (Drillthrough) |
| Detail map points | — | Other model calculation | Referral Detail (Drillthrough) |
| Referrals closed during month | GOLD-KPI-121 | Catalogue business measure | Overall Performance |
| Snapshot referrals previous month | GOLD-KPI-118 | Catalogue business measure | No direct visual binding found; may be a DAX dependency |
| Snapshot referrals MoM change | GOLD-KPI-119 | Catalogue business measure | Overall Performance |
| Snapshot referrals MoM percent | GOLD-KPI-120 | Catalogue business measure | Overall Performance |

## Historical catalogue

The earlier v01/Gold v02 inventory is retained below as historical evidence only. Its counts, table names and readiness statements do not describe the current WIP.

# WMPP v01 Semantic Model — Measure Catalogue

**Source project:** `project X/report v01 extracted/semantic_model __/SM_WMPP.pbip`
**Source file:** `SM_WMPP.SemanticModel/definition/tables/_Measures.tmdl`

## Current inventory

| Item | Count |
|---|---:|
| Tables | 79 |
| Columns | 850 |
| Relationships | 48 |
| Measures | 95 |

This catalogue is generated from the committed v01 TMDL and replaces the older V13.1 documentation that referred to 90 or 117 measures. Measure names are preserved exactly as defined in the semantic model.

## Active Gold v02 boundary

This is an inventory of the extracted **v01** Power BI model, not a declaration
of the active notebook-created Gold schema. In particular,
`fact_referral_offer` and `fact_ipa` are v01 names. The active objects are
`gold.fact_referral_provider` and `gold.fact_ipa`, with lower-case snake-case
fields throughout the active Gold model. This file is retained only as a v01
archive; do not recreate its measures against its legacy tables. The active
DAX build instructions are in
[Gold Semantic Model DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md).

## `Closed_Date` derivation

The v01 model now exposes `Closed_Date` in both `fact_referral_offer` and `fact_referral`:

1. `fact_referral_offer[Closed_Date]` returns the date portion of `modified_date` only when `has_offer = TRUE()`; otherwise it returns DAX `BLANK()`.
2. `fact_referral[Closed_Date]` returns the latest related `fact_referral_offer[Closed_Date]` across matching offer rows. If no related row has `has_offer = TRUE()`, it remains `BLANK()`/null.

The v01 `fact_referral_offer` table does not expose a separate upstream `closed_date` field. Therefore the implementation uses the available `modified_date` as the closure timestamp proxy. If the source system later provides a canonical closure timestamp, replace the row-level expression and retain the same null-handling rule.

## Measures by display folder

### Uncategorised

| Measure | Source |
|---|---|
| `'(NEW)Total Offers Made'` | `_Measures.tmdl` |
| `'Accepted Offer to IPA Conversion %'` | `_Measures.tmdl` |
| `'Accepted Offers (Scoped Table)'` | `_Measures.tmdl` |
| `'Accepted Offers Base'` | `_Measures.tmdl` |
| `'Active Awaiting Offers (Engaged)'` | `_Measures.tmdl` |
| `'Active Awaiting Offers (No Engagement)'` | `_Measures.tmdl` |
| `'Active Referral Engagement Rate'` | `_Measures.tmdl` |
| `'Active Referrals Awaiting Offers'` | `_Measures.tmdl` |
| `'Active Referrals Under Offer'` | `_Measures.tmdl` |
| `'Active Referrals With Provider Engagement'` | `_Measures.tmdl` |
| `'Average Days in Draft'` | `_Measures.tmdl` |
| `'Avg Offers per Provider (Under Offer)'` | `_Measures.tmdl` |
| `'Avg Offers per Referral Under Offer'` | `_Measures.tmdl` |
| `'Closed Referral Previous Month'` | `_Measures.tmdl` |
| `'Closed Referrals (by Reason)'` | `_Measures.tmdl` |
| `'Closed Referrals MoM %'` | `_Measures.tmdl` |
| `'Critical Offers (30+ Days)'` | `_Measures.tmdl` |
| `'Dashboard Last Refreshed:'` | `_Measures.tmdl` |
| `'Directory Summary Count'` | `_Measures.tmdl` |
| `'Draft No Activity 7+ Days'` | `_Measures.tmdl` |
| `'Draft No Activity Since Creation (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Draft Offer Count (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Draft Offers Missing Dates'` | `_Measures.tmdl` |
| `'Draft Offers Updated After Creation'` | `_Measures.tmdl` |
| `'Draft Offers With Activity Since Creation'` | `_Measures.tmdl` |
| `'Draft With No Activity Since Creation (%)'` | `_Measures.tmdl` |
| `'Drafts No Activity 14+ Days (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Drafts With No Activity 14+ Days'` | `_Measures.tmdl` |
| `'Female Referrals'` | `_Measures.tmdl` |
| `'Fostering Chart Count'` | `_Measures.tmdl` |
| `'Fostering Providers'` | `_Measures.tmdl` |
| `'Framework Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Framework Providers'` | `_Measures.tmdl` |
| `'IPA Completed'` | `_Measures.tmdl` |
| `'IPA Created to Completion %'` | `_Measures.tmdl` |
| `'IPA Created'` | `_Measures.tmdl` |
| `'IPA Exists'` | `_Measures.tmdl` |
| `'IPAs Pending Completion'` | `_Measures.tmdl` |
| `'Is Awaiting IPA Creation'` | `_Measures.tmdl` |
| `'Is In Accepted KPI'` | `_Measures.tmdl` |
| `'Is IPA Completed'` | `_Measures.tmdl` |
| `'Is IPA Pending'` | `_Measures.tmdl` |
| `'Is Non Framework Provider'` | `_Measures.tmdl` |
| `'Latest Export per Offer'` | `_Measures.tmdl` |
| `'Latest Offer Status Count'` | `_Measures.tmdl` |
| `'Male Referrals'` | `_Measures.tmdl` |
| `'No. Providers Who Made Offers'` | `_Measures.tmdl` |
| `'NON Framework Providers'` | `_Measures.tmdl` |
| `'Offer Count'` | `_Measures.tmdl` |
| `'Offer IDs (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers At Risk (8–14 Days)'` | `_Measures.tmdl` |
| `'Offers Awaiting IPA Creation'` | `_Measures.tmdl` |
| `'Offers in Draft (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers Outside Timeframe (15–30 Days)'` | `_Measures.tmdl` |
| `'Offers per Provider (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers Still to Progress to IPA'` | `_Measures.tmdl` |
| `'Oldest Draft Age (Days)'` | `_Measures.tmdl` |
| `'Open Referral Previous Month'` | `_Measures.tmdl` |
| `'Open Referral'` | `_Measures.tmdl` |
| `'Open Referrals MoM %'` | `_Measures.tmdl` |
| `'Other Referrals'` | `_Measures.tmdl` |
| `'Overlap Referrals'` | `_Measures.tmdl` |
| `'Pending Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Pending Offers 0–7 Days'` | `_Measures.tmdl` |
| `'Pending Offers 15–30 Days'` | `_Measures.tmdl` |
| `'Pending Offers 30+ Days'` | `_Measures.tmdl` |
| `'Pending Offers 8–14 Days'` | `_Measures.tmdl` |
| `'Pending Offers by Age Bucket'` | `_Measures.tmdl` |
| `'Placement Type Totals (Visual)'` | `_Measures.tmdl` |
| `'Provider Homes Registered'` | `_Measures.tmdl` |
| `'Provider with Offers over 30+ Days'` | `_Measures.tmdl` |
| `'Providers - Fostering'` | `_Measures.tmdl` |
| `'Providers - Residential'` | `_Measures.tmdl` |
| `'Providers - Supported Accommodation'` | `_Measures.tmdl` |
| `'Providers Registered'` | `_Measures.tmdl` |
| `'Referrals Awaiting Offer'` | `_Measures.tmdl` |
| `'Referrals Cancelled/Closed'` | `_Measures.tmdl` |
| `'Referrals Currently Active'` | `_Measures.tmdl` |
| `'Referrals Not Yet Closed (Created in Period)'` | `_Measures.tmdl` |
| `'Referrals This FY'` | `_Measures.tmdl` |
| `'Referrals This Month'` | `_Measures.tmdl` |
| `'Referrals With Offers (Created in Period)'` | `_Measures.tmdl` |
| `'Referrals With Offers'` | `_Measures.tmdl` |
| `'Referrals With One or More Offers'` | `_Measures.tmdl` |
| `'Residential Homes'` | `_Measures.tmdl` |
| `'Spot Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Successful Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Successful Offers to IPA Completed %'` | `_Measures.tmdl` |
| `'Supported Accommodation Homes'` | `_Measures.tmdl` |
| `'Total Gendered Referrals'` | `_Measures.tmdl` |
| `'Total Offers Made (Active Referrals Under Offer)'` | `_Measures.tmdl` |
| `'Total Offers Made Historically'` | `_Measures.tmdl` |
| `'Total Referrals That Recieved Offers'` | `_Measures.tmdl` |
| `'Total Referrals'` | `_Measures.tmdl` |
| `'Unsuccessful Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
