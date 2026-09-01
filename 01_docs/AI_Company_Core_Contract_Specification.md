# AI Company — Core Contract Specification

Version: 1.0
Status: DERIVED FROM FROZEN CANONICAL ARCHITECTURE
Authority: NONE
Canonical Authority: AI_Company_Canonical_Architecture.md

---

# 1. Purpose

This document defines the explicit contracts required for the
`02_core` layer of AI Company.

It is derived exclusively from:

`00_architecture/AI_Company_Canonical_Architecture.md`

It does not amend, replace, extend, or reinterpret the Canonical
Architecture.

If this document conflicts with the Canonical Architecture:

THE CANONICAL ARCHITECTURE WINS.

The purpose of this document is to provide an implementation-neutral
contract surface between canonical responsibilities and future Core
modules.

This document must remain subordinate to the Canonical Architecture.

---

# 2. Core Architectural Position

The Core owns canonical AI Company meaning.

The Core must remain semantically valid if all external integrations
are removed.

The Core must not depend on:

- Weft
- LLM providers
- HTTP clients
- databases
- external workflow engines
- external agent platforms
- cloud providers
- operating-system-specific integration mechanisms
- development tools

The Core may define contracts that can later be implemented or consumed
by Runtime and Integration layers.

The Core must not depend on those implementation layers.

---

# 3. Dependency Direction

The canonical dependency direction is:

Tools / Tests
      |
      v
Integrations
      |
      v
Runtime
      |
      v
Core

For Core production modules:

ALLOWED:
- standard language/runtime facilities
- other Core contracts and canonical Core concepts
- explicit abstractions required by canonical Core responsibilities

FORBIDDEN:
- Runtime implementations
- Integration implementations
- Weft SDKs
- provider SDKs
- HTTP clients
- database clients
- external workflow engines
- cloud SDKs
- OS-specific integration mechanisms
- development tools

A Core module must never require an external operational system in order
to remain semantically meaningful.

---

# 4. Contract Definition Requirements

Every canonical Core authority must have an explicit contract.

Each contract defines, where applicable:

- Responsibility
- Canonical Owner
- Inputs
- Outputs
- Invariants
- Mutable State
- State Owner
- Dependencies
- Forbidden Dependencies
- Failure Modes
- Observability
- Tests
- Architectural Home

Implementation classes are not automatically canonical contracts.

A class may implement a contract without becoming the authority merely
because it exists.

---

# 5. Canonical Authority Matrix

| Canonical Concept | Canonical Authority | Core Home |
|---|---|---|
| Company Intent | Intent Authority | `02_core` |
| Company Objectives | Objective Authority | `02_core` |
| Strategic Decisions | Decision Authority | `02_core` |
| Task Definition | Canonical Task Authority | `02_core` |
| Task State | Task Lifecycle Authority | `02_core` |
| Task Queue State | Queue Authority | `02_core` |
| Agent Identity | Agent Authority | `02_core` |
| Capability Semantics | Capability Authority | `02_core` |
| Capability Availability | Capability Authority | `02_core` |
| Hardware Capability Profile | Hardware Capability Authority | `02_core` |
| Hardware Observation | Hardware Observer | `02_core` |
| Resource State | Resource State Authority | `02_core` |
| Task Evaluation | Task Evaluation Authority | `02_core` |
| Agent Selection | Agent Selection Authority | `02_core` |
| Execution Readiness | Readiness Authority | `02_core` |
| Execution Authorization | Authorization Authority | `02_core` |
| Execution Attempt | Execution Authority | `02_core` |
| Execution Result | Execution Result Authority | `02_core` |
| Memory | Memory Authority | `02_core` |
| Experience | Experience Authority | `02_core` |
| Trust | Trust Authority | `02_core` |
| Learning | Learning Authority | `02_core` |

Runtime Construction is owned by the Composition Root and therefore is
not a Core authority.

Execution System is a Runtime responsibility and is not a Core
execution implementation.

---

# 6. Company Intent Contract

## Responsibility

Represent canonical organizational purpose and desired direction.

## Canonical Owner

Intent Authority.

## Inputs

- organizational intent information
- explicit human-owner direction where applicable

## Outputs

- canonical Company Intent representation

## Invariants

- Intent is organizational meaning.
- Intent is not an executable Task.
- Intent does not directly execute work.
- Intent does not authorize execution.

## Mutable State

