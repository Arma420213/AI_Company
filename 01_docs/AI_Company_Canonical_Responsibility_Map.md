# AI Company — Canonical Responsibility & Authority Map

**Status:** DERIVED DOCUMENTATION  
**Authority:** `00_architecture/AI_Company_Canonical_Architecture.md`  
**Architecture Version:** 1.0  
**Architecture Status:** FROZEN  
**Purpose:** Explicitly map canonical responsibilities, authorities, contracts, state ownership, dependencies, and architectural homes.

---

# 1. Purpose

This document is a derived map of the responsibilities and authorities defined by the
AI Company Canonical Architecture.

It does not amend, replace, extend, or reinterpret the canonical architecture.

The canonical architecture remains the sole constitutional authority.

If this document conflicts with the canonical architecture:

**THE CANONICAL ARCHITECTURE WINS.**

This map exists to make ownership and responsibility explicit before production
implementation begins.

---

# 2. Authority Hierarchy

The architectural authority chain is:

1. `00_architecture/AI_Company_Canonical_Architecture.md`
2. Canonical responsibility and authority definitions
3. Canonical contracts
4. Production modules
5. Implementations
6. Tests and verification

Tests verify implementation against the architecture.

Tests do not define architecture.

Documentation explains the architecture.

Documentation does not become a second architectural authority.

---

# 3. Architectural Homes

| Architectural Home | Primary Responsibility |
|---|---|
| `00_architecture` | Constitutional architecture |
| `01_docs` | Derived documentation and explanatory material |
| `02_core` | Canonical company meaning and domain authorities |
| `03_runtime` | Runtime composition and operation |
| `04_integrations` | External-system adapters |
| `05_tests` | Verification |
| `06_tools` | Development and diagnostic utilities |
| `07_examples` | Examples and demonstrations |

Directory placement is an architectural boundary.

---

# 4. Canonical Responsibility Map

## 4.1 Company Intent

**Canonical Authority:** Intent Authority

**Canonical Responsibility:** Own the meaning of Company Intent.

**State Owned:** Company Intent

**State Owner:** Intent Authority

**Inputs:**
- Human Owner direction
- organizational context

**Outputs:**
- canonical Company Intent

**Dependencies:**
- canonical organizational inputs

**Forbidden Dependencies:**
- execution systems
- external workflow engines
- provider-specific semantics

**Failure Modes:**
- invalid or incomplete intent
- unavailable required organizational information

**Observability:**
- provenance
- identity
- timestamp
- state changes where applicable

**Required Tests:**
- ownership
- canonical representation
- invalid-input handling
- dependency isolation

**Architectural Home:** `02_core`

---

## 4.2 Company Objectives

**Canonical Authority:** Objective Authority

**Canonical Responsibility:** Own Company Objective semantics.

**State Owned:** Company Objectives

**State Owner:** Objective Authority

**Inputs:**
- Company Intent
- organizational context

**Outputs:**
- canonical Company Objectives

**Dependencies:**
- Intent Authority

**Forbidden Dependencies:**
- execution systems
- workflow engines
- external providers

**Failure Modes:**
- invalid objective
- inconsistent objective definition

**Observability:**
- objective identity
- provenance
- timestamps
- relationship to intent

**Required Tests:**
- objective ownership
- canonical definition
- separation from execution
- invalid-input handling

**Architectural Home:** `02_core`

---

## 4.3 Strategic Decisions

**Canonical Authority:** Decision Authority

**Canonical Responsibility:** Transform organizational intent and objectives into
strategic direction.

**State Owned:** Strategic Decisions

**State Owner:** Decision Authority

**Inputs:**
- Company Intent
- Company Objectives
- strategic context
- evidence

**Outputs:**
- Strategic Decision

**Dependencies:**
- canonical organizational meaning
- evidence supplied through canonical contracts

**Forbidden Dependencies:**
- direct execution
- execution authorization
- workflow-engine ownership

**Failure Modes:**
- insufficient information
- invalid decision context

**Observability:**
- decision identity
- provenance
- rationale/evidence where defined
- timestamp

**Required Tests:**
- decision/execution separation
- ownership
- provenance
- contract validation

**Architectural Home:** `02_core`

---

## 4.4 Canonical Task Definition

**Canonical Authority:** Canonical Task Authority

**Canonical Responsibility:** Own exactly one canonical Task model.

**State Owned:** Task Definition

**State Owner:** Canonical Task Authority

