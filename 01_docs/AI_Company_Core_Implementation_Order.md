# AI Company — Core Implementation Order

**VERSION:** 1.0
**STATUS:** DERIVED IMPLEMENTATION SPECIFICATION
**AUTHORITY:** SUBORDINATE TO THE FROZEN CANONICAL ARCHITECTURE
**PARENT CONTRACT:** `01_docs/AI_Company_Core_Contract_Specification.md`
**PARENT DERIVATION:** `01_docs/AI_Company_Core_Module_Derivation.md`
**IMPLEMENTATION TARGET:** `02_core`

---

# 1. Purpose

This document defines the canonical implementation sequence for the
AI Company Core modules.

It does not define new architecture.

It does not define new canonical authorities.

It does not redefine canonical responsibilities.

It does not authorize production implementation by itself.

Its purpose is to provide a controlled construction sequence for the
Core modules already derived from the frozen Canonical Architecture.

The Canonical Architecture remains authoritative.

---

# 2. Constitutional Authority

The implementation sequence is subordinate to:

1. `00_architecture/AI_Company_Canonical_Architecture.md`
2. `01_docs/AI_Company_Core_Contract_Specification.md`
3. `01_docs/AI_Company_Core_Module_Derivation.md`

If this document conflicts with any of those sources, this document is
wrong and must be corrected.

Architecture wins.

---

# 3. Implementation Rule

Core implementation follows:

CANONICAL ARCHITECTURE
    |
    v
CANONICAL RESPONSIBILITY
    |
    v
CANONICAL AUTHORITY
    |
    v
CANONICAL CONTRACT
    |
    v
CORE MODULE
    |
    v
IMPLEMENTATION
    |
    v
TESTS

Reverse reasoning is forbidden.

A Python implementation must never become the source from which
canonical architecture is inferred.

---

# 4. Semantic Dependency vs Implementation Dependency

This distinction is mandatory.

A semantic dependency means that one canonical concept:

- refers to another concept;
- consumes another concept as input;
- represents an association;
- uses another concept as evidence;
- participates in a canonical relationship.

A concrete implementation dependency means that one Python module must
actually import another Python implementation.

These are not equivalent.

Therefore:

SEMANTIC DEPENDENCY
    !=
CONCRETE IMPORT DEPENDENCY

A semantic relationship must not automatically create a Python import
dependency.

---

# 5. Semantic Graph

The canonical semantic graph may contain relationships that are not
topologically sortable as Python imports.

Examples include:

Task Evaluation
    |
    +--> Experience
    |
    +--> Trust

Experience
    |
    +--> Execution Result

Execution Result
    |
    +--> Execution Attempt

Execution Attempt
    |
    +--> Execution Authorization

Execution Authorization
    |
    +--> Execution Proposal

Execution Proposal
    |
    +--> Agent Selection

Agent Selection
    |
    +--> Task Evaluation

This is a legitimate semantic relationship graph.

It must not be converted into circular concrete imports.

---

# 6. Agent / Capability Association Rule

Agent and Capability are canonically distinct concepts.

Agent may reference Capability.

Capability may reference Agent-related availability information.

This does not authorize mutual concrete imports.

Implementations should prefer stable canonical identifiers,
value representations, explicit contracts, or other architecture-safe
reference mechanisms when direct imports would create a cycle.

Agent remains owned by Agent Authority.

Capability remains owned by Capability Authority.

Neither authority is transferred by the association.

---

# 7. Concrete Import Rule

Concrete Core imports must form an acyclic implementation graph.

A Core module may import another Core module only when the concrete
implementation genuinely requires that implementation.

Semantic reference alone is insufficient justification for an import.

When a semantic relationship does not require executable behavior from
the referenced module, the implementation should use an appropriate
canonical reference representation rather than importing the authority's
implementation merely to represent the relationship.

Circular imports are implementation defects unless explicitly proven
unavoidable and architecture-safe.

---

# 8. No New Canonical Authority

Implementation ordering must never introduce:

- a new authority;
- a second owner;
- a parallel Task model;
- a second Agent model;
- a second Capability model;
- a second lifecycle authority;
- a second Trust authority;
- a second Memory authority;
- a second Experience authority;
- a second Learning authority.

