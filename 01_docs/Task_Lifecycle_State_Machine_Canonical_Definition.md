# AI Company — Task Lifecycle State Machine — Canonical Definition

**Version:** 1.0
**Status:** CANONICAL DERIVATION — PRE-IMPLEMENTATION
**Authority:** AI Company Canonical Architecture
**Canonical Owner:** Task Lifecycle Authority
**Architectural Home:** `02_core`

---

# 1. Purpose

This document defines the canonical Task Lifecycle State Machine.

It establishes:

- the complete Task Lifecycle state set;
- the initial state;
- terminal states;
- valid transitions;
- invalid transitions;
- transition causality;
- transition evidence;
- lifecycle invariants;
- terminal-state rules;
- semantic separation from other canonical state domains.

This document is subordinate to:

    00_architecture/AI_Company_Canonical_Architecture.md

The frozen Canonical Architecture remains the highest authority.

This document does not introduce a competing Task model.

It does not define Queue State.

It does not define Execution Readiness.

It does not define Execution Authorization.

It does not define Execution Attempt state.

It does not redefine Execution Result semantics.

---

# 2. Constitutional Basis

The Canonical Architecture establishes that Task Lifecycle Authority owns:

- valid Task lifecycle states;
- valid Task lifecycle transitions;
- transition validation;
- terminal states;
- lifecycle history;
- lifecycle consistency;
- transition causality.

All canonical Task lifecycle transitions must pass through the
Task Lifecycle Authority.

No:

- Queue;
- Agent;
- Integration;
- Workflow Engine;
- Execution Pipeline;
- External System;

may directly mutate canonical Task Lifecycle State.

Execution Result may provide evidence for a lifecycle transition.

Execution Result does not perform the transition.

---

# 3. Canonical Semantic Principle

Task Lifecycle State represents the organizational lifecycle position
of canonical company work.

It does not represent the operational state of:

- a queue;
- a readiness evaluation;
- an authorization;
- an execution attempt;
- an external workflow;
- an external provider.

Therefore:

    Task Lifecycle State
        !=
    Queue State

    Task Lifecycle State
        !=
    Execution Readiness

    Task Lifecycle State
        !=
    Execution Authorization

    Task Lifecycle State
        !=
    Execution Attempt State

    Task Lifecycle State
        !=
    Execution Result

This separation is mandatory.

---

# 4. Canonical State Set

The canonical Task Lifecycle State Machine contains exactly four states:

    CREATED
    IN_PROGRESS
    COMPLETED
    CANCELLED

No additional lifecycle state is introduced by implementation without
an explicit architectural decision.

---

# 5. Initial State

The unique initial lifecycle state is:

    CREATED

A newly established canonical Task begins in `CREATED`.

Creation of the canonical Task definition does not imply:

- queue membership;
- execution readiness;
- execution authorization;
- execution;
- execution success.

The initial lifecycle state therefore records canonical existence of
the Task within the Task lifecycle.

---

# 6. Terminal States

The canonical terminal states are:

    COMPLETED
    CANCELLED

A Task in a terminal state cannot transition to another lifecycle state.

Terminal-state protection belongs exclusively to the
Task Lifecycle Authority.

---

# 7. Non-Terminal States

The non-terminal states are:

    CREATED
    IN_PROGRESS

A non-terminal Task may continue through its lifecycle according to
the valid transition graph.

A failed Execution Attempt does not automatically create a new
Task Lifecycle state.

The Task may remain in `IN_PROGRESS` while additional execution
attempts, recovery, retry, or organizational decisions occur.

---

# 8. Canonical Transition Graph

The complete valid transition graph is:

    [INITIAL]
        |
        v
     CREATED
        |
        | activate
        v
   IN_PROGRESS
      /       \
     /         \
success       cancellation
   /             \
  v               v
COMPLETED      CANCELLED
  [TERM]         [TERM]


Formally:

    CREATED -> IN_PROGRESS
    IN_PROGRESS -> COMPLETED
    IN_PROGRESS -> CANCELLED

