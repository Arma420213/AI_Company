# AI Company — Agent Selection Semantic Model Contract

**VERSION:** 1.0
**STATUS:** DERIVED — PRE-IMPLEMENTATION SEMANTIC MODEL
**AUTHORITY:** SUBORDINATE TO THE FROZEN CANONICAL ARCHITECTURE
**PARENT CONTRACT:** `01_docs/AI_Company_Core_Contract_Specification.md`
**PARENT DERIVATION:** `01_docs/AI_Company_Core_Module_Derivation.md`
**RELATED CONTRACT:** `Agent Selection Contract`
**RELATED SEMANTIC MODEL:** `AI_Company_Task_Evaluation_Semantic_Model_Contract.md`
**ARCHITECTURAL HOME:** `02_core/agent_selection.py`
**CANONICAL OWNER:** Agent Selection Authority

---

# 1. Purpose

This document defines the canonical semantic model of Agent Selection.

It does not define Python implementation details.

It does not create a new architectural authority.

It does not redefine Agent semantics.

It does not redefine Capability semantics.

It does not redefine Resource State semantics.

It does not redefine Experience semantics.

It does not redefine Trust semantics.

It does not redefine Task Evaluation semantics.

It does not redefine Execution Readiness.

It does not redefine Execution Authorization.

Its purpose is to define what a canonical Agent Selection means before
the production implementation is created.

The frozen Canonical Architecture remains authoritative.

If this document conflicts with the Canonical Architecture, this
document is wrong and must be corrected.

Architecture wins.

---

# 2. Constitutional Derivation

Agent Selection follows the canonical construction chain:

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
SEMANTIC MODEL
    |
    v
CORE IMPLEMENTATION
    |
    v
TESTS

Reverse derivation is forbidden.

The implementation must not become the source from which Agent
Selection semantics are inferred.

---

# 3. Canonical Responsibility

Agent Selection determines the appropriate Agent for a Task under the
known selection context.

The selection may consider:

- Task requirements;
- Capability requirements;
- Agent availability;
- Capability fit;
- Resource compatibility;
- hardware compatibility where relevant;
- Experience;
- Trust;
- cost;
- risk;
- reliability;
- other explicitly relevant canonical selection context.

Agent Selection produces a canonical Agent Selection record.

Agent Selection is a selection authority.

It is not an execution authority.

It is not an authorization authority.

It is not a strategic decision authority.

It is not a Task Evaluation authority.

---

# 4. Canonical Owner

The canonical owner of Agent Selection state is:

**Agent Selection Authority**

There must be exactly one canonical authority for Agent Selection state.

No other Core authority may become a second owner of canonical Agent
Selection state.

In particular:

- Agent Authority does not own Agent Selection;
- Capability Authority does not own Agent Selection;
- Resource State Authority does not own Agent Selection;
- Task Evaluation Authority does not own Agent Selection;
- Experience Authority does not own Agent Selection;
- Trust Authority does not own Agent Selection;
- Readiness Authority does not own Agent Selection;
- Authorization Authority does not own Agent Selection;
- Execution Authority does not own Agent Selection.

An implementation helper must not silently become another Agent Selection
authority.

---

# 5. Definition of Agent Selection

An Agent Selection is a canonical, evidence-grounded representation of
the Agent selected for a Task under a specified known selection context.

Conceptually:

    Task
      +
    Candidate Agents
      +
    Selection Context
      +
    Evidence
      |
      v
    Agent Selection

The selection identifies an Agent considered appropriate under the
evaluated selection context.

It does not guarantee that execution will occur.

It does not authorize execution.

It does not establish execution readiness.

It does not represent an execution attempt.

It does not represent an execution result.

---

# 6. Task Identity

Every Agent Selection must be associated with a canonical Task identity.

Agent Selection does not duplicate the canonical Task definition.

The canonical Task remains owned by Canonical Task Authority.

Agent Selection may reference Task information required for selection.

Agent Selection must not mutate:

