"""Keep published Gold v02 DAX measures independent of Bronze and Silver."""

import re
import sys
from pathlib import Path


ROOT = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2
    else Path(__file__).resolve().parents[1]
)
GUIDE = (
    ROOT
    / "client documentation"
    / "04_Data_and_Reporting"
    / "GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md"
)

guide = GUIDE.read_text(encoding="utf-8")
dax_blocks = re.findall(r"```DAX\s*\n(.*?)```", guide, flags=re.DOTALL | re.IGNORECASE)
assert dax_blocks, "the Gold semantic-model guide has no DAX code blocks"

allowed_gold_tables = {
    "bridge_provider_framework",
    "dim_date",
    "dim_provider",
    "dim_provider_home",
    "dim_provider_submission_document",
    "fact_offer",
    "fact_referral",
    "fact_referral_lifecycle_event",
    "fact_referral_provider",
    "fact_referral_snapshot",
    "fct_ipa",
}
for block_number, dax in enumerate(dax_blocks, start=1):
    normalised = dax.lower()
    for prohibited_source in ("bronze.", "silver.", "gold."):
        assert prohibited_source not in normalised, (
            f"DAX block {block_number} uses a physical-layer qualifier: {prohibited_source}"
        )
    for table_name in re.findall(r"'([^']+)'\s*\[", dax):
        assert table_name in allowed_gold_tables, (
            f"DAX block {block_number} references non-Gold or retired table "
            f"'{table_name}'"
        )

print(f"PASS {len(dax_blocks)} published DAX blocks use active Gold model tables only")
print("VALIDATION PASSED")