These are the only canonical lifecycle transitions.

---

# 9. Transition Matrix

| Previous State | Next State | Valid |
|---|---|---|
| CREATED | CREATED | NO |
| CREATED | IN_PROGRESS | YES |
| CREATED | COMPLETED | NO |
| CREATED | CANCELLED | NO |
| IN_PROGRESS | CREATED | NO |
| IN_PROGRESS | IN_PROGRESS | NO |
| IN_PROGRESS | COMPLETED | YES |
| IN_PROGRESS | CANCELLED | YES |
| COMPLETED | CREATED | NO |
| COMPLETED | IN_PROGRESS | NO |
| COMPLETED | COMPLETED | NO |
| COMPLETED | CANCELLED | NO |
| CANCELLED | CREATED | NO |
| CANCELLED | IN_PROGRESS | NO |
| CANCELLED | COMPLETED | NO |
| CANCELLED | CANCELLED | NO |

The matrix is exhaustive.

Any transition not explicitly marked valid is rejected.

---

# 10. CREATED → IN_PROGRESS

This transition means that the canonical Task has entered active
organizational work.

The transition does NOT mean:

- the Task is queued;
- the Task is ready;
- the Task is authorized;
- an execution attempt succeeded;
- an execution attempt is currently running.

The transition requires an explicit lifecycle transition request
accepted by Task Lifecycle Authority.

Possible evidence may include:

- a valid organizational activation decision;
- evidence that the Task has entered the execution process;
- an accepted execution-attempt initiation event.

The evidence vocabulary must remain canonical.

External provider state alone cannot establish this transition.

---

# 11. IN_PROGRESS → COMPLETED

This transition means that the canonical Task has satisfied the
applicable completion criteria.

Execution Result may provide evidence for this transition.

A successful Execution Result does not itself mutate Task State.

The lifecycle authority must validate:

- Task identity;
- previous lifecycle state;
- proposed next state;
- transition cause;
- transition provenance;
- required completion evidence.

Only Task Lifecycle Authority may commit:

    IN_PROGRESS -> COMPLETED

---

# 12. IN_PROGRESS → CANCELLED

This transition means that cancellation of the canonical Task has
been accepted and the lifecycle has reached its terminal cancelled
position.

Cancellation semantics must remain distinct from execution
cancellation mechanics.

The execution system may perform operational cancellation.

The execution system does not directly mutate canonical Task State.

The lifecycle authority validates the canonical cancellation transition.

A failed attempt to cancel execution does not automatically establish
the canonical `CANCELLED` lifecycle state.

---

# 13. Execution Failure Semantics

`FAILED` is an Execution Result category.

It is NOT a Task Lifecycle State.

Therefore:

    Execution Result = FAILED

does not imply:

    Task Lifecycle State = FAILED

A failed execution attempt may leave the Task in:

    IN_PROGRESS

This permits:

- retry;
- recovery;
- another Execution Attempt;
- additional evaluation;
- organizational intervention.

The Task Lifecycle Authority may later transition the Task to:

    COMPLETED

or:

    CANCELLED

when the corresponding canonical transition criteria are satisfied.

---

# 14. Execution Result Separation

The canonical relationship is:

    Execution Attempt
          |
          v
    Execution Result
          |
          | evidence
          v
    Task Lifecycle Authority
          |
          v
    Task Lifecycle Transition

Execution Result does not become lifecycle authority.

Execution Result does not directly mutate Task State.

The existence of:

    SUCCESS
    FAILED
    BLOCKED
    UNAVAILABLE
    DEGRADED
    CANCELLED

as Execution Result categories does not expand the Task Lifecycle
state set.

---

# 15. Execution Readiness Separation

Execution Readiness remains:

    READY
    DEGRADED
    BLOCKED
    UNAVAILABLE

These states belong to Readiness Authority.

They do not become Task Lifecycle states.

For example:

    Readiness = BLOCKED

does not imply:

    Task Lifecycle = BLOCKED

A Task may remain:

    CREATED

