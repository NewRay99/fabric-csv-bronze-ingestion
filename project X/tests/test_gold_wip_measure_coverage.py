"""Keep formula predicates and VAR bindings out of the guide measure inventory."""

from validate_gold_wip_measure_coverage import guide_measure_names


def test_measure_inventory_excludes_templates_variables_and_predicates():
    text = '''```DAX
Open Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Referrals Created This Financial Year =
VAR financial_year_start = DATE ( 2026, 4, 1 )
RETURN CALCULATE ( [Total Referrals], 'dim_date'[date] >= financial_year_start )

<Base> Previous Month = CALCULATE ( [<Base>], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```'''
    assert guide_measure_names(text) == {
        "Open Referrals", "Referrals Created This Financial Year"
    }