Execution Proposal remains a canonical execution-flow contract/object
without an independent canonical state authority.

---

# 9. Canonical Implementation Sequence

The following is the canonical construction sequence.

The sequence is an implementation sequence, not the runtime execution
flow.

| Order | Candidate Core Module | Canonical Authority |
|---:|---|---|
| 1 | `02_core/intent.py` | Intent Authority |
| 2 | `02_core/objective.py` | Objective Authority |
| 3 | `02_core/strategic_decision.py` | Decision Authority |
| 4 | `02_core/capability.py` | Capability Authority |
| 5 | `02_core/agent.py` | Agent Authority |
| 6 | `02_core/hardware_capability.py` | Hardware Capability Authority |
| 7 | `02_core/hardware_observation.py` | Hardware Observer |
| 8 | `02_core/resource_state.py` | Resource State Authority |
| 9 | `02_core/task.py` | Canonical Task Authority |
| 10 | `02_core/task_queue.py` | Queue Authority |
| 11 | `02_core/execution_proposal.py` | No independent authority |
| 12 | `02_core/execution_readiness.py` | Readiness Authority |
| 13 | `02_core/execution_authorization.py` | Authorization Authority |
| 14 | `02_core/execution_attempt.py` | Execution Authority |
| 15 | `02_core/execution_result.py` | Execution Result Authority |
| 16 | `02_core/task_lifecycle.py` | Task Lifecycle Authority |
| 17 | `02_core/memory.py` | Memory Authority |
| 18 | `02_core/experience.py` | Experience Authority |
| 19 | `02_core/trust.py` | Trust Authority |
| 20 | `02_core/learning.py` | Learning Authority |
| 21 | `02_core/task_evaluation.py` | Task Evaluation Authority |
| 22 | `02_core/agent_selection.py` | Agent Selection Authority |

---

# 10. Sequence Interpretation

The implementation sequence is intentionally different from the
canonical runtime flow.

The runtime flow remains:

HUMAN OWNER
    |
    v
COMPANY OBJECTIVES
    |
    v
STRATEGIC DECISION
    |
    v
CANONICAL TASK
    |
    v
TASK EVALUATION
    |
    v
AGENT SELECTION + RESOURCE EVALUATION
    |
    v
EXECUTION READINESS
    |
    v
EXECUTION AUTHORIZATION
    |
    v
EXECUTION SYSTEM
    |
    v
EXECUTION PIPELINE
    |
    v
EXECUTION ATTEMPT
    |
    v
OBSERVED OUTCOME
    |
    v
EXECUTION RESULT
    |
    v
TASK LIFECYCLE UPDATE
    |
    v
MEMORY / EXPERIENCE / TRUST
    |
    v
LEARNING
    |
    v
FUTURE DECISIONS

The implementation sequence exists to construct the software
foundations needed to support this flow.

It must not replace or reinterpret the runtime flow.

---

# 11. Foundation Phase

The first implementation group establishes basic canonical
organizational and physical concepts.

Modules:

1. `intent.py`
2. `objective.py`
3. `strategic_decision.py`
4. `capability.py`
5. `agent.py`
6. `hardware_capability.py`
7. `hardware_observation.py`
8. `resource_state.py`
9. `task.py`
10. `task_queue.py`

This phase establishes canonical identity, organizational direction,
capability, participant, physical capability, observation, resource
state, Task definition, and queue semantics.

No execution implementation is introduced in this phase.

---

# 12. Execution Contract Phase

The second implementation group establishes the execution-flow
representations.

Modules:

11. `execution_proposal.py`
12. `execution_readiness.py`
13. `execution_authorization.py`
14. `execution_attempt.py`
15. `execution_result.py`
16. `task_lifecycle.py`

Execution Proposal is a contract/object and has no independent
canonical state authority.

Execution Readiness remains distinct from Authorization.

Authorization remains distinct from Execution.

Execution Attempt remains distinct from Task.

Execution Result remains distinct from Task Lifecycle state.

---

# 13. Evidence Phase

The third implementation group establishes canonical organizational
evidence and learning structures.

Modules:

17. `memory.py`
18. `experience.py`
19. `trust.py`
20. `learning.py`

