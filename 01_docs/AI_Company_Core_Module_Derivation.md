# AI Company — Core Module Derivation Specification

**VERSION:** 1.0  
**STATUS:** DERIVED — PRE-IMPLEMENTATION  
**ROLE:** SUBORDINATE ARCHITECTURAL DERIVATION  
**AUTHORITY:** NONE  
**PARENT:** `00_architecture/AI_Company_Canonical_Architecture.md`  
**RELATED:** `01_docs/AI_Company_Canonical_Responsibility_Map.md`  
**RELATED:** `01_docs/AI_Company_Core_Contract_Specification.md`

---

# 1. Purpose

This document derives a candidate production module map for `02_core`.

It does not amend, extend, replace, or reinterpret the Canonical Architecture.

The derivation follows:

CANONICAL ARCHITECTURE
→ CANONICAL RESPONSIBILITY
→ CANONICAL AUTHORITY
→ CANONICAL CONTRACT
→ MODULE
→ IMPLEMENTATION
→ TESTS

No production implementation is authorized merely by the existence of this document.

---

# 2. Architectural Authority

The Canonical Architecture is the constitutional authority.

This document is subordinate to:

`00_architecture/AI_Company_Canonical_Architecture.md`

The Core Contract Specification and this Module Derivation Specification are derived documents.

If any conflict exists:

ARCHITECTURE WINS.

No module may create a second canonical authority.

---

# 3. Core Boundary

`02_core` owns canonical company meaning.

Core must remain semantically valid if:

- Weft is removed;
- LLM providers are removed;
- external agents are removed;
- databases are removed;
- HTTP clients are removed;
- cloud services are removed;
- OS-specific integration mechanisms are removed;
- external workflow engines are removed.

Core must not depend on:

- Weft;
- LLM providers;
- external agent platforms;
- databases;
- HTTP clients;
- cloud providers;
- operating-system integration mechanisms;
- external workflow engines;
- development tools;
- test utilities.

---

# 4. Module Derivation Rules

A proposed module is valid only when its architectural home is obvious.

Every production module must have:

1. Responsibility
2. Canonical Owner
3. Canonical Contract
4. Inputs
5. Outputs
6. Mutable State
7. State Owner
8. Dependencies
9. Forbidden Dependencies
10. Failure Modes
11. Observability
12. Tests
13. Affected Architectural Invariants

A module must not silently acquire responsibilities belonging to another authority.

One canonical authority may be implemented through more than one cohesive module if necessary.

One module must not become a competing owner of another canonical state.

---

# 5. Canonical Authority → Module Map

| # | Canonical Concept | Canonical Authority | Candidate Core Module |
|---|---|---|---|
| 1 | Company Intent | Intent Authority | `intent.py` |
| 2 | Company Objectives | Objective Authority | `objective.py` |
| 3 | Strategic Decisions | Decision Authority | `strategic_decision.py` |
| 4 | Task Definition | Canonical Task Authority | `task.py` |
| 5 | Task State | Task Lifecycle Authority | `task_lifecycle.py` |
| 6 | Task Queue State | Queue Authority | `task_queue.py` |
| 7 | Agent Identity | Agent Authority | `agent.py` |
| 8 | Capability Semantics / Availability | Capability Authority | `capability.py` |
| 9 | Hardware Capability Profile | Hardware Capability Authority | `hardware_capability.py` |
| 10 | Hardware Observation | Hardware Observer | `hardware_observation.py` |
| 11 | Resource State | Resource State Authority | `resource_state.py` |
| 12 | Task Evaluation | Task Evaluation Authority | `task_evaluation.py` |
| 13 | Agent Selection | Agent Selection Authority | `agent_selection.py` |
| 14 | Execution Proposal | No independent authority | `execution_proposal.py` |
| 15 | Execution Readiness | Readiness Authority | `execution_readiness.py` |
| 16 | Execution Authorization | Authorization Authority | `execution_authorization.py` |
| 17 | Execution Attempt | Execution Authority | `execution_attempt.py` |
| 18 | Execution Result | Execution Result Authority | `execution_result.py` |
| 19 | Memory | Memory Authority | `memory.py` |
| 20 | Experience | Experience Authority | `experience.py` |
| 21 | Trust | Trust Authority | `trust.py` |
| 22 | Learning | Learning Authority | `learning.py` |