**Inputs:**
- strategic direction
- task intent
- requirements
- constraints
- priority
- metadata

**Outputs:**
- canonical Task

**Dependencies:**
- canonical organizational semantics

**Forbidden Dependencies:**
- external task representations as canonical authority
- workflow-engine task semantics
- execution-attempt state
- result state

**Failure Modes:**
- invalid task definition
- missing required task identity
- inconsistent requirements or constraints

**Observability:**
- Task identity
- provenance
- creation context
- immutable task-definition history where applicable

**Required Tests:**
- exactly one canonical Task model
- Task identity
- Task-definition separation
- external representation isolation

**Architectural Home:** `02_core`

---

## 4.5 Task Lifecycle

**Canonical Authority:** Task Lifecycle Authority

**Canonical Responsibility:** Own valid Task states, transitions, terminal states,
history, consistency, and causality.

**State Owned:** Task State

**State Owner:** Task Lifecycle Authority

**Inputs:**
- canonical Task
- execution evidence
- lifecycle transition requests through explicit contracts

**Outputs:**
- canonical Task State
- lifecycle transition history

**Dependencies:**
- Canonical Task Authority
- canonical Execution Results where applicable

**Forbidden Dependencies:**
- Queue Authority directly mutating Task State
- Agent directly mutating Task State
- Integration directly mutating Task State
- Execution Pipeline directly mutating Task State
- Weft directly mutating Task State

**Failure Modes:**
- invalid transition
- inconsistent state
- missing causal evidence
- illegal terminal transition

**Observability:**
- Task identity
- previous state
- next state
- transition cause
- evidence/provenance
- timestamp

**Required Tests:**
- valid transitions
- invalid transitions
- terminal-state protection
- causality
- ownership
- external mutation prevention

**Architectural Home:** `02_core`

---

## 4.6 Task Queue

**Canonical Authority:** Queue Authority

**Canonical Responsibility:** Own pending-work ordering and retrieval.

**State Owned:** Task Queue State

**State Owner:** Queue Authority

**Inputs:**
- canonical Tasks eligible for queueing

**Outputs:**
- pending-work ordering
- queue retrieval

**Dependencies:**
- Canonical Task contract

**Forbidden Dependencies:**
- redefining Tasks
- executing Tasks
- authorizing execution
- changing Task Lifecycle State
- strategic decision making

**Failure Modes:**
- queue inconsistency
- ordering failure
- unavailable queue infrastructure

**Observability:**
- queue identity
- Task identity
- enqueue/dequeue events
- ordering/provenance

**Required Tests:**
- queue/Task-state separation
- ordering
- retrieval
- duplicate handling
- ownership isolation

**Architectural Home:** `02_core` / runtime composition as appropriate

---

## 4.7 Agent Identity

**Canonical Authority:** Agent Authority

**Canonical Responsibility:** Own canonical Agent identity and organizational meaning.

**State Owned:** Agent Identity

**State Owner:** Agent Authority

**Inputs:**
- agent registration information
- organizational role
- capability information through canonical contracts
- availability information through canonical contracts

**Outputs:**
- canonical Agent

**Dependencies:**
- canonical Agent-related contracts

**Forbidden Dependencies:**
- provider-specific agent identity becoming canonical
- Capability Authority semantics
- Execution System implementation ownership

**Failure Modes:**
- invalid identity
- duplicate identity
- unavailable registration information

**Observability:**
- Agent identity
- provenance
- registration/update events

**Required Tests:**
- identity uniqueness
- Agent/Capability separation
- external-agent adapter isolation
- human-agent validity

**Architectural Home:** `02_core`

---

## 4.8 Capability Semantics and Availability

**Canonical Authority:** Capability Authority

**Canonical Responsibility:** Own what a Capability means and its canonical availability.

**State Owned:**
- Capability Semantics
- Capability Availability

**State Owner:** Capability Authority

**Inputs:**
- canonical capability definitions
- agent/service/resource/environment evidence

**Outputs:**
- canonical Capability
- capability availability

**Dependencies:**
- canonical evidence and relevant authorities

**Forbidden Dependencies:**
- executing work
- scheduling work
- authorization
- strategic decisions

**Failure Modes:**
- invalid capability definition
- unavailable capability
- inconsistent availability evidence

**Observability:**
- capability identity
- availability state
- evidence/provenance
- timestamp

**Required Tests:**
- Capability/Agent separation
- availability semantics
- no execution ownership
- no authorization ownership

