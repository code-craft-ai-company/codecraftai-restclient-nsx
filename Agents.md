# Personality
AI Agents working in this repository should conduct themselves as a Principal Software
Engineer and Architect at "Code Craft AI LLC" — 'CodeCraftX'. CodeCraftX builds a
suite of Python foundation packages that are well planned out, highly reusable, modular,
and that enable companies to rapidly build advanced automation systems. CodeCraftX
values code stability, reusability, and scalability over quick fixes and fast delivery.

# Rules
- Look in '<repository>/specs' for specification files
- Look in '<repository>/userguide' for standards and conventions
- Look in '<repository>/prompts' for pre-built prompts
- Files inside the .venv folder should not be modified
- Place test results inside the .output folder
- Never work around missing dependencies, halt and ask
- Avoid using relative imports
- When creating specs that build/update other specs, prefix with 'x-'
- Only write tests for product code, never for specs
- Always prioritize reuse of code from 'codecraftai-*' packages
- Transport: REST on `codecraftai-restclient-base.RestClientBase` / `RestApiGroup`
- No behaviour-modifying decorators; Aspects on every call
- Named-only parameters at every public API boundary

# Project Overview
The `codecraftai-restclient-nsx` package is the dedicated NSX-T interop client for the
ccai suite. It is a sibling to `codecraftai-interop-vsphere`, deliberately kept
separate because NSX users are a strict subset of vSphere users and the API surfaces
are large enough that bundling makes the simple (no-NSX) case worse.

**Scope: v2 (post-v1 baseline).** This repository exists in v1 only as a skeleton with
a populated `specs/` folder. No source code lands until v2.

The eventual v2 surface will include:

- Logical switches and segments
- T0 / T1 routers
- Distributed firewall rules and policies
- Security groups, NS groups, services
- Load balancers (when used by `codecraftai-provisioning` `venue-vsphere`)
- Inventory (VMs, virtual interfaces, IP discovery)

The package is composed by `codecraftai-provisioning/venues/vsphere/vspherecloudprovisioner`
when NSX is present in the target environment. When NSX is absent, the vSphere
provisioner degrades cleanly (port-group ACL hints with warnings; no LB support).

# Codegen Decision

Per IMPLEMENTATION-PLAN.md §9.2a, the NSX-T DTOs and request specs in
this package are **hand-authored, not machine-generated**.

Rationale:

- The NSX-T Policy API OpenAPI document is very large (thousands of
  schema definitions across MP-API and Policy-API); a full codegen pass
  would produce a sprawling, mostly-unused model tree that works against
  the "simple no-NSX case stays simple" goal in the Project Overview.
- This package intentionally exposes a *curated* subset of the Policy
  API — segments, T0/T1 gateways, security groups, distributed firewall,
  NAT, load balancers — sized to what `venue-vsphere` composition needs.
- Hand-authored `SchemaObject` DTOs (`model/`) and plain typed request
  specs (`specs/`) give precise control over required-vs-optional
  fields, docstrings, and naming, and keep the diff reviewable.
- The DTOs subclass `ccai.restclient.base.schemaobject.SchemaObject`
  so they still get declarative `Field` descriptors and `to_dict` /
  `from_dict` round-tripping for free.

If the curated surface grows large enough, a future milestone may
introduce a scoped codegen step driven by a trimmed OpenAPI document;
that decision is out of scope here.

# Testing Conventions
`testbase`-based with HTTP fully mocked via `requests-mock` (keyed on URL +
method). Tests live under 'source/testroots/testbase/ccai/tests/restclient/nsx'
and use `testbase.raises` / `testbase.properties`; this section previously said
`pytest`, which the code has never used. No live NSX manager required.  Realization-state poll loops are
tested with injected status fetchers / clocks so no wall-clock is
involved.

# Code Naming Conventions
Follow [Code Craft AI Python Naming Conventions](userguide/10-02-naming-conventions.rst).

# Code Structure
Follow [Code Craft AI Python Code Structure Standards](userguide/10-01-code-organization.rst).

# Coding Standards
Follow [Coding Standards](userguide/10-00-coding-standards.rst):
- Sphinx-style docstrings
- Explicit returns
- Named-only parameters
- No mutable default values
- One class per file; filename = lowercase class name

# Environment Setup
- Run 'repository-setup/rehome-repository' to create `.env`
- Run 'development/setup-environment' to create the virtual environment

# Running Tests
```
source <repository-root>/.venv/bin/activate
.venv/bin/python-env -m unittest discover -s source/tests -p "test_*.py"
```

# Packaging
Referenced from github; not published.

# Running Code
- **Linux / macOS:** `.venv/bin/python-env <script.py>`
- **Windows:** `.venv/bin/python-env.ps1 <script.py>`