**Important:** The number of module entries is not a constitutional authority count.

`Execution Proposal` is explicitly not an additional canonical state authority.

The 21 state-owning authorities defined by Architecture §51 remain unchanged.

---

# 6. Intent Module

**Candidate:** `02_core/intent.py`

**Responsibility:** Represent and protect canonical Company Intent semantics.

**Canonical Owner:** Intent Authority.

**Canonical State:** Company Intent.

**State Owner:** Intent Authority.

**Inputs:**
- organizational intent data;
- explicit owner-provided intent changes.

**Outputs:**
- canonical intent representation.

**Dependencies:**
- core value types only;
- explicit domain contracts.

**Forbidden Dependencies:**
- Runtime;
- Integrations;
- Weft;
- external providers;
- Tools.

**Failure Modes:**
- invalid intent;
- structurally incomplete intent;
- invalid mutation request.

**Observability:**
- validation failures;
- provenance of accepted intent changes.

**Tests:**
- intent validity;
- ownership;
- immutability/mutation rules;
- forbidden dependency inspection.

**Invariants:**
- Company owns semantics;
- one canonical authority;
- architecture wins.

---

# 7. Objective Module

**Candidate:** `02_core/objective.py`

**Responsibility:** Own canonical Company Objective semantics.

**Canonical Owner:** Objective Authority.

**Canonical State:** Company Objectives.

**State Owner:** Objective Authority.

**Inputs:**
- Company Intent;
- explicit objective definitions;
- permitted objective updates.

**Outputs:**
- canonical objectives.

**Dependencies:**
- canonical Intent contract;
- core value types.

**Forbidden Dependencies:**
- Runtime;
- Integrations;
- Tools;
- execution systems.

**Failure Modes:**
- invalid objective;
- objective inconsistent with required structure;
- invalid transition/update.

**Observability:**
- objective validation;
- provenance of changes.

**Tests:**
- objective validity;
- objective ≠ execution;
- ownership invariants.

---

# 8. Strategic Decision Module

**Candidate:** `02_core/strategic_decision.py`

**Responsibility:** Transform organizational intent/objectives into strategic direction.

**Canonical Owner:** Decision Authority.

**Canonical State:** Strategic Decisions.

**State Owner:** Decision Authority.

**Inputs:**
- Company Intent;
- Company Objectives;
- strategic context;
- permitted decision inputs.

**Outputs:**
- Strategic Decision.

**Dependencies:**
- canonical Intent;
- canonical Objective;
- core decision contracts.

**Forbidden Dependencies:**
- Execution System;
- Weft;
- external providers;
- Tools.

**Failure Modes:**
- invalid decision;
- insufficient decision context;
- conflicting decision constraints.

**Observability:**
- decision provenance;
- decision inputs;
- decision identity.

**Tests:**
- decision ≠ execution;
- strategic ownership;
- provenance;
- no execution side effects.

---

# 9. Task Module

**Candidate:** `02_core/task.py`

**Responsibility:** Own canonical Task definition.

**Canonical Owner:** Canonical Task Authority.

**Canonical State:** Task Definition.

**State Owner:** Canonical Task Authority.

**Inputs:**
- authorized organizational direction;
- task intent;
- requirements;
- constraints;
- priority;
- metadata.

**Outputs:**
- canonical Task.

**Dependencies:**
- canonical decision/task value contracts.

**Forbidden Dependencies:**
- queue implementation;
- execution;
- lifecycle mutation;
- Weft;
- Integrations;
- Tools.

**Failure Modes:**
- invalid task;
- invalid requirements;
- malformed constraints.

**Observability:**
- Task identity;
- creation provenance;
- validation failures.

**Tests:**
- single canonical Task model;
- immutable intended-work definition;
- Task ≠ Attempt;
- Task ≠ Result;
- Task ≠ Queue State.

---

# 10. Task Lifecycle Module

**Candidate:** `02_core/task_lifecycle.py`