Canonical Company Intent state.

## State Owner

Intent Authority.

## Dependencies

- canonical Core concepts only

## Forbidden Dependencies

- Runtime
- Integrations
- Weft
- external providers
- execution engines

## Failure Modes

- invalid intent representation
- conflicting update request
- invalid state mutation

## Observability

Changes to canonical intent should be observable with provenance.

## Tests

- intent ownership
- intent immutability/controlled mutation semantics
- separation from execution
- dependency isolation

---

# 7. Company Objective Contract

## Responsibility

Represent desired organizational outcomes.

## Canonical Owner

Objective Authority.

## Inputs

- Company Intent
- organizational direction
- explicit objective definition

## Outputs

- canonical Company Objective

## Invariants

- Objectives are not executable by themselves.
- Objective semantics have one canonical owner.
- Objectives may lead to strategic decisions, projects, tasks,
  resource requirements, or priorities.
- Objective authority does not execute work.

## Mutable State

Objective state.

## State Owner

Objective Authority.

## Dependencies

- Intent contract
- canonical Core concepts

## Forbidden Dependencies

- Execution System
- Weft
- external workflow engines
- providers

## Failure Modes

- invalid objective
- conflicting objective mutation
- invalid objective state

## Observability

Objective creation and changes must be traceable.

## Tests

- objective ownership
- objective/execution separation
- objective/intent relationship
- mutation validation

---

# 8. Strategic Decision Contract

## Responsibility

Transform organizational intent into organizational direction.

## Canonical Owner

Decision Authority.

## Inputs

- Company Intent
- Company Objectives
- strategic context
- relevant evidence

## Outputs

- Strategic Decision
- strategic priority information where applicable

## Invariants

- Strategic Decision does not execute work.
- Strategic Decision does not become Execution Authorization.
- Decision authority remains separate from execution authority.

## Mutable State

Strategic decision state.

## State Owner

Decision Authority.

## Dependencies

- Intent
- Objectives
- canonical evidence where applicable

## Forbidden Dependencies

- Execution System
- Weft
- provider-specific execution mechanisms

## Failure Modes

- invalid decision
- missing required context
- conflicting decision state

## Observability

Decision provenance must be retained.

## Tests

- decision ownership
- separation from execution
- objective-to-decision relationship
- provenance

---

# 9. Canonical Task Contract

## Responsibility

Define the canonical unit of company work.

## Canonical Owner

Canonical Task Authority.

## Inputs

- task intent
- requirements
- constraints
- priority
- metadata

## Outputs

- canonical Task

## Canonical Task Fields

The canonical Task concept includes:

- Task Identity
- Task Intent
- Task Requirements
- Task Constraints
- Task Priority
- Task Metadata

## Invariants

- Exactly one canonical Task model exists.
- Task definition is distinct from Task lifecycle state.
- Task definition is distinct from execution attempts.
- Task definition is distinct from execution results.
- Task definition is distinct from observations.
- Task definition is distinct from learning evidence.
- External task representations are not canonical Tasks.

## Mutable State

Only state explicitly belonging to Task definition.

## State Owner

Canonical Task Authority.

## Dependencies

- canonical Core value/concept types

## Forbidden Dependencies

- Weft task models
- provider task models
- workflow-engine task models
- Runtime implementations
- Integration implementations

## Failure Modes

- invalid Task definition
- missing identity
- invalid requirements
- invalid constraints

## Observability

Task creation and canonical changes must be traceable.

## Tests

- single canonical Task model
- field validation
- separation from lifecycle
- separation from attempts
- separation from results
- external representation isolation

---

# 10. Task Lifecycle Contract

## Responsibility

Own canonical Task lifecycle state and valid transitions.

## Canonical Owner

Task Lifecycle Authority.

## Inputs

- current Task state
- proposed transition
- transition evidence
- Execution Results where applicable

## Outputs

- validated lifecycle transition
- updated canonical Task lifecycle state
- lifecycle history

## Invariants

- Only Task Lifecycle Authority mutates canonical Task lifecycle state.
- Queue cannot mutate Task state.
- Agents cannot mutate Task state.
- Integrations cannot mutate Task state.
- Workflow engines cannot mutate Task state.
- Execution pipelines cannot mutate Task state.
- Execution Results provide evidence but do not perform transitions.
- Lifecycle state and Execution Result remain separate.

## Mutable State

