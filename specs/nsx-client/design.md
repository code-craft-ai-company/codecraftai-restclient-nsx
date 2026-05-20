# Design

## Overview

**Scope: v2 stub.** This spec documents the intended shape of `NsxClient` so the
v1 work in `automojo-interop-vsphere` and `automojo-provisioning` `venue-vsphere`
can refer to it as a future composition target. The v1 release ships this
package as spec-only; the source/packages tree does not contain implementation.

The eventual v2 client will be a `RestClientBase` subclass following the same
shape as `automojo-interop-vsphere.VSphereClient` — session-token authentication,
`RestApiGroup` subclasses behind cached client properties, Aspects on every call,
typed DTOs from `model/`, typed request specs from `specs/`.

---

## Architecture (v2 forecast)

```
┌────────────────────────────────────────────────────────────┐
│   automojo-provisioning  venue-vsphere                     │
│   (composes NSX when present, degrades when absent)        │
└─────────────────────┬──────────────────────────────────────┘
                      │ optional composition
                      ▼
┌────────────────────────────────────────────────────────────┐
│   NsxClient (subclass of RestClientBase)                   │
│                                                            │
│   @property Segments      @property T0Routers              │
│   @property T1Routers     @property Dfw                    │
│   @property SecurityGroups@property NsGroups               │
│   @property Services      @property LoadBalancers          │
│   @property Nat           @property Inventory              │
└─────────────────────┬──────────────────────────────────────┘
                      │ inherits from
                      ▼
┌────────────────────────────────────────────────────────────┐
│   automojo-restclient-base.RestClientBase                  │
└────────────────────────────────────────────────────────────┘
```

---

## Data Model (v2 forecast)

DTOs to be declared in `model/`:

- `SegmentSummary`, `SegmentInfo`
- `T0RouterSummary`, `T1RouterSummary`
- `DfwRule`, `DfwPolicy`
- `SecurityGroupSummary`, `NsGroupSummary`
- `ServiceSummary`
- `LoadBalancerSummary`, `LbVirtualServer`, `LbPool`, `LbProfile`
- `NatRule`
- `NsxInventoryVmRecord`, `NsxInventoryVifRecord`

Request specs in `specs/`:

- `SegmentSpec`
- `T1RouterSpec`
- `DfwRuleSpec`, `DfwPolicySpec`
- `SecurityGroupSpec`
- `LoadBalancerSpec`, `LbVirtualServerSpec`, `LbPoolSpec`
- `NatRuleSpec`

---

## Module Layout (v2 forecast)

```
source/packages/automojo/restclient/nsx/
├── __init__.py                   # v1: raises NotImplementedError on import
├── nsxclient.py                  # v2 entry
├── nsxsession.py                 # v2
├── aspectsnsx.py                 # v2
├── apigroups/                    # v2 — segmentgroup.py, t0routergroup.py, ...
├── model/                        # v2 DTOs
└── specs/                        # v2 request specs
```

In v1 only `__init__.py` exists; importing any submodule raises a clear
`NotImplementedError`.

---

## See Also

- `automojo-interop-vsphere` — the v1 sibling whose extraction pattern this
  package follows in v2.
- `automojo-provisioning` `venue-vsphere` — the composer; documents the
  graceful-degradation contract this package depends on.
- `PLAN-VPN-AND-CLOUD-PROVISIONING.md` §6.6 — the design decision that NSX is its
  own package and not bundled into the vSphere interop client.

---

## Testing Strategy

In v1: a single test asserts that importing any submodule under
`automojo.restclient.nsx` raises `NotImplementedError` with a clear message. No
other tests exist in v1.

In v2 (forecast): per-API-group unit tests against `MockHttpSession`; round-trip
DTO tests; Aspects forwarding tests; structural test that every declared API
group inherits `RestApiGroup`. Mirrors the testing strategy of
`automojo-interop-vsphere`.
