# AI Company — Experience Canonical Contract

**VERSION: 1.0
**STATUS: DERIVED — CANONICAL CORE CONTRACT
**AUTHORITY: SUBORDINATE TO THE FROZEN CANONICAL ARCHITECTURE
**PARENT CONTRACT: 01_docs/AI_Company_Core_Contract_Specification.md
**IMPLEMENTATION ORDER: 18
**CANONICAL AUTHORITY: Experience Authority
**ARCHITECTURAL HOME: 02_core/experience.py

---

# 1. Constitutional Position

This document defines the canonical contract of Organizational Experience.

It is derived from:

00_architecture/AI_Company_Canonical_Architecture.md

01_docs/AI_Company_Core_Contract_Specification.md

01_docs/AI_Company_Core_Implementation_Order.md

01_docs/AI_Company_Memory_Canonical_Contract.md

It does not redefine the Canonical Architecture.

If this contract conflicts with the Canonical Architecture:

THE CANONICAL ARCHITECTURE WINS.

If this contract conflicts with the Memory contract, the contracts must be interpreted according to their respective ownership boundaries. Memory owns evidence preservation. Experience owns the canonical representation of derived organizational experience.

No implementation detail may redefine this contract.

---

# 2. Purpose

Experience represents structured organizational knowledge derived from preserved evidence.

Experience answers questions of the form:

what happened in a relevant context;

what was learned from repeated or significant events;

what patterns have been observed;

what contextual relationships are supported by evidence;

what outcomes have historically been associated with particular conditions;

what operational knowledge can be retained for future organizational use.

Experience is therefore derived knowledge, not raw evidence.

The fundamental distinction is:

Memory
    |
    | preserves evidence
    v
Experience
    |
    | represents derived organizational knowledge
    v
Trust / Learning / Future Decision Context

Experience must preserve the relationship between derived knowledge and the evidence from which that knowledge was derived.

Experience must never become an untraceable collection of conclusions.

---

# 3. Canonical Responsibility

Experience is responsible for:

deriving structured organizational experience from canonical evidence;

preserving the identity of that experience;

preserving the evidence references supporting the experience;

preserving relevant temporal and contextual information;

representing observed patterns and outcomes;

distinguishing evidence from derived interpretation;

maintaining the canonical state of Experience;

exposing Experience as a reusable organizational knowledge structure.

Experience is not responsible for:

preserving raw evidence as the canonical evidence authority;

determining canonical Trust;

producing Learning decisions;

evaluating Tasks;

selecting Agents;

authorizing execution;

executing work;

making Strategic Decisions.

---

# 4. Canonical Owner

The sole canonical owner of Experience state is:

Experience Authority

Exactly one canonical Experience Authority exists.

No other Core authority may own or redefine canonical Experience state.

The following are not Experience Authority:

Memory Authority;

Trust Authority;

Learning Authority;

Task Evaluation Authority;

Agent Selection Authority;

Runtime services;

Integration adapters;

persistence systems;

databases;

caches;

external agent platforms.

An implementation class may support Experience Authority but does not acquire independent canonical authority.

---

# 5. Architectural Home

The canonical Core implementation home is:

02_core/experience.py

Experience belongs to the Core layer.

The implementation must remain semantically meaningful without:

Runtime;

Integrations;

Weft;

LLM providers;

HTTP clients;

databases;

cloud services;

workflow engines;

external agent platforms;

OS-specific mechanisms.

External systems may provide evidence or persistence mechanisms through explicit adapters.

They do not define canonical Experience semantics.

---

# 6. Fundamental Semantic Distinction

Experience must remain distinct from Memory.

The canonical distinction is:

Memory:
    "What evidence do we retain?"

Experience:
    "What structured organizational knowledge can be represented
     from that evidence?"

Memory preserves evidence.

Experience represents derived organizational knowledge.

Therefore:

Evidence
    !=
Experience

And:

Memory Record
    !=
Experience Record

Experience must not simply become a renamed Memory Record with additional fields.

---