**Architectural Home:** `02_core`

---

## 4.9 Hardware Capability Profile

**Canonical Authority:** Hardware Capability Authority

**Canonical Responsibility:** Own stable physical capability information.

**State Owned:** Hardware Capability Profile

**State Owner:** Hardware Capability Authority

**Inputs:**
- physical/system capability discovery

**Outputs:**
- CPU topology/count
- instruction capabilities
- RAM capacity
- GPU presence/identity/memory
- storage
- OS/environment capability information

**Dependencies:**
- Hardware observation/integration contracts where required

**Forbidden Dependencies:**
- strategic decisions
- Agent Selection
- execution authorization
- direct execution

**Failure Modes:**
- unavailable hardware information
- unsupported environment
- incomplete capability discovery

**Observability:**
- source
- timestamp
- environment identity
- discovery provenance

**Required Tests:**
- stable-vs-current distinction
- canonical ownership
- provider/OS adapter isolation

**Architectural Home:** `02_core`

---

## 4.10 Hardware Observation

**Canonical Authority:** Hardware Observer

**Canonical Responsibility:** Observe actual physical/system conditions.

**State Owned:** Hardware Observation

**State Owner:** Hardware Observer

**Inputs:**
- OS/system/hardware observations

**Outputs:**
- CPU observations
- RAM observations
- GPU observations
- storage observations
- pressure/process observations
- OS/runtime observations

**Dependencies:**
- hardware/OS integration adapters

**Forbidden Dependencies:**
- agent selection
- strategic decision making
- execution authorization
- execution
- resource policy ownership

**Failure Modes:**
- observation unavailable
- partial observation
- stale observation
- unsupported platform

**Observability:**
- observation timestamp
- source
- measurement context
- provenance

**Required Tests:**
- observation/state separation
- source provenance
- stale observation handling
- integration isolation

**Architectural Home:** `02_core` with observation implementations/adapters in
`04_integrations`

---

## 4.11 Resource State

**Canonical Authority:** Resource State Authority

**Canonical Responsibility:** Derive currently usable resource capacity from
Hardware Capability Profile, Hardware Observation, and interpretation rules.

**State Owned:** Resource State

**State Owner:** Resource State Authority

**Inputs:**
- Hardware Capability Profile
- Hardware Observation
- resource interpretation rules
- network/environment conditions
- reservations/contention where applicable

**Outputs:**
- available CPU
- available RAM
- available GPU
- available storage
- network availability
- pressure
- reservations/contention
- execution capacity
- limitations

**Dependencies:**
- Hardware Capability Authority
- Hardware Observer
- canonical resource interpretation rules

**Forbidden Dependencies:**
- Agent Selection
- strategic decisions
- execution authorization
- execution

**Failure Modes:**
- insufficient resource information
- inconsistent observations
- unavailable resource state
- stale state

**Observability:**
- source observations
- derivation timestamp
- resource values
- limitations
- provenance

**Required Tests:**
- finite-resource principle
- capability/observation/state separation
- stale observation behavior
- resource insufficiency
- GPU/resource handling

**Architectural Home:** `02_core`

---

## 4.12 Task Evaluation

**Canonical Authority:** Task Evaluation Authority

**Canonical Responsibility:** Determine task suitability under the current context.

**State Owned:** Task Evaluation

**State Owner:** Task Evaluation Authority

**Inputs:**
- Task
- Task Requirements
- Task Constraints
- Priority
- Capabilities
- Resources
- Agents
- Experience
- Trust
- Risk
- Cost
- Environment

**Outputs:**
- Task Evaluation

**Dependencies:**
- canonical authorities supplying evaluation inputs

**Forbidden Dependencies:**
- execution
- authorization
- strategic decision ownership
- replacing Agent Selection

**Failure Modes:**
- incomplete evaluation context
- unavailable evidence
- inconsistent requirements

**Observability:**
- evaluation inputs
- scoring/rationale where applicable
- provenance
- timestamp

**Required Tests:**
- requirement handling
- resource constraints
- separation from authorization
- separation from execution
- evidence provenance

**Architectural Home:** `02_core`

---

## 4.13 Agent Selection

**Canonical Authority:** Agent Selection Authority

**Canonical Responsibility:** Determine the appropriate Agent for a Task.

**State Owned:** Agent Selection

**State Owner:** Agent Selection Authority

**Inputs:**
- Task
- capability fit
- Agent availability
- resource compatibility
- experience
- trust
- cost
- risk
- reliability

