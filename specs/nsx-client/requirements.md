# Requirements

## Introduction

The `nsx-client` feature delivers `NsxClient`, a `RestClientBase` subclass that
talks to NSX-T Manager. **This is a v2 (post-v1 baseline) feature.** This spec
exists in v1 only as the scope-baseline so that the v1 work in
`automojo-interop-vsphere` and `automojo-provisioning` `venue-vsphere` can refer to
it as a future composition target without ambiguity. No source code lands in v1.

The v2 surface, when implemented, will cover NSX-T logical networking
(switches/segments, T0/T1 routers), security (DFW rules, security groups, NS
groups), services (load balancers, NAT), and inventory (VMs, virtual interfaces,
IP discovery).

The `automojo-provisioning` `venue-vsphere` composes `NsxClient` when present and
degrades cleanly when NSX is not configured in the target environment — that
graceful-degradation behaviour is part of the v1 `venue-vsphere` contract, not
this spec.

---

## Requirements

### Requirement 1: Scope and Versioning Statement

**User Story:** As a downstream consumer planning future composition, I want a
clear scope statement for what NSX support means in this repository.

#### Acceptance Criteria

1. THE SYSTEM SHALL document that this package targets NSX-T 4.x as the primary
   API revision; NSX-V (legacy) is explicitly out of scope.
2. THE SYSTEM SHALL document that the v1 release of the automojo monorepo ships
   this package as **spec-only**: no `source/packages/` code is published.
3. THE SYSTEM SHALL document that the first source code milestone for this
   package is v2, post the v1 baseline shipping of `automojo-interop-vsphere`
   and `automojo-provisioning` `venue-vsphere`.

---

### Requirement 2: Client Construction (v2)

#### Acceptance Criteria

1. WHEN the v2 client is implemented THE SYSTEM SHALL construct
   `NsxClient(base_url=..., credential=NsxManagerCredential(...), aspects=...)`
   on `RestClientBase`.
2. WHEN authentication is required THE SYSTEM SHALL use NSX Manager session
   tokens (or basic auth, depending on operator config), retrieved on first
   call and refreshed via the `AUTHENTICATION_FAILURES` retry hook.

---

### Requirement 3: v2 API Groups (Forecast)

#### Acceptance Criteria

1. THE SYSTEM SHALL provide (in v2) the following `RestApiGroup` subclasses
   accessed as properties on `NsxClient`:
   - `Segments` — logical segments
   - `T0Routers`, `T1Routers` — gateway tiers
   - `Dfw` — distributed firewall rules and policies
   - `SecurityGroups`, `NsGroups` — group memberships
   - `Services` — predefined service objects
   - `LoadBalancers` — LB virtual servers, pools, profiles
   - `Nat` — NAT rules
   - `Inventory` — VM, VIF, IP discovery
2. WHEN a v1 consumer attempts to import this package's source modules THE
   SYSTEM SHALL surface a clear "not implemented in v1" error from the package
   `__init__` (in the form of a `NotImplementedError` raised eagerly).

---

### Requirement 4: Composition by venue-vsphere

#### Acceptance Criteria

1. WHEN `automojo-provisioning` `venue-vsphere` detects NSX is configured in the
   target environment AND `automojo-restclient-nsx` v2 is installed THE SYSTEM
   SHALL be composed into the venue provisioner.
2. WHEN NSX is not configured OR this package is not installed THE SYSTEM SHALL
   be skipped silently; `venue-vsphere` degrades cleanly per its own contract
   (port-group ACL hints; no LB support).