# 7. Experience Derivation

Experience may derive knowledge from evidence including:

Memory Records;

Execution Results;

Execution Attempts;

Observations;

Task Lifecycle evidence;

Task context;

Agent context;

Capability context;

Resource context;

historical evidence;

provenance.

Experience may combine multiple evidence records when the canonical semantics justify such a relationship.

Experience must preserve references to the evidence supporting the derived knowledge.

The derivation relationship must remain traceable.

Conceptually:

Evidence A
     \
Evidence B ----> Experience
     /
Evidence C

The Experience record must not erase the evidence relationship.

---

# 8. Evidence Is Not Interpretation

Experience may contain interpretation.

Memory must not.

Experience may therefore represent concepts such as:

repeated success under a context;

recurring failure conditions;

observed operational pattern;

historically successful approach;

historically problematic condition;

contextual relationship;

accumulated outcome pattern.

However, the Experience representation must distinguish:

supporting evidence;

derived experience;

confidence or evidentiary qualification, where applicable.

Experience must not silently present an interpretation as if it were raw evidence.

---

# 9. Canonical Experience Model

A canonical Experience representation must conceptually preserve:

experience identity;

subject or scope;

derived knowledge;

supporting evidence references;

temporal context;

relevant contextual references;

provenance/derivation information;

evidence state or qualification where applicable;

metadata that does not redefine another authority.

The exact Python representation is an implementation concern.

The semantic contract is authoritative over the representation.

---

# 10. Experience Identity

Every canonical Experience record must have a stable identity.

Experience identity must be distinct from:

Memory identity;

Task identity;

Agent identity;

Execution Attempt identity;

Execution Result identity;

Trust identity;

Learning identity.

A Memory Record may support an Experience Record.

It does not become the Experience Record.

Experience identity must not be derived merely by reusing another authority's identity.

---

# 11. Supporting Evidence References

Every derived Experience must be traceable to its supporting evidence where such evidence is required by the Experience semantics.

Experience may reference:

Memory Records;

Execution Results;

Observations;

Tasks;

Agents;

Capabilities;

Resource States;

lifecycle evidence.

References identify evidence or context.

References do not transfer ownership.

Experience must not create parallel canonical models of referenced concepts.

---

# 12. Temporal Semantics

Experience must preserve temporal meaning.

At minimum, the implementation must distinguish, where applicable:

temporal position of the underlying evidence;

period represented by the experience;

time at which the Experience was derived or retained.

Historical experience must not silently rewrite the historical evidence from which it was derived.

A later Experience may supersede or refine an earlier Experience only through an explicit canonical relationship.

Ordinary mutation must not silently rewrite historical meaning.

---

# 13. Immutability and Historical Integrity

A canonical Experience representation should be treated as an immutable derived knowledge snapshot unless a future canonical contract explicitly defines controlled mutation semantics.

A new interpretation of historical evidence must not silently mutate an existing Experience record.

Where experience evolves, the implementation must preserve the relationship between:

previous experience
        +
new evidence
        =
new or explicitly revised experience

The mechanism must preserve historical traceability.

---

# 14. Experience State Ownership

Only Experience Authority may mutate canonical Experience state.

The following may provide evidence or requests but do not directly own Experience state:

Memory Authority;

Execution System;

Agents;

Runtime;

Integrations;

Trust Authority;

Learning Authority;

Task Evaluation Authority;

Agent Selection Authority.

This preserves the one-authority rule.

---

# 15. Relationship to Memory

The canonical direction is:

Memory
   |
   v
Experience

Memory preserves evidence.

Experience consumes evidence and derives structured knowledge.

Memory does not consume Experience to redefine historical evidence.

Experience must not mutate Memory.

Experience must not replace Memory.

Experience must preserve references to the Memory evidence that supports its derived knowledge.

Therefore:

Memory owns evidence.
Experience owns derived experience.

---

# 16. Relationship to Trust

The canonical relationship is:

Memory
   |
   v
Experience
   |
   v
Trust

Trust may consume Experience as one source of relevant evidence.

