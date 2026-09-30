# Power BI / DAX Guidance

## Reporting reassessment 30 September 2026

Use current WIP TMDL for exact expressions. Snapshot month, current referral creation cohort and closure flow are separate filter roles. Use category-aware distinct-referral measures and explicit offer/referral or provider/IPA transfer instead of adding bidirectional paths. Journey selectors clear only their own selection. Neither REMOVEFILTERS nor ALLSELECTED should be treated as a bypass of RLS.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


Assume a `DimDate` table is related to `FactReferral[ReferralCreatedDate]` and inactive date relationships are used for other lifecycle dates.

```DAX
Referral Count := DISTINCTCOUNT ( FactReferral[ReferralID] )

Referrals Previous Month :=
CALCULATE ( [Referral Count], DATEADD ( DimDate[Date], -1, MONTH ) )

Referral Month Change := [Referral Count] - [Referrals Previous Month]

Referral Month Change % := DIVIDE ( [Referral Month Change], [Referrals Previous Month] )

Median Days to IPA :=
MEDIANX (
    FILTER ( FactReferral, NOT ISBLANK ( FactReferral[DaysToIPA] ) ),
    FactReferral[DaysToIPA]
)

Placed by Target % :=
DIVIDE (
    CALCULATE (
        DISTINCTCOUNT ( FactReferral[ReferralID] ),
        FactReferral[PlacedByRequiredDate] = TRUE ()
    ),
    CALCULATE (
        DISTINCTCOUNT ( FactReferral[ReferralID] ),
        NOT ISBLANK ( FactReferral[IPAIssuedDate] ),
        NOT ISBLANK ( FactReferral[RequiredPlacementDate] )
    )
)
```

Use the notebook-created `Fact Referral` fields directly for target reporting:
`PlacedByRequiredDate` and `RequiredPlacementDateOutcome`. `Fact Placement`
does not contain `RequiredPlacementDate`. The complete v02 measure set is in
[Measures Comparison Checklist](Measures_Comparison_Checklist.md).

For open referrals as at a previous date, use status history or snapshots where possible. A simple created/closed interval calculation is only safe when referrals cannot reopen and closure dates are immutable.