or:

    IN_PROGRESS

while its current execution readiness is `BLOCKED`.

Readiness describes current execution feasibility.

Lifecycle describes organizational Task position.

---

# 16. Queue State Separation

Queue State belongs to Queue Authority.

Queue membership does not define Task Lifecycle State.

Therefore:

    enqueue(Task)

does not imply:

    Task State = IN_PROGRESS

and:

    dequeue(Task)

does not imply:

    Task State = IN_PROGRESS

or:

    Task State = CREATED

Queue operations modify Queue State only.

A lifecycle transition must be separately requested and validated
through Task Lifecycle Authority.

---

# 17. Authorization Separation

Execution Authorization is distinct from Task Lifecycle State.

Authorization does not automatically transition:

    CREATED -> IN_PROGRESS

and revocation or expiration of authorization does not automatically
transition the Task to another lifecycle state.

Authorization provides permission for a specific proposed execution.

Task Lifecycle Authority remains the owner of Task lifecycle mutation.

---

# 18. Execution Attempt Separation

An Execution Attempt represents one concrete attempt to perform an
authorized Execution Proposal.

Multiple Execution Attempts may belong to one Task.

Therefore:

    one Task
        |
        +--> Attempt 1
        |
        +--> Attempt 2
        |
        +--> Attempt N

Attempt state must not become a second Task Lifecycle State.

A failed Attempt does not create a new canonical Task.

A retry does not create a new canonical Task.

---

# 19. Cancellation Separation

Cancellation has multiple operational concepts:

- cancellation requested;
- cancellation accepted;
- cancellation in progress;
- execution successfully cancelled;
- cancellation failure.

These are cancellation/execution semantics.

They are not additional Task Lifecycle States.

Only a validated canonical lifecycle transition establishes:

    IN_PROGRESS -> CANCELLED

A cancellation request alone does not necessarily establish the
terminal lifecycle state.

---

# 20. Transition Causality

Every lifecycle transition must identify a canonical cause.

The minimum transition record must contain:

    task identity
    previous state
    next state
    transition cause
    transition provenance
    transition evidence
    validation result
    transition timestamp

The cause must explain why the lifecycle transition is valid.

Examples of causal sources include:

- canonical Task creation;
- organizational activation;
- execution evidence;
- completion evidence;
- cancellation decision;
- canonical organizational intervention.

These are causal categories.

They are not additional lifecycle states.

---

# 21. Transition Provenance

Every accepted transition must preserve provenance sufficient to establish:

- who or what requested the transition;
- which canonical authority validated it;
- when it occurred;
- which Task it concerned;
- what evidence supported it;
- which previous state existed;
- which new state was established.

Provider-specific identifiers may be preserved as integration-level
provenance but do not become canonical lifecycle identity.

---

# 22. Transition Validation

Task Lifecycle Authority MUST validate all of the following before
committing a transition:

1. Task identity is canonical.
2. Current state is known.
3. Proposed next state is known.
4. The state pair exists in the canonical transition graph.
5. The transition cause is valid.
6. Required evidence is present.
7. Provenance is present.
8. Terminal-state rules are satisfied.
9. The transition does not violate lifecycle invariants.

A syntactically valid state name is insufficient.

A semantically plausible transition is insufficient.

Only an explicitly valid graph edge may be committed.

---

# 23. Terminal-State Protection

Once a Task reaches:

    COMPLETED

or:

    CANCELLED

the Task Lifecycle Authority must reject all further lifecycle
transitions.

Terminal states are immutable with respect to Task Lifecycle State.

No:

- retry;
- queue operation;
- execution callback;
- integration callback;
- external workflow;
- agent action;

may reopen a terminal Task.

A new unit of work requires a new canonical Task.

---

# 24. Repeated Transition Rules

The canonical state machine does not define self-transitions.

Therefore:

    CREATED -> CREATED

and:

    IN_PROGRESS -> IN_PROGRESS

are invalid.

A transition event that does not change lifecycle state must not be
recorded as a lifecycle transition.

