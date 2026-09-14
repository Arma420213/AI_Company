# AI Company — Resource State Semantic Model Contract

**Version:** 1.0  
**Status:** DERIVED — PRE-IMPLEMENTATION CONTRACT  
**Authority:** NONE  
**Canonical Authority:** `00_architecture/AI_Company_Canonical_Architecture.md`  
**Architectural Home:** `02_core/resource_state.py`  
**Canonical Owner:** Resource State Authority

---

# 1. Constitutional Position

This document defines the semantic value model required to implement the
canonical Resource State contract.

It is derived from:

- `00_architecture/AI_Company_Canonical_Architecture.md`
- `01_docs/AI_Company_Canonical_Responsibility_Map.md`
- `01_docs/AI_Company_Core_Contract_Specification.md`
- `01_docs/AI_Company_Core_Module_Derivation.md`
- `01_docs/AI_Company_Resource_State_Canonical_Contract.md`

The canonical architecture has precedence over this document.

This document defines semantic contracts only.

It does not create a new canonical authority.

---

# 2. Purpose

The Resource State semantic model provides the minimum canonical vocabulary
required to transform:

```text
Hardware Capability
        +
Hardware Observation
        +
Resource Interpretation Rules
        +
Resource Constraints
        ↓
Resource Values
        ↓
Resource State
The model exists to distinguish:
- structural capability,
- observed evidence,
- interpreted current usable capacity,
- limitations,
- uncertainty,
- reservations,
- contention,
- and environmental or operational restrictions.
The model must remain independent from:
- task requirements,
- agent selection,
- execution readiness,
- authorization,
- scheduling,
- allocation,
- execution,
- runtime orchestration,
- integrations,
- providers,
- operating-system APIs,
- databases,
- HTTP services,
- cloud services.

---

# 3. Semantic Ownership
The Resource State Authority owns the meaning of:
- Resource Value
- Resource Interpretation Rules as Resource State inputs
- Resource Constraints as Resource State inputs
- Resource State derivation
- current usable finite resource capacity
No separate authority is introduced for:
- Resource Values
- Interpretation Rules
- Resource Constraints
These are semantic inputs and value contracts belonging to the
Resource State domain.

---

# 4. Resource Value

## 4.1 Definition
A Resource Value represents the interpreted value of one canonical
resource dimension at a specific Resource State evaluation.
A Resource Value is not:
- a hardware capability,
- a raw hardware observation,
- a task requirement,
- a task feasibility result,
- an execution decision,
- an agent-selection score,
- an authorization result.
It is an interpreted resource-domain value.

## 4.2 Canonical Semantic Components
A Resource Value may contain the following semantic components:
Dimension
Identifies the resource dimension represented by the value.
Canonical dimensions include:
- CPU
- memory
- GPU
- storage
- network
Additional dimensions may exist only when justified by the canonical
architecture.
Quantity
An optional finite quantitative value.
Quantity is optional because not every resource dimension has a meaningful
canonical numeric representation.
Examples:
- CPU capacity may be quantitative.
- Memory capacity may be quantitative.
- Storage capacity may be quantitative.
- GPU may contain quantitative capacity where meaningful.
- Network may primarily be represented through availability or condition.
Absence of quantity does not mean zero.
Unit
An optional semantic unit associated with a quantitative quantity.
Units must remain provider-independent.
Provider-specific representations must not become canonical Resource Value
semantics.
Status
Describes the semantic condition of the value.
Canonical statuses are:
- KNOWN
- UNAVAILABLE
- UNOBSERVED
- INCOMPLETE
- CONSTRAINED
Limitation
An optional explanation of a condition affecting the value.
Examples include:
- stale observation,
- missing observation,
- incomplete evidence,
- inconsistent evidence,
- reservation,
- contention,
- environmental limitation,
- operational restriction.
A limitation explains state semantics.
It does not perform scheduling, allocation, selection, authorization, or
execution.

---

# 5. Resource Value Status Semantics

## 5.1 KNOWN
KNOWN means the Resource State Authority has sufficient valid evidence and
interpretation to represent the value.
For quantitative values:
- quantity must be present,
- quantity must be finite,
- quantity must not be negative.

## 5.2 UNAVAILABLE
UNAVAILABLE means the resource dimension cannot currently be represented
as usable capacity.
This is distinct from zero.
UNAVAILABLE must not be silently converted into numeric zero.

## 5.3 UNOBSERVED
UNOBSERVED means the required evidence for the resource dimension has not
been observed or supplied.
UNOBSERVED must not be interpreted as zero.

## 5.4 INCOMPLETE
INCOMPLETE means available evidence exists but is insufficient to establish
a complete Resource Value.
An incomplete value must not be completed by invented data.
Unrelated resource dimensions may remain valid.

## 5.5 CONSTRAINED
CONSTRAINED means the resource value is affected by a canonical resource
constraint.
Examples:
- reservation,
- committed capacity,
- contention,
- environmental limitation,
- operational restriction.
A constraint may reduce usable capacity.
A constraint cannot create capacity.

---

# 6. Resource Value Invariants

The following invariants are mandatory.

## 6.1 Unknown Is Not Zero
The following semantic states are distinct:
quantity = 0
quantity = absent
status = UNOBSERVED
status = UNAVAILABLE
status = INCOMPLETE
status = CONSTRAINED
No implementation may collapse these meanings without an explicit canonical
interpretation rule.

## 6.2 Quantitative Values Are Finite
Where quantity is used:
- it must be finite,
- it must not be negative.
NaN and infinite values are invalid canonical Resource Values.

## 6.3 Constraints Cannot Manufacture Capacity
A constraint can reduce usable capacity.
It cannot increase structural capability or create usable capacity where no
capacity exists.

## 6.4 Capability Is a Ceiling
Where a quantitative Resource Value can be compared with a corresponding
Hardware Capability value:
usable capacity <= structural capability
must hold.

## 6.5 Dimensions Remain Semantically Independent
Failure to establish one resource dimension must not automatically invalidate
all unrelated resource dimensions.
For example:
GPU = UNOBSERVED
memory = KNOWN
storage = KNOWN
is a valid semantic combination.

---

# 7. Resource Interpretation Rules

## 7.1 Definition
Resource Interpretation Rules are immutable semantic rules used by the
Resource State Authority to interpret Hardware Capability and Hardware
Observation into Resource Values.
They are policy/value inputs.
They are not an Authority.

## 7.2 Required Semantic Areas
Interpretation Rules must define how the Resource State Authority handles:
- observation freshness,
- unknown information,
- incomplete information,
- inconsistent information.

## 7.3 Freshness
Interpretation Rules may define a freshness threshold or equivalent policy
for determining whether an observation remains usable for Resource State
derivation.
A stale observation must not silently be treated as current.
The semantic result may be, depending on the rule:
- preserved with limitation,
- marked unavailable,
- or otherwise explicitly represented.
No implicit freshness assumption is permitted.

## 7.4 Unknown Information
Canonical unknown handling must never assume:
unknown = zero
Permitted semantic policies include:
- preserve unknown information,
- mark the affected value unavailable.
An interpretation rule may not manufacture missing capacity.

## 7.5 Incomplete Information
Incomplete evidence must remain explicitly represented.
Permitted semantic policies include:
- preserve incomplete information,
- mark the affected value unavailable.
Unrelated valid dimensions should remain usable where possible.

## 7.6 Inconsistent Information
When observations or inputs are inconsistent, the interpretation rules must
define the semantic response.
Permitted responses include:
- reject the affected derivation,
- mark the affected value unavailable,
- preserve the conflict explicitly,
- derive unaffected dimensions independently.
The Resource State Authority must not arbitrarily choose a value merely to
produce a complete snapshot.

---

# 8. Resource Constraints

## 8.1 Definition
Resource Constraints represent conditions that reduce or limit currently
usable resource capacity.
They are immutable Resource State inputs.
They are not a scheduler, allocator, or execution authority.

## 8.2 Canonical Constraint Categories
Resource Constraints may represent:
- reservations,
- committed capacity,
- contention,
- environmental limitations,
- operational restrictions.

## 8.3 Reservations
A reservation represents capacity that is unavailable for general current
use.
A reservation may reduce usable capacity.
A reservation does not create capacity.

## 8.4 Committed Capacity
Committed capacity represents capacity already committed by the operating
environment or other canonical resource conditions.
Committed capacity may reduce currently usable capacity.
It must remain independent of task-specific scheduling semantics.

## 8.5 Contention
Contention represents competing use or pressure affecting currently usable
capacity.
Contention is descriptive Resource State information.
It is not a scheduling decision.

## 8.6 Environmental Limitations
Environmental limitations represent conditions that reduce usable resource
capacity independently of a specific task.
Examples may include:
- thermal or operational restrictions,
- externally imposed capacity limitations,
- unavailable infrastructure conditions.
Provider-specific mechanisms must not become canonical semantics.

## 8.7 Operational Restrictions
Operational restrictions represent canonical restrictions on currently usable
capacity.
They must not become:
- authorization rules,
- task policies,
- agent policies,
- execution policies.

---

# 9. Capacity Semantics

Where quantitative structural capacity exists, Resource State derivation must
respect:
0 <= usable capacity <= structural capability
Where reservations, commitments, contention, or limitations reduce capacity:
usable capacity <= unconstrained usable capacity
Constraints cannot increase capacity.
If insufficient capacity exists, the Resource State remains valid.
Insufficient capacity is not itself:
- a task failure,
- a readiness result,
- an authorization failure,
- an execution failure.

---

# 10. Quantitative and Semantic Dimensions

Not every canonical resource dimension must be represented by the same numeric
model.
The semantic model therefore distinguishes:
Quantitative dimensions
Dimensions where finite quantities can meaningfully represent capacity.
Examples:
- CPU
- memory
- storage
- some GPU capacity representations
Semantic dimensions
Dimensions where availability or condition may be more meaningful than a
single canonical quantity.
Example:
- network
A Resource State implementation must not force every resource dimension into
an artificial numeric quantity merely for structural uniformity.

---

# 11. Relationship to Hardware Capability

Hardware Capability represents structural potential.
It answers:
What can this hardware structurally provide?
Resource Value represents interpreted current usable capacity.
It answers:
What capacity is currently usable according to the available evidence,
interpretation rules, and constraints?
Therefore:
Hardware Capability != Resource Value
Resource State must not redefine Hardware Capability.

---

# 12. Relationship to Hardware Observation

Hardware Observation represents evidence.
It answers:
What has been observed?
Resource Value represents interpretation.
It answers:
What does the available evidence mean for current usable resource capacity?
Therefore:
Hardware Observation != Resource Value
Interpretation belongs to Resource State Authority.
Hardware Observation must remain descriptive.

---

# 13. Canonical Derivation Chain

The canonical semantic derivation is:
Hardware Capability
        +
Hardware Observation
        +
Resource Interpretation Rules
        +
Resource Constraints
        ↓
Resource Value
        ↓
Resource State
The derivation must preserve:
- evidence provenance,
- interpretation conditions,
- limitations,
- resource identity,
- evaluation time,
- finite capacity invariants.

---

# 14. Provenance

Resource Value and Resource State derivation must remain explainable.
The semantic model must permit reconstruction of:
- which hardware/environment was evaluated,
- when it was evaluated,
- which observations were used,
- which interpretation rules were applied,
- which constraints affected the result,
- which limitations remained.
Provider-specific identifiers may appear as provenance metadata when useful,
but they must not redefine canonical semantics.

---

# 15. No New Authorities

This semantic model explicitly forbids creation of:
- ResourceValueAuthority
- InterpretationAuthority
- ResourceConstraintAuthority
The following remain inputs or value contracts:
Resource Value
Resource Interpretation Rules
Resource Constraints
The canonical owner remains:
Resource State Authority

---

# 16. Dependency Rules

The semantic model must remain within the Core boundary.
Allowed dependencies are limited to:
- Python standard library,
- canonical Core contracts,
- canonical Core value types.
Forbidden dependencies include:
- 02_company_runtime,
- integrations,
- Weft,
- LLM providers,
- HTTP clients,
- databases,
- cloud services,
- OS monitoring APIs,
- vendor hardware APIs,
- task execution systems,
- agent selection systems,
- readiness systems.

---

# 17. Placement Rule

The initial implementation home for these semantic value contracts is:
02_core/resource_state.py
This is intentional.
A separate canonical module must not be created merely because a semantic
concept has a distinct dataclass.
A separate Core value module may be introduced only if genuine canonical reuse
across independent authorities is demonstrated.
Until such reuse exists:
Resource Value
Resource Interpretation Rules
Resource Constraints
remain part of the Resource State semantic boundary.

---

# 18. Relationship to Runtime

Runtime may consume Resource State.
Runtime must not redefine:
- Resource Value semantics,
- interpretation rules,
- constraint semantics,
- finite capacity invariants,
- unknown/incomplete semantics.
Runtime composition does not create Resource State authority.

---

# 19. Relationship to Task Evaluation

Task-specific comparison between:
task requirements
        +
resource state
belongs to Task Evaluation.
Resource State must not answer:
Can this specific task run?
Resource State answers only:
What resource capacity currently exists?

---

# 20. Relationship to Agent Selection

Agent Selection may consume Resource State.
Resource State must not:
- rank agents,
- select agents,
- score agents,
- choose execution candidates.
Therefore:
Resource State → Agent Selection
is permitted as consumption.
The reverse semantic dependency is forbidden.

---

# 21. Relationship to Execution Readiness

Execution Readiness may consume Resource State.
Resource State must not determine:
- READY,
- DEGRADED,
- BLOCKED,
- UNAVAILABLE
as execution-readiness states.
Those meanings belong to the Readiness Authority.
Resource Value status such as UNAVAILABLE is a resource-domain semantic
condition and must not be confused with execution readiness.

---

# 22. Non-Goals

This semantic model does not define:
- hardware probing,
- hardware monitoring,
- operating-system monitoring,
- vendor APIs,
- network probing,
- task feasibility,
- task allocation,
- scheduling,
- agent selection,
- execution readiness,
- authorization,
- execution,
- persistence,
- runtime orchestration.

---

# 23. Implementation Derivation Rule

The implementation of 02_core/resource_state.py must be derived from:
AI Company Canonical Architecture
        ↓
Resource State Responsibility
        ↓
Resource State Authority
        ↓
Resource State Canonical Contract
        ↓
Resource State Semantic Model Contract
        ↓
Implementation
        ↓
Tests
The implementation must not be derived from the limitations of the existing
resource_state.py.
The existing structural strengths should be preserved where compatible:
- immutable Resource State snapshots,
- immutable provenance,
- Resource State Authority ownership,
- state identity,
- hardware identity,
- timestamps,
- state history,
- Core isolation.
The existing caller-created-only state pattern is semantically incomplete and
must be extended to support canonical derivation.

---

# 24. Intentional Design Boundary

This contract deliberately does not prescribe the final Python API.
In particular, it does not yet mandate:
- constructor names,
- method names,
- exact enum implementation,
- exact unit representation,
- exact mapping representation,
- exact constraint storage structure.
Those implementation details must be derived only after the semantic contract
has been validated against the existing Core model.

---

# 25. Canonical Summary

Resource State semantics are defined by the following principle:
Resource State Authority interprets Hardware Capability and Hardware
Observation through explicit Resource Interpretation Rules and Resource
Constraints, producing Resource Values that represent currently usable
finite resource capacity.

The semantic model preserves the distinction:
Capability = structural potential
Observation = evidence
Interpretation = meaning
Constraint = limitation
Resource Value = interpreted dimension
Resource State = canonical current capacity snapshot
No unknown value becomes zero by assumption.
No constraint creates capacity.
No resource value becomes a task decision.
No Resource State responsibility becomes an execution responsibility.
No new authority is created.

---

# 26. Contract Status

SEMANTIC MODEL: DERIVED — PRE-IMPLEMENTATION
This document is the semantic basis for the next implementation audit.
Before modifying:
02_core/resource_state.py
the following must be completed:
1. semantic contract audit,
2. compatibility audit against hardware_capability.py,
3. compatibility audit against hardware_observation.py,
4. implementation derivation,
5. test derivation.
Until those steps are complete, resource_state.py remains unchanged.