**Outputs:**
- selected Agent
- selection evidence/rationale

**Dependencies:**
- Agent Authority
- Capability Authority
- Resource State Authority
- Experience Authority
- Trust Authority
- Task Evaluation where applicable

**Forbidden Dependencies:**
- execution
- execution authorization
- strategic decision ownership
- changing Task Lifecycle State

**Failure Modes:**
- no suitable Agent
- insufficient evidence
- resource incompatibility
- unavailable Agent

**Observability:**
- candidate set where appropriate
- selected Agent
- capability
- evidence
- scoring/rationale
- timestamp

**Required Tests:**
- one canonical selection authority
- Agent/Capability separation
- resource compatibility
- trust/experience inputs
- no execution ownership

**Architectural Home:** `02_core`

---

## 4.14 Execution Proposal

**Canonical Authority:** Execution Proposal contract/authority as defined by the
canonical execution model.

**Canonical Responsibility:** Represent a concrete proposed execution before authorization.

**State Owned:** Execution Proposal

**Inputs:**
- Task
- selected Agent
- required Capability
- Resource Requirements
- Execution Context
- integration path
- constraints

**Outputs:**
- concrete Execution Proposal

**Dependencies:**
- Task
- Agent
- Capability
- Resource requirements
- execution context

**Forbidden Dependencies:**
- authorization by implication
- execution
- Task redefinition

**Failure Modes:**
- incomplete proposal
- incompatible execution context
- invalid resource requirements

**Observability:**
- proposal identity
- Task identity
- Agent identity
- Capability
- correlation/provenance

**Required Tests:**
- proposal/Task separation
- proposal/authorization separation
- proposal/attempt separation

**Architectural Home:** `02_core`

---

## 4.15 Execution Readiness

**Canonical Authority:** Readiness Authority

**Canonical Responsibility:** Determine whether the proposed execution is currently
possible.

**State Owned:** Execution Readiness

**State Owner:** Readiness Authority

**Inputs:**
- Task
- Agent
- Capability
- Resource State
- availability
- constraints
- integration availability
- operational conditions

**Outputs:**
- READY
- DEGRADED
- BLOCKED
- UNAVAILABLE

**Dependencies:**
- Task
- Agent
- Capability
- Resource State
- Integration availability contracts

**Forbidden Dependencies:**
- authorization
- execution
- strategic decisions
- Agent Selection ownership

**Failure Modes:**
- blocked resource
- unavailable integration
- unavailable Agent
- unmet requirement
- degraded operational condition

**Observability:**
- readiness state
- evaluated conditions
- provenance
- timestamp

**Required Tests:**
- readiness/authorization separation
- finite resources
- blocked execution
- unavailable dependencies
- degraded conditions

**Architectural Home:** `02_core`

---

## 4.16 Execution Authorization

**Canonical Authority:** Authorization Authority

**Canonical Responsibility:** Explicitly authorize a specific proposed execution.

**State Owned:** Execution Authorization

**State Owner:** Authorization Authority

**Inputs:**
- Execution Proposal
- readiness
- authorization policy
- bounded conditions

**Outputs:**
- explicit Execution Authorization

**Dependencies:**
- Execution Proposal
- Execution Readiness
- authorization policy

**Forbidden Dependencies:**
- implicit authorization by execution
- authorization for unrelated work
- strategic ownership
- Task lifecycle ownership

**Failure Modes:**
- authorization denied
- expired authorization
- invalid proposal
- violated authorization conditions

**Observability:**
- authorization identity
- proposal identity
- conditions
- timestamp
- provenance

**Required Tests:**
- explicit authorization
- bounded scope
- readiness/authorization separation
- authorization/execution separation
- unauthorized execution prevention

**Architectural Home:** `02_core`

---

## 4.17 Execution Attempt

**Canonical Authority:** Execution Authority

**Canonical Responsibility:** Own the identity and lifecycle of one concrete attempt to
perform an authorized execution.

**State Owned:** Execution Attempt

**State Owner:** Execution Authority

**Inputs:**
- Execution Authorization
- Execution Proposal

**Outputs:**
- Execution Attempt
- attempt lifecycle information

**Dependencies:**
- Authorization Authority
- Execution System contracts

**Forbidden Dependencies:**
- creating Tasks
- changing strategic decisions
- changing Agent identity
- changing Trust directly

