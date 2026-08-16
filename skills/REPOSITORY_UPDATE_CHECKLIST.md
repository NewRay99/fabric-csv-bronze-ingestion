# Repository Integration Checklist

When the pack is copied into the active repository:

1. Add `SOUL.md` and `PROJECT_STATE.md` to the `project X` root.
2. Add `FFD.md` beside `HLD.md` and `TFD.md` in
   `client documentation/03_Architecture_and_Design`.
3. Add links to `SOUL.md`, `PROJECT_STATE.md`, and `FFD.md` in the project
   `README.md`.
4. Add `FFD.md` to the client-documentation index.
5. Record the new specialist project charter and FFD baseline in
   `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md`.
6. Record any semantic-model-specific documentation governance change in
   `change tracking/SEMANTIC_MODEL_CHANGELOG.md` only if model behaviour or its
   controlled documentation actually changes.
7. Run link checks and the existing portable validators.
8. Commit only after review; do not overwrite unrelated working-tree changes.