- current Task lifecycle state
- lifecycle history

## State Owner

Task Lifecycle Authority.

## Dependencies

- Task contract
- canonical Execution Result contract where applicable

## Forbidden Dependencies

- direct lifecycle mutation from queue
- direct lifecycle mutation from execution
- direct lifecycle mutation from integrations

## Failure Modes

- invalid transition
- illegal terminal transition
- causality violation
- inconsistent lifecycle history

## Observability

Every transition should preserve causality and provenance.

## Tests

- valid transitions
- invalid transitions
- terminal states
- lifecycle history
- transition causality
- result-to-transition separation

---

# 11. Task Queue Contract

## Responsibility

Own pending-work ordering and retrieval.

## Canonical Owner

Queue Authority.

## Inputs

- canonical Tasks
- explicit queue policy

## Outputs

- ordered eligible Tasks

## Invariants

- Queue state is separate from Task state.
- Queue does not redefine Tasks.
- Queue does not execute Tasks.
- Queue does not authorize execution.
- Queue does not make strategic decisions.
- Queue does not mutate canonical Task lifecycle state.

## Mutable State

Pending-work queue state.

## State Owner

Queue Authority.

## Dependencies

- canonical Task contract
- explicit queue policy

## Forbidden Dependencies

- Execution System
- lifecycle mutation mechanisms
- strategic decision mechanisms
- Weft workflow semantics as canonical meaning

## Failure Modes

- invalid queue operation
- duplicate queue entry
- unavailable Task
- ordering inconsistency

## Observability

Queue operations should be traceable.

## Tests

- ordering
- retrieval
- queue/Task-state separation
- duplicate handling
- lifecycle isolation

---

# 12. Agent Contract

## Responsibility

Represent an organizational execution participant.

## Canonical Owner

Agent Authority.

## Inputs

- identity
- role
- capabilities
- availability
- requirements
- execution characteristics
- experience context
- trust context

## Outputs

- canonical Agent

## Invariants

- Agent is an organizational participant.
- Agent is distinct from Capability.
- Agent is distinct from Task.
- Agent is distinct from Execution Engine.
- Agent is distinct from Execution Result.
- Agent may represent human, AI, software, local, external, or hybrid
  execution participants.
- Execution implementation is outside canonical Agent identity.

## Mutable State

Agent identity and canonical organizational properties as explicitly
defined by the Agent contract.

## State Owner

Agent Authority.

## Dependencies

- Capability contract
- canonical experience/trust context where represented

## Forbidden Dependencies

- provider-specific Agent identity as canonical identity
- execution engine implementation
- Weft identity as canonical Agent identity

## Failure Modes

- invalid identity
- invalid availability state
- invalid capability association

## Observability

Agent identity and relevant state changes require provenance.

## Tests

- Agent identity ownership
- Agent/Capability separation
- human Agent validity
- external Agent representation isolation

---

# 13. Capability Contract

## Responsibility

Define what can potentially be performed and canonical capability
availability semantics.

## Canonical Owner

Capability Authority.

## Inputs

- capability definition
- relevant availability evidence
- organizational and environmental conditions where applicable

## Outputs

- canonical Capability
- capability availability state

## Invariants

- Capability is not execution.
- Capability is not an Agent.
- Capability Authority does not execute Tasks.
- Capability Authority does not authorize execution.
- Capability Authority does not make strategic decisions.

## Mutable State

Capability availability where mutable.

## State Owner

Capability Authority.

## Dependencies

- canonical Agent concepts
- canonical hardware/resource concepts where relevant

## Forbidden Dependencies

- execution engines
- provider-specific capability semantics as canonical meaning

## Failure Modes

- invalid capability
- inconsistent availability
- unsupported capability state

## Observability

Capability changes must be traceable.

## Tests

- capability ownership
- Agent/Capability separation
- availability semantics
- execution separation

---

# 14. Hardware Capability Profile Contract

## Responsibility

Represent relatively stable physical execution-environment capability.

## Canonical Owner

Hardware Capability Authority.

## Inputs

- structural hardware information

## Outputs

- Hardware Capability Profile

## Invariants

- Represents potential physical capability.
- Does not represent current availability.
- Is distinct from Hardware Observation.
- Is distinct from Resource State.

## Mutable State

Profile state only where the physical environment changes or the
profile is explicitly refreshed.

## State Owner

Hardware Capability Authority.