Operational observations may still be recorded in their own
appropriate evidence domains.

---

# 25. Invalid Transition Rules

The following are always invalid:

    CREATED -> COMPLETED
    CREATED -> CANCELLED
    IN_PROGRESS -> CREATED
    COMPLETED -> *
    CANCELLED -> *

where `*` represents any lifecycle state.

Invalid transitions must:

- be rejected;
- not mutate canonical Task State;
- not create lifecycle history entries as accepted transitions;
- remain observable as validation failures where required.

An invalid transition cannot become canonical through repetition,
retry, queue behavior, or integration behavior.

---

# 26. Lifecycle History

Task Lifecycle Authority owns lifecycle history.

Each accepted transition must append a canonical history record.

History must preserve:

- Task identity;
- previous state;
- next state;
- cause;
- provenance;
- evidence reference;
- timestamp;
- validation outcome.

History is append-oriented evidence of canonical lifecycle transitions.

History must not become a second lifecycle authority.

Current Task Lifecycle State remains owned by Task Lifecycle Authority.

---

# 27. Exactly-One-State Invariant

At any canonical point in time, each Task has exactly one current
Task Lifecycle State.

A Task cannot simultaneously be:

    CREATED
    AND
    IN_PROGRESS

or:

    IN_PROGRESS
    AND
    COMPLETED

Lifecycle state must therefore be represented as one canonical value.

Historical states belong to lifecycle history and are not simultaneous
current states.

---

# 28. Single Authority Invariant

Exactly one authority owns Task Lifecycle State:

    Task Lifecycle Authority

The following are not lifecycle authorities:

- Canonical Task Authority;
- Queue Authority;
- Readiness Authority;
- Authorization Authority;
- Execution Authority;
- Execution Result Authority;
- Runtime;
- Integration adapters;
- external workflow engines;
- external agents.

---

# 29. Canonical Task Separation Invariant

The canonical Task remains the immutable definition of intended work.

Task Lifecycle State remains a separate mutable domain.

The lifecycle implementation must not mutate the immutable Task definition
in order to represent lifecycle changes.

---

# 30. Retry Invariant

Retry creates another Execution Attempt.

Retry does not create:

- another Task;
- another Task identity;
- another lifecycle authority.

A Task may have multiple attempts while remaining in:

    IN_PROGRESS

until a valid lifecycle transition establishes a terminal state.

---

# 31. Queue Invariant

Queue membership is independent of Task Lifecycle State.

The Queue Authority cannot perform:

    TaskLifecycleAuthority.transition(...)

implicitly as a side effect of:

- enqueue;
- dequeue;
- ordering;
- retrieval.

Lifecycle transition requires an explicit canonical lifecycle operation.

---

# 32. Integration Invariant

External systems may report:

- task status;
- execution status;
- completion;
- failure;
- cancellation;
- callbacks;
- observations.

These reports are evidence.

They do not directly mutate canonical Task Lifecycle State.

Integration adapters must translate external evidence into canonical
contracts before it can be considered by Task Lifecycle Authority.

---

# 33. Runtime Invariant

Runtime may coordinate lifecycle operations.

Runtime does not own Task Lifecycle semantics.

Runtime may invoke Task Lifecycle Authority.

Runtime may not create an alternative lifecycle state machine.

Runtime implementation state must not become canonical Task State.

---

# 34. State Machine Completeness

The canonical lifecycle graph is intentionally complete.

There are exactly:

    4 lifecycle states
    1 initial state
    2 terminal states
    3 valid transitions

Valid transitions:

    CREATED -> IN_PROGRESS
    IN_PROGRESS -> COMPLETED
    IN_PROGRESS -> CANCELLED

All other state pairs are invalid.

---

# 35. Canonical Meaning of Each State

## CREATED

The canonical Task exists and has entered the Task lifecycle.

It has not yet reached active lifecycle work.

`CREATED` says nothing about:

- queue membership;
- readiness;
- authorization;
- execution;
- resource availability.

---

