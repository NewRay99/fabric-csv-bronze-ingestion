> **Implemented Gold v02 status:** the active `04_gold_model` notebook now
> publishes `gold.fact_referral`, `gold.fact_referral_snapshot`,
> `gold.fact_offer`, `gold.fact_placement`, and
> `gold.fact_referral_provider`, plus referral-board, monthly and provider
> performance KPI views. Refer to
> [Measures Comparison Checklist](Measures_Comparison_Checklist.md)
> for the supported fields, source limitations and new DAX measures. Items in
> this backlog remain proposed where they depend on fields not delivered by the
> source, including reopened dates, actual placement dates, region and
> complexity.

## The key distinction: referrals are demand; placements are outcomes

Your referrals table does **not** need to contain one row per day or month to support time-series reporting.

A referral with a `ReferralCreatedDate` is an event. Connect it to a calendar table and count referrals by day, week or month:

- Referrals created in July
- Referrals created in June
- Referrals created this month versus last month
- Twelve-month referral trend

However, `ReferralCreatedDate` alone cannot tell you how many referrals were open at the end of each historical month. For that, you need either status history or a periodic snapshot.

## Do not create an artificial referral end date

A pseudo end date based on estimated duration would mix two different processes:

1. **Referral lifecycle:** finding and agreeing a suitable home.
2. **Placement lifecycle:** the child occupying that home.

A referral should receive an actual `ReferralClosedDate` whenever the referral reaches a terminal outcome, such as:

- Placement agreed
- Referral withdrawn
- Referral cancelled
- No suitable placement found
- Child’s circumstances changed
- Referral duplicated
- Transferred to another service

The closure date should therefore exist even when no placement is agreed. Store a `ReferralClosureReason` alongside it.

The placement’s estimated start, estimated end, actual start, actual end, duration and cost belong in the **IPA/Placement table**, not as the referral end date.

---

# Recommended referral dates

## Essential board-reporting dates

| Date | Meaning | Main board use |
|---|---|---|
| `ReferralCreatedDate` | Referral entered the system | Demand and referral volumes |
| `RequiredPlacementDate` | Date by which a placement is needed | Urgency and overdue referrals |
| `FirstActionDate` | First meaningful action by the placement team | Responsiveness and SLA |
| `FirstOfferDate` | First provider offer received | Supply response time |
| `OfferAcceptedDate` | Officer accepted the preferred home | Successful matching |
| `IPAIssuedDate` | Placement formally assigned | Confirmed placements |
| `ReferralClosedDate` | Referral process completed | Throughput and days open |
| `LastActivityDate` | Most recent action, offer or review | Stalled referral monitoring |
| `ReopenedDate` | Referral reopened after closure | Rework and instability |

`RequiredPlacementDate` should normally be captured when the referral is created rather than derived.

## Useful offer-level dates

Because one referral may receive multiple offers, these belong in an Offer table:

- `OfferSubmittedDate`
- `OfferReviewedDate`
- `OfferWithdrawnDate`
- `OfferAcceptedDate`
- `OfferRejectedDate`
- `ProposedPlacementStartDate`
- `OfferExpiryDate`

Each provider home offered should ideally be a separate row.

## Placement/IPA dates

These should be kept separate from referral dates:

- `IPAIssuedDate`
- `PlannedPlacementStartDate`
- `ActualPlacementStartDate`
- `PlannedPlacementEndDate`
- `ActualPlacementEndDate`
- `PlacementEndedDate`
- `PlacementBreakdownDate`, where relevant

---

# Recommended derived durations

These are measures or calculated fields, not additional artificial dates.

| Measure | Calculation |
|---|---|
| Referral age | As-of date minus referral created date |
| Days to first action | First action date minus created date |
| Days to first offer | First offer date minus created date |
| Days to accepted offer | Accepted offer date minus created date |
| Days to IPA | IPA issued date minus created date |
| Days open | Closed date minus created date, or as-of date minus created date |
| Days without activity | As-of date minus last activity date |
| Days past required date | As-of date minus required placement date |
| Offer review time | Offer reviewed date minus offer submitted date |
| IPA processing time | IPA date minus accepted offer date |

