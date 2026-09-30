# WMPP shared icon pack

Consolidated 30 September 2026. This is the shared source location for report SVG
icons. Existing pack files were preserved without changing their artwork.

- Root: established KPI, navigation and general-purpose icons.
- `lucide-originals/`: upstream source SVGs; retain their licence/provenance.
- `report-variants/`: ink/light annotation variants.
- `category-icons/`: priority, status, placement and Yes/No icons.
- `journey/`: referral/provider journey and connected-rail icons.
- `navigation-bubbles/`: navigation button states and backgrounds.
- `report-resources/`: other icons collected from the deployed reports.
- `variants/`: differing artwork with the same filename, preserved by content hash;
  these are not a new approved palette or permission to replace deployed artwork.

`ICON_MIGRATION_20260930.json` maps every source to its pack file, records hashes,
and identifies the rollback backup. Identical same-name files share a destination.
Required Power BI `StaticResources` copies remain inside their report packages;
removing them would break visuals. The consolidation does not change report
definitions, bookmarks, the model, icon colours or licences.

Mockups, full-page reference graphics, retired reports and review backups are not
icon sources to relocate and remain untouched. See `LUCIDE_LICENSE.txt` and the
existing source catalogues for licensing/provenance.