Experience must not calculate canonical Trust.

Experience must not:

increase Trust;

decrease Trust;

assign Trust scores;

own Trust state;

determine Trust trends;

replace Trust Authority.

Trust remains responsible for canonical Trust semantics.

An Experience statement such as:

"Agent X has historically completed similar tasks successfully."

does not itself become:

"Agent X has Trust = 0.91."

The first is Experience.

The second belongs to Trust.

---

# 17. Relationship to Learning

The canonical relationship is:

Memory
   |
   v
Experience
   |
   v
Learning

Learning may consume Experience as one source of organizational knowledge.

Experience must not become Learning Authority.

Experience does not:

define Learning Signals;

determine what should be learned;

execute learning updates;

change organizational strategy;

directly modify future decisions.

Learning remains responsible for canonical learning semantics.

Learning may use Experience to produce Learning Signals or improved organizational knowledge according to the Learning contract.

---

# 18. Experience vs Learning

The distinction is:

Experience:
    "This is structured knowledge derived from what happened."

Learning:
    "This is a canonical learning signal or organizational
     improvement derived from available evidence and experience."

Experience is therefore an input to Learning.

Experience must not absorb Learning semantics merely because Experience is itself derived.

---

# 19. Experience vs Trust

The distinction is:

Experience:
    historical/contextual organizational knowledge

Trust:
    canonical trust state derived from relevant evidence

Experience may describe reliability-related historical patterns.

Trust determines canonical Trust semantics.

Experience must never become a hidden Trust accumulator.

---

# 20. Experience vs Memory

The distinction is:

Memory:
    evidence preservation

Experience:
    evidence-derived organizational knowledge

Memory must preserve evidence even when no Experience is derived.

Experience must not be required for Memory to remain valid.

A Memory Record may exist without an Experience Record.

An Experience Record must not exist without an appropriate evidentiary basis when its semantics require evidence.

---

# 21. Experience vs Task Evaluation

Experience may be consumed by Task Evaluation.

Task Evaluation determines Task suitability under current context.

Therefore:

Experience
    |
    v
Task Evaluation

Experience does not evaluate a Task.

Experience does not determine:

whether a Task should execute;

whether a Task is feasible;

whether resources are sufficient;

whether an Agent should be selected;

whether execution is authorized.

Those responsibilities remain with their respective authorities.

---

# 22. Experience vs Agent Selection

Experience may provide historical knowledge relevant to Agent Selection.

For example, Experience may preserve:

historical performance patterns;

contextual success patterns;

recurring failure conditions;

experience with a capability.

Experience does not:

select Agents;

rank Agents;

assign Agents;

authorize Agents to execute;

mutate Agent state.

Agent Selection remains the canonical owner of selection semantics.

---

# 23. Experience vs Strategic Decision

Experience may provide evidence or derived organizational knowledge to future strategic reasoning.

Experience does not create or mutate Strategic Decisions.

The canonical relationship is:

Experience
    |
    v
Future Decision Context

not:

Experience
    =
Strategic Decision

Decision Authority remains the sole owner of Strategic Decision semantics.

---

# 24. Canonical Inputs

Experience may consume:

Memory Records;

Execution Results;

Execution Attempts;

Observations;

Task Lifecycle evidence;

Tasks;

Agents;

Capabilities;

Resource State;

provenance;

historical evidence;

previously established Experience where the canonical semantics permit refinement.

Input consumption does not transfer ownership.

Experience must not mutate the canonical state of any input authority.

---

# 25. Canonical Outputs

Experience produces or exposes:

canonical Experience records;

derived organizational knowledge;

supporting evidence references;

contextual references;

derivation/provenance information;

qualification or uncertainty information where applicable.

Experience does not produce:

Trust state;

Trust scores;

Learning decisions;

Learning Authority state;

Task Evaluation decisions;

Agent Selection decisions;

Execution Readiness;

Execution Authorization;

Execution;

Strategic Decisions.

---

# 26. Uncertainty and Evidentiary Qualification