The canonical evidence direction remains:

Execution
    |
    v
Observation
    |
    v
Memory
    |
    v
Experience
    |
    v
Trust / Learning Signals
    |
    v
Future Decisions

Evidence-derived modules must not become execution authorities.

---

# 14. Decision Input Phase

The final implementation group establishes decision authorities that
consume the organizational evidence structures.

Modules:

21. `task_evaluation.py`
22. `agent_selection.py`

Task Evaluation may consume:

- Task;
- Capability;
- Agent;
- Resource State;
- Experience;
- Trust;
- Strategic context.

Agent Selection may consume:

- Task;
- Capability;
- Agent;
- Resource State;
- Experience;
- Trust;
- availability;
- compatibility;
- cost;
- risk;
- reliability.

Neither module may execute work or authorize execution.

---

# 15. Why Evaluation and Selection Are Late in Construction

Task Evaluation and Agent Selection are intentionally placed after
Experience, Trust, and Learning in the implementation sequence.

This does not mean the runtime executes Learning before Evaluation for
every Task.

It means the concrete implementations of the decision authorities are
constructed after the evidence structures they are expected to consume
have stable canonical contracts.

The runtime may invoke these authorities according to the canonical
runtime flow.

Implementation construction order and runtime invocation order are
different dimensions.

---

# 16. Execution Proposal Construction Rule

Execution Proposal appears before Task Evaluation and Agent Selection
in the implementation sequence even though the runtime flow produces
the proposal from the selected execution context.

This is intentional.

The Proposal module defines the canonical representation of:

- Task;
- selected Agent;
- required Capability;
- Resource Requirements;
- Execution Context;
- integration path;
- relevant constraints.

Its implementation must not require concrete imports of the complete
selection or evaluation engines merely to represent those associations.

References should remain contract-safe and identity-based where
appropriate.

---

# 17. Execution Result Construction Rule

Execution Result is implemented before Memory, Experience, Trust, and
Learning.

This establishes the canonical outcome representation before the
evidence authorities consume that outcome.

Execution Result remains evidence about an Attempt.

It does not mutate:

- Task Lifecycle;
- Trust;
- Experience;
- Strategic Decision.

Those mutations remain under their respective canonical authorities.

---

# 18. Task Lifecycle Construction Rule

Task Lifecycle is implemented after Execution Result because results
provide evidence for lifecycle transitions.

The result does not directly perform the transition.

The canonical relationship remains:

Execution Result
    |
    v
Task Lifecycle Authority
    |
    v
Task State Transition

Task Lifecycle Authority remains the sole owner of canonical Task
state transitions.

---

# 19. Memory Construction Rule

Memory is implemented after the canonical execution outcome structures
exist.

Memory stores evidence and organizational knowledge.

Memory does not become:

- a decision authority;
- an execution authority;
- a strategic authority;
- a lifecycle authority.

External persistence systems may implement storage mechanisms through
Integration adapters but do not become the canonical Memory authority.

---

# 20. Experience Construction Rule

Experience consumes evidence from:

- Memory;
- Observation;
- Execution Result;
- historical evidence;
- provenance.

Experience derives structured knowledge.

Experience may influence:

- Task Evaluation;
- Agent Selection;
- planning;
- risk;
- future decisions.

Experience does not execute work.

---

# 21. Trust Construction Rule

Trust consumes relevant evidence including:

- Execution Results;
- Experience;
- Observations;
- historical reliability;
- trends;
- consistency;
- provenance.

Trust updates remain owned by Trust Authority.

An Agent claim of success is not sufficient evidence by itself.

Evidence must be correctly associated with the relevant:

- Agent;
- Capability;
- Task;
- Attempt;
- context.

---

# 22. Learning Construction Rule

Learning consumes:

- Observation;
- Memory;
- Experience;
- Trust Signals;
- Execution Results;
- historical evidence.

Learning produces Learning Signals and improved organizational
knowledge.

Learning must not:

- execute work;
- authorize work;
- bypass Task Lifecycle Authority;
- silently mutate Strategic Decisions;
- redefine canonical semantics.

---

# 23. Forward References and Contract-Safe References

When a semantic relationship crosses implementation boundaries, the
implementation may use architecture-safe mechanisms including:

