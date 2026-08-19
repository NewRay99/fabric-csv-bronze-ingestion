# Power BI / DAX Guidance

Assume a `DimDate` table is related to `FactReferral[ReferralCreatedDate]` and inactive date relationships are used for other lifecycle dates.

```DAX
Referral Count := DISTINCTCOUNT ( FactReferral[ReferralID] )

Referrals Previous Month :=
CALCULATE ( [Referral Count], DATEADD ( DimDate[Date], -1, MONTH ) )

Referral Month Change := [Referral Count] - [Referrals Previous Month]

Referral Month Change % := DIVIDE ( [Referral Month Change], [Referrals Previous Month] )

Median Days to IPA :=
MEDIANX (
    FILTER ( FactReferral, NOT ISBLANK ( FactReferral[IPAIssuedDate] ) ),
    DATEDIFF ( FactReferral[ReferralCreatedDate], FactReferral[IPAIssuedDate], DAY )
)

Placed by Target % :=
DIVIDE (
    CALCULATE (
        DISTINCTCOUNT ( FactPlacement[PlacementID] ),
        FactPlacement[IPAIssuedDate] <= FactPlacement[RequiredPlacementDate]
    ),
    DISTINCTCOUNT ( FactPlacement[PlacementID] )
)
```

For open referrals as at a previous date, use status history or snapshots where possible. A simple created/closed interval calculation is only safe when referrals cannot reopen and closure dates are immutable.