For board reporting, show both the **median** and the percentage meeting an agreed SLA. Median is often more useful than average because a small number of very old referrals can distort the average.

---

# Suggested data model

## 1. Referral fact table

One row per referral:

```text
FactReferral
------------
ReferralID
ChildID
ReferralCreatedDate
RequiredPlacementDate
FirstActionDate
FirstOfferDate
OfferAcceptedDate
IPAIssuedDate
ReferralClosedDate
ClosureReason
CurrentStatus
LastActivityDate
PlacementTypeRequired
Region
Priority
ComplexityBand
```

## 2. Offer fact table

One row for each home offered:

```text
FactOffer
---------
OfferID
ReferralID
ProviderID
HomeID
OfferSubmittedDate
OfferReviewedDate
OfferDecisionDate
OfferStatus
ProposedStartDate
EstimatedDuration
EstimatedCost
RejectionReason
```

This lets you answer:

- How many offers did each referral receive?
- How many providers responded?
- How many different homes were considered?
- Which providers have the highest acceptance rate?
- How long does it take officers to review offers?

## 3. IPA/placement fact table

One row per formally agreed placement:

```text
FactPlacement
-------------
PlacementID
ReferralID
AcceptedOfferID
IPAIssuedDate
PlannedStartDate
ActualStartDate
PlannedEndDate
ActualEndDate
EstimatedCost
ActualCost
PlacementStatus
EndReason
```

## 4. Referral status history

One row every time the status changes:

```text
FactReferralStatusHistory
-------------------------
ReferralID
Status
StatusStartDateTime
StatusEndDateTime
ChangedBy
Reason
```

This is important because a `CurrentStatus` column only tells you what is open now. It does not tell you what was open three months ago.

## 5. Referral snapshot

For board reporting, create a daily or month-end snapshot:

```text
FactReferralSnapshot
--------------------
SnapshotDate
ReferralID
Status
DaysOpen
AgeBand
OfferCount
ProviderCount
HasOffer
RequiredPlacementDate
IsOverdue
LastActivityDate
```

A month-end snapshot is sufficient for many board reports. A daily snapshot gives better operational reporting.

---

# How to report referrals this month and last month

A referral table does not have to be a snapshot table for this measure. Each referral has a created-date event.

Create a calendar table and connect:

```text
Date[Date]  1 ---- *  Referral[ReferralCreatedDate]
```

Then create:

```DAX
Referral Count :=
DISTINCTCOUNT ( Referral[ReferralID] )
```

When the report is filtered to July 2026, this measure returns referrals created in July.

```DAX
Referrals Previous Month :=
CALCULATE (
    [Referral Count],
    DATEADD ( 'Date'[Date], -1, MONTH )
)
```

```DAX
Referral Month Change :=
[Referral Count] - [Referrals Previous Month]
```

```DAX
Referral Month Change % :=
DIVIDE (
    [Referral Month Change],
    [Referrals Previous Month]
)
```

You can present this as:

```text
Referrals created this month:       128
Referrals created last month:       114
Change:                              +14
Percentage change:                  +12.3%
```

For a partially completed month, compare:

- Month-to-date against the same number of days last month, or
- The latest completed month against the preceding completed month

Do not compare ten days of the current month against a full previous month without clearly labelling it.

---

# Measuring open referrals over time

There are two different questions.

## Open referrals now

This can be calculated using current status:

```DAX
Open Referrals Now :=
CALCULATE (
    [Referral Count],
    Referral[CurrentStatus] = "Open"
)
```

## Open referrals as at a previous month-end

This requires `CreatedDate` and a reliable `ClosedDate`, or preferably status history/snapshots.

Where a referral has one simple lifecycle and cannot reopen:

```DAX
Open Referrals As At :=
VAR AsAtDate =
    MAX ( 'Date'[Date] )
RETURN
    CALCULATE (
        DISTINCTCOUNT ( Referral[ReferralID] ),
        REMOVEFILTERS ( 'Date' ),
        FILTER (
            ALL (
                Referral[ReferralCreatedDate],
                Referral[ReferralClosedDate]
            ),
            Referral[ReferralCreatedDate] <= AsAtDate
                && (
                    ISBLANK ( Referral[ReferralClosedDate] )
                    || Referral[ReferralClosedDate] > AsAtDate
                )
        )
    )
```