**Responsibility:** Own valid Task lifecycle states and transitions.

**Canonical Owner:** Task Lifecycle Authority.

**Canonical State:** Task State and transition history.

**State Owner:** Task Lifecycle Authority.

**Inputs:**
- Task;
- Execution Results;
- lifecycle transition requests;
- canonical evidence.

**Outputs:**
- validated lifecycle transitions;
- updated canonical Task state.

**Dependencies:**
- canonical Task;
- canonical Execution Result contract.

**Forbidden Dependencies:**
- queue as state authority;
- execution engine;
- Weft;
- agent implementation;
- Tools.

**Failure Modes:**
- invalid transition;
- unknown state;
- terminal-state mutation;
- causality violation.

**Observability:**
- transition identity;
- previous state;
- new state;
- evidence;
- provenance.

**Tests:**
- valid transitions;
- invalid transitions;
- terminal states;
- result → lifecycle transition;
- no direct queue/executor mutation.

---

# 11. Task Queue Module

**Candidate:** `02_core/task_queue.py`

**Responsibility:** Own pending-work ordering and retrieval semantics.

**Canonical Owner:** Queue Authority.

**Canonical State:** Task Queue State.

**State Owner:** Queue Authority.

**Inputs:**
- canonical Tasks;
- queue insertion/retrieval requests.

**Outputs:**
- ordered pending Tasks;
- queue state information.

**Dependencies:**
- canonical Task contract.

**Forbidden Dependencies:**
- Task lifecycle authority;
- execution;
- authorization;
- strategic decision making;
- agent selection.

**Failure Modes:**
- invalid queue entry;
- duplicate queue state;
- retrieval failure;
- ordering violation.

**Observability:**
- queue operation;
- Task identity;
- ordering;
- provenance.

**Tests:**
- queue state ≠ Task state;
- queue does not execute;
- queue does not authorize;
- queue does not mutate lifecycle directly.

---

# 12. Agent Module

**Candidate:** `02_core/agent.py`

**Responsibility:** Own canonical Agent identity and organizational execution-participant semantics.

**Canonical Owner:** Agent Authority.

**Canonical State:** Agent Identity.

**State Owner:** Agent Authority.

**Inputs:**
- Agent definitions;
- organizational role;
- capability references;
- availability information.

**Outputs:**
- canonical Agent.

**Dependencies:**
- Capability contract where required;
- core value types.

**Forbidden Dependencies:**
- provider-specific identity;
- Weft;
- external agent APIs;
- execution implementation.

**Failure Modes:**
- invalid Agent identity;
- duplicate identity;
- invalid role/definition.

**Observability:**
- Agent identity;
- provenance;
- availability-related evidence.

**Tests:**
- Agent ≠ Capability;
- Agent ≠ Task;
- Agent ≠ execution implementation;
- human and AI Agents remain valid under common model.

---

# 13. Capability Module

**Candidate:** `02_core/capability.py`

**Responsibility:** Own canonical Capability semantics and availability semantics.

**Canonical Owner:** Capability Authority.

**Canonical State:** Capability Semantics and Capability Availability.

**State Owner:** Capability Authority.

**Inputs:**
- capability definitions;
- relevant availability evidence;
- environmental constraints.

**Outputs:**
- canonical Capability;
- canonical availability state.

**Dependencies:**
- core Agent/Resource contracts where explicitly required.

**Forbidden Dependencies:**
- execution;
- scheduling;
- strategic decisions;
- provider-specific capability semantics.

**Failure Modes:**
- invalid capability;
- inconsistent availability;
- unsupported capability state.

**Observability:**
- capability identity;
- availability evidence;
- provenance.

**Tests:**
- capability ≠ execution;
- capability ≠ Agent;
- availability does not authorize execution.

---

# 14. Hardware Capability Module

**Candidate:** `02_core/hardware_capability.py`

**Responsibility:** Represent stable physical/environmental capability.

**Canonical Owner:** Hardware Capability Authority.

**Canonical State:** Hardware Capability Profile.

**State Owner:** Hardware Capability Authority.

**Inputs:**
- validated hardware profile observations.

**Outputs:**
- canonical Hardware Capability Profile.

