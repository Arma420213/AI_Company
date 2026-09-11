# AI Company — Task Lifecycle State Machine Contract

**Version:** 0.1
**Status:** ARCHITECTURAL DERIVATION — NOT YET IMPLEMENTATION
**Authority:** AI Company Canonical Architecture
**Canonical Owner:** Task Lifecycle Authority

---

# 1. Purpose

This document defines the contract boundary for the canonical
Task Lifecycle State Machine.

It exists to establish the exact semantic information that must be
defined before implementing the Task Lifecycle Authority.

This document does not introduce a competing Task model.

It does not implement lifecycle state.

It does not define execution readiness.

It does not define execution results.

It does not define queue state.

---

# 2. Constitutional Basis

The Canonical Architecture establishes that the Task Lifecycle Authority
owns:

- valid lifecycle states
- valid lifecycle transitions
- transition validation
- terminal states
- lifecycle history
- lifecycle consistency
- transition causality

All canonical Task lifecycle transitions must pass through the
Task Lifecycle Authority.

No queue, agent, integration, workflow engine, execution pipeline,
or external system may directly mutate canonical Task lifecycle state.

The canonical Task itself remains the immutable definition of intended
work.

Task Lifecycle State is a separate mutable state domain.

---

# 3. State Machine Ownership

The canonical ownership chain is:

    Canonical Task
        |
        v
    Task Lifecycle State Machine
        |
        v
    Task Lifecycle Authority
        |
        v
    Canonical Task Lifecycle State

The State Machine defines semantic validity.

The Task Lifecycle Authority applies that validity to an individual Task.

No other component may become an alternative lifecycle authority.

---

# 4. Required State Machine Elements

The canonical State Machine MUST define:

1. Complete lifecycle state set
2. Exactly one initial state, unless a canonical alternative is explicitly
   defined
3. Terminal state set
4. Allowed transitions
5. Forbidden transitions
6. Transition validation rules
7. Transition causality requirements
8. Required transition evidence
9. Lifecycle invariants
10. Terminal-state immutability rules
11. Rules governing repeated transitions
12. Rules governing invalid transitions

No implementation may silently invent any of these elements.

---

# 5. Current Canonical Status

The Canonical Architecture requires the existence of the above concepts,
but does not currently enumerate the complete Task Lifecycle state graph.

Therefore the following are presently:

    REQUIRED BY ARCHITECTURE
        - lifecycle states
        - valid transitions
        - terminal states
        - transition validation
        - lifecycle consistency
        - transition causality
        - lifecycle history

    NOT YET CANONICALLY ENUMERATED
        - exact lifecycle state names
        - initial lifecycle state
        - exact terminal state names
        - complete transition graph
        - mandatory transitions
        - explicitly forbidden transitions
        - per-state transition preconditions
        - per-state transition evidence requirements

These missing definitions MUST NOT be fabricated by implementation code.

---

# 6. Semantic Separation

The following concepts MUST remain distinct.

## 6.1 Task Lifecycle State

Represents the canonical organizational lifecycle position of a Task.

Owner:

    Task Lifecycle Authority

---

## 6.2 Execution Readiness

Represents whether execution is currently ready, degraded, blocked,
or unavailable.

Owner:

    Readiness Authority

The Execution Readiness state set MUST NOT automatically become the
Task Lifecycle state set.

---

## 6.3 Execution Result

Represents the outcome of an execution attempt.

Canonical outcome semantics include:

- SUCCESS
- FAILED
- BLOCKED
- UNAVAILABLE
- DEGRADED
- CANCELLED

These are execution-result semantics.

They MUST NOT automatically be interpreted as Task Lifecycle states.

An Execution Result may provide evidence for a lifecycle transition,
but it does not perform the transition.

---

## 6.4 Task Queue State

Represents queue membership, ordering, and pending-work retrieval.

Owner:

    Queue Authority

Queue state MUST NOT be used as a substitute for Task Lifecycle State.

---

# 7. Transition Contract

Every canonical lifecycle transition MUST have:

    Task identity
    previous lifecycle state
    new lifecycle state
    transition cause
    transition provenance
    required evidence
    authoritative validation