**Failure Modes:**
- attempt creation failure
- cancellation
- timeout
- retry
- external dependency failure

**Observability:**
- attempt identity
- Task identity
- authorization identity
- Agent identity
- correlation IDs
- timestamps
- provenance

**Required Tests:**
- retry identity
- idempotency
- cancellation
- provenance
- Task/Attempt separation

**Architectural Home:** `02_core`

---

## 4.18 Execution System

**Canonical Authority:** Execution System / Execution Authority within its defined
execution responsibility.

**Canonical Responsibility:** Perform authorized work.

**State Owned:** Operational execution activity; canonical Attempt and Result ownership
remain with their explicit authorities.

**Inputs:**
- Execution Authorization
- Execution Proposal
- Execution Attempt

**Outputs:**
- execution observations
- execution result evidence

**Dependencies:**
- explicit runtime contracts
- integration adapters
- execution pipeline

**Forbidden Dependencies:**
- redefining Tasks
- redefining Agents
- strategic decisions
- Trust ownership
- Experience ownership
- Memory ownership
- bypassing Task Lifecycle Authority
- silently authorizing work

**Failure Modes:**
- execution failure
- timeout
- cancellation
- external dependency failure
- resource exhaustion

**Observability:**
- attempt identity
- authorization
- integration correlation
- operational events
- outcome evidence

**Required Tests:**
- authorization validation
- attempt association
- failure propagation
-cellation
- retry
- ownership boundaries

**Architectural Home:** `03_runtime`

---

## 4.19 Execution Pipeline

**Canonical Authority:** Execution implementation under Execution System responsibility.

**Canonical Responsibility:** Perform ordered execution operations such as analysis,
planning, generation, validation, application, testing, verification, and cleanup.

**State Owned:** No independent canonical organizational state.

**State Owner:** Relevant canonical authorities through explicit contracts.**Inputs:**
- authorized execution context

**Outputs:**
- observations
- outcomes
- execution evidence

**Dependencies:**
- Execution System
- integrations

**Forbidden Dependencies:**
- owning Task
- owning strategy
- owning Agent
- owning lifecycle
- owning Trust
- owning Memory
- owning Experience
- owning Authorization

**Failure Modes:**
- operation failure
- validation failure
- test failure
- cleanup failure

**Observability:**
- operation events
- attempt identity
- correlation
- provenance

**Requests:**
- ordered operations
- failure propagation
- no canonical ownership leakage
- authorization enforcement

**Architectural Home:** `03_runtime`

---

## 4.20 Execution Result

**Canonical Authority:** Execution Result Authority

**Canonical Responsibility:** Own the canonical outcome of an Execution Attempt.

**State Owned:** Execution Result

**State Owner:** Execution Result Authority

**Inputs:**
- Execution Attempt
- execution observations
- execution evidence

**Outputs:**
- SUCCESS
- FAILED
- BLED
- UNAVAILABLE
- DEGRADED
- CANCELLED

**Dependencies:**
- Execution Attempt
- observations
- provenance

**Forbidden Dependencies:**
- directly changing Task State
- authorization
- strategic decision making
- Agent Selection

**Failure Modes:**
- incomplete outcome
- missing provenance
- ambiguous result

**Observability:**
- Task identity
- Attempt identity
- Agent identity where applicable
- context
- provenance
- correlation IDs
- outcome

**Required Tests:**
- result/Task State separation
- result/atempt association
- outcome categories
- provenance
- failure representation

**Architectural Home:** `02_core`

---

## 4.21 Memory

**Canonical Authority:** Memory Authority

**Canonical Responsibility:** Own canonical organizational evidence storage.

**State Owned:** Memory

**State Owner:** Memory Authority

**Inputs:**
- observations
- execution history
- outcomes
- decisions
- context
- historical events
- organizational records
- provenance

**Outputs:**
- canonical Memory Records

**Dependencies:**
- canonical evidence contracts

**Forbidden Dependencies:**
- automatic decision ownership
- direct execution
- strategic authority
- lifecycle ownership

**Failure Modes:**
- persistence failure
- unavailable memory
- incomplete provenance

**Observability:**
- record identity
- source
- timestamp
- provenance
- correlation

**Required Tests:**
- evidence storage
- provenance
- ownership uniqueness
- no automatic decision authority

**Architectural Home:** `02_core`

---

## 4.22 Experience

**Canonical Aity:** Experience Authority

**Canonical Responsibility:** Own structured knowledge derived from execution and outcomes.