## Dependencies

- canonical hardware concepts only

## Forbidden Dependencies

- OS-specific observer implementations
- runtime monitoring implementation
- resource decision logic

## Failure Modes

- incomplete hardware profile
- invalid hardware description
- unavailable hardware information

## Observability

Profile source and observation provenance must be retained where
applicable.

## Tests

- capability/observation separation
- profile completeness
- stable-structure semantics

---

# 15. Hardware Observation Contract

## Responsibility

Represent observed physical conditions.

## Canonical Owner

Hardware Observer.

## Inputs

- hardware/environment observations

## Outputs

- Hardware Observation records

## Invariants

- Observation is descriptive.
- Observation does not decide execution feasibility.
- Observation does not select Agents.
- Observation does not authorize execution.
- Observation does not become canonical state merely because it is logged.

## Mutable State

Observed records.

## State Owner

Hardware Observer for observation records.

## Dependencies

- canonical hardware observation structures

## Forbidden Dependencies

- Task selection
- Agent selection
- authorization
- execution

## Failure Modes

- unavailable sensor
- incomplete observation
- stale observation
- measurement failure

## Observability

Observation timestamp and source must be retained.

## Tests

- descriptive semantics
- provenance
- separation from Resource State
- no decision authority

---

# 16. Resource State Contract

## Responsibility

Represent currently usable execution capacity.

## Canonical Owner

Resource State Authority.

## Inputs

- Hardware Capability Profile
- Hardware Observation
- Resource Interpretation Rules
- operational resource information where canonically available

## Outputs

- Resource State

## Invariants

- Resource State represents finite usable capacity.
- Resource State is distinct from Hardware Capability Profile.
- Resource State is distinct from Hardware Observation.
- Resource State does not select Agents.
- Resource State does not authorize execution.
- Resource State does not execute Tasks.
- Physical resource limitations can block execution.

## Mutable State

Current Resource State.

## State Owner

Resource State Authority.

## Dependencies

- Hardware Capability Profile
- Hardware Observation
- canonical resource interpretation rules

## Forbidden Dependencies

- Agent Selection implementation
- Execution System
- strategic decision implementation

## Failure Modes

- stale resource information
- inconsistent observations
- insufficient resources
- unavailable resource information

## Observability

Resource state should retain observation/evaluation provenance.

## Tests

- capability/observation/state separation
- finite resource enforcement
- resource insufficiency
- pressure/availability handling

---

# 17. Task Evaluation Contract

## Responsibility

Evaluate suitability of a Task for proposed execution under known
organizational context.

## Canonical Owner

Task Evaluation Authority.

## Inputs

- Task
- Task Requirements
- Task Constraints
- Strategic Priority
- Capability information
- Agent information
- Resource State
- Experience
- Trust
- risk/cost/environmental context where applicable

## Outputs

- Task Evaluation

## Invariants

- Evaluation does not execute.
- Evaluation does not authorize.
- Evaluation does not replace Strategic Decision authority.
- Evaluation does not replace Agent Selection authority.
- Evaluation does not replace Readiness authority.

## Mutable State

Evaluation records where explicitly maintained.

## State Owner

Task Evaluation Authority.

## Dependencies

- Task
- Capability
- Agent
- Resource State
- Experience
- Trust
- strategic context

## Forbidden Dependencies

- Execution System
- direct provider execution

## Failure Modes

- incomplete evaluation context
- unavailable required evidence
- inconsistent requirements
- indeterminate evaluation

## Observability

Evaluation inputs and provenance should be traceable.

## Tests

- evaluation separation
- requirement handling
- resource handling
- trust/experience input handling
- no authorization

---

# 18. Agent Selection Contract

## Responsibility

Determine the appropriate Agent for a Task.

## Canonical Owner

Agent Selection Authority.

## Inputs

- Task
- capability requirements
- available Agents
- availability
- experience
- trust
- resource compatibility
- hardware compatibility
- cost
- risk
- reliability

## Outputs

- Agent Selection decision

## Invariants

- There is one canonical Agent Selection authority.
- Selection does not execute.
- Selection remains separate from Execution System.
- Selection does not become authorization.

## Mutable State

Selection decision records where retained.

## State Owner

Agent Selection Authority.

## Dependencies

- Task
- Agent
- Capability
- Resource State
- Experience
- Trust

## Forbidden Dependencies

