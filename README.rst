=========================================
Code Craft AI Interop - NSX-T
=========================================

The ``codecraftai-restclient-nsx`` package is the dedicated NSX-T interop client for the
ccai suite. It is a sibling to ``codecraftai-interop-vsphere``, deliberately kept
separate because NSX users are a strict subset of vSphere users and the API surfaces are
large enough that bundling makes the simple (no-NSX) case worse. The package is composed
by ``codecraftai-provisioning/venues/vsphere`` when NSX is present, and the vSphere
provisioner degrades cleanly when it is absent.

**Scope: v2 (post-v1 baseline).** This repository exists in v1 only as a skeleton with a
populated ``specs/`` folder. No source code lands until v2.

Highlights
==========

- ``NsxClient`` — a ``RestClientBase`` subclass talking to the NSX-T Manager Policy API (``/policy/api/v1/``).
- Curated Policy API surface — logical switches and segments, T0/T1 routers, distributed firewall rules and policies, security groups, NS groups, and services.
- Load balancers and inventory — load balancers (when used by ``codecraftai-provisioning`` ``venue-vsphere``) and inventory of VMs, virtual interfaces, and IP discovery.
- Asynchronous realization — every mutating call returns an ``NsxRealizationHandle`` (conforming to ``ITaskHandle``) that polls realization state until a terminal state is reached.
- Hand-authored DTOs — per IMPLEMENTATION-PLAN.md §9.2a, the NSX-T DTOs and request specs are hand-authored, not machine-generated, to keep the model tree sized to what ``venue-vsphere`` composition needs.

Repository Structure
====================

- ``source/packages/ccai/restclient/nsx/`` - Package source code.
- ``source/testroots/testbase/ccai/tests/restclient/nsx/`` - TestBase test roots.
- ``specs/`` - Requirements, design, and task documentation (Kiro-style).

Running Tests
=============

.. code-block:: bash

   source .venv/bin/activate
   testbase testing run --root ./source/testroots/testbase --includes=testbase.ccai.tests

Standards and Conventions
=========================

Coding standards, naming conventions, and code organization standards follow the
Code Craft AI suite-wide conventions. See ``Agents.md`` for the project rules and the
referenced standards documents.

Additional Resources
====================

- Project rules and references: ``Agents.md``
- Codegen decision: ``Agents.md`` (Codegen Decision section)