The transition MUST be accepted only if the State Machine declares
the transition valid.

A transition MUST NOT be accepted merely because both state names
are syntactically valid.

---

# 8. Transition Causality

A lifecycle transition must have an identifiable canonical cause.

Possible causes may include information produced by:

- Task creation
- evaluation
- authorization
- execution observation
- execution result
- cancellation
- organizational decision

These are examples of causal sources, not an authorization to introduce
corresponding lifecycle states.

The final causal vocabulary must be defined by the canonical lifecycle
contract.

---

# 9. Terminal State Contract

The State Machine MUST explicitly identify terminal states.

A terminal state MUST have defined rules preventing invalid continuation
of the lifecycle.

The exact terminal-state set is currently NOT CANONICALLY DEFINED.

Therefore implementation MUST NOT assume that:

    SUCCESS
    FAILED
    CANCELLED

or any other execution outcome is automatically a terminal Task
Lifecycle state.

That relationship requires an explicit canonical decision.

---

# 10. Initial State Contract

The State Machine MUST define the initial lifecycle state of a Task.

The Canonical Architecture currently does not explicitly enumerate
that state.

Therefore implementation MUST NOT invent an initial lifecycle state
without first establishing it as a canonical contract.

---

# 11. Transition Graph Contract

The final State Machine MUST be representable as an explicit directed
transition graph:

    State A
       |
       | valid transition
       v
    State B

Every permitted edge MUST be explicitly represented.

Every transition not represented by the canonical graph MUST be rejected
unless the canonical contract explicitly defines another mechanism.

The graph MUST NOT be inferred from:

- queue behavior
- execution pipeline behavior
- runtime behavior
- integration callbacks
- execution-result names
- readiness states

---

# 12. Lifecycle Invariants

The final State Machine MUST preserve at least these architectural
invariants:

1. Exactly one canonical lifecycle state exists for a Task at a time.

2. Lifecycle state is separate from immutable Task definition.

3. Lifecycle transitions have exactly one canonical authority.

4. Queue operations cannot mutate lifecycle state directly.

5. Execution systems cannot mutate lifecycle state directly.

6. Integrations cannot mutate lifecycle state directly.

7. Execution Results provide evidence but do not perform lifecycle
   transitions.

8. Lifecycle history records validated transitions.

9. Invalid transitions cannot become canonical state.

10. Terminal-state rules cannot be bypassed.

11. No second lifecycle representation may become a competing
    canonical source of truth.

---

# 13. Implementation Gate

The Task Lifecycle Authority MUST NOT be implemented as a definitive
canonical component until the following have been canonically defined:

    [ ] Complete lifecycle states
    [ ] Initial state
    [ ] Terminal states
    [ ] Allowed transitions
    [ ] Forbidden transitions
    [ ] Transition causes
    [ ] Transition evidence
    [ ] Transition validation rules
    [ ] Lifecycle invariants
    [ ] Terminal-state rules

Until this gate is complete, any implementation is considered
architectural experimentation rather than canonical production logic.

---

# 14. Required Next Architectural Decision

The next canonical decision is therefore:

    DEFINE THE TASK LIFECYCLE STATE MACHINE

That decision must establish:

    STATE SET
        +
    INITIAL STATE
        +
    TERMINAL STATES
        +
    TRANSITION GRAPH
        +
    TRANSITION CAUSALITY
        +
    VALIDATION RULES

Only after that decision is complete may the project define:

    02_core/task_lifecycle.py

and its definitive contract tests.

---

# 15. Non-Goals

This contract does NOT define:

- Task model structure
- Task Queue behavior
- Agent selection
- Resource State
- Execution Readiness
- Execution Authorization
- Execution Engine
- Execution Result semantics
- Memory
- Experience
- Trust
- Learning
- Weft behavior
- external integration behavior

Those responsibilities remain owned by their respective canonical
authorities.

---

# 16. Architectural Rule

No implementation detail may be promoted into canonical Task Lifecycle
semantics merely because an implementation needs a state.

Canonical meaning flows from the architecture and its explicit contracts
into implementation.

It does not flow backwards from implementation into architecture.