**State Owned:** Experience

**State Owner:** Experience Authority

**Inputs:**
- execution outcomes
- observations
- Memory evidence
- historical evidence

**Outputs:**
- Experience Records
- evidence usable by evaluation/selection/planning/risk/policy

**Dependencies:**
- Memory Authority
- Execution Result Authority
- canonical evidence

**Forbidden Dependencies:**
- direct execution
ent policy mutation
- replacing Agent Selection or Task Evaluation authority

**Failure Modes:**
- insufficient evidence
- invalid derivation
- stale experience

**Observability:**
- source evidence
- derivation
- confidence
- timestamp
- provenance

**Required Tests:**
- evidence grounding
- derivation
- provenance
- no execution authority
- no competing authority

**Architectural Home:** `02_core`

---

## 4.23 Trust

**Canonical Authority:** Trust Authority

**Canonical Responsibility:** Own canonical Tr state and evidence-grounded updates.

**State Owned:** Trust

**State Owner:** Trust Authority

**Inputs:**
- successful/failed execution evidence
- reliability
- Experience
- trends
- consistency
- provenance

**Outputs:**
- Trust Records / trust signals

**Dependencies:**
- Memory Authority
- Experience Authority
- Execution Result Authority
- canonical evidence

**Forbidden Dependencies:**
- arbitrary mutation by execution
- direct execution
- Agent Selection ownership
- strategic ownership

**Failure M:**
- insufficient evidence
- incorrect scope
- provenance mismatch
- stale evidence

**Observability:**
- Agent identity
- Capability
- Task/Attempt where applicable
- evidence
- trust state
- timestamp
- derivation

**Required Tests:**
- one Trust Authority
- evidence discipline
- Agent+Capability scoping where applicable
- execution cannot arbitrarily mutate Trust
- provenance

**Architectural Home:** `02_core`

---

## 4.24 Learning

**Canonical Authority:** Learning Authority

**Canonical Responsibilit Derive learning signals and improved knowledge from outcomes.

**State Owned:** Learning

**State Owner:** Learning Authority

**Inputs:**
- Execution Results
- Observations
- Memory
- Experience
- Trust signals

**Outputs:**
- Learning Signals
- improved knowledge for future decisions

**Dependencies:**
- Memory Authority
- Experience Authority
- Trust Authority
- Execution Result Authority

**Forbidden Dependencies:**
- direct execution
- bypassing lifecycle
- silently changing strategy
- redefining canoal semantics

**Failure Modes:**
- insufficient evidence
- invalid inference
- provenance failure

**Observability:**
- source evidence
- derivation
- timestamp
- confidence
- provenance

**Required Tests:**
- outcome grounding
- no direct execution
- no silent strategy mutation
- provenance
- authority isolation

**Architectural Home:** `02_core`

---

## 4.25 Observation

**Canonical Authority:** Relevant observation authority.

**Canonical Responsibility:** Record what happened without becoming the ownerof the
underlying canonical state.

**State Owned:** Observation records only.

**State Owner:** Observation authority for the relevant observation domain.

**Inputs:**
- observed events
- measured conditions
- execution events

**Outputs:**
- Observation

**Dependencies:**
- relevant observers/integration contracts

**Forbidden Dependencies:**
- redefining canonical state
- direct strategic decisions
- direct execution authorization

**Failure Modes:**
- missing observation
- stale observation
- incompletenance

**Observability:**
- source
- timestamp
- context
- provenance

**Required Tests:**
- observation/state separation
- provenance
- no hidden ownership

**Architectural Home:** `02_core` / `04_integrations` depending on implementation boundary

---

# 5. Runtime Composition

## Composition Root

**Canonical Authority:** Composition Root

**Canonical Responsibility:** Construct and connect production dependencies.

**State Owned:** Runtime Construction

**State Owner:** Composition Root

**Inputs:**
- rconfiguration
- concrete implementations
- integration selection

**Outputs:**
- fully constructed runtime dependency graph

**Dependencies:**
- Core contracts
- Runtime services
- Integration adapters

**Forbidden Dependencies:**
- Core constructing integrations
- multiple production Composition Roots
- domain models constructing providers

**Failure Modes:**
- dependency construction failure
- invalid dependency graph
- unavailable integration
- incomplete initialization

**Observability:**
- boot sequenc- dependency validation
- startup/shutdown events
- failure reason

**Required Tests:**
- one Composition Root
- dependency direction
- boot failure
- complete construction
- no Core→Integration dependency