**Dependencies:**
- core value types;
- explicit observation contract.

**Forbidden Dependencies:**
- OS-specific probing code;
- hardware vendor SDKs;
- Runtime;
- Integrations.

**Failure Modes:**
- invalid profile;
- incomplete capability data;
- inconsistent hardware identity.

**Observability:**
- profile provenance;
- profile identity;
- validation failures.

**Tests:**
- stable capability ≠ current observation;
- hardware profile remains provider-independent.

---

# 15. Hardware Observation Module

**Candidate:** `02_core/hardware_observation.py`

**Responsibility:** Represent canonical physical observations.

**Canonical Owner:** Hardware Observer.

**Canonical State:** Hardware Observation.

**State Owner:** Hardware Observer.

**Inputs:**
- observations supplied through the explicit observation contract.

**Outputs:**
- canonical Hardware Observation.

**Dependencies:**
- Hardware Capability contract;
- core observation types.

**Forbidden Dependencies:**
- direct OS/hardware probing implementation;
- Runtime integration logic;
- execution decisions.

**Failure Modes:**
- unavailable observation;
- stale observation;
- malformed observation;
- incomplete observation.

**Observability:**
- timestamp;
- source;
- observation identity;
- provenance.

**Tests:**
- observation is descriptive;
- observation does not decide;
- observation does not authorize;
- observation does not execute.

**Boundary Note:**

The physical hardware observer implementation belongs behind the integration boundary.

The canonical observation contract belongs in Core.

---

# 16. Resource State Module

**Candidate:** `02_core/resource_state.py`

**Responsibility:** Represent currently usable finite resource capacity.

**Canonical Owner:** Resource State Authority.

**Canonical State:** Resource State.

**State Owner:** Resource State Authority.

**Inputs:**
- Hardware Capability Profile;
- Hardware Observation;
- interpretation rules;
- resource constraints.

**Outputs:**
- canonical Resource State.

**Dependencies:**
- hardware capability;
- hardware observation;
- resource value contracts.

**Forbidden Dependencies:**
- agent selection;
- execution authorization;
- strategic decisions;
- provider-specific resource APIs.

**Failure Modes:**
- insufficient data;
- inconsistent resource state;
- unavailable capacity;
- invalid resource interpretation.

**Observability:**
- resource snapshot identity;
- timestamp;
- source observations;
- derived availability.

**Tests:**
- finite resource principle;
- capability ≠ current availability;
- resource state ≠ selection;
- resource state ≠ authorization.

---

# 17. Task Evaluation Module

**Candidate:** `02_core/task_evaluation.py`

**Responsibility:** Determine suitability of a Task under current organizational and physical context.

**Canonical Owner:** Task Evaluation Authority.

**Canonical State:** Task Evaluation.

**State Owner:** Task Evaluation Authority.

**Inputs:**
- Task;
- requirements;
- constraints;
- capabilities;
- resource state;
- available agents;
- experience;
- trust;
- risk/cost/environment context.

**Outputs:**
- Task Evaluation.

**Dependencies:**
- canonical Task;
- Capability;
- Resource State;
- Agent;
- Experience;
- Trust.

**Forbidden Dependencies:**
- execution;
- authorization;
- strategic decision replacement;
- provider-specific implementation.

**Failure Modes:**
- insufficient evaluation context;
- resource mismatch;
- capability mismatch;
- invalid evaluation.

**Observability:**
- evaluation inputs;
- score/reason;
- evidence;
- provenance.

**Tests:**
- evaluation ≠ execution;
- evaluation ≠ authorization;
- finite-resource constraints;
- traceability.

---

# 18. Agent Selection Module

**Candidate:** `02_core/agent_selection.py`

**Responsibility:** Determine the appropriate Agent for a Task under the canonical selection criteria.

**Canonical Owner:** Agent Selection Authority.

**Canonical State:** Agent Selection.

**State Owner:** Agent Selection Authority.

**Inputs:**
- Task;
- Capability;
- availability;
- Resource State;
- experience;
- trust;
- cost/risk/reliability context.

**Outputs:**
- canonical Agent Selection.