## IN_PROGRESS

The canonical Task is in active organizational work.

`IN_PROGRESS` does not mean that an execution process is continuously
running.

A Task may temporarily have:

- no active attempt;
- a failed attempt;
- a blocked readiness assessment;
- unavailable resources;
- a pending retry;
- a new authorization requirement.

These conditions belong to their respective domains.

---

## COMPLETED

The canonical Task has satisfied its applicable completion criteria.

`COMPLETED` is terminal.

No further lifecycle transition is permitted.

---

## CANCELLED

The canonical Task has reached its terminal cancelled position through
a validated cancellation transition.

`CANCELLED` is terminal.

No further lifecycle transition is permitted.

---

# 36. Canonical Flow

The canonical organizational lifecycle is therefore:

    Canonical Task
          |
          v
       CREATED
          |
          | validated activation
          v
     IN_PROGRESS
       /       \
      /         \
 execution      cancellation
 evidence        decision
    |               |
    v               v
 COMPLETED       CANCELLED

Execution readiness, authorization, attempts, and results operate
around this lifecycle without becoming lifecycle states.

---

# 37. Implementation Boundary

The future implementation:

    02_core/task_lifecycle.py

must implement this contract.

It must not introduce:

- additional states;
- implicit transitions;
- automatic queue-to-lifecycle transitions;
- automatic readiness-to-lifecycle transitions;
- automatic authorization-to-lifecycle transitions;
- automatic execution-result-to-lifecycle mutations;
- provider-specific lifecycle states;
- runtime-specific lifecycle states.

Any required semantic extension must first be addressed at the
canonical contract level.

---

# 38. Test Boundary

The future contract tests must verify at minimum:

- complete state set;
- unique initial state;
- terminal states;
- valid transition graph;
- invalid transition rejection;
- terminal-state protection;
- repeated-transition rejection;
- transition causality;
- provenance;
- lifecycle history;
- Task/lifecycle separation;
- Queue/lifecycle separation;
- Readiness/lifecycle separation;
- Authorization/lifecycle separation;
- Attempt/lifecycle separation;
- Result/lifecycle separation;
- external mutation prevention;
- Core dependency isolation.

Tests verify this contract.

Tests do not define the contract.

---

# 39. Implementation Gate

Production implementation of:

    02_core/task_lifecycle.py

is authorized only when:

    [x] State set defined
    [x] Initial state defined
    [x] Terminal states defined
    [x] Valid transitions defined
    [x] Invalid transitions defined
    [x] Transition causality defined
    [x] Transition evidence defined
    [x] Validation rules defined
    [x] Lifecycle invariants defined
    [x] Terminal-state rules defined

The lifecycle implementation must remain subordinate to this contract
and to the frozen Canonical Architecture.

---

# 40. Architectural Rule

Canonical Task Lifecycle State describes the organizational lifecycle
of canonical work.

It must never become a disguised representation of:

- queue state;
- readiness;
- authorization;
- execution attempt state;
- execution result;
- external workflow state.

The purpose of the State Machine is semantic coherence.

Implementation convenience must never expand the canonical state model.

---

# 41. Final Canonical State Machine

The canonical Task Lifecycle State Machine is:

```text
                 +------------------+
                 |      CREATED     |
                 +------------------+
                          |
                          | activate
                          v
                 +------------------+
                 |   IN_PROGRESS   |
                 +------------------+
                    /            \
                   /              \
             success              cancellation
                 /                  \
                v                    v
      +------------------+   +------------------+
      |    COMPLETED     |   |    CANCELLED     |
      |    TERMINAL      |   |    TERMINAL      |
      +------------------+   +------------------+

Canonical state set:

CREATED
IN_PROGRESS
COMPLETED
CANCELLED

Initial state:

CREATED

Terminal states:

COMPLETED
CANCELLED

Valid transitions:

CREATED -> IN_PROGRESS
IN_PROGRESS -> COMPLETED
IN_PROGRESS -> CANCELLED

No other lifecycle transition is canonical.
