"""
AI Company Core — Canonical Experience Authority

Experience represents structured organizational knowledge derived from
preserved evidence.

Experience owns:
- canonical Experience identity
- derived organizational knowledge
- supporting evidence references
- contextual references
- temporal context
- derivation provenance
- evidentiary qualification
- canonical Experience state

Experience does not own:
- raw evidence preservation
- Trust
- Learning
- Task Evaluation
- Agent Selection
- Strategic Decisions
- Execution

This module must remain independent of:
- Runtime
- Integrations
- Weft
- external providers
- HTTP clients
- databases
- persistence systems
- workflow engines
- OS-specific mechanisms

Semantic relationships with Memory, Trust, Learning, Tasks, Agents,
Capabilities, Resource State, Execution Results, and other Core concepts
do not automatically require concrete imports.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class ExperienceProvenance:
    """
    Provenance describing how canonical Experience was derived.

    This is distinct from Memory provenance.

    Memory provenance identifies the origin of retained evidence.

    Experience provenance identifies the derivation of Experience from
    supporting evidence.
    """

    source: str
    authority: str
    derived_at: datetime
    derivation_method: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Experience provenance requires a source."
            )

        if not self.authority.strip():
            raise ValueError(
                "Experience provenance requires an authority."
            )

        if not self.derivation_method.strip():
            raise ValueError(
                "Experience provenance requires a derivation method."
            )

        if self.derived_at.tzinfo is None:
            raise ValueError(
                "Experience provenance derived_at "
                "must be timezone-aware."
            )


@dataclass(frozen=True)
class ExperienceReference:
    """
    Immutable reference to another canonical concept.

    References preserve semantic traceability without transferring
    ownership and without creating parallel domain models.

    reference_kind identifies the role of the reference, for example:
    - EVIDENCE
    - CONTEXT

    The referenced concept remains owned by its own canonical authority.
    """

    concept: str
    identity: str
    reference_kind: str

    def __post_init__(self) -> None:
        if not self.concept.strip():
            raise ValueError(
                "Experience reference requires a concept."
            )

        if not self.identity.strip():
            raise ValueError(
                "Experience reference requires an identity."
            )

        if not self.reference_kind.strip():
            raise ValueError(
                "Experience reference requires a reference kind."
            )


@dataclass(frozen=True)
class ExperienceTemporalContext:
    """
    Canonical temporal context of derived Experience.

    evidence_start/evidence_end describe the represented evidence period
    where a period is applicable.

    derived_at identifies when the Experience was derived.

    These timestamps are deliberately distinct.
    """

    evidence_start: datetime | None
    evidence_end: datetime | None
    derived_at: datetime

    def __post_init__(self) -> None:
        if self.derived_at.tzinfo is None:
            raise ValueError(
                "Experience temporal context derived_at "
                "must be timezone-aware."
            )

        if (
            self.evidence_start is not None
            and self.evidence_start.tzinfo is None
        ):
            raise ValueError(
                "Experience evidence_start "
                "must be timezone-aware."
            )

        if (
            self.evidence_end is not None
            and self.evidence_end.tzinfo is None
        ):
            raise ValueError(
                "Experience evidence_end "
                "must be timezone-aware."
            )

        if (
            self.evidence_start is not None
            and self.evidence_end is not None
            and self.evidence_start > self.evidence_end
        ):
            raise ValueError(
                "Experience evidence_start must not be after "
                "evidence_end."
            )


def _freeze_value(value: object) -> object:
    """
    Convert supported structured values into immutable representations.

    Experience preserves derived knowledge structure without introducing
    semantics belonging to another canonical authority.
    """

    if isinstance(value, Mapping):
        return MappingProxyType(
            {
                key: _freeze_value(item)
                for key, item in value.items()
            }
        )

    if isinstance(value, list):
        return tuple(
            _freeze_value(item)
            for item in value
        )

    if isinstance(value, tuple):
        return tuple(
            _freeze_value(item)
            for item in value
        )

    if isinstance(value, set):
        return frozenset(
            _freeze_value(item)
            for item in value
        )

    return value


@dataclass(frozen=True)
class ExperienceRecord:
    """
    Immutable canonical representation of derived organizational
    Experience.

    ExperienceRecord is distinct from:
    - MemoryRecord
    - Task
    - Agent
    - Capability
    - Resource State
    - Execution Result
    - Trust state
    - Learning state
    """

    experience_id: str
    subject: str
    scope: str
    derived_knowledge: object
    supporting_evidence: tuple[ExperienceReference, ...]
    contextual_references: tuple[ExperienceReference, ...]
    temporal_context: ExperienceTemporalContext
    provenance: ExperienceProvenance
    evidentiary_qualification: str | None = None
    metadata: Mapping[str, str] = MappingProxyType({})

    def __post_init__(self) -> None:
        if not self.experience_id.strip():
            raise ValueError(
                "Experience requires a canonical identity."
            )

        if not self.subject.strip():
            raise ValueError(
                "Experience requires a subject."
            )

        if not self.scope.strip():
            raise ValueError(
                "Experience requires a scope."
            )

        if self.derived_knowledge is None:
            raise ValueError(
                "Experience requires derived knowledge."
            )

        if (
            self.evidentiary_qualification is not None
            and not self.evidentiary_qualification.strip()
        ):
            raise ValueError(
                "Experience evidentiary qualification "
                "must not be empty."
            )

        evidence_references = tuple(
            self.supporting_evidence
        )
        context_references = tuple(
            self.contextual_references
        )

        for reference in evidence_references:
            if reference.reference_kind != "EVIDENCE":
                raise ValueError(
                    "Supporting Experience references must have "
                    "reference_kind='EVIDENCE'."
                )

        for reference in context_references:
            if reference.reference_kind != "CONTEXT":
                raise ValueError(
                    "Contextual Experience references must have "
                    "reference_kind='CONTEXT'."
                )

        object.__setattr__(
            self,
            "supporting_evidence",
            evidence_references,
        )

        object.__setattr__(
            self,
            "contextual_references",
            context_references,
        )

        object.__setattr__(
            self,
            "derived_knowledge",
            _freeze_value(self.derived_knowledge),
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


class ExperienceAuthority:
    """
    Sole canonical authority for mutable Experience state.

    Experience Authority owns Experience records.

    It does not:
    - preserve raw Memory evidence
    - calculate Trust
    - mutate Trust state
    - perform Learning
    - mutate Learning state
    - evaluate Tasks
    - select Agents
    - make Strategic Decisions
    - authorize execution
    - execute work
    - persist through external infrastructure
    """

    AUTHORITY_NAME = "Experience Authority"

    def __init__(
        self,
        initial_records: Mapping[str, ExperienceRecord] | None = None,
    ) -> None:
        self._records: dict[str, ExperienceRecord] = (
            dict(initial_records)
            if initial_records is not None
            else {}
        )

        for key, record in self._records.items():
            if not isinstance(record, ExperienceRecord):
                raise TypeError(
                    "Experience Authority initial records must "
                    "contain ExperienceRecord instances only."
                )

            if key != record.experience_id:
                raise ValueError(
                    "Experience record collection key must match "
                    "experience_id."
                )

    @property
    def records(
        self,
    ) -> Mapping[str, ExperienceRecord]:
        """
        Return the canonical Experience collection read-only.
        """

        return MappingProxyType(dict(self._records))

    def get_experience(
        self,
        experience_id: str,
    ) -> ExperienceRecord | None:
        """
        Return one canonical Experience record by identity.
        """

        return self._records.get(experience_id)

    def retain(
        self,
        *,
        experience_id: str,
        subject: str,
        scope: str,
        derived_knowledge: object,
        supporting_evidence: tuple[
            ExperienceReference,
            ...,
        ],
        contextual_references: tuple[
            ExperienceReference,
            ...,
        ] = (),
        temporal_context: ExperienceTemporalContext,
        provenance: ExperienceProvenance,
        evidentiary_qualification: str | None = None,
        metadata: Mapping[str, str] | None = None,
    ) -> ExperienceRecord:
        """
        Retain a new immutable canonical Experience record.

        Existing identities cannot be silently overwritten.

        Failure to derive or retain Experience does not modify the
        underlying evidence.
        """

        if experience_id in self._records:
            raise ValueError(
                "Conflicting Experience mutation: "
                f"experience '{experience_id}' already exists."
            )

        record = ExperienceRecord(
            experience_id=experience_id,
            subject=subject,
            scope=scope,
            derived_knowledge=derived_knowledge,
            supporting_evidence=supporting_evidence,
            contextual_references=contextual_references,
            temporal_context=temporal_context,
            provenance=provenance,
            evidentiary_qualification=(
                evidentiary_qualification
            ),
            metadata=(
                {}
                if metadata is None
                else metadata
            ),
        )

        self._records[experience_id] = record
        return record