**Dependencies:**
- Agent;
- Capability;
- Resource State;
- Experience;
- Trust;
- Task Evaluation where explicitly required.

**Forbidden Dependencies:**
- Execution System;
- authorization;
- direct provider execution;
- Weft.

**Failure Modes:**
- no suitable Agent;
- insufficient evidence;
- unavailable resources;
- selection conflict.

**Observability:**
- candidate set;
- selection rationale;
- scores/evidence;
- provenance.

**Tests:**
- one canonical selection authority;
- selection ≠ execution;
- selection ≠ authorization.

---

# 19. Execution Proposal Module

**Candidate:** `02_core/execution_proposal.py`

**Responsibility:** Represent the concrete proposed execution associating the relevant canonical entities.

**Canonical Owner:** No independent canonical authority.

**Canonical State:** No independent canonical state ownership.

**Inputs:**
- Task;
- selected Agent;
- required Capability;
- Resource Requirements;
- Execution Context;
- integration path;
- constraints.

**Outputs:**
- Execution Proposal.

**Dependencies:**
- Task;
- Agent;
- Capability;
- Resource Requirements;
- Execution Context.

**Forbidden Dependencies:**
- creation of a new canonical authority;
- lifecycle ownership;
- authorization ownership;
- execution ownership;
- provider-specific semantic authority.

**Failure Modes:**
- incomplete proposal;
- inconsistent Task/Agent/Capability association;
- incompatible requirements.

**Observability:**
- proposal identity;
- Task identity;
- Agent identity;
- Capability identity;
- correlation/provenance.

**Tests:**
- proposal ≠ Task;
- proposal ≠ Authorization;
- proposal ≠ Attempt;
- proposal ≠ Result;
- no independent canonical state owner;
- no independent authority.

**Architectural Constraint:**

Architecture §51 does not define an Execution Proposal Authority.

Therefore this module must remain a value/contract representation inside the execution flow and must not become a canonical state authority.

---

# 20. Execution Readiness Module

**Candidate:** `02_core/execution_readiness.py`

**Responsibility:** Determine whether a proposed execution is currently possible.

**Canonical Owner:** Readiness Authority.

**Canonical State:** Execution Readiness.

**State Owner:** Readiness Authority.

**Inputs:**
- Execution Proposal;
- Task;
- Agent;
- Capability;
- Resource State;
- availability;
- constraints;
- integration availability;
- operational conditions.

**Outputs:**
- READY;
- DEGRADED;
- BLOCKED;
- UNAVAILABLE.

**Dependencies:**
- Execution Proposal;
- Resource State;
- Agent;
- Capability;
- integration availability contract.

**Forbidden Dependencies:**
- authorization;
- execution;
- strategic decision;
- direct provider invocation.

**Failure Modes:**
- unavailable resource;
- unavailable integration;
- unsatisfied requirement;
- degraded operational condition.

**Observability:**
- readiness decision;
- blocking reason;
- resource context;
- evidence.

**Tests:**
- READY ≠ AUTHORIZED;
- readiness ≠ execution;
- blocked is valid;
- finite resources respected.

---

# 21. Execution Authorization Module

**Candidate:** `02_core/execution_authorization.py`

**Responsibility:** Explicitly authorize a specific proposed execution.

**Canonical Owner:** Authorization Authority.

**Canonical State:** Execution Authorization.

**State Owner:** Authorization Authority.

**Inputs:**
- Execution Proposal;
- readiness;
- authorization conditions;
- permitted organizational decision.

**Outputs:**
- bounded Execution Authorization.

**Dependencies:**
- Execution Proposal;
- Execution Readiness;
- required authorization inputs.

**Forbidden Dependencies:**
- execution;
- task lifecycle ownership;
- strategic decision replacement;
- silent authorization.

**Failure Modes:**
- missing authorization;
- invalid scope;
- expired authorization;
- readiness failure;
- constraint violation.

**Observability:**
- authorization identity;
- proposal identity;
- bounds;
- conditions;
- provenance.

**Tests:**
- readiness ≠ authorization;
- authorization ≠ execution;
- authorization must be bounded;
- no unrelated work authorization.

---

# 22. Execution Attempt Module

