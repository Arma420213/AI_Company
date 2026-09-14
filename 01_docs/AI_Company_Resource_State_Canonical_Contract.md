AI Company — Resource State Canonical Contract

Version: 1.0
Status: DERIVED — PRE-IMPLEMENTATION CONTRACT
Authority: NONE
Canonical Authority: 00_architecture/AI_Company_Canonical_Architecture.md
Architectural Home: 02_core/resource_state.py
Canonical Owner: Resource State Authority

---

# 1. Constitutional Position

This document defines the implementation-neutral canonical contract for Resource State.

It is derived from:

00_architecture/AI_Company_Canonical_Architecture.md

01_docs/AI_Company_Canonical_Responsibility_Map.md

01_docs/AI_Company_Core_Contract_Specification.md

01_docs/AI_Company_Core_Module_Derivation.md

01_docs/AI_Company_Core_Implementation_Order.md

It does not amend, replace, extend, or reinterpret the frozen Canonical Architecture.

If this contract conflicts with the Canonical Architecture:

THE CANONICAL ARCHITECTURE WINS.

---

# 2. Responsibility

Resource State represents the currently usable finite execution and operational resource capacity known to AI Company.

The canonical derivation is:

Hardware Capability Profile
            +
Hardware Observation
            +
Resource Interpretation Rules
            +
Canonical Resource Constraints
            |
            v
      Resource State

Resource State therefore does not merely repeat hardware information.

It is the canonical interpretation of what resource capacity is currently usable within the known evidence and constraints.

Resource State is a snapshot of current conditions.

It is not:

permanent hardware capability;

raw hardware observation;

Task feasibility;

Agent selection;

execution readiness;

execution authorization;

execution.

---

# 3. Canonical Ownership

Canonical Authority: Resource State Authority.

Canonical State: Resource State.

State Owner: Resource State Authority.

There must be exactly one canonical owner of Resource State.

No:

Runtime service;

Integration;

Hardware Observer;

Agent;

Selection Engine;

Execution System;

external provider

may become a competing Resource State authority.

---

# 4. Core Boundary

Resource State belongs to 02_core.

The Core implementation must remain meaningful if all external integrations are removed.

resource_state.py must not depend on:

Runtime;

Integrations;

Weft;

LLM providers;

HTTP clients;

databases;

cloud SDKs;

operating-system APIs;

hardware-monitoring libraries;

development tools.

Physical observation mechanisms remain outside Core.

They provide canonical Hardware Observations.

They do not define Resource State semantics.

---

# 5. Fundamental Semantic Distinctions

## 5.1 Hardware Capability

Hardware Capability answers:

What can this environment structurally provide?

Examples:

CPU topology/capacity;

installed RAM;

GPU presence/capacity;

storage capacity.

It represents structural potential.

## 5.2 Hardware Observation

Hardware Observation answers:

What has actually been observed in the physical environment?

Examples:

CPU utilization;

available memory;

GPU condition;

storage availability;

system pressure.

It represents evidence.

## 5.3 Resource State

Resource State answers:

What resource capacity is currently considered usable?

It is derived from capability, observation, interpretation, and constraints.

Therefore:

Capability != Observation != Resource State

This distinction is constitutional.

---

# 6. Canonical Inputs

Resource State consumes four semantic input categories.

## 6.1 Hardware Capability Profile

Defines structural ceilings and capabilities.

## 6.2 Hardware Observation

Provides current physical/environmental evidence.

## 6.3 Resource Interpretation Rules

Define how capability and observation become usable capacity.

Interpretation rules belong to Resource State Authority.

They are not a second authority.

They must remain provider-independent.

## 6.4 Resource Constraints

May include:

reservations;

contention;

committed capacity;

environmental limitations;

operational restrictions.

Constraints may reduce usable capacity.

They can never manufacture physical capacity.

---

# 7. Canonical Output

A Resource State must semantically contain, where applicable:

Resource State identity;

hardware/environment identity;

derivation timestamp;

source observation provenance;

CPU state;

memory state;

GPU state;

storage state;

network availability;

resource pressure;

reservations/contention;

limitations;

derivation provenance.

Additional resource dimensions may exist.

They must not create another resource authority.

---

# 8. Snapshot Semantics

Resource State represents resource conditions at a particular point in time.

A canonical Resource State therefore requires:

identity;

hardware/environment identity;

derivation/evaluation timestamp;

source observation identity or provenance.

New observations may produce new Resource States.

Historical Resource States must not silently mutate into newer states.

---

# 9. Finite Resource Principle

AI Company must never assume unlimited physical execution capacity.

For every finite resource dimension:

usable capacity <= structural capacity

and:

reserved/committed capacity
    <=
capacity from which it is derived

Negative finite capacities are invalid.

A Resource State may legitimately indicate insufficient capacity.

Insufficient capacity is a valid resource condition.

It is not itself an execution failure.

---

# 10. Capacity Invariants

## 10.1 Capability Is a Ceiling

Resource State cannot silently exceed Hardware Capability.

## 10.2 Observation Is Evidence

Observation does not become permanent capability.

