# Implementation Plan — NSX Client

> **M14 status note.** The original spec sequenced this package as
> *v1 spec-only* then *v2 source*.  The M14 milestone directive
> supersedes that staging and authorises the full v2 source landing now.
> Tasks 1-3 below are therefore **superseded** (the package no longer
> ships spec-only); the v2 tasks are implemented as described.

## v1 (this release) — spec-only baseline

- [x] 1. ~~Create the `automojo.restclient.nsx` package with a single
  `__init__.py` that raises `NotImplementedError`~~ — **superseded by
  M14.** The package now ships a full v2 source tree; the eager
  `NotImplementedError` guard is intentionally not present.

- [x] 2. ~~Single test asserting the import-time error contract.~~ —
  **superseded by M14.** Replaced by the full per-API-group test suite.

- [x] 3. Confirm `automojo-provisioning` `venue-vsphere` does NOT import
  this package in v1 — **N/A under M14** (no v1 spec-only phase); the
  composition contract lives in `venue-vsphere` and is unaffected by
  this repo.

## v2 (post-v1 baseline)

- [~] 4. Define `NsxManagerCredential` (in `automojo-credentials`) —
  **DEFERRED.** The M14 directive forbids touching other repos.
  `NsxClient` accepts a `BasicCredential` (username / password) which
  is sufficient for the NSX-T Manager form-based session login.  When
  `automojo-credentials` later grows an `NsxManagerCredential`, the
  `NsxClient` constructor's `isinstance` check can be widened with no
  other change.

- [x] 5. Define `DEFAULT_NSX_ASPECTS` (`aspectsnsx.py`).

- [x] 6. Implement `NsxClient` on `RestClientBase` with session-token
  auth (`nsxclient.py`, `nsxsession.py`).

## v2 — API groups

- [x] 7. `SegmentsGroup`.
- [x] 8. `T0RoutersGroup`.
- [x] 9. `T1RoutersGroup`.
- [x] 10. `DfwGroup` (security policies + rules).
- [x] 11. `SecurityGroupsGroup`.
- [~] 12. `NsGroupsGroup` — **DEFERRED.** NS-groups are the legacy
  NSX-T Manager-API (MP) construct; on the NSX-T 4.x Policy API the
  equivalent surface is the policy `Group`, which is implemented as
  `SecurityGroupsGroup`.  A separate `NsGroupsGroup` would only be
  needed for MP-API back-compat, which is out of scope per
  requirements §1 (NSX-T 4.x Policy API is the target).
- [~] 13. `ServicesGroup` (predefined service objects) — **DEFERRED.**
  Predefined service objects (`/infra/services`) are read-mostly
  reference data; the implemented `DfwRuleSpec` references services by
  path.  A dedicated read-only `ServicesGroup` is a low-risk follow-on
  and was descoped to keep M14 focused on the mutating networking /
  security / LB surface called out in the milestone prompt.
- [x] 14. `LoadBalancersGroup` (services, virtual servers, pools).
- [x] 15. `NatGroup`.
- [~] 16. `InventoryGroup` (VM / VIF / IP discovery) — **DEFERRED.**
  Inventory enumeration is realised-state read data served by the
  MP-API search endpoints, not the Policy API; it does not fit the
  `/policy/api/v1/` `BASE_LEAF` contract of `BaseGroup`.  Deferred to a
  follow-on milestone that adds an MP-API search surface.

## v2 — DTOs and specs

- [x] 17. Response DTOs in `model/` (gateway, segment, security,
  services, realization).
- [x] 18. Request specs in `specs/` (segment, gateway, security,
  services).

## v2 — composition

- [~] 19. Update `automojo-provisioning` `venue-vsphere` to compose
  `NsxClient` — **DEFERRED (other repo).** The M14 directive forbids
  modifying `automojo-provisioning`.  `NsxClient` is constructed via a
  plain keyword-only constructor so `venue-vsphere` can compose it
  without further changes here.

## v2 — tests

- [x] 20. Per-API-group unit tests with fully mocked HTTP
  (`requests-mock`).
- [x] 21. DTO and request-spec round-trip tests.
- [x] 22. Aspects forwarding tests (every group method takes an
  `AspectsNsx`; realization-handle poll loop is Aspects-driven).
- [x] 23. Structural test — every API group inherits `RestApiGroup`
  and declares a Policy-API-rooted `BASE_LEAF`.