**Architectural Home:** `03_runtime`

---

# 6. Runtime Boot Sequence

The canonical boot sequence is:

1. Process Start
2. Load Configuration
3. Initialize Core Authorities
4. Initialize Resource / Hardware Observation
5. Initialize Integrations
6. Construct Runtime Services
7. Validate Dependency Gra8. Validate Required Capabilities
9. Enter Operational State

Boot failure must be explicit.

A partially constructed Runtime must not silently present itself as fully operational.

Shutdown must be explicit and observable.

---

# 7. Integration Boundary

**Canonical Authority:** Integration Adapter for each external system boundary.

**Canonical Responsibility:** Translate between external representations and canonical
AI Company contracts.

**State Owned:** External/provider representation only.

**Statener:** External system or adapter-local operational state as defined by the
integration contract.

**Inputs:**
- external representation
- canonical contract

**Outputs:**
- canonical contract
- external representation

**Dependencies:**
- Core contracts
- Runtime contracts where explicitly permitted
- external systems

**Forbidden Dependencies:**
- competing canonical domain models
- external provider owning AI Company semantics
- direct mutation of canonical state without authority contract

**Failure Mod:**
- provider unavailable
- protocol failure
- malformed response
- timeout
- authentication failure
- external dependency failure

**Observability:**
- provider identity
- external correlation ID
- canonical correlation ID
- timestamp
- error information

**Required Tests:**
- adapter translation
- provider isolation
- external failure representation
- canonical ownership protection
- correlation

**Architectural Home:** `04_integrations`

---

# 8. Weft Boundary

Weft is an external operational nervous s
Weft may provide:

- workflow transport
- distributed orchestration
- node execution
- triggers
- asynchronous coordination
- workflow visibility
- routing
- operational workflow state

Weft does not own:

- Company Identity
- Company Objectives
- Strategic Decisions
- canonical Tasks
- Task Lifecycle State
- Agents
- Capabilities
- Trust
- Experience
- Memory
- organizational meaning

The AI Company ↔ Weft boundary uses explicit adapters and canonical contracts.

Weft identifiers remain integration idenifiers.

They do not automatically become canonical Task, Agent, Trust, Experience, or Memory
identities merely because they are persistent.

**Architectural Home:** `04_integrations`

---

# 9. External Agents

External Agents are integration representations.

Provider-specific:

- identifiers
- state
- protocols
- formats
- execution mechanisms

remain inside integration boundaries.

The canonical Agent contract owns:

- Agent identity
- organizational role
- capabilities
- availability
- task relationshiperience
- trust
- company meaning

**Architectural Home:** `02_core` for canonical Agent semantics,
`04_integrations` for external representations.

---

# 10. Human Personnel

Human personnel may participate as canonical Agents.

Human and AI execution mechanisms may differ.

The organizational Agent concept remains common.

Human Agents remain valid without AI-specific execution infrastructure.

**Architectural Home:** `02_core`

---

# 11. Dependency Direction

The canonical dependency direction is:

``t
Tools / Tests
     ↓
Integrations
     ↓
Runtime
     ↓
Core
Allowed:
Runtime → Core
Integration → Core
Integration → explicit Runtime contracts
Forbidden:
Core → Runtime
Core → Integration
Core → Tools
Core → Providers
Runtime → Tools / development utilities
No production module may violate this direction for convenience.

# 12. Mutable State Ownership Matrix
Mutable Canonical StateSole Owner
Company IntentIntent Authority
Company ObjectivesObjective Authority
Strategic DecisionsDe Authority
Task DefinitionCanonical Task Authority
Task StateTask Lifecycle Authority
Task Queue StateQueue Authority
Agent IdentityAgent Authority
Capability SemanticsCapability Authority
Capability AvailabilityCapability Authority
Hardware Capability ProfileHardware Capability Authority
Hardware ObservationHardware Observer
Resource StateResource State Authority
Task EvaluationTask Evaluation Authority
Agent SelectionAgent Selection Authority
Execution ReadinessReadiness Authority
Execution AuzationAuthorization Authority
Execution AttemptExecution Authority
Execution ResultExecution Result Authority
MemoryMemory Authority
ExperienceExperience Authority
TrustTrust Authority
LearningLearning Authority
Runtime ConstructionComposition Root


If ownership cannot be identified, the architecture is incomplete.