## 10.3 Usable Capacity Is Derived

Canonical usable capacity must be produced by canonical interpretation rules.

Arbitrary caller-provided values must not become canonical merely because they are wrapped in a ResourceState.

## 10.4 Constraints Cannot Create Capacity

Reservations, contention and pressure may reduce usable capacity.

They cannot increase physical capacity.

## 10.5 Resource Dimensions Are Independent

CPU, memory, GPU, storage and network are distinct.

For example:

CPU available != GPU available
RAM available != storage available
network available != local compute available

Availability in one dimension cannot be inferred solely from another.

---

# 11. Unknown Is Not Zero

Missing information must not silently become zero.

For example:

GPU observation unavailable

does not automatically mean:

GPU capacity = 0

Likewise:

storage observation unavailable

does not automatically mean:

storage unavailable

unless canonical evidence establishes that fact.

The implementation must preserve the distinction between:

known;

unavailable;

unobserved;

incomplete;

constrained.

The exact value representation must remain a Core contract decision.

---

# 12. Observation Freshness

Resource State depends on current observations.

Therefore observation freshness is semantically relevant.

A stale observation must not silently be presented as current truth.

If an observation is stale under the applicable interpretation policy, the resulting Resource State must preserve that limitation.

Freshness thresholds belong to canonical Resource State interpretation policy.

They must not be independently invented by an Integration or Task evaluator.

---

# 13. Incomplete Observations

Resource State may be derived from incomplete evidence only if the incompleteness remains explicit.

The authority must not invent missing values.

One unavailable dimension must not automatically invalidate unrelated valid dimensions.

For example:

GPU observation unavailable

must not necessarily invalidate:

CPU resource state
Memory resource state
Storage resource state

---

# 14. Inconsistent Observations

When canonical inputs contradict one another, the Resource State Authority must not silently select an arbitrary value.

The interpretation contract must define whether to:

reject derivation;

mark the affected dimension unavailable/invalid;

preserve the conflict as a limitation;

derive unaffected dimensions.

The resulting state must retain sufficient provenance to explain the outcome.

---

# 15. Resource Pressure

Resource pressure is part of Resource State where supported by canonical observations.

Pressure describes current conditions affecting usable capacity.

Pressure is not:

Task evaluation;

Agent selection;

authorization;

execution.

Resource State may interpret pressure into usable capacity or limitations, but it must not turn pressure into a Task-specific decision.

---

# 16. Reservations and Contention

Reservations and contention belong to Resource State when they affect currently usable capacity.

They may reduce available capacity.

They cannot create capacity.

Resource State must remain descriptive.

It must not answer:

Which Task receives this resource?

That is outside Resource State Authority.

Resource State is not a scheduler or allocator.

---

# 17. Canonical Resource Dimensions

CPU

Represents currently usable CPU capacity and relevant conditions.

It is distinct from physical CPU capability.

Memory

Represents currently usable memory capacity and relevant limitations.

It is distinct from installed memory capacity.

GPU

Represents currently usable GPU capacity where applicable.

The following must remain distinguishable where evidence supports it:

GPU absent;

GPU present;

GPU observation unavailable;

GPU currently unusable.

Vendor-specific GPU APIs do not define canonical semantics.

Storage

Represents currently usable storage capacity and limitations.

It is distinct from structural storage capacity.

Network

Represents network availability when relevant and observable.

Network availability does not authorize communication or execution.

Other Resources

Additional resource dimensions may exist under the same ownership and finite-resource principles.

---

# 18. Provenance

Every Resource State must preserve enough provenance to determine:

what environment it describes;

when it was derived;

which observations contributed;

which authority derived it;

which limitations affected it.

Provider-specific provenance may be preserved as source metadata.

It must not redefine canonical semantics.

---

# 19. Identity

Resource State requires its own canonical identity.

It must not be confused with:

hardware identity;

observation identity;

Task identity;

execution attempt identity.

Multiple Resource States may exist for one hardware environment over time.

---

# 20. Mutability

Individual Resource State records should be immutable.

Changing resource conditions should result in new Resource State evidence rather than mutation of historical canonical state.

The Resource State Authority may own a mutable collection/history of Resource States.

Caches, projections and persistence records are not canonical owners.

---

# 21. Failure Modes

The authority must explicitly account for:

missing Hardware Capability;

missing Hardware Observation;

stale observations;

incomplete observations;

inconsistent observations;

insufficient information;

unavailable capacity;

invalid interpretation;

impossible negative capacity;

capacity exceeding structural capability;

invalid reservation/contention data;

missing provenance;

invalid identity;

invalid timestamp.

Failure in one resource dimension should not automatically destroy valid information from unrelated dimensions.

---

# 22. Forbidden Responsibilities

Resource State Authority must not own:

strategic decisions;

Task definition;

Task lifecycle;

Task evaluation;

Agent selection;

execution readiness for a concrete proposal;

execution authorization;

execution;

scheduling;

Task-specific resource allocation;

hardware probing;

OS monitoring;

provider APIs.

The separation is:

Resource State
    !=