**Candidate:** `02_core/execution_attempt.py`

**Responsibility:** Own identity and canonical representation of one execution attempt.

**Canonical Owner:** Execution Authority.

**Canonical State:** Execution Attempt.

**State Owner:** Execution Authority.

**Inputs:**
- Execution Authorization;
- Execution Proposal;
- retry/cancellation/idempotency context.

**Outputs:**
- Execution Attempt.

**Dependencies:**
- Authorization;
- Proposal;
- canonical Task identity.

**Forbidden Dependencies:**
- strategic decision;
- Task definition mutation;
- lifecycle mutation;
- provider-specific state authority.

**Failure Modes:**
- duplicate attempt;
- invalid authorization;
- cancellation;
- retry conflict;
- idempotency conflict.

**Observability:**
- attempt identity;
- authorization identity;
- Task identity;
- timestamps;
- correlation IDs.

**Tests:**
- multiple Attempts per Task;
- retry preserves Task identity;
- attempt ≠ Task;
- attempt ≠ Result.

---

# 23. Execution Result Module

**Candidate:** `02_core/execution_result.py`

**Responsibility:** Represent the canonical outcome of an Execution Attempt.

**Canonical Owner:** Execution Result Authority.

**Canonical State:** Execution Result.

**State Owner:** Execution Result Authority.

**Inputs:**
- Execution Attempt;
- observations;
- executor outcome;
- provenance.

**Outputs:**
- SUCCESS;
- FAILED;
- BLOCKED;
- UNAVAILABLE;
- DEGRADED;
- CANCELLED.

**Dependencies:**
- Execution Attempt;
- Observation;
- provenance contracts.

**Forbidden Dependencies:**
- direct Task lifecycle mutation;
- authorization;
- strategic decision;
- trust mutation;
- experience mutation.

**Failure Modes:**
- malformed result;
- missing provenance;
- inconsistent attempt association.

**Observability:**
- outcome;
- Attempt;
- Task;
- Agent;
- Capability;
- context;
- provider/correlation IDs where applicable.

**Tests:**
- Result ≠ Task State;
- Result does not mutate lifecycle directly;
- one terminal result per Attempt;
- provenance completeness.

---

# 24. Memory Module

**Candidate:** `02_core/memory.py`

**Responsibility:** Own canonical evidence storage semantics.

**Canonical Owner:** Memory Authority.

**Canonical State:** Memory Records.

**State Owner:** Memory Authority.

**Inputs:**
- observations;
- execution history;
- outcomes;
- decisions/context;
- historical organizational records;
- provenance.

**Outputs:**
- canonical Memory Records;
- evidence retrieval.

**Dependencies:**
- canonical evidence contracts.

**Forbidden Dependencies:**
- automatic decision authority;
- execution;
- trust mutation;
- provider-specific storage semantics.

**Failure Modes:**
- invalid record;
- missing provenance;
- storage/consistency failure at contract level.

**Observability:**
- record identity;
- source;
- timestamp;
- provenance;
- correlation.

**Tests:**
- memory is evidence;
- memory does not automatically decide;
- provenance discipline;
- one canonical memory authority.

---

# 25. Experience Module

**Candidate:** `02_core/experience.py`

**Responsibility:** Derive structured knowledge from execution/outcome evidence.

**Canonical Owner:** Experience Authority.

**Canonical State:** Experience Records.

**State Owner:** Experience Authority.

**Inputs:**
- Memory;
- Execution Results;
- observations;
- historical execution evidence.

**Outputs:**
- Experience Records;
- derived experience signals.

**Dependencies:**
- Memory;
- Execution Result;
- Observation.

**Forbidden Dependencies:**
- direct execution;
- authorization;
- arbitrary trust mutation;
- strategic decision replacement.

**Failure Modes:**
- insufficient evidence;
- inconsistent evidence;
- invalid derivation.

**Observability:**
- evidence references;
- derivation rule;
- confidence;
- provenance.

**Tests:**
- experience is evidence;
- experience does not execute;
- experience derivation is traceable.

---

# 26. Trust Module

**Candidate:** `02_core/trust.py`