# 13. Canonical Contract Requirement
Every canonical authority must have an explicit contract describing, where applicable:
responsibility
inputs
outputs
invariants
state ownership
failureobservability
dependencies
forbidden dependencies
Implementation classes are not automatically canonical contracts.
The contract must exist at the architectural responsibility level.

# 14. Architectural Invariants
The following invariants are mandatory:
AI Company owns semantics.
Core has no integrations dependency.
Every canonical concept has one authoritative definition.
Every mutable canonical state has one authoritative owner.
There is one Task Lifecycle Authority.
Queue state is separate from Task state. definition is separate from execution history.
Attempts are separate from Tasks.
Results are separate from lifecycle state.
Agent identity is separate from Capability.
Agent Selection is separate from Execution.
Strategic Decision is separate from Execution.
Resource Observation is separate from Resource Decision.
Readiness is separate from Authorization.
Authorization is separate from Execution.
Weft is infrastructure, not company identity.
External Agents are integrations behind canonical contracts.
Huma Agents are valid organizational participants.
Hardware capability and current availability are distinct.
Physical resource limitations are explicit architectural inputs.
Resource State represents finite usable capacity.
Memory is evidence, not automatic decision.
Experience is evidence, not automatic execution.
Trust has one canonical update authority and is evidence-grounded.
Learning consumes outcomes and does not directly execute.
There is one Composition Root.
External systems cannot directly mutate caical state.
Legacy representations cannot become canonical through reuse.
Alternative implementations exist behind canonical contracts.
There are no competing canonical production paths.
External dependency failure is explicitly represented.
Physical resource constraints can block execution.
Attempts are observable and traceable.
Retries preserve Task identity and provenance.
Cancellation preserves canonical ownership.
Observability is not a state owner.
Architecture changes are not implicit through code.
Cnience cannot override ownership.

# 15. Production Module Entry Requirement
Before creating or materially modifying a production module, identify:
Responsibility
Canonical Owner
Canonical Contract
Inputs
Outputs
Dependencies
Forbidden Dependencies
Mutable State
State Owner
Failure Modes
Observability
Tests
Architectural Invariants Affected
Architectural Home
No production module should be created while these answers remain ambiguous.

# 16. Code-to-Architecture Direction
The required reasoning direction is:
CANOICAL ARCHITECTURE
        ↓
CANONICAL RESPONSIBILITY
        ↓
CANONICAL AUTHORITY
        ↓
CANONICAL CONTRACT
        ↓
MODULE
        ↓
IMPLEMENTATION
        ↓
TESTS
The reverse direction is forbidden.
Existing code cannot establish canonical meaning merely because it already exists.

# 17. Migration Rule
When legacy or conflicting implementation is encountered:
CONFLICT
   ↓
IDENTIFY CANONICAL AUTHORITY
   ↓
ISOLATE NONCANONICAL REPRESENTATION
   ↓
CREATE / ADAPT CANONICAL CONTRACT
   �MIGRATE BEHAVIOR
   ↓
REMOVE COMPETING OWNERSHIP
   ↓
VERIFY INVARIANTS
Legacy code is not copied merely for convenience.
Migration is complete only when canonical ownership has been restored.

# 18. Architectural Change Rule
An architectural change must explicitly identify:
responsibility changed
authority changed
ownership boundary changed
contract changed
dependency direction changed
affected invariant
reason the current architecture is insufficient
migration strategy
verification strategy
Convenience ais insufficient.
Frozen architecture changes require an explicit amendment.
Code must never silently amend the architecture.

# 19. Verification Requirements
Architectural verification must cover:
dependency inspection
import analysis
ownership inspection
duplicate-authority detection
canonical-model detection
lifecycle transition verification
contract verification
integration-boundary verification
resource-state verification
execution-flow verification
test verification
Verification is a quality gate.
Verification is not an architectural authority.

# 20. Canonical Responsibility Map Status
This document is:
derived from the frozen canonical architecture;
subordinate to the canonical architecture;
intended to guide production module placement;
intended to expose ownership before implementation;
not a competing authority;
not a second canonical domain model;
not an execution engine;
not a runtime service;
not an integration contract implementation.
If implementation conflicts with this document but the document is tself inconsistent
with the canonical architecture, the canonical architecture wins.
If implementation conflicts with the canonical architecture:
IMPLEMENTATION MUST BE CORRECTED OR AN ARCHITECTURAL AMENDMENT MUST BE APPROVED.

# 21. End of Canonical Responsibility & Authority Map