- Execution System
- provider-specific agent selection authority as canonical meaning

## Failure Modes

- no suitable Agent
- insufficient evidence
- unavailable Agent
- capability mismatch
- resource incompatibility

## Observability

Selection rationale and relevant evidence should be traceable.

## Tests

- capability fit
- availability
- trust/experience inputs
- resource compatibility
- single-authority enforcement
- execution separation

---

# 19. Execution Proposal Contract

## Responsibility

Represent a concrete proposed execution before authorization.

## Canonical Owner

No independent canonical state authority is defined for Execution
Proposal by the frozen Canonical Architecture.

Execution Proposal is a canonical execution-flow contract/object defined
by the architecture. It associates canonical Task, Agent, Capability,
Resource Requirements, Execution Context, integration path, and relevant
constraints.

It must not become a separate authority over Task, Agent, Capability,
Resource State, Readiness, Authorization, Execution Attempt, or
Execution Result.

## Inputs

- Task
- selected Agent
- required Capability
- Resource Requirements
- Execution Context
- integration path
- relevant constraints

## Outputs

- Execution Proposal

## Invariants

- Proposal is not a Task definition.
- Proposal is not authorization.
- Proposal is not an Execution Attempt.
- Proposal is not an Execution Result.
- Proposal must reference canonical identities.

## Mutable State

Proposal records if persisted.

## State Owner

No independent canonical state owner is introduced for Execution Proposal
by this specification.

If proposal records are persisted, their persistence must not become a
competing canonical authority over Task, Agent, Readiness,
Authorization, Execution Attempt, or Execution Result state.

## Dependencies

- Task
- Agent
- Capability
- Resource Requirement
- Execution Context

## Forbidden Dependencies

- provider-specific task semantics as canonical meaning
- Weft workflow state as proposal identity

## Failure Modes

- missing selected Agent
- missing capability
- invalid requirements
- invalid context

## Observability

Proposal identity and provenance must be traceable.

## Tests

- association correctness
- identity preservation
- separation from authorization
- separation from attempt/result

---

# 20. Execution Readiness Contract

## Responsibility

Determine whether a proposed execution is currently possible.

## Canonical Owner

Readiness Authority.

## Inputs

- Execution Proposal
- Task requirements
- Agent requirements
- Capability requirements
- Resource State
- availability
- execution constraints
- integration availability
- operational conditions

## Outputs

Canonical readiness state:

- READY
- DEGRADED
- BLOCKED
- UNAVAILABLE

## Invariants

- Readiness is not strategy.
- Readiness is not authorization.
- READY does not imply authorization.
- Readiness describes current possibility under known conditions.

## Mutable State

Readiness evaluation records where retained.

## State Owner

Readiness Authority.

## Dependencies

- Execution Proposal
- Resource State
- Agent
- Capability
- operational condition contracts

## Forbidden Dependencies

- authorization execution
- Execution System
- strategic decision

## Failure Modes

- insufficient resources
- unavailable Agent
- unavailable capability
- unavailable integration
- degraded operating conditions
- insufficient information

## Observability

Readiness decision inputs and reasons should be traceable.

## Tests

- READY
- DEGRADED
- BLOCKED
- UNAVAILABLE
- readiness/authorization separation

---

# 21. Execution Authorization Contract

## Responsibility

Provide explicit permission for the Execution System to perform a
specific proposed execution.

## Canonical Owner

Authorization Authority.

## Inputs

- Execution Proposal
- readiness information
- authorization conditions
- applicable constraints

## Outputs

- bounded Execution Authorization

## Invariants

- Authorization is explicit.
- READY does not imply authorization.
- Authorization identifies the proposal it applies to.
- Authorization is bounded by its conditions.
- Authorization cannot silently become permission for unrelated work.
- Authorization is distinct from execution.

## Mutable State

Authorization records.

## State Owner

Authorization Authority.

## Dependencies

- Execution Proposal
- Readiness
- canonical authorization rules

## Forbidden Dependencies

- Execution System as authorization owner
- Weft as authorization owner
- provider-specific authorization semantics

## Failure Modes

- unauthorized request
- expired authorization
- invalid proposal reference
- violated authorization conditions

## Observability

Authorization identity, scope, conditions, provenance and correlation
must be traceable.

## Tests

- explicit authorization
- proposal binding
- bounded scope
- expiration/condition handling
- readiness/authorization separation

---