- Task intent;
- Task requirements;
- Task constraints;
- Task priority;
- Task metadata;
- Task provenance;
- Task lifecycle state.

Selection is an interpretation of the Task under selection context.

It does not redefine the Task.

---

# 7. Agent Identity

Every selected Agent must be identifiable through the canonical Agent
identity.

Agent identity remains owned by Agent Authority.

Agent Selection may reference an Agent identity.

Agent Selection must not:

- create canonical Agent identity;
- redefine Agent identity;
- mutate Agent properties;
- mutate Agent availability;
- become Agent Authority.

The selected Agent reference does not transfer ownership.

---

# 8. Candidate Agent Semantics

Agent Selection may operate over a set of candidate Agents.

A candidate Agent is an Agent considered as a possible selection subject
under the current selection context.

Candidate membership does not imply:

- selection;
- assignment;
- authorization;
- execution readiness;
- execution.

A candidate set may be preserved as selection evidence or observability
information where appropriate.

The candidate set is not itself the canonical output of Agent Selection.

The canonical output is the selected Agent or an explicitly represented
non-selection outcome.

---

# 9. Selection Output

The canonical positive selection output is:

**selected Agent**

The selected Agent is represented by reference to canonical Agent
identity.

Agent Selection must not copy ownership of the Agent into the selection
record.

The semantic relationship is:

    Agent Selection
        references
    Agent

not:

    Agent Selection
        owns
    Agent

---

# 10. No Suitable Agent

Agent Selection must be able to represent the situation in which no
candidate Agent can be selected under the known selection context.

"No suitable Agent" is a valid selection outcome.

It does not mean:

- the Task is invalid;
- the Task is permanently impossible;
- Task Evaluation is UNSUITABLE;
- execution is unauthorized;
- execution readiness is BLOCKED;
- execution has failed.

The meaning is limited to Agent Selection:

    no suitable Agent
        =
    no candidate Agent can be selected under the
    applicable selection context and evidence.

The exact representation of this non-selection outcome must remain
explicit and must not be encoded as an arbitrary Agent identity.

---

# 11. Insufficient Selection Evidence

Insufficient evidence is a valid selection condition.

Examples include:

- unavailable Agent information;
- unavailable Capability information;
- unavailable Resource State;
- insufficient Experience evidence;
- insufficient Trust evidence;
- unresolved requirements;
- unresolved resource compatibility;
- unresolved risk or reliability information.

Insufficient evidence must not silently be converted into:

- a positive selection;
- a negative factual claim about an Agent;
- an arbitrary default Agent;
- a numeric zero;
- an arbitrary ranking position.

Where the available evidence cannot justify a selection, the semantic
model must preserve that uncertainty.

---

# 12. Selection Context

Agent Selection is contextual.

The same Task may result in a different selection when relevant
selection context changes.

Selection context may include:

- Task requirements;
- Capability requirements;
- available Agents;
- Agent availability;
- Resource State;
- hardware compatibility;
- Experience;
- Trust;
- cost;
- risk;
- reliability;
- environmental conditions;
- other explicitly relevant canonical context.

Context must be represented or referenced sufficiently for the selection
to be explainable.

The selection must not silently depend on mutable external state that
cannot be identified or traced.

---

# 13. Capability Semantics

Capability information may be used as selection evidence.

Capability semantics remain owned by Capability Authority.

Agent Selection may determine whether an Agent provides relevant
Capability support for the Task.

Agent Selection must not:

- redefine Capability;
- create canonical Capability state;
- mutate Capability availability;
- become Capability Authority.

Capability fit is selection evidence.

It is not itself authorization.

---

# 14. Resource State Semantics

Resource State may be used as selection context.

Resource State describes currently usable resource capacity.

Agent Selection may determine whether an Agent is compatible with the
known Resource State.

Agent Selection must not:

- derive Resource State;
- modify Resource State;
- allocate resources;
- reserve resources;
- schedule resources;
- become Resource State Authority.

The distinction remains:

    Resource State
        =
    current usable resource capacity

    Agent Selection
        =
    selection of an appropriate Agent using that context

