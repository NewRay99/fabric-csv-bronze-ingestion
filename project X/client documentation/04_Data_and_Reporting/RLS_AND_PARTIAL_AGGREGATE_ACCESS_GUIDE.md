# RLS and partial aggregate access guide

## Purpose

This guide captures the partial-RLS design discussed in the ChatGPT Work
conversation **“Power BI Partial RLS Setup”** and reconciles it with WMPP
requirement R55.

The required behaviour is:

- authorised users can see approved organisation-wide summary KPIs;
- row-level referral and related detail is limited to the user's authorised
  authority and/or UserGroup scope; and
- unrestricted summaries cannot be sliced finely enough to disclose a child,
  referral, provider interaction or another team's small population.

Power BI DAX cannot remove an RLS filter. Microsoft recommends a separate
summary model table for partial-RLS scenarios. See [RLS guidance: Design
partial RLS](https://learn.microsoft.com/en-us/power-bi/guidance/rls-guidance#design-partial-rls).

## Client-site status — 20 September 2026

The reviewed `SM_WMPP_v16` semantic model has:

- no `roles/` definition and therefore no model RLS role;
- no UPN, UserGroup, authority or security-scope mapping table;
- no UserGroup/security key on `fact_referral`;
- a `region` field that the reviewed Gold notebook populates as `NULL`;
- no intentionally safe organisation-wide aggregate fact separated from the
  detail security path; and
- four bidirectional business relationships, including an active current-
  referral-to-snapshot relationship, which should be removed before RLS.

RLS is therefore **not implemented** in the current client-site package. R55
and partial RLS are blocked until the data owner supplies authoritative scope
keys and the identity team supplies user-to-scope mappings. Do not implement a
role against the current null `region` placeholder.

## Repository implementation candidate — 20 September 2026

The client ZIP remains the immutable baseline, but the repository candidate at
`reports/current/SM WMPP v16 updated` now implements a deny-by-default model:

- setup creates empty governed configuration tables
  `monitoring.cfg_security_scope`, `monitoring.cfg_user_scope_access` and
  `monitoring.cfg_referral_scope`;
- Gold publishes `dim_security_scope`, `sec_user_scope_access` and
  `bridge_referral_scope`, applying active/effective-date rules;
- the TMDL role `WMPP Dynamic Detail RLS` filters current referrals, snapshots
  and scoped provider KPI aggregates with `USERPRINCIPALNAME()`;
- ordinary fact relationships are single-direction and the direct
  current-to-snapshot fact relationship is removed; and
- `fact_referral_global_summary` is physically identifier-free and is not
  included in the detail role.

Empty mappings return no secured detail. Before deployment, the client must
load approved mappings and complete the identity/test matrix below. The global
summary currently has no small-cell suppression because neither a threshold
nor disclosure policy has been approved; do not grant Build/export access to
it until that decision is made.

## Security decisions required

Information Governance and the data owner must approve:

1. the protected detail scope: local authority, region, placement UserGroup,
   or a combination;
2. cross-boundary rules, including which authorities can see a shared case;
3. which operational roles can see organisation-wide summary data;
4. the approved aggregate visibility grain;
5. the small-number threshold and suppression method;
6. whether provider-level aggregates are organisation-wide or scoped;
7. access to message/free-text and officer feedback fields;
8. break-glass membership, duration, approval and audit; and
9. whether external/B2B identities are in scope and which identifier is
   authoritative.

## Target model

Use two deliberately separated paths.

```text
SECURED DETAIL

sec_user_scope_access --allowed scopes-- bridge_referral_scope
                                          | explicit role predicate
                                          v
                                   fact_referral / snapshot
                                      /    |    \
                             fact_offer fact_ipa provider detail


APPROVED GLOBAL SUMMARY

dim_snapshot_month --------------------> fact_referral_global_summary
dim_status ---------------------------->          |
dim_placement_type -------------------->          +-- no referral/person/provider IDs

There is no relationship from sec_user_scope_access or dim_security_scope to
fact_referral_global_summary.
```

`bridge_referral_scope` supports a referral that is legitimately visible to
more than one authority or UserGroup. If the business confirms exactly one
scope per referral, a validated `security_scope_key` can instead sit directly
on `fact_referral` and its related facts.

The global summary must be a physical Gold object at the approved grain. Do
not copy the detail fact and merely hide identifiers. Hidden columns are not a
security boundary.

## Minimum Gold objects

| Object | Required columns/purpose |
| --- | --- |
| `dim_security_scope` | `security_scope_key`, scope type, authority/UserGroup code, display name, valid dates, active flag |
| `sec_user_scope_access` | normalised `user_principal_name`, `security_scope_key`, valid dates, approval/audit fields; active dates are applied before publication |
| `bridge_referral_scope` | `referral_id`, `security_scope_key`, access reason and validity where cross-boundary access is possible |
| `fact_referral_global_summary` | approved month/status/placement-type dimensions and additive counts only |
| `dim_disclosure_rule` | approved threshold, effective dates and owner if suppression is configurable |

Normalise UPNs to lower case and trim whitespace in Gold. Unknown, missing or
expired mappings must deny detail by default. Give an all-area operational user
explicit rows for the approved scopes rather than a wildcard that is difficult
to audit.

## Approved aggregate visibility grain

“Aggregate visibility grain” means the finest organisation-wide breakdown a
user may see even when they cannot see the underlying referrals.

An initial proposal for approval is:

| Organisation-wide summary may include | Keep on the secured detail path unless separately approved |
| --- | --- |
| Snapshot month | Referral/person/placement identifiers |
| Broad referral status | Provider or home |
| Broad placement type | Placement officer or social worker |
| A high-level authority total, only if cross-authority totals are approved | UserGroup or case team |
| Pre-approved KPI counts/rates | Exact age, exact postcode and free text |

This is a proposal, not an approval. Combining month, provider, exact age,
gender, location and placement type can reduce an “aggregate” to one case.
Subtraction can also disclose another team's population; for example, global
count 101 minus the user's count 100 reveals one out-of-scope referral.

Build only the approved columns into `fact_referral_global_summary`. Apply the
approved suppression rule in Gold so that users with Build permission cannot
recover unsuppressed small cells by writing a different DAX query. A display
measure such as `IF([Count] < threshold, BLANK(), [Count])` can improve the
report experience, but it is not a substitute for a safe aggregate object and
controlled semantic-model permissions.

## Dynamic RLS role

The repository candidate creates one dynamic role, `WMPP Dynamic Detail RLS`.
The published access table is already active/effective-date filtered; its
identity permission is:

```DAX
LOWER ( 'sec_user_scope_access'[user_principal_name] ) =
LOWER ( USERPRINCIPALNAME () )
```

Prefer a Gold view that already applies valid-from/valid-to dates, so the role
expression remains simple and testable.

The implemented role evaluates `bridge_referral_scope` explicitly in the
permissions for `fact_referral` and `fact_referral_snapshot`, avoiding a
general bidirectional relationship. The current-referral permission propagates
to related offer, IPA, lifecycle and provider-assignment facts over active
single-direction relationships. If a later design replaces this with **Apply
security filter in both directions**, limit it to one approved relationship
and performance-test it. See [Row-level security with Power
BI](https://learn.microsoft.com/fabric/security/service-admin-row-level-security#bi-directional-cross-filtering-with-rls).

RLS propagates only through active relationships. `USERELATIONSHIP` does not
make an inactive path carry RLS. See [Active versus inactive relationship
guidance](https://learn.microsoft.com/en-us/power-bi/guidance/relationships-active-inactive#inactive-relationships).

## Partial-RLS measures

The measures are intentionally simple because the security boundary is in the
model, not in `REMOVEFILTERS`.

```DAX
Organisation Referrals =
SUM ( 'fact_referral_global_summary'[referral_count] )

My Authorised Referrals =
DISTINCTCOUNT ( 'fact_referral'[referral_id] )

My Share of Organisation Referrals =
DIVIDE ( [My Authorised Referrals], [Organisation Referrals] )
```

Do not use `ALL`, `REMOVEFILTERS` or a disconnected measure to try to bypass
RLS on the detail fact. DAX cannot override the security filter.

## Related-detail propagation

The same security scope must protect:

- current and snapshot referral detail;
- offers and IPAs;
- provider assignments and reason records;
- referral lifecycle events;
- provider/officer messages; and
- drill-through and export data.

Prefer active, single-direction referral/dimension-to-detail paths. Remove the
client model's general bidirectional fact relationships first. If message text
must be hidden from users who may still see the row, RLS is insufficient
because it filters rows, not columns; separate the text into a more restricted
semantic model/table or implement an approved object-level security design.

## Power BI Service configuration

1. Create and validate the dynamic role in the semantic model.
2. Publish to the controlled workspace.
3. Assign an Entra security group, not individuals where avoidable, to the RLS
   role.
4. Give report consumers the workspace **Viewer** role or distribute through
   an app. Microsoft states that RLS applies to Viewers; workspace Admin,
   Member and Contributor roles have edit permission and RLS does not apply to
   them. See [RLS with workspaces](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security#use-rls-with-workspaces-in-power-bi).
5. Restrict Build, Analyze in Excel, export and downstream semantic-model
   permissions according to the approved aggregate design.
6. Record role membership, mapping refresh, mapping owner and emergency access
   in the operational audit process.

`USERPRINCIPALNAME()` returns the service-resolved UPN. For B2B users the value
may differ from the user's mail address, so test with the actual guest identity
and store the observed UPN in the mapping. Microsoft's service guidance also
notes that “Test as role” does not fully reproduce an external user's identity.

## Test matrix

Test with real Viewer identities in addition to Desktop “View as”.

| Test identity/scenario | Expected detail | Expected global summary |
| --- | --- | --- |
| One UserGroup | Only referrals mapped to that group | Approved organisation summary |
| Multiple groups | Union of approved groups, with no duplicate counts | Approved organisation summary |
| One authority | Only referrals visible to that authority, including approved cross-boundary cases | Approved organisation summary |
| No mapping | No detail rows | Either approved global summary or no report access, per policy |
| Expired mapping | No detail rows after expiry | Per policy |
| Break-glass | Time-limited approved detail, fully audited | Approved organisation summary |
| Workspace Member/Contributor | RLS is not an effective control | Must not be used as an RLS acceptance identity |

For each identity, test:

- permitted and prohibited referral IDs;
- counts by every slicer available on the report;
- drill-through, tooltip pages, exports and Analyze in Excel;
- current and snapshot facts;
- provider messages/free text;
- global-minus-local subtraction scenarios; and
- suppressed small cells and combinations of filters.

Acceptance requires zero prohibited referral visibility and signed approval of
the aggregate grain and suppression rule across all 14 authority scenarios and
the required UserGroup scenarios.

## Operational controls

- Refresh the security mapping before the semantic model or make the mapping
  part of the same atomic release.
- Alert on duplicate UPN/scope rows, unknown scopes, expired-only users and
  detail facts without a valid security scope.
- Review access at an agreed cadence and on staff/team changes.
- Use the controlled break-glass process in the HOLD register; do not hard-code
  an unrestricted username in DAX.
- Re-run the complete RLS test pack after relationship, role, scope or aggregate
  grain changes.