# 22. Execution Attempt Contract

## Responsibility

Represent one concrete attempt to perform an authorized Execution
Proposal.

## Canonical Owner

Execution Authority.

## Inputs

- Execution Authorization
- Execution Proposal
- selected Agent
- attempt metadata

## Outputs

- Execution Attempt

## Invariants

- Each attempt has its own identity.
- Multiple attempts may belong to one Task.
- Attempts are associated with authorization and proposal.
- Attempt identity is distinct from Task identity.
- Attempt identity supports retry, idempotency, cancellation, recovery,
  audit and provenance.

## Mutable State

Attempt operational state where canonically defined.

## State Owner

Execution Authority.

## Dependencies

- Execution Authorization
- Execution Proposal
- Task
- Agent

## Forbidden Dependencies

- Weft attempt identity as canonical attempt identity
- provider attempt identity as canonical organizational identity

## Failure Modes

- invalid authorization
- invalid proposal
- duplicate attempt
- cancellation
- recovery failure

## Observability

Attempt identity, authorization, proposal, Agent, timestamps and
correlation information must be traceable.

## Tests

- attempt uniqueness
- Task identity preservation
- retry behavior
- idempotency
- cancellation
- provenance

---

# 23. Execution Result Contract

## Responsibility

Represent the canonical outcome of an Execution Attempt.

## Canonical Owner

Execution Result Authority.

## Inputs

- Execution Attempt
- observed execution outcome
- execution context
- provenance

## Outputs

Canonical result categories:

- SUCCESS
- FAILED
- BLOCKED
- UNAVAILABLE
- DEGRADED
- CANCELLED

## Invariants

- Result is evidence about what happened.
- Result does not mutate Task lifecycle state directly.
- Result is distinct from Authorization.
- Result is distinct from Agent Selection.
- Result is distinct from Strategic Decision.
- Result is associated with the relevant Attempt and Task.
- A completed Attempt has one terminal result.

## Mutable State

Execution Result records.

## State Owner

Execution Result Authority.

## Dependencies

- Execution Attempt
- Task
- Agent where applicable
- Observation
- provenance

## Forbidden Dependencies

- direct Task lifecycle mutation
- direct Trust mutation
- direct Experience mutation
- strategic decision mutation

## Failure Modes

- malformed result
- missing attempt identity
- missing provenance
- conflicting terminal outcome

## Observability

Result provenance must be sufficient to reconstruct what happened.

## Tests

- result categories
- attempt association
- provenance
- lifecycle separation
- terminal-result semantics

---

# 24. Memory Contract

## Responsibility

Store organizational knowledge and historical evidence.

## Canonical Owner

Memory Authority.

## Inputs

- observations
- execution history
- outcomes
- decisions
- contextual knowledge
- historical events
- organizational records
- provenance

## Outputs

- Memory Records
- evidence retrieval

## Invariants

- Memory is evidence storage.
- Memory does not automatically decide.
- Memory does not automatically execute.
- Memory has one canonical ownership authority.
- Evidence retains provenance where applicable.

## Mutable State

Memory records.

## State Owner

Memory Authority.

## Dependencies

- canonical evidence structures
- provenance structures

## Forbidden Dependencies

- automatic execution
- automatic strategic mutation
- external database as semantic authority

## Failure Modes

- storage failure
- provenance loss
- duplicate evidence
- inconsistent record

## Observability

Memory operations should preserve provenance and correlation.

## Tests

- evidence storage
- retrieval
- provenance
- no automatic decision
- no automatic execution

---

# 25. Experience Contract

## Responsibility

Represent structured knowledge derived from previous execution and
observed outcomes.

## Canonical Owner

Experience Authority.

## Inputs

- relevant observations
- execution results
- historical evidence
- Memory records

## Outputs

- Experience Records
- derived experience signals

## Invariants

- Experience is evidence.
- Experience is not execution authority.
- Experience is derived through explicit canonical rules.
- Experience may influence evaluation, selection, planning, risk and
  future decisions.
- Experience has one canonical authority.

## Mutable State

Experience records.

## State Owner

Experience Authority.

## Dependencies

- Memory
- Observation
- Execution Result
- provenance

## Forbidden Dependencies

- direct execution
- hidden strategy mutation
- provider-specific experience authority

## Failure Modes

- insufficient evidence
- invalid derivation
- provenance loss
- conflicting experience evidence