Selection must not answer a resource question by changing canonical
Resource State.

---

# 15. Experience Semantics

Experience may be used as selection evidence.

Experience remains independently owned by Experience Authority.

Agent Selection may use relevant Experience evidence when determining
Agent suitability for the Task.

Agent Selection must not:

- mutate Experience;
- create canonical Experience state;
- invent historical evidence;
- become Experience Authority.

Experience evidence remains evidence.

It does not become Agent Selection state merely because it is consulted.

---

# 16. Trust Semantics

Trust may be used as selection evidence.

Trust remains independently owned by Trust Authority.

Agent Selection may use relevant Trust evidence when determining whether
an Agent is appropriate for the Task.

Agent Selection must not:

- modify Trust;
- increase Trust;
- decrease Trust;
- infer canonical Trust state independently;
- become Trust Authority.

Trust evidence does not transfer ownership.

---

# 17. Task Evaluation Separation

Task Evaluation and Agent Selection are distinct semantic concepts.

The distinction is:

    Task Evaluation
        =
    evaluate Task suitability

    Agent Selection
        =
    determine the appropriate Agent

Task Evaluation may provide relevant context to Agent Selection.

Agent Selection may use the result or evidence of Task Evaluation where
applicable.

Agent Selection must not silently become Task Evaluation.

In particular:

    Task Evaluation = SUITABLE
        !=
    Agent Selection = successful

A Task may be suitable while no suitable Agent is currently available.

Likewise:

    Agent Selection = successful
        !=
    Execution Readiness = READY

Selection does not imply readiness.

---

# 18. Selection Evidence

Agent Selection must be evidence-grounded.

Relevant evidence may include:

- Task requirements;
- Capability fit;
- Agent availability;
- Resource compatibility;
- hardware compatibility;
- Experience;
- Trust;
- cost;
- risk;
- reliability;
- relevant environmental context;
- Task Evaluation context where applicable.

Evidence must be associated with the relevant canonical concepts.

Where evidence is unavailable, the selection must not silently invent a
positive or negative fact.

Unknown evidence remains unknown.

---

# 19. Evidence State

Selection evidence may have different states of availability or quality.

Examples include:

- KNOWN;
- UNAVAILABLE;
- UNOBSERVED;
- INCOMPLETE;
- INCONSISTENT.

These states describe evidence.

They are not themselves Agent Selection outcomes.

For example:

    Trust evidence unavailable
        !=
    Agent unsuitable

Likewise:

    Resource evidence incomplete
        !=
    Agent incompatible

The selection must preserve uncertainty when the evidence is insufficient
for a justified conclusion.

---

# 20. Inconsistent Evidence

Conflicting evidence must be represented explicitly.

Examples include:

- contradictory Agent availability information;
- contradictory Capability information;
- incompatible Resource State observations;
- conflicting Experience evidence;
- conflicting Trust evidence;
- contradictory selection constraints.

Agent Selection must not silently resolve material contradictions by
arbitrarily choosing one value.

Where contradictions prevent a justified selection, the selection may
produce a non-selection or indeterminate outcome as explicitly
represented by the semantic model.

The contradiction must remain traceable.

---

# 21. Selection Rationale

Agent Selection should preserve an explainable rationale where the
selection requires one.

Rationale should identify the relevant evidence and selection reasoning.

Rationale must not become an opaque container for arbitrary Runtime
state.

Rationale should remain:

- relevant;
- traceable;
- bounded to Agent Selection semantics;
- distinguishable from execution logs.

Execution details do not become selection rationale merely because they
are included in a field.

---

# 22. Candidate Set as Evidence

Where appropriate, the candidate set may be retained as selection
evidence.

If retained, it should identify the Agents considered by the selection
process.

Candidate-set preservation does not establish that the Agents were
ranked.

Candidate-set preservation does not require a ranking algorithm.

Candidate-set preservation does not require a numeric score.

Candidate-set preservation does not transfer Agent ownership.

