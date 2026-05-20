===================
automojo-interop-nsx
===================

The ``automojo-interop-nsx`` package is the dedicated NSX-T interop client
for the automojo suite.  It provides ``NsxClient``, a ``RestClientBase``
subclass that talks to the NSX-T Manager Policy API
(``/policy/api/v1/``).

It is a sibling to ``automojo-interop-vsphere``, deliberately kept
separate because NSX users are a strict subset of vSphere users and the
API surfaces are large enough that bundling makes the simple (no-NSX)
case worse.

API surface
===========

- Segments (logical switches)
- Tier-0 / Tier-1 gateways
- Security groups
- Distributed firewall policies and rules
- NAT rules
- Load balancers (services, virtual servers, pools)

NSX-T policy mutations are realized asynchronously; every mutating call
returns an ``NsxRealizationHandle`` (conforming to ``ITaskHandle``) that
polls realization state until a terminal state is reached.