## Observability

Derivation inputs and provenance must be traceable.

## Tests

- evidence derivation
- provenance
- separation from execution
- influence on decision inputs without authority transfer

---

# 26. Trust Contract

## Responsibility

Represent confidence derived from relevant evidence.

## Canonical Owner

Trust Authority.

## Inputs

- successful execution evidence
- failed execution evidence
- historical reliability
- experience
- observed trends
- consistency
- relevant provenance

## Outputs

- Trust Records
- trust signals for authorized decision systems

## Invariants

- Trust is evidence for decisions.
- Trust is not an execution command.
- Trust is not arbitrarily mutated by execution components.
- Trust updates pass through Trust Authority.
- Trust remains traceable to relevant evidence.
- Trust scope must remain explicit and appropriate.

## Mutable State

Trust records.

## State Owner

Trust Authority.

## Dependencies

- Memory
- Experience
- Observation
- Execution Result
- provenance

## Forbidden Dependencies

- direct execution mutation
- arbitrary Agent self-report as sufficient evidence
- unrelated system failure as sufficient evidence

## Failure Modes

- insufficient evidence
- unrelated evidence
- provenance mismatch
- conflicting evidence
- invalid scope

## Observability

Trust updates must expose evidence provenance and scope.

## Tests

- evidence grounding
- scope
- update ownership
- provenance
- positive/negative evidence
- unrelated-evidence rejection

---

# 27. Learning Contract

## Responsibility

Transform observed outcomes into improved organizational knowledge.

## Canonical Owner

Learning Authority.

## Inputs

- Observation
- Memory
- Experience
- Trust Signals
- Execution Results
- relevant historical evidence

## Outputs

- Learning Signals
- improved organizational knowledge

## Invariants

Canonical direction:

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

Learning:

- does not bypass Task Lifecycle Authority
- does not directly execute work
- does not silently mutate strategic decisions
- does not redefine canonical semantics
- does not become an alternative execution authority

## Mutable State

Learning records/signals.

## State Owner

Learning Authority.

## Dependencies

- Observation
- Memory
- Experience
- Trust
- Execution Result

## Forbidden Dependencies

- Execution System
- direct authorization
- direct strategic mutation

## Failure Modes

- insufficient evidence
- inconsistent evidence
- invalid derivation
- provenance loss

## Observability

Learning derivations must preserve evidence provenance.

## Tests

- execution-to-learning direction
- evidence grounding
- no direct execution
- no lifecycle bypass
- no semantic redefinition

---

# 28. Observation and Provenance Cross-Cutting Contract

Observation and provenance are cross-cutting canonical concerns.

Observation remains descriptive.

Provenance should identify, where applicable:

- source
- timestamp
- Task
- Agent
- Capability
- Execution Attempt
- authorization
- execution context
- resource context
- external provider
- outcome
- correlation identifiers

Observations must not become canonical state merely because they are
logged.

Evidence without sufficient provenance must not silently become
high-confidence organizational knowledge.

---

# 29. Canonical State Ownership Matrix

Every mutable canonical state has exactly one owner.

| Mutable State | Owner |
|---|---|
| Company Intent | Intent Authority |
| Company Objectives | Objective Authority |
| Strategic Decisions | Decision Authority |
| Task Definition | Canonical Task Authority |
| Task State | Task Lifecycle Authority |
| Task Queue State | Queue Authority |
| Agent Identity | Agent Authority |
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

No Core implementation may introduce another owner for these states.

---

# 30. Mandatory Separations

The following distinctions are architectural invariants.

## Task

Task
!=
Task State
!=
Execution Attempt
!=
Execution Result

## Hardware

Hardware Capability Profile
!=
Hardware Observation
!=
Resource State

## Organizational Decision Flow

Task Evaluation
!=
Agent Selection
!=
Execution Readiness
!=
Execution Authorization
!=
Execution

## Organizational Identity

Agent
!=
Capability

## Evidence

Observation
!=
Memory
!=
Experience
!=
Trust
!=
Learning

These concepts may be related but must not collapse into one authority.

---

# 31. Result and Lifecycle Boundary

The canonical result flow is:

Execution Attempt
      |
      v
Execution Result
      |
      v
Task Lifecycle Authority
      |
      v
Task State Transition

Execution Result does not directly mutate Task State.

This boundary must remain explicit in all implementations.

---

# 32. External Representation Boundary

