"""
AI Company Core — Canonical Task Evaluation

Canonical representation and ownership of Task Evaluation.

Task Evaluation represents the evidence-grounded assessment of whether
a canonical Task is suitable for proposed execution under a specified
known organizational context.

This module belongs to the canonical Core layer.

Task Evaluation is deliberately separate from:

- Task definition
- Task lifecycle
- Task queue state
- Resource State
- Agent Selection
- Execution Readiness
- Execution Authorization
- Execution Attempt
- Execution Result
- Experience
- Trust mutation
- execution itself

This module must remain independent of:

- Runtime
- Integrations
- Tools
- Weft
- external providers
- workflow engines
- persistence systems
- execution infrastructure

Semantic relationships to other canonical concepts are represented
through stable references and evidence records rather than by creating
unnecessary concrete import dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from types import MappingProxyType
from typing import Mapping, Optional


class EvaluationConclusion(str, Enum):
    """
    Canonical conclusion of a Task Evaluation.
    """

    SUITABLE = "SUITABLE"
    UNSUITABLE = "UNSUITABLE"
    CONDITIONALLY_SUITABLE = "CONDITIONALLY_SUITABLE"
    INDETERMINATE = "INDETERMINATE"


class EvidenceState(str, Enum):
    """
    Canonical availability state of evaluation evidence.

    Evidence state must not be confused with EvaluationConclusion.
    """

    KNOWN = "KNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    UNOBSERVED = "UNOBSERVED"
    INCOMPLETE = "INCOMPLETE"
    INCONSISTENT = "INCONSISTENT"


@dataclass(frozen=True)
class EvaluationReference:
    """
    Stable reference to another canonical concept.

    A reference does not transfer ownership of the referenced concept.
    """

    concept: str
    identity: str
    reference_kind: str

    def __post_init__(self) -> None:
        if not self.concept.strip():
            raise ValueError(
                "Evaluation reference concept must not be empty."
            )

        if not self.identity.strip():
            raise ValueError(
                "Evaluation reference identity must not be empty."
            )

        if not self.reference_kind.strip():
            raise ValueError(
                "Evaluation reference kind must not be empty."
            )


@dataclass(frozen=True)
class EvaluationEvidence:
    """
    One explicit piece of evidence used by Task Evaluation.

    Evidence may be known, unavailable, unobserved, incomplete, or
    inconsistent.

    Unknown evidence is never silently converted into negative evidence.
    """

    dimension: str
    state: EvidenceState
    reference: Optional[EvaluationReference] = None
    detail: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.dimension.strip():
            raise ValueError(
                "Evaluation evidence dimension must not be empty."
            )

        if self.detail is not None and not self.detail.strip():
            raise ValueError(
                "Evaluation evidence detail must not be empty."
            )


@dataclass(frozen=True)
class EvaluationCondition:
    """
    Explicit condition attached to a conditional suitability conclusion.

    Conditions are outputs of evaluation.

    Task Evaluation does not satisfy, wait for, schedule, reserve, or
    authorize conditions.
    """

    condition_id: str
    description: str
    references: tuple[EvaluationReference, ...] = ()

    def __post_init__(self) -> None:
        if not self.condition_id.strip():
            raise ValueError(
                "Evaluation condition ID must not be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Evaluation condition description must not be empty."
            )

        object.__setattr__(
            self,
            "references",
            tuple(self.references),
        )


@dataclass(frozen=True)
class EvaluationRules:
    """
    Immutable semantic rules used to derive an evaluation.

    Rules are inputs to Task Evaluation.

    They are not a separate canonical authority.
    """

    rules_id: str
    version: str
    description: str

    def __post_init__(self) -> None:
        if not self.rules_id.strip():
            raise ValueError(
                "Evaluation rules ID must not be empty."
            )

        if not self.version.strip():
            raise ValueError(
                "Evaluation rules version must not be empty."
            )

        if not self.description.strip():
            raise ValueError(
                "Evaluation rules description must not be empty."
            )


@dataclass(frozen=True)
class EvaluationContext:
    """
    Immutable explicit context used for one Task Evaluation.

    Context is represented through canonical references and bounded
    semantic values.

    This object does not own any referenced concept.
    """

    strategic_context: tuple[EvaluationReference, ...] = ()
    capability_context: tuple[EvaluationReference, ...] = ()
    agent_context: tuple[EvaluationReference, ...] = ()
    resource_state_context: tuple[EvaluationReference, ...] = ()
    experience_context: tuple[EvaluationReference, ...] = ()
    trust_context: tuple[EvaluationReference, ...] = ()
    risk_context: Mapping[str, str] = MappingProxyType({})
    cost_context: Mapping[str, str] = MappingProxyType({})
    environmental_context: Mapping[str, str] = MappingProxyType({})

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "strategic_context",
            tuple(self.strategic_context),
        )

        object.__setattr__(
            self,
            "capability_context",
            tuple(self.capability_context),
        )

        object.__setattr__(
            self,
            "agent_context",
            tuple(self.agent_context),
        )

        object.__setattr__(
            self,
            "resource_state_context",
            tuple(self.resource_state_context),
        )

        object.__setattr__(
            self,
            "experience_context",
            tuple(self.experience_context),
        )

        object.__setattr__(
            self,
            "trust_context",
            tuple(self.trust_context),
        )

        object.__setattr__(
            self,
            "risk_context",
            self._freeze_text_mapping(
                self.risk_context,
                "risk context",
            ),
        )

        object.__setattr__(
            self,
            "cost_context",
            self._freeze_text_mapping(
                self.cost_context,
                "cost context",
            ),
        )

        object.__setattr__(
            self,
            "environmental_context",
            self._freeze_text_mapping(
                self.environmental_context,
                "environmental context",
            ),
        )

    @staticmethod
    def _freeze_text_mapping(
        values: Mapping[str, str],
        field_name: str,
    ) -> Mapping[str, str]:
        normalized: dict[str, str] = {}

        for key, value in values.items():
            if not key.strip():
                raise ValueError(
                    f"{field_name} keys must not be empty."
                )

            if not value.strip():
                raise ValueError(
                    f"{field_name} values must not be empty."
                )

            normalized[key] = value

        return MappingProxyType(normalized)


@dataclass(frozen=True)
class TaskEvaluationProvenance:
    """
    Provenance of one canonical Task Evaluation.
    """

    source: str
    timestamp: datetime
    authority: str
    derivation_method: str
    rules_id: str
    context_references: tuple[EvaluationReference, ...] = ()

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Task evaluation provenance source must not be empty."
            )

        if not self.authority.strip():
            raise ValueError(
                "Task evaluation provenance authority must not be empty."
            )

        if not self.derivation_method.strip():
            raise ValueError(
                "Task evaluation derivation method must not be empty."
            )

        if not self.rules_id.strip():
            raise ValueError(
                "Task evaluation provenance rules ID must not be empty."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Task evaluation provenance timestamp must be "
                "timezone-aware."
            )

        object.__setattr__(
            self,
            "context_references",
            tuple(self.context_references),
        )


@dataclass(frozen=True)
class TaskEvaluation:
    """
    Immutable canonical Task Evaluation record.

    A Task Evaluation is an evidence-grounded interpretation of a Task
    under a specified context.

    It does not mutate the Task and does not authorize execution.
    """

    evaluation_id: str
    task_id: str
    conclusion: EvaluationConclusion
    context: EvaluationContext
    evidence: tuple[EvaluationEvidence, ...]
    rules: EvaluationRules
    provenance: TaskEvaluationProvenance
    reason: Optional[str] = None
    conditions: tuple[EvaluationCondition, ...] = ()

    def __post_init__(self) -> None:
        if not self.evaluation_id.strip():
            raise ValueError(
                "Task evaluation requires a canonical identity."
            )

        if not self.task_id.strip():
            raise ValueError(
                "Task evaluation requires a canonical Task identity."
            )

        if self.reason is not None and not self.reason.strip():
            raise ValueError(
                "Task evaluation reason must not be empty when provided."
            )

        object.__setattr__(
            self,
            "evidence",
            tuple(self.evidence),
        )

        object.__setattr__(
            self,
            "conditions",
            tuple(self.conditions),
        )

        if (
            self.conclusion
            == EvaluationConclusion.CONDITIONALLY_SUITABLE
            and not self.conditions
        ):
            raise ValueError(
                "CONDITIONALLY_SUITABLE evaluations require "
                "explicit conditions."
            )

        if (
            self.conclusion
            != EvaluationConclusion.CONDITIONALLY_SUITABLE
            and self.conditions
        ):
            raise ValueError(
                "Evaluation conditions are only valid for "
                "CONDITIONALLY_SUITABLE conclusions."
            )

        if (
            self.conclusion == EvaluationConclusion.INDETERMINATE
            and not self.reason
        ):
            raise ValueError(
                "INDETERMINATE evaluations require an explainable reason."
            )


class TaskEvaluationAuthority:
    """
    Sole canonical authority for Task Evaluation state.

    This authority records immutable evaluation snapshots.

    It does not:

    - redefine Tasks
    - mutate Tasks
    - derive Resource State
    - allocate resources
    - select Agents
    - mutate Capability state
    - mutate Experience
    - mutate Trust
    - determine Execution Readiness
    - authorize execution
    - execute work
    """

    AUTHORITY_NAME = "Task Evaluation Authority"

    def __init__(
        self,
        initial_evaluations: Mapping[str, TaskEvaluation] | None = None,
    ) -> None:
        self._evaluations: dict[str, TaskEvaluation] = {}

        if initial_evaluations is not None:
            for evaluation_id, evaluation in initial_evaluations.items():
                if evaluation_id != evaluation.evaluation_id:
                    raise ValueError(
                        "Task Evaluation collection key must match "
                        "evaluation_id."
                    )

                if evaluation_id in self._evaluations:
                    raise ValueError(
                        "Conflicting Task Evaluation identity."
                    )

                self._evaluations[evaluation_id] = evaluation

    @property
    def evaluations(self) -> Mapping[str, TaskEvaluation]:
        """
        Return canonical evaluations as a read-only mapping.
        """
        return MappingProxyType(dict(self._evaluations))

    def get_evaluation(
        self,
        evaluation_id: str,
    ) -> TaskEvaluation | None:
        """
        Return one canonical evaluation by identity.
        """
        return self._evaluations.get(evaluation_id)

    def record_evaluation(
        self,
        evaluation: TaskEvaluation,
    ) -> TaskEvaluation:
        """
        Record one immutable canonical Task Evaluation.

        Existing evaluation identities cannot be silently overwritten.
        """

        if evaluation.evaluation_id in self._evaluations:
            raise ValueError(
                "Conflicting Task Evaluation mutation: "
                f"evaluation '{evaluation.evaluation_id}' already exists."
            )

        self._evaluations[evaluation.evaluation_id] = evaluation
        return evaluation