**Responsibility:** Own canonical trust state and evidence-grounded trust updates.

**Canonical Owner:** Trust Authority.

**Canonical State:** Trust Records.

**State Owner:** Trust Authority.

**Inputs:**
- relevant evidence;
- Execution Results;
- Experience;
- reliability/trend evidence;
- scoped Agent/Capability context.

**Outputs:**
- Trust Records;
- trust signals.

**Dependencies:**
- Memory;
- Experience;
- Execution Result;
- Agent;
- Capability.

**Forbidden Dependencies:**
- arbitrary executor mutation;
- ungrounded trust increase;
- direct execution;
- provider-specific trust authority.

**Failure Modes:**
- insufficient evidence;
- wrong Agent association;
- wrong Capability association;
- provenance failure;
- conflicting evidence.

**Observability:**
- trust scope;
- evidence references;
- update reason;
- timestamp;
- confidence.

**Tests:**
- trust is evidence-grounded;
- Agent+Capability scoping;
- executor cannot arbitrarily mutate trust;
- provenance preserved;
- one Trust Authority.

---

# 27. Learning Module

**Candidate:** `02_core/learning.py`

**Responsibility:** Own canonical learning signals derived from outcomes and evidence.

**Canonical Owner:** Learning Authority.

**Canonical State:** Learning Signals.

**State Owner:** Learning Authority.

**Inputs:**
- Execution Results;
- Observations;
- Memory;
- Experience;
- Trust signals.

**Outputs:**
- Learning Signals;
- improved knowledge for future decisions.

**Dependencies:**
- Memory;
- Experience;
- Trust;
- Execution Result;
- Observation.

**Forbidden Dependencies:**
- direct execution;
- silent strategy mutation;
- authorization;
- lifecycle bypass.

**Failure Modes:**
- insufficient evidence;
- contradictory evidence;
- invalid learning derivation.

**Observability:**
- learning signal identity;
- evidence;
- derivation;
- confidence;
- provenance.

**Tests:**
- learning consumes outcomes;
- learning does not execute;
- learning does not silently mutate strategy;
- evidence traceability.

---

# 28. Cross-Module Dependency Rules

The following are canonical semantic relationships.

## 28.1 Intent → Objective

Objectives may use canonical Intent.

Objective authority remains distinct.

## 28.2 Objective → Strategic Decision

Strategic Decisions may use Objectives and Intent.

Decision authority remains distinct.

## 28.3 Strategic Decision → Task

Strategic direction may result in canonical Tasks.

Task authority remains distinct.

## 28.4 Task → Evaluation

Tasks are evaluated under current context.

Evaluation does not mutate Task meaning.

## 28.5 Evaluation → Agent Selection

Evaluation evidence may inform Agent Selection.

Selection remains separate.

## 28.6 Agent + Capability + Resource State → Execution Proposal

A proposal associates canonical entities.

The proposal introduces no new authority.

## 28.7 Proposal → Readiness

Readiness determines current possibility.

READY does not authorize.

## 28.8 Readiness → Authorization

Authorization is separate and explicit.

## 28.9 Authorization → Attempt

An authorized proposal may produce an Execution Attempt.

## 28.10 Attempt → Result

Each Attempt produces an Execution Result.

## 28.11 Result → Lifecycle

Execution Result provides evidence.

Task Lifecycle Authority performs the canonical state transition.

The Result must not directly own Task state.

## 28.12 Outcome → Memory / Experience / Trust / Learning

Execution evidence feeds canonical learning structures.

None of these may bypass their respective authorities.

---

# 29. Hardware and Resource Boundary

The Core semantic chain is:

Hardware Capability Profile
+
Hardware Observation
→
Resource State
→
Task Evaluation / Agent Selection / Readiness

The following distinctions are mandatory:

- Hardware Capability ≠ Hardware Observation
- Hardware Observation ≠ Resource State
- Resource State ≠ Agent Selection
- Resource State ≠ Authorization
- Resource State ≠ Execution

Physical resource constraints may block execution.

Finite resource capacity must never be treated as infinite.

---

# 30. Integration Boundary

Core defines canonical contracts.

Integration implementations live outside Core.

Examples include:

- physical hardware observers;
- Weft adapters;
- LLM providers;
- external agents;
- databases;
- filesystems;
- communications;
- OS interfaces;
- external APIs.

The required direction is:

External System
→ Integration Adapter
→ Canonical Core Contract

and:

Canonical Core Contract
→ Integration Adapter
→ External System

No external provider representation becomes canonical merely because it is persistent or widely used.

---

# 31. Runtime Boundary

Runtime composes and operates Core.

Runtime may depend on Core.

Core must not depend on Runtime.

Runtime owns:

- dependency construction;
- service composition;
- lifecycle coordination;
- execution coordination;
- startup/shutdown;
- runtime configuration.

Core modules must receive dependencies through explicit contracts.

Core modules must not construct Runtime or Integration dependencies directly.

---

# 32. Proposed Core Package Shape

The following is a candidate physical organization only.

It is not itself a new architectural authority.

```text
02_core/
├── intent.py
├── objective.py
├── strategic_decision.py
├── task.py
├── task_lifecycle.py
├── task_queue.py
├── agent.py
├── capability.py
├── hardware_capability.py
├── hardware_observation.py
├── resource_state.py
├── task_evaluation.py
├── agent_selection.py
├── execution_proposal.py
├── execution_readiness.py
├── execution_authorization.py
├── execution_attempt.py
├── execution_result.py
├── memory.py
├── experience.py
├── trust.py
└── learning.py
This layout is subject to implementation review.
A cohesive module may contain multiple related value objects where doing so does not collapse canonical ownership.
A single authority must remain identifiable even when implemented across multiple files.

---

# 33. What This Specification Does Not Authorize
This document does not authorize:
production implementation;
dependency construction;
integration implementation;
Runtime implementation;
Weft integration;
external agent integration;
database integration;
hardware probing;
automatic strategy generation;
autonomous architecture modification;
new canonical authorities;
alternate Task models;
alternate lifecycle authorities;
alternate selection authorities;
alternate trust authorities.

---

# 34. Implementation Gate
Before creating each production module, verify:
Architecture section identified.
Responsibility identified.
Canonical Authority identified.
Canonical Contract identified.
State ownership identified.
Inputs identified.
Outputs identified.
Dependencies identified.
Forbidden dependencies identified.
Failure modes identified.
Observability identified.
Tests identified.
Architectural invariants identified.
No competing canonical authority introduced.
No integration dependency enters Core.
No implementation convenience overrides ownership.
Only after these checks may implementation begin.

---

# 35. Verification Gate
The module derivation must be verified through:
authority coverage;
authority uniqueness;
state-owner uniqueness;
module ownership consistency;
dependency-direction inspection;
forbidden dependency inspection;
Execution Proposal authority check;
Task/Lifecycle/Queue separation;
Agent/Capability separation;
Hardware Capability/Observation separation;
Resource State separation;
Readiness/Authorization separation;
Authorization/Execution separation;
Attempt/Result separation;
Result/Lifecycle separation;
Memory/Experience/Trust/Learning separation;
integration-boundary inspection.

---

# 36. Canonical Authority Coverage
The following 21 state-owning authorities from Architecture §51 must remain covered:
Intent Authority
Objective Authority
Decision Authority
Canonical Task Authority
Task Lifecycle Authority
Queue Authority
Agent Authority
Capability Authority
Hardware Capability Authority
Hardware Observer
Resource State Authority
Task Evaluation Authority
Agent Selection Authority
Readiness Authority
Authorization Authority
Execution Authority
Execution Result Authority
Memory Authority
Experience Authority
Trust Authority
Learning Authority
Execution Proposal is intentionally excluded from this authority count.

---

# 37. Final Architectural Position
The Core implementation must emerge from the canonical architecture.
The implementation must never be used to redefine the architecture.
The correct direction is:
ARCHITECTURE
→ RESPONSIBILITY
→ AUTHORITY
→ CONTRACT
→ MODULE
→ IMPLEMENTATION
→ TEST
The reverse direction is forbidden.
ARCHITECTURE WINS.
NO PARALLEL CANONICAL AUTHORITY IS PERMITTED.
