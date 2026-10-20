# Linked referral current status — 19 October 2026

Recovery copies for three WIP files:

- `Linked Provider Referrals.tmdl`: semantic model `definition/tables`.
- `visual.json`: Provider Explorer page `08ef33dc6a87d1b14392`, visual `586a1ac1befa7498ed75`.
- `mobile.json`: the same visual's phone formatting.

`before-files.json` records all 4,333 WIP file hashes, sizes and timestamps before
the change. The cached database is included in that preservation baseline.

The only intended WIP changes are the new measure, the new table projection and
its desktop/mobile column widths. Relationships, roles, source queries, existing
measure definitions, candidate statuses, visual filters and phone layout remain
unchanged. This does not deploy or update the running Desktop model.

Validation:

- Seven tests in `test_wmpp_linked_referral_status.py` and
  `test_wmpp_linked_offer_pairs.py` pass.
- Native TMDL deserialization passes (73 tables, 54 relationships, two roles).
- The exact saved new measure and existing visibility guard were evaluated as
  query-local measures against cached Import data, without saving or refreshing.
  One shared-referral test produced one visible linked-provider row with the
  correct referral current status and zero mismatches. Missing provider search
  and unmatched-referral cases returned blank.
- Native UI rendering is not verified; reopen the saved WIP project to load the
  new definition. Preserve any other unsaved Desktop edits separately first.