This gives the number of referrals that had been created but not yet closed on the selected date.

However, this becomes unreliable when referrals can:

- Reopen
- Move backwards through statuses
- Be temporarily suspended
- Have closure dates overwritten

For those situations, use the status-history or snapshot table.

---

# Example showing why multiple dates are necessary

Assume these three referrals:

| Referral | Created | Accepted | IPA issued | Closed | Position at 31 July |
|---|---:|---:|---:|---:|---|
| R1001 | 3 July | 8 July | 9 July | 9 July | Closed successfully |
| R1002 | 28 July | Blank | Blank | Blank | Open |
| R1003 | 20 June | 5 July | 6 July | 6 July | Closed successfully |

For July reporting:

- **Referrals created in July:** R1001 and R1002 = 2
- **Offers accepted in July:** R1001 and R1003 = 2
- **IPAs issued in July:** R1001 and R1003 = 2
- **Open referrals at 31 July:** R1002 = 1

R1003 contributes to June referral demand but July placement outcomes. This is why one date cannot answer every question.

---

# Board measures to present

## 1. Referral demand

These show how much new work is entering the service:

- Referrals created this month
- Referrals created last month
- Month-on-month change
- Rolling 12-month referral trend
- Referrals by placement type
- Referrals by region, age group or complexity
- Urgent referrals received

Recommended visual:

- KPI cards for current and previous month
- Twelve-month line chart
- Stacked column by placement type

## 2. Current pipeline

These show the amount of work still unresolved:

- Open referrals today
- Open referrals at previous month-end
- Referrals with no provider offers
- Referrals beyond required placement date
- Referrals with no activity for more than three or seven days
- Open referrals by age band

Example age bands:

```text
0–2 days
3–7 days
8–14 days
15–28 days
29+ days
```

Recommended visual:

- Month-end open-referral trend
- Stacked bar by age band
- Exception table for overdue cases

## 3. Provider response and supply

These show whether sufficient suitable homes are being offered:

- Number of offers received
- Average or median offers per referral
- Percentage of referrals receiving at least one offer
- Percentage receiving an offer within two working days
- Number of unique providers responding
- Number of unique homes offered
- Referrals with only one available option
- Provider offer acceptance rate

A referral receiving five offers from one provider should not necessarily be presented as equivalent to receiving offers from five independent providers. Show both:

- Number of offers
- Number of unique providers
- Number of unique homes

## 4. Matching outcomes

These show completed placement-finding activity:

- Offers accepted this month
- IPAs issued this month
- Referrals successfully matched
- Referrals withdrawn or cancelled
- Referrals closed without a placement
- Median days from referral to accepted offer
- Median days from referral to IPA
- Percentage matched within 7, 14 and 28 days

Recommended visual:

- Monthly created versus matched chart
- Outcome distribution
- Median time-to-match trend

## 5. Placement economics

These should come from the accepted offer or placement record:

- Estimated placement cost
- Actual placement cost
- Average and median weekly cost
- Cost by placement type
- Estimated versus actual cost variance
- High-cost placements
- Total committed placement value
- Planned placement duration

Avoid adding costs from every offer. Only an accepted offer should normally contribute to committed placement expenditure.

---

# Be careful with “conversion rate”

This measure can be misleading:

```text
IPAs issued this month ÷ referrals created this month
```

The IPAs issued this month may relate to referrals created in previous months.

Use two separate measures:

### Monthly throughput

```text
IPAs issued during the month
```

This measures completed work during the period.

### Referral cohort success

```text
Percentage of referrals created in a particular month
that received an IPA within 7, 14 or 28 days
```

For example:

| Referral-created cohort | Matched within 7 days | Within 14 days | Within 28 days |
|---|---:|---:|---:|
| April 2026 | 42% | 69% | 88% |
| May 2026 | 45% | 72% | 90% |
| June 2026 | 38% | 65% | 84% |