Experience must not convert uncertain evidence into unjustified certainty.

If supporting evidence is:

unavailable;

incomplete;

inconsistent;

unobserved;

the resulting Experience must preserve appropriate qualification where the uncertainty affects the derived knowledge.

Experience must distinguish:

strongly supported experience
        !=
weakly supported experience
        !=
unresolved interpretation

The exact confidence model belongs to the Experience contract only if explicitly defined.

Experience must not silently borrow Trust semantics to represent confidence.

---

# 27. Contradictory Evidence

Experience must not silently resolve contradictory evidence.

If evidence supports conflicting interpretations, Experience must preserve the contradiction or explicitly represent the unresolved state.

For example:

Evidence A -> successful outcome
Evidence B -> failed outcome

must not automatically become:

Experience -> always successful

without a canonical derivation rule.

Experience may represent a contextual distinction where the evidence supports it.

The reconciliation semantics must remain explicit.

---

# 28. Derivation Provenance

Experience must preserve sufficient information to answer:

from which evidence was this Experience derived?

when was the evidence relevant?

when was the Experience derived?

under what context was it derived?

what canonical authority produced it?

Experience provenance must not be confused with Memory provenance.

Memory provenance describes the origin of retained evidence.

Experience derivation provenance describes how canonical Experience was derived from that evidence.

Therefore:

Memory provenance
    !=
Experience derivation provenance

---

# 29. No Inference Leakage

Experience must not silently create state belonging to another authority.

Creating Experience must not implicitly create:

Trust;

Learning;

Task Evaluation;

Agent Selection;

Strategic Decision;

Execution Authorization.

An Experience derivation may be consumed by those authorities later.

Consumption is not ownership.

---

# 30. No Parallel Domain Models

Experience must not redefine:

Task;

Agent;

Capability;

Resource State;

Execution Attempt;

Execution Result;

Task Lifecycle;

Memory;

Trust;

Learning;

Strategic Decision.

Experience may reference these concepts through:

canonical identifiers;

immutable references;

stable value representations;

explicit contracts;

forward references where appropriate;

protocol-style abstractions where appropriate.

A semantic relationship does not automatically justify a concrete import.

---

# 31. Concrete Dependency Rules

02_core/experience.py may depend on:

standard language/runtime facilities;

canonical Core contracts;

canonical Core value representations;

stable canonical identifiers;

immutable reference structures;

explicit abstractions required by Experience semantics.

It must not depend on:

Runtime implementations;

Integration implementations;

Weft;

LLM providers;

HTTP clients;

database clients;

cloud SDKs;

external workflow engines;

external agent platforms;

OS-specific mechanisms;

development tools.

Core dependency direction remains:

Runtime / Integrations
          |
          v
         Core

Never:

Core
  |
  v
Runtime / Integrations

---

# 32. Semantic Dependency vs Import Dependency

Experience has semantic relationships with:

Memory;

Execution Result;

Observation;

Task;

Agent;

Capability;

Resource State;

Trust;

Learning.

These relationships do not automatically require concrete imports.

Concrete imports are justified only when the implementation genuinely requires executable behavior from another Core implementation.

Where a semantic relationship is sufficient, prefer:

canonical identifiers;

immutable references;

explicit value types;

contract-safe abstractions.

Circular imports must not be created merely to represent semantic relationships.

---

# 33. Mutable State

The canonical mutable state owned by Experience Authority consists only of state explicitly belonging to Experience.

Potential state includes:

canonical Experience records;

Experience identity;

derivation relationships;

historical Experience records;

controlled Experience lifecycle/version information if explicitly defined.

Experience must not own:

Memory state;

Trust state;

Learning state;

Task state;

Agent state;

Capability state;

Resource State;

Execution state.

---

# 34. Failure Semantics

Experience must explicitly distinguish failures such as:

invalid Experience identity;

missing required supporting evidence;

invalid evidence reference;

invalid provenance;

invalid temporal information;

contradictory or insufficient derivation input;

duplicate Experience identity;

