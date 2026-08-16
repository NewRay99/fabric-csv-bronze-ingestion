# WMPP report v01 — extracted PBIP projects

This folder contains the two independent projects from `report v01.zip`:

- `semantic_model __/SM_WMPP.pbip` — the semantic-model project. Its `SM_WMPP.Report` folder is the local authoring shell that binds to `../SM_WMPP.SemanticModel`.
- `Report/WMPP PILOT DASHBOARD V13.pbip` — the report project published against the Fabric `SM_WMPP` semantic model through `definition.pbir`.

Use the helper report under `semantic_model __/SM_WMPP.Report` to preview local TMDL changes. The report under `Report/` remains connected to the published workspace model until its dataset reference is intentionally changed.

The local semantic-model TMDL includes the `Closed_Date` derivation documented in `../brand pack/WMPP_Semantic_Model_Measures.md`.

The original ZIP and legacy V13.1 extraction remain in the parent folder for comparison and rollback.