The canonical semantic model therefore distinguishes:

    candidate set
        !=
    ranked list
        !=
    selected Agent

---

# 23. Score Semantics

A numeric score is not a required canonical representation of Agent
Selection.

The canonical architecture does not define:

- a universal Agent Selection score;
- a score range;
- score weights;
- score normalization;
- a capability/experience/trust formula;
- a universal ranking function;
- a mandatory numeric comparison mechanism.

Therefore a numeric score must not be introduced as a required
canonical field merely because an implementation can calculate one.

If a future selection policy explicitly defines a score, that score is
supporting selection evidence unless and until a separate canonical
semantic contract establishes stronger meaning.

A score must not silently become:

- the definition of Agent suitability;
- authorization;
- readiness;
- Trust state;
- Experience state.

---

# 24. Ranking Semantics

Agent Selection does not canonically require a ranked list of Agents.

The canonical output is the selected Agent or an explicitly represented
non-selection outcome.

A candidate set may exist without ranking.

A future ranking mechanism must not be treated as canonical merely
because an implementation produces ordered candidates.

Ranking semantics require explicit architectural and semantic definition
before they can become canonical.

---

# 25. Tie-Breaking

The canonical Agent Selection semantic model does not define a universal
tie-breaking rule.

No implementation may silently establish a universal tie-breaking rule
and present it as architectural meaning.

Examples of non-canonical assumptions include:

- lowest Agent ID wins;
- first candidate wins;
- highest score wins;
- newest Agent wins;
- oldest Agent wins;
- alphabetical order wins.

If a future canonical selection policy requires tie-breaking, the rule
must be explicitly defined by an appropriate higher-level semantic
contract.

---

# 26. Selection Policy

Agent Selection requires selection semantics sufficient to determine an
appropriate Agent from the available evidence.

However, the canonical semantic model does not prescribe a universal
selection algorithm.

A future policy may define:

- required Capability conditions;
- availability conditions;
- resource compatibility rules;
- risk constraints;
- cost constraints;
- reliability requirements;
- evidence thresholds;
- other explicit selection criteria.

Such policy must remain subordinate to the Canonical Architecture.

Selection policy must not silently:

- execute work;
- authorize execution;
- mutate Agent state;
- mutate Capability state;
- mutate Resource State;
- mutate Experience;
- mutate Trust;
- mutate Task Lifecycle State.

---

# 27. No Default-Agent Semantics

Agent Selection must not silently select an arbitrary default Agent when
the selection evidence is insufficient.

In particular, the absence of a suitable selection must not be converted
into:

- the first registered Agent;
- a preferred Agent without canonical justification;
- an available Agent merely because it exists;
- a highest-ranked implementation artifact;
- an implementation-specific fallback.

A selected Agent must be supported by the applicable selection semantics
and evidence.

---

# 28. Selection Identity

Every canonical Agent Selection must have an identity distinct from:

- Task identity;
- Agent identity;
- Capability identity;
- Resource State identity;
- Task Evaluation identity;
- Execution Proposal identity;
- Execution Attempt identity;
- Execution Result identity.

Selection identity identifies the selection record itself.

Identity must not be confused with the identity of the selected Agent.

Conceptually:

    selection_id
        !=
    task_id
        !=
    agent_id

---

# 29. Evidence References

Where selection evidence comes from another canonical authority, the
selection should preserve references sufficient to identify the relevant
evidence.

Examples include references to:

- Task identity;
- Agent identity;
- Capability identity;
- Resource State identity;
- Experience record identity;
- Trust record identity;
- Task Evaluation identity;
- relevant selection context.

Referencing evidence does not transfer ownership.

For example:

    Agent Selection
        references
    Resource State

does not mean:

    Agent Selection Authority
        owns
    Resource State

Resource State Authority remains the sole owner of Resource State.

---

# 30. Provenance

Every canonical Agent Selection must preserve sufficient provenance to
explain:

- selection identity;
- Task identity;
- selected Agent identity where one exists;
- selection timestamp;
- selection context;
- relevant evidence;
- selection authority;
- derivation information.

Provenance must not be confused with selection evidence itself.

Provenance explains where and under which context the selection was
derived.

---

# 31. Temporal Semantics

Agent Selection is time-dependent.

A selection describes the appropriate Agent under the context known at the
time of selection.

Changes to:

- Agent availability;
- Capability availability;
- Resource State;
- Experience;
- Trust;
- environmental conditions;
- Task requirements;
- Task constraints;
- risk;
- cost;
- reliability;

may change a later selection.

A new selection under materially different context should produce a new
selection record where the canonical semantics require a new decision.

Historical selection records must not silently change because their
inputs changed later.

---

# 32. Immutability

A canonical Agent Selection record is a selection snapshot.

Once recorded, its semantic meaning must not be silently mutated.

If the same Task is considered again under different selection context,
the new selection is a new selection record.

Historical evidence remains associated with the selection under which it
was considered.

---

# 33. Selection Does Not Assign an Agent

Agent Selection determines an appropriate Agent.

It does not itself create an execution assignment unless a separate
canonical contract explicitly defines such responsibility.

The distinction is:

    selected Agent
        !=
    execution assignment

    execution assignment
        !=
    execution authorization

    execution authorization
        !=
    execution

Agent Selection must therefore not:

- reserve an Agent;
- schedule an Agent;
- start work;
- dispatch work;
- authorize work.

---

# 34. Selection Does Not Establish Readiness

Agent Selection does not determine whether a proposed execution is
currently possible.

That responsibility belongs to Execution Readiness.

Therefore:

    Agent Selection
        !=
    Execution Readiness

A selected Agent may subsequently be:

- unavailable;
- resource-incompatible;
- operationally blocked;
- otherwise not ready.

Selection must not preempt Readiness Authority.

---

# 35. Selection Does Not Authorize Execution

Agent Selection never constitutes authorization.

The semantic distinction is:

    selected Agent
        !=
    authorized Agent execution

Authorization requires its own canonical authority and contract.

Agent Selection must not expose an operation whose semantic meaning is
authorization.

---

# 36. Selection Does Not Execute

Agent Selection must never execute a Task.

It must not:

- dispatch execution;
- invoke providers;
- invoke Weft;
- start processes;
- submit external jobs;
- call execution APIs;
- create Execution Attempts;
- create Execution Results.

Execution belongs outside Agent Selection.

---

# 37. Failure and Non-Selection Conditions

The semantic model recognizes that selection may fail to produce a
selected Agent.

Relevant conditions include:

- no suitable Agent;
- insufficient evidence;
- unavailable Agent;
- capability mismatch;
- resource incompatibility;
- inconsistent evidence;
- unresolved selection constraints.

These conditions are selection outcomes or selection evidence.

They are not automatically:

- Task failure;
- execution failure;
- authorization denial;
- execution unavailability;
- Task lifecycle transitions.

The responsible authority must preserve the semantic boundary.

---

# 38. Observability

Agent Selection should make the following information traceable where
applicable:

- selection identity;
- Task identity;
- candidate set;
- selected Agent;
- relevant Capability evidence;
- relevant Resource State evidence;
- Experience evidence;
- Trust evidence;
- cost/risk/reliability evidence;
- rationale;
- provenance;
- timestamp.

Observability information is not automatically canonical state.

Logging or diagnostic information must not become a second Agent
Selection authority.

---

# 39. Semantic Separation Summary

The following distinctions are mandatory:

    Task
        !=
    Task Evaluation
        !=
    Agent Selection
        !=
    Execution Proposal
        !=
    Execution Readiness
        !=
    Execution Authorization
        !=
    Execution Attempt
        !=
    Execution Result

Likewise:

    Agent
        !=
    Agent Selection

and:

    Capability
        !=
    Capability Fit

and:

    Resource State
        !=
    Resource Compatibility

and:

    Experience
        !=
    Experience Evidence

and:

    Trust
        !=
    Trust Evidence