Task Evaluation
    !=
Agent Selection
    !=
Execution Readiness
    !=
Execution Authorization

---

# 23. Integration Boundary

The physical observation path is:

Physical / OS / Vendor Observation
              |
              v
      Integration Adapter
              |
              v
   Hardware Observation
              |
              v
    Resource State Authority

OS APIs, vendor SDKs and monitoring libraries remain outside Core.

resource_state.py consumes canonical observations, not hardware APIs.

---

# 24. Runtime Boundary

Runtime may compose:

Hardware Capability;

Hardware Observation;

Resource State;

Task Evaluation;

Agent Selection;

Execution Readiness;

Execution Authorization.

Runtime may coordinate these authorities.

Runtime must not redefine Resource State semantics.

---

# 25. Relation to Task Evaluation

Task Evaluation may consume Resource State.

For example:

Resource State:
    usable memory = X

followed by:

Task requirement <= X

The comparison belongs to Task Evaluation.

Resource State must not contain Task-specific feasibility logic.

---

# 26. Relation to Agent Selection

Agent Selection may consume Resource State.

The correct relationship is:

Resource State
      |
      v
Agent Selection input

not:

Resource State
      |
      v
Selected Agent

Resource State provides evidence.

Agent Selection owns the selection decision.

---

# 27. Relation to Execution Readiness

Execution Readiness may consume Resource State.

The relationship is:

Resource State
      |
      v
Execution Readiness

Resource State itself must not emit the Task-specific readiness states:

READY
DEGRADED
BLOCKED
UNAVAILABLE

Those belong to Readiness Authority.

---

# 28. Dependency Rules

02_core/resource_state.py may depend only on:

standard language/runtime facilities;

canonical Core contracts;

canonical Core value types.

It must not depend on:

03_runtime;

04_integrations;

Weft;

external providers;

HTTP;

databases;

cloud SDKs;

OS APIs;

hardware monitoring libraries;

development tools;

test utilities.

Semantic dependency does not automatically justify a concrete Python import.

---

# 29. Observability

A Resource State must be explainable.

At minimum its provenance should permit reconstruction of:

Resource State
    |
    +-- hardware/environment
    +-- derivation timestamp
    +-- source observations
    +-- interpretation/limitations
    +-- derived availability

Canonical Resource State must not require hidden provider state to explain itself.

---

# 30. Test Obligations

Tests must verify at minimum:

Ownership

one Resource State authority;

authority-owned mutable state;

no competing authority.

Separation

Capability != Resource State;

Observation != Resource State;

Resource State != Task Evaluation;

Resource State != Agent Selection;

Resource State != Readiness;

Resource State != Authorization.

Finite Resources

usable capacity cannot exceed structural capability;

negative capacities are rejected;

constraints cannot create capacity;

dimensions remain independent.

Evidence

stale observations are handled explicitly;

incomplete observations remain distinguishable;

inconsistent observations are handled explicitly;

provenance is retained.

Dependency Isolation

no Runtime imports;

no Integration imports;

no provider-specific imports;

Core remains independently executable.

Behavioral Isolation

no execution;

no Agent selection;

no authorization;

no scheduling;

no Task-specific allocation.

---

# 31. Implementation Derivation Rule

The implementation must be judged against this contract.

The contract must not be rewritten to justify the current Python implementation.

The existing implementation already contains useful structural properties:

immutable Resource State;

immutable provenance;

timezone-aware timestamps;

read-only mappings;

explicit identity;

authority-owned state collection;

Core-only dependencies.

Those properties should be preserved where they remain compatible.

However, the current implementation primarily performs:

caller-created ResourceState
        |
        v
record_state()

The canonical contract requires the semantic boundary:

Hardware Capability
        +
Hardware Observation
        +
Interpretation Rules
        +
Resource Constraints
        |
        v
Resource State

That is the principal implementation gap to resolve.

---

# 32. Non-Goals

This contract does not define:

physical hardware probing;

OS monitoring;

vendor GPU APIs;

network probing;

Task resource requirements;

Task evaluation algorithms;

Agent selection algorithms;

readiness algorithms;

authorization policy;

scheduling;

Task resource allocation;

execution mechanisms;

persistence technology;

Runtime composition.

Those belong to their respective authorities and architectural layers.

---

# 33. Canonical Summary

The Resource State Authority owns one responsibility:

Derive and represent currently usable finite resource capacity from canonical hardware capability, canonical hardware observations, and explicit resource interpretation and constraint rules.

The canonical chain is:

STRUCTURAL CAPABILITY
        |
        v
CURRENT OBSERVATION
        |
        v
INTERPRETATION + CONSTRAINTS
        |
        v
CURRENT USABLE RESOURCE STATE

Therefore:

Hardware Capability
    = structural potential

Hardware Observation
    = observed condition

Resource State
    = currently usable capacity

Task Evaluation
    = task-specific suitability

Agent Selection
    = participant selection

Execution Readiness
    = current proposal feasibility

Execution Authorization
    = explicit permission

No authority may silently absorb another authority's responsibility.

Architecture remains supreme.