invalid mutation;

unsupported Experience state;

invalid contextual reference.

A failure to derive Experience must not alter the underlying evidence.

In particular:

failure to derive Experience
    !=
failure of the underlying event

Likewise:

absence of Experience
    !=
absence of evidence

---

# 35. Persistence Boundary

Persistence is an implementation mechanism.

Experience is not equivalent to:

a database table;

a cache;

a vector store;

a file;

an event log;

an external knowledge base.

The canonical relationship is:

Experience Authority
        |
        v
Canonical Experience
        |
        v
Persistence Adapter
        |
        v
External Storage

Persistence must not become Experience Authority.

---

# 36. Runtime Boundary

Runtime may:

construct Experience Authority;

provide canonical evidence;

coordinate Experience operations;

select persistence mechanisms;

coordinate downstream consumers.

Runtime must not redefine Experience semantics.

Runtime is not Experience Authority.

---

# 37. Integration Boundary

Integrations may translate external information into canonical evidence or canonical Experience inputs.

The direction is:

External System
      |
      v
Integration Adapter
      |
      v
Canonical Core Evidence / Contract
      |
      v
Experience Authority

External provider semantics must not become canonical Experience semantics merely because an adapter exposes them.

---

# 38. One-Way Semantic Ownership

The canonical ownership direction is:

Memory Authority
       |
       v
Experience Authority
       |
       +------> Trust Authority
       |
       +------> Learning Authority
       |
       +------> Task Evaluation Authority
       |
       +------> Agent Selection Authority
       |
       v
Future Decision Context

This diagram describes semantic consumption, not necessarily concrete Python imports.

Experience owns Experience.

Downstream authorities own their respective interpretations.

---

# 39. Canonical Invariants

The following invariants are mandatory.

E-01 — Single Authority

Exactly one canonical Experience Authority exists.

E-02 — Canonical Identity

Every canonical Experience record has a stable identity distinct from identities owned by other authorities.

E-03 — Evidence Derivation

Experience is derived from identifiable canonical evidence where evidence is required by the Experience semantics.

E-04 — Evidence Traceability

Derived Experience remains traceable to its supporting evidence.

E-05 — Interpretation Separation

Experience remains distinguishable from raw Memory evidence.

E-06 — Provenance

Experience preserves sufficient derivation provenance.

E-07 — Temporal Integrity

Historical Experience remains historically distinguishable.

E-08 — Uncertainty Preservation

Experience does not silently convert incomplete, unavailable, unobserved, or inconsistent evidence into unjustified certainty.

E-09 — Contradiction Preservation

Conflicting evidence does not disappear through silent reconciliation.

E-10 — Ownership Isolation

Experience does not mutate state owned by another canonical authority.

E-11 — No Trust Leakage

Experience does not calculate or own Trust.

E-12 — No Learning Leakage

Experience does not calculate or own Learning Signals or Learning state.

E-13 — No Decision Leakage

Experience does not become Task Evaluation or Strategic Decision authority.

E-14 — No Selection Leakage

Experience does not select, rank, assign, or authorize Agents.

E-15 — No Execution Authority

Experience cannot execute, authorize, schedule, or dispatch work.

E-16 — No Duplicate Models

Experience does not define parallel canonical models for other Core concepts.

E-17 — Core Isolation

Experience remains independent of Runtime and Integrations.

E-18 — Persistence Independence

Experience remains semantically valid without external persistence.

E-19 — Historical Integrity

Existing Experience cannot be silently rewritten by ordinary evidence ingestion.

E-20 — Reference Ownership

References to Memory, Task, Agent, Capability, Execution Result, or other canonical concepts do not transfer ownership.

---

# 40. Canonical Evidence Chain

The complete canonical evidence chain is:

Execution / Observation
        |
        v
      Memory
        |
        v
    Experience
        |
        +----------+
        |          |
        v          v
      Trust     Learning
        |
        +----------+
                   |
                   v
          Future Decision Context

This chain does not imply that every event must pass through every authority.