- canonical identifiers;
- stable value representations;
- explicit contract types;
- forward references;
- protocol-style interfaces where appropriate;
- immutable reference structures.

The selected mechanism must preserve canonical ownership.

Convenience must never create a competing authority.

A reference mechanism must not silently become a second domain model.

---

# 24. Prohibited Implementation Shortcuts

The following are prohibited:

- importing a module solely because its concept is semantically related;
- creating duplicate domain models to break an import cycle;
- moving authority into a convenient utility module;
- allowing persistence models to become canonical models;
- allowing integration models to become canonical models;
- allowing Weft models to become canonical Task or Agent models;
- allowing execution code to mutate canonical organizational state directly;
- allowing a convenience service to become a hidden authority;
- solving an implementation cycle by changing canonical ownership.

---

# 25. Core Dependency Boundary

Every module under `02_core` must remain independent of:

- Weft;
- LLM providers;
- HTTP clients;
- databases;
- external workflow engines;
- external agent platforms;
- cloud providers;
- OS-specific integration mechanisms;
- development tools;
- runtime implementation modules.

Core may define contracts consumed by Runtime and Integrations.

Core must not depend on Runtime or Integrations.

---

# 26. Integration Boundary

External systems follow:

External System
    |
    v
Integration Adapter
    |
    v
Canonical AI Company Contract

Outbound:

Canonical AI Company Contract
    |
    v
Integration Adapter
    |
    v
External Contract

Provider-specific identifiers, state machines, protocols, and formats
remain outside canonical Core semantics.

---

# 27. Runtime Boundary

Runtime composes and operates Core.

Runtime owns:

- dependency construction;
- lifecycle/service composition;
- runtime coordination;
- execution coordination;
- startup;
- shutdown;
- integration selection;
- operational policy application.

Core remains independent of Runtime.

---

# 28. State Ownership Gate

The implementation sequence must preserve the canonical ownership table.

| Canonical State | Owner |
|---|---|
| Company Intent | Intent Authority |
| Company Objectives | Objective Authority |
| Strategic Decisions | Decision Authority |
| Task Definition | Canonical Task Authority |
| Task State | Task Lifecycle Authority |
| Task Queue State | Queue Authority |
| Agent Identity | Agent Authority |
| Capability Semantics | Capability Authority |
| Capability Availability | Capability Authority |
| Hardware Capability Profile | Hardware Capability Authority |
| Hardware Observation | Hardware Observer |
| Resource State | Resource State Authority |
| Task Evaluation | Task Evaluation Authority |
| Agent Selection | Agent Selection Authority |
| Execution Readiness | Readiness Authority |
| Execution Authorization | Authorization Authority |
| Execution Attempt | Execution Authority |
| Execution Result | Execution Result Authority |
| Memory | Memory Authority |
| Experience | Experience Authority |
| Trust | Trust Authority |
| Learning | Learning Authority |

Execution Proposal has no independent canonical state owner.

---

# 29. One Authority Rule

There must be exactly one canonical authority for every mutable
canonical state.

An implementation class may support an authority.

An adapter may translate to or from an authority.

A persistence representation may store authority state.

A cache may project authority state.

None of these automatically become canonical authority.

---

# 30. Runtime Flow vs Construction Sequence

The following distinction is mandatory.

RUNTIME FLOW answers:

"What happens when AI Company operates?"

IMPLEMENTATION SEQUENCE answers:

"In what controlled order do we construct the Core software?"

DEPENDENCY GRAPH answers:

"What semantic and concrete relationships exist?"

These are three different architectural dimensions.

They must not be collapsed into one ordering concept.

---

# 31. Implementation Checkpoint Rule

No Core module is considered implemented merely because its file
exists.

Each module must pass:

1. canonical responsibility check;
2. canonical authority check;
3. contract compliance check;
4. state ownership check;
5. dependency check;
6. forbidden dependency check;
7. failure-mode check;
8. observability check;
9. unit tests;
10. architectural invariant check.

---

# 32. Import Graph Verification

Once implementation begins, the concrete Python import graph must be
audited independently from the semantic graph.

The audit must verify:

- no forbidden Core imports;
- no Core → Runtime imports;
- no Core → Integration imports;
- no Core → Tools imports;
- no unintended circular imports;
- no provider-specific imports;
- no hidden duplicate canonical models;
- no authority transfer caused by imports.

A semantic cycle is not automatically an import cycle.

An import cycle is not automatically acceptable merely because a
semantic relationship exists.

---

# 33. Implementation Order Verification

The implementation-order audit must verify:

- all 22 candidate modules are present in the specification;
- every order value is unique;
- order values are exactly 1 through 22;
- Strategic Decision precedes Task;
- Execution Result precedes Memory;
- Memory precedes Experience;
- Experience precedes Trust;
- Trust precedes Learning;
- Learning precedes Task Evaluation;
- Task Evaluation precedes Agent Selection;
- Execution Proposal has no independent authority;
- no new canonical authority appears.

The audit must not attempt to prove that the complete semantic graph is
a DAG.

That would confuse semantic relationships with concrete imports.

---

# 34. Pre-Implementation Gate

Before creating any file under `02_core`, verify:

- Canonical Architecture hash is unchanged;
- Core Contract Specification hash is unchanged;
- Core Module Derivation hash is unchanged;
- this Implementation Order is internally consistent;
- no competing canonical authority exists;
- concrete dependency rules are defined;
- semantic/reference/import distinction is explicit;
- implementation checkpoints are defined.

If any condition fails:

NO-GO.

---

# 35. Production Implementation Gate

Production Core implementation may begin only after the
pre-implementation gate passes.

The first implementation must not introduce:

- Runtime dependencies;
- Integration dependencies;
- provider dependencies;
- hidden authority;
- duplicate canonical models;
- lifecycle bypass;
- execution bypass;
- strategic mutation;
- trust mutation outside Trust Authority;
- memory mutation outside Memory Authority;
- semantic redefinition.

---

# 36. Verification Gate

After implementation, verify:

- architecture compliance;
- responsibility compliance;
- authority ownership;
- dependency direction;
- import graph;
- canonical model uniqueness;
- lifecycle ownership;
- execution separation;
- result/lifecycle separation;
- resource-state separation;
- readiness/authorization separation;
- authorization/execution separation;
- provenance;
- retry identity;
- cancellation;
- recovery;
- external dependency failure;
- integration boundaries;
- tests.

Verification is a quality gate.

Verification is not a canonical authority.

---

# 37. Architectural Invariants

The implementation must preserve at minimum:

- AI Company owns canonical semantics.
- Core has no Integration dependency.
- Every canonical concept has one authoritative definition.
- Every mutable canonical state has one authoritative owner.
- Task definition is separate from Task state.
- Task state is separate from Execution Result.
- Attempts are separate from Tasks.
- Agent identity is separate from Capability.
- Agent Selection is separate from Execution.
- Strategic Decision is separate from Execution.
- Resource Observation is separate from Resource Decision.
- Hardware capability is separate from current Resource State.
- Readiness is separate from Authorization.
- Authorization is separate from Execution.
- Weft remains external infrastructure.
- External Agents remain behind Integration boundaries.
- Human Agents remain valid organizational participants.
- Memory remains evidence.
- Experience remains evidence.
- Trust remains evidence-grounded.
- Learning consumes outcomes.
- Learning does not directly execute.
- Physical resource constraints remain explicit.
- External dependency failure remains representable.
- Attempts remain traceable.
- Retries preserve Task identity.
- Cancellation preserves canonical ownership.
- Observability does not become state ownership.
- Convenience does not override ownership.
- No competing canonical production path exists.

---

# 38. Final Constitutional Statement

This document is an implementation aid.

It is not a second architecture.

It is not a second responsibility map.

It is not a second authority map.

It is not a replacement for the Core Contract Specification.

It is not a replacement for the Core Module Derivation Specification.

If any statement in this document conflicts with the frozen Canonical
Architecture, the conflict is resolved in favor of the Canonical
Architecture.

ARCHITECTURE WINS.

NO PARALLEL CANONICAL AUTHORITY IS PERMITTED.

NO PRODUCTION CORE IMPLEMENTATION IS AUTHORIZED BY THIS DOCUMENT ALONE.

---

# 39. End of Core Implementation Order