External/provider/persistence/transport representations are not canonical.

Inbound:

External Representation
        |
        v
Adapter
        |
        v
Canonical Core Contract

Outbound:

Canonical Core Contract
        |
        v
Integration Adapter
        |
        v
External Contract

The Core must not import external provider models merely for convenience.

---

# 33. Weft Boundary

Weft is external operational infrastructure.

Weft may provide:

- workflow transport
- distributed orchestration
- node execution
- triggers
- asynchronous coordination
- workflow visibility
- routing
- workflow state
- operational coordination

Weft must not become the owner of:

- Company Identity
- Company Objectives
- Strategic Decisions
- canonical Tasks
- Task lifecycle state
- Agents
- Capabilities
- Trust
- Experience
- Memory
- organizational meaning

Weft identifiers remain integration identifiers.

Canonical AI Company identifiers remain canonical.

---

# 34. Human and External Agents

Human personnel may be represented by the canonical Agent contract.

External AI/software agents must enter through Integration boundaries.

In both cases:

Agent identity
      |
      v
Canonical Agent Contract

Provider-specific representations remain outside Core semantics.

---

# 35. Core Module Entry Gate

No production Core module may be created until its implementation
answers:

1. What responsibility does it own?
2. Who is the canonical owner?
3. What canonical contract does it implement?
4. What are its inputs?
5. What are its outputs?
6. What are its invariants?
7. What mutable state does it own?
8. Who owns that state?
9. What are its dependencies?
10. What dependencies are forbidden?
11. What are its failure modes?
12. How is it observable?
13. What tests verify it?
14. Which architectural invariants does it affect?
15. Why is `02_core` its architectural home?

If these questions cannot be answered clearly, implementation must not
begin.

---

# 36. Core Implementation Rules

Production Core code must follow:

Canonical Architecture
        |
        v
Canonical Responsibility
        |
        v
Canonical Authority
        |
        v
Canonical Contract
        |
        v
Core Module
        |
        v
Implementation
        |
        v
Tests

The reverse reasoning is forbidden.

Existing code must never determine the canonical architecture merely
because it already exists elsewhere.

---

# 37. Core Verification Requirements

Before a Core checkpoint is accepted, verify where applicable:

- dependency inspection
- import analysis
- ownership inspection
- duplicate-authority detection
- canonical-model detection
- lifecycle transition verification
- contract verification
- resource-state verification
- execution-flow verification
- test verification

The verification system is a quality gate.

It is not an architectural authority.

---

# 38. Core Architectural Invariants

Every Core implementation must preserve at minimum:

- AI Company owns canonical semantics.
- Core has no integration dependency.
- Every canonical concept has one authoritative definition.
- Every mutable canonical state has one authoritative owner.
- One Task lifecycle authority exists.
- Queue state is separate from Task state.
- Task definition is separate from execution history.
- Attempts are separate from Tasks.
- Results are separate from lifecycle state.
- Agent identity is separate from Capability.
- Agent Selection is separate from Execution.
- Strategic Decision is separate from Execution.
- Resource Observation is separate from Resource Decision.
- Hardware capability is distinct from current availability.
- Readiness is separate from Authorization.
- Authorization is separate from Execution.
- External systems cannot directly mutate canonical state.
- Memory is evidence, not automatic decision.
- Experience is evidence, not automatic execution.
- Trust has one canonical update authority.
- Trust is evidence-grounded.
- Learning consumes outcomes and does not directly execute.
- Physical resource constraints can block execution.
- Attempts remain observable and traceable.
- Retries preserve Task identity and provenance.
- Cancellation preserves canonical ownership.
- Observability does not become state ownership.
- Convenience does not override ownership.

---

# 39. No Production Code in This Specification

This document defines contracts only.

It does not define:

- Python classes
- concrete persistence
- Runtime implementations
- Integration implementations
- Weft adapters
- provider SDK usage
- database schemas
- OS-specific monitoring implementations
- execution engines

Those implementations must be derived from these contracts and the
Canonical Architecture.

---

# 40. Status

Document status:

DERIVED
NON-CANONICAL
IMPLEMENTATION GUIDANCE

Canonical authority remains:

`00_architecture/AI_Company_Canonical_Architecture.md`

If implementation conflicts with the Canonical Architecture:

THE CANONICAL ARCHITECTURE WINS.

End of Core Contract Specification.