It defines semantic ownership.

For example:

Trust may consume Execution Result directly;

Learning may consume Memory directly;

Task Evaluation may consume Experience and Trust;

Agent Selection may consume Experience and Trust.

The existence of a direct evidence path does not remove the ownership of any intermediate authority.

---

# 41. Memory → Experience Boundary

Memory answers:

What evidence do we retain?

Experience answers:

What structured organizational knowledge is derived from that evidence?

Therefore:

Memory = preservation
Experience = derivation

Memory must not perform Experience derivation.

Experience must not become the canonical storage authority for raw evidence.

---

# 42. Experience → Trust Boundary

Experience answers:

What historically derived knowledge do we have?

Trust answers:

What canonical Trust state is supported by relevant evidence?

Therefore:

Experience != Trust

Experience may provide evidence.

Trust determines Trust semantics.

---

# 43. Experience → Learning Boundary

Experience answers:

What structured organizational knowledge has been derived?

Learning answers:

What organizational learning signal or improvement should be represented from available evidence and knowledge?

Therefore:

Experience != Learning

Experience may be consumed by Learning.

Learning does not become a hidden mutation mechanism for Experience.

---

# 44. Downstream Decision Boundary

Experience may influence future decision authorities.

It does not make those decisions.

The canonical distinction is:

Experience
    |
    v
Decision Input
    |
    v
Decision Authority

not:

Experience
    =
Decision

---

# 45. Test Requirements

Canonical Experience tests must verify at minimum:

Experience Authority ownership.

Stable Experience identity.

Distinction between Experience and Memory.

Evidence traceability.

Derivation provenance.

Temporal semantics.

Historical integrity.

Immutability or explicitly controlled mutation semantics.

Uncertainty preservation.

Contradiction preservation.

Reference ownership.

No mutation of Memory state.

No mutation of Trust state.

No mutation of Learning state.

No Task Evaluation authority leakage.

No Agent Selection authority leakage.

No Strategic Decision authority leakage.

No Execution authority.

No duplicate domain models.

Persistence independence.

Core dependency isolation.

Runtime/Integration isolation.

Provider independence.

Separation from Trust semantics.

Separation from Learning semantics.

---

# 46. Implementation Gate

02_core/experience.py must not be implemented until its implementation can be derived directly from this contract.

The implementation must not introduce semantics absent from:

the Frozen Canonical Architecture;

the Core Contract Specification;

the Core Implementation Order;

the Memory Canonical Contract;

this Experience Canonical Contract.

The implementation must not use its own behavior to redefine Experience semantics.

The contract is authoritative over the implementation.

---

# 47. Architectural Boundary Summary

The canonical boundaries are:

                    RAW / CANONICAL EVIDENCE
                              |
                              v
                         MEMORY
                  evidence preservation
                              |
                              v
                       EXPERIENCE
                  derived knowledge
                       /          \
                      /            \
                     v              v
                  TRUST          LEARNING
              trust semantics   learning semantics
                     \              /
                      \            /
                       v          v
                    FUTURE DECISION CONTEXT

Ownership remains separate at every stage.

No downstream authority may silently absorb the authority of another stage.

---

# 48. Final Canonical Definition

Experience is the canonical Core authority responsible for representing structured organizational knowledge derived from preserved evidence, with traceable provenance, temporal context, and evidentiary qualification.

Experience:

derives;

structures;

contextualizes;

preserves derived organizational knowledge.

Experience does not:

preserve raw evidence as Memory;

calculate Trust;

perform Learning;

evaluate Tasks;

select Agents;

make Strategic Decisions;

authorize execution;

execute work.

The constitutional boundary is therefore:

MEMORY
    = canonical evidence preservation

EXPERIENCE
    = canonical derived organizational knowledge

TRUST
    = canonical trust semantics

LEARNING
    = canonical learning semantics

These are four distinct authorities.

Their semantic relationships do not imply shared ownership.

Their semantic relationships do not require circular implementation dependencies.

And none of them may become a hidden substitute for another.