This is one of the strongest board-level views because it shows whether newer referrals are being resolved more quickly.

---

# Recommended board dashboard

## Top row: headline KPIs

- New referrals this month
- New referrals previous month
- Open referrals now
- Open referrals aged over 14 days
- IPAs issued this month
- Median days to IPA

## Middle row: demand and pipeline

- Twelve-month referral-created trend
- Month-end open-referral trend
- Open referrals by age band
- Referrals by placement requirement

## Bottom row: performance and outcome

- Percentage receiving first offer within SLA
- Percentage matched within 7, 14 and 28 days
- Referral closure outcomes
- Estimated placement costs
- Referrals with no offers or no recent activity

---

# Minimum changes I would make now

At a minimum, introduce:

```text
ReferralCreatedDate
RequiredPlacementDate
FirstActionDate
FirstOfferDate
OfferAcceptedDate
IPAIssuedDate
ReferralClosedDate
ReferralClosureReason
LastActivityDate
```

Then create:

1. A proper date dimension.
2. An Offer fact table with one row per offered home.
3. A Referral Status History table.
4. A daily or month-end open-referral snapshot.
5. Separate measures for referrals created, offers accepted, IPAs issued, referrals closed and referrals open as at a date.

The main principle is:

> **Created date measures demand, accepted/IPA dates measure successful throughput, closed date measures completion, and snapshots measure the open workload at a point in time.**

The referral-created date is therefore valuable and correct for board reporting. It simply should not be used as the only date for every referral and placement measure.



## IDEAS for Imporovement
Would a Sankey diagram be worth using. If so what could we use it for


# Answer


Yes — a **Sankey diagram could be very valuable**, but I would use it for one specific purpose: showing **how referrals flow through the placement process and where they are being lost or delayed**.

I would **not** make it one of the main headline visuals. Your KPI cards, target hit rates, ageing and required-placement-date measures are better for the board's primary view. A Sankey would work brilliantly as a supporting **“Referral Journey / Placement Pipeline”** visual.

### Best Sankey for your model

I would build something like:

**Referrals Created → Urgency → Provider Response → Offer Outcome → IPA / Closure Outcome**

For example:

```text
128 Referrals
     │
     ├── Critical 14
     │      ├── Offers received 11
     │      │      ├── Accepted 8
     │      │      │      ├── IPA by target 5
     │      │      │      └── IPA late 3
     │      │      └── Not accepted 3
     │      └── No offer 3
     │
     ├── High 31
     ├── Medium 49
     └── Planned 34
```

Visually, the width of the flow tells the board immediately where referrals are going.

The most important final split should probably be:

**Placed by Required Placement Date**
**Placed after Required Placement Date**
**Still Open**
**Withdrawn / Cancelled**
**Closed — no match**

That connects the Sankey directly to the target logic we designed.

---

## Sankey 1 — Referral Journey

This would probably be my first choice.

### Stage 1
**PlacementUrgencyBand**

- Critical
- High
- Medium
- Planned

### Stage 2
**Provider response**

- No offers
- 1 offer
- 2–3 offers
- 4+ offers

### Stage 3
**Matching decision**

- Offer accepted
- Offers rejected
- Provider withdrew
- Referral withdrawn
- Still searching

### Stage 4
**Final position**

- IPA issued by target
- IPA issued late
- Open — on track
- Open — overdue
- Closed without placement

This could reveal something such as:

> Critical referrals are disproportionately flowing into **No Offer → Overdue**, while planned referrals mostly flow through **Multiple Offers → Accepted → IPA by Target**.

That is a much more useful story than simply reporting "18 referrals are overdue."

---

# Sankey 2 — Provider → Home → Placement

There is another very useful operational Sankey based on your provider structure.

You said one provider can have multiple homes and can put forward several homes.

So:

```text
Provider
   ↓
Home offered
   ↓
Referral
   ↓
Accepted / Rejected
   ↓
IPA
```

For example:

```text
BrightCare
   ├── Oak House ─────────► 12 referrals ──► 5 accepted ──► 4 IPA
   ├── Rose Lodge ────────► 8 referrals  ──► 3 accepted ──► 3 IPA
   └── Meadow View ───────► 18 referrals ──► 10 accepted ─► 9 IPA

Northstar
   ├── ...
```

This becomes particularly powerful for commissioners and placement managers because they can see:

- which providers are engaging;
- which homes are frequently put forward;
- which homes officers actually select;
- where providers generate lots of offers but few successful matches;
- which providers tend to support Critical/High referrals.

I would keep this off the main board page and use it on a **Provider Performance** page.

---

# Sankey 3 — Where overdue referrals come from

This could be an excellent executive visual.

Start specifically with referrals that missed their `RequiredPlacementDate`:

```text
Overdue referrals
        ↓
Urgency
        ↓
Reason for delay
        ↓
Current position
```

Example:

```text
25 Overdue
    │
    ├── Critical 5
    ├── High 9
    ├── Medium 8
    └── Planned 3
             ↓
       No provider response
       Unsuitable offers
       Officer review delay
       Funding approval
       Child needs changed
             ↓
       Still searching
       Offer under review
       Accepted awaiting IPA
```

This would be extremely useful if you introduce a proper:

**`DelayReason` / `PlacementBarrierReason`**

field.

Potential controlled values:

- No provider response
- No suitable home available
- Location constraint
- Education constraint
- Sibling placement requirement
- Complex needs
- Cost/funding approval
- Offer awaiting review
- Provider withdrew
- Child circumstances changed
- Awaiting IPA administration

Then the board isn't merely told:

> 18 referrals are overdue.

They see:

> **18 referrals are overdue; 9 are caused primarily by lack of suitable provider supply, 5 by complex matching requirements and 4 by internal processing.**

That creates an actionable management conversation.

---

## One important data modelling issue

There is a trap in your data.

A referral may have:

> **1 Referral → many Offers → many Homes**

So if you create one large Sankey directly from referral → offer → IPA, you can accidentally inflate referral numbers.

For example:

```text
Referral R001
 ├── Offer A
 ├── Offer B
 ├── Offer C
 └── Offer D
```

That's **one referral**, not four referrals.

Therefore I'd have two slightly different Sankey datasets.

**Referral Sankey:** use `DISTINCTCOUNT(ReferralID)` at referral lifecycle stages.

**Offer Sankey:** use `OfferID` when examining provider/home behaviour.

Don't mix those counts without making the measure very clear.

---

# A Sankey I'd put into your presentation

I'd add a fourth dashboard/page called:

## **REFERRAL JOURNEY & BOTTLENECKS**

Top KPIs:

**128**
Referrals Created

**109**
Received ≥1 Offer

**97**
Preferred Match Selected

**91**
IPA Issued

**76%**
Placed by Required Date

**18**
Currently Overdue

Then a large Sankey occupying about 60–70% of the page:

```text
URGENCY              RESPONSE             DECISION              OUTCOME

Critical ───────┐
High ───────────┼──► No Offer ──────────► Still Searching ───► Overdue
Medium ─────────┼──► One Offer ─────────► Rejected ──────────► Open
Planned ────────┘    Multiple Offers ───► Accepted ──────────► IPA
                                                                  │
                                                   ┌──────────────┴─────────────┐
                                                   ▼                            ▼
                                             Within Target                Target Missed
```

Alongside it I'd put three callouts:

> **24% of Critical referrals missed their Required Placement Date**

> **72% of referrals receiving 2+ suitable home offers were placed within target**

> **No suitable offer is the largest contributor to overdue referrals**

Those are fictitious figures for design purposes, of course, but this is the type of insight the visual should surface.

## My recommendation

For the board pack I'd use **one Sankey only**:

**`Urgency → Offer availability → Match decision → Required Placement Date outcome`**

That would complement the dashboards we've already designed extremely well because the dashboards tell the board **what happened**, while the Sankey helps explain **how referrals got there**.

The more detailed **Provider → Home → Referral → Accepted → IPA** Sankey can then sit on the operational/provider analysis page.