These distinctions preserve single ownership of canonical state.

---

# 40. Architectural Invariants

The following invariants apply to the Agent Selection semantic model:

1. There is exactly one canonical Agent Selection Authority.

2. Agent Selection owns Agent Selection state and does not own Agent,
   Capability, Resource State, Experience, Trust, Task, or Execution
   state.

3. Agent Selection references canonical identities rather than
   duplicating ownership.

4. Selection does not imply execution.

5. Selection does not imply authorization.

6. Selection does not imply readiness.

7. Selection does not mutate input authorities.

8. A candidate set is not automatically a ranked list.

9. Ranking is not a canonical requirement.

10. Numeric scoring is not a canonical requirement.

11. No universal score formula is defined by this semantic model.

12. No universal tie-breaking rule is defined by this semantic model.

13. Insufficient evidence must remain distinguishable from negative
    evidence.

14. No arbitrary default Agent may be silently selected.

15. Historical selection records must remain semantically stable.

16. Selection provenance and relevant evidence must remain traceable.

17. Agent Selection must remain independent of Runtime and Integrations.

18. Agent Selection must not become an execution provider abstraction.

19. Agent Selection must not replace Task Evaluation.

20. Agent Selection must not replace Execution Readiness.

21. Agent Selection must not replace Execution Authorization.

---

# 41. Explicitly Unresolved Semantic Decisions

The following decisions are intentionally NOT defined by this semantic
model because the current canonical architecture does not establish
them:

- universal Agent Selection scoring formula;
- universal score range;
- score weighting;
- universal ranking algorithm;
- candidate ordering semantics;
- universal tie-breaking;
- mandatory ranking output;
- mandatory numeric score;
- provider-specific selection heuristics;
- implementation-specific fallback Agent;
- execution assignment semantics.

These decisions must not be invented inside `agent_selection.py`.

If any of them later becomes canonical, the corresponding architectural
or semantic contract must be explicitly updated first.

---

# 42. Implementation Boundary

The future Core implementation must derive from this semantic model.

The implementation may choose architecture-safe Python representations
for:

- selection identity;
- selected Agent reference;
- non-selection outcome;
- evidence;
- rationale;
- context;
- provenance.

The implementation must not introduce semantics that are absent from
this model.

In particular, `agent_selection.py` must not silently introduce:

- universal scoring;
- mandatory ranking;
- tie-breaking;
- Agent mutation;
- Capability mutation;
- Resource allocation;
- Trust mutation;
- Experience mutation;
- Task mutation;
- readiness;
- authorization;
- execution.

Implementation convenience is not architectural authority.

---

# 43. Test Derivation

Before production implementation, the contract tests should verify at
minimum:

- canonical selection identity;
- Task identity preservation;
- selected Agent identity preservation;
- explicit non-selection representation;
- evidence preservation;
- rationale traceability;
- provenance;
- temporal semantics;
- immutability;
- candidate-set separation from ranking;
- absence of mandatory numeric scoring;
- absence of mandatory ranking;
- absence of universal tie-breaking;
- no default-Agent fallback;
- separation from Task Evaluation;
- separation from Resource State ownership;
- separation from Experience ownership;
- separation from Trust ownership;
- separation from Execution Readiness;
- separation from Execution Authorization;
- separation from Execution;
- Core dependency isolation;
- single-authority enforcement.

Tests verify this semantic model.

Tests do not become the source of architectural meaning.

---

# 44. Final Semantic Statement

Canonical Agent Selection means:

    determining the appropriate canonical Agent for a canonical Task
    under a known selection context, using traceable evidence, while
    preserving the ownership and semantic boundaries of Task, Agent,
    Capability, Resource State, Experience, Trust, Evaluation, Readiness,
    Authorization, and Execution.

It does not mean:

    ranking agents by an implementation-defined score,
    assigning work,
    reserving resources,
    authorizing execution,
    or executing the Task.

The Canonical Architecture remains the constitutional authority.

Architecture wins.
