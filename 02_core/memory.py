"""
AI Company Core — Canonical Memory Authority

Canonical preservation of organizational evidence for future organizational use.

Memory owns retained evidence, provenance, temporal context, and canonical
references.

Memory does not interpret evidence into:
- Experience
- Trust
- Learning
- Task Evaluation
- Agent Selection
- Strategic Decision
- Execution Readiness
- Execution Authorization
- Execution

This module is independent of:
- Runtime
- Integrations
- persistence systems
- databases
- external providers
- workflow engines
- OS-specific integration
- execution infrastructure
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from types import MappingProxyType
from typing import Mapping


class MemoryEvidenceState(str, Enum):
    """
    Canonical state of retained evidence.

    These states preserve uncertainty explicitly.

    In particular:
        UNAVAILABLE != false
        UNOBSERVED != false
    """

    KNOWN = "KNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    UNOBSERVED = "UNOBSERVED"
    INCOMPLETE = "INCOMPLETE"
    INCONSISTENT = "INCONSISTENT"


def _freeze_evidence(
    value: object,
) -> object:
    """
    Convert supported evidence structures into immutable representations.

    Memory preserves evidence content but does not assign domain semantics
    to that content.
    """

    if isinstance(value, Mapping):
        return MappingProxyType(
            {
                key: _freeze_evidence(item)
                for key, item in value.items()
            }
        )

    if isinstance(value, list):
        return tuple(
            _freeze_evidence(item)
            for item in value
        )

    if isinstance(value, tuple):
        return tuple(
            _freeze_evidence(item)
            for item in value
        )

    if isinstance(value, set):
        return frozenset(
            _freeze_evidence(item)
            for item in value
        )

    return value


@dataclass(frozen=True)
class MemoryProvenance:
    """
    Canonical provenance attached to retained evidence.

    evidence_timestamp identifies the temporal position of the originating
    evidence.

    Optional originating concept and identity identify the canonical
    organizational source of the evidence when such an origin exists.

    These fields identify provenance only. They do not transfer ownership
    of the originating concept to Memory.
    """

    source: str
    authority: str
    evidence_timestamp: datetime
    source_type: str | None = None
    originating_concept: str | None = None
    originating_identity: str | None = None

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Memory provenance requires a source."
            )

        if not self.authority.strip():
            raise ValueError(
                "Memory provenance requires an authority."
            )

        if self.evidence_timestamp.tzinfo is None:
            raise ValueError(
                "Memory provenance evidence_timestamp "
                "must be timezone-aware."
            )

        if (
            self.source_type is not None
            and not self.source_type.strip()
        ):
            raise ValueError(
                "Memory provenance source_type must not be empty."
            )

        if (
            self.originating_concept is None
            and self.originating_identity is not None
        ):
            raise ValueError(
                "Memory provenance originating_identity requires "
                "originating_concept."
            )

        if (
            self.originating_concept is not None
            and not self.originating_concept.strip()
        ):
            raise ValueError(
                "Memory provenance originating_concept must not be empty."
            )

        if (
            self.originating_identity is not None
            and not self.originating_identity.strip()
        ):
            raise ValueError(
                "Memory provenance originating_identity must not be empty."
            )


@dataclass(frozen=True)
class MemoryReference:
    """
    Immutable reference to another canonical organizational concept.

    A reference identifies another authority's state or evidence.

    It does not transfer ownership to Memory.
    """

    concept: str
    identity: str

    def __post_init__(self) -> None:
        if not self.concept.strip():
            raise ValueError(
                "Memory reference requires a concept."
            )

        if not self.identity.strip():
            raise ValueError(
                "Memory reference requires an identity."
            )


@dataclass(frozen=True)
class MemoryRecord:
    """
    Immutable canonical representation of retained organizational evidence.

    MemoryRecord preserves evidence and its provenance.

    evidence represents the preserved content. Its structure is deliberately
    domain-neutral; Memory does not interpret its meaning.

    retained_at identifies when Memory retained the evidence.

    It does not redefine the semantics of referenced concepts.
    """

    memory_id: str
    evidence: object | None
    evidence_state: MemoryEvidenceState
    provenance: MemoryProvenance
    retained_at: datetime
    references: tuple[MemoryReference, ...] = ()
    metadata: Mapping[str, str] = MappingProxyType({})

    def __post_init__(self) -> None:
        if not self.memory_id.strip():
            raise ValueError(
                "Memory Record requires a canonical identity."
            )

        if self.retained_at.tzinfo is None:
            raise ValueError(
                "Memory Record retained_at must be timezone-aware."
            )

        if not isinstance(
            self.evidence_state,
            MemoryEvidenceState,
        ):
            raise ValueError(
                "Memory Record requires a valid evidence state."
            )

        if (
            isinstance(self.evidence, str)
            and not self.evidence.strip()
        ):
            raise ValueError(
                "Memory evidence must be non-empty when provided."
            )

        if (
            self.evidence is None
            and self.evidence_state == MemoryEvidenceState.KNOWN
        ):
            raise ValueError(
                "KNOWN Memory evidence requires evidence content."
            )

        object.__setattr__(
            self,
            "evidence",
            _freeze_evidence(self.evidence),
        )

        object.__setattr__(
            self,
            "references",
            tuple(self.references),
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


class MemoryAuthority:
    """
    Sole canonical authority for mutable Memory state.

    Memory Authority preserves evidence.

    It does not:
    - interpret evidence;
    - evaluate Tasks;
    - select Agents;
    - calculate Trust;
    - create Experience;
    - produce Learning;
    - authorize execution;
    - execute work;
    - schedule work;
    - persist through external infrastructure.
    """

    AUTHORITY_NAME = "Memory Authority"

    def __init__(
        self,
        initial_records: Mapping[str, MemoryRecord] | None = None,
    ) -> None:
        self._records: dict[str, MemoryRecord] = (
            dict(initial_records)
            if initial_records is not None
            else {}
        )

        for key, record in self._records.items():
            if not isinstance(record, MemoryRecord):
                raise TypeError(
                    "Memory Authority initial records must contain "
                    "MemoryRecord instances only."
                )

            if key != record.memory_id:
                raise ValueError(
                    "Memory record collection key must match memory_id."
                )

    @property
    def records(self) -> Mapping[str, MemoryRecord]:
        """
        Return the canonical Memory collection read-only.
        """

        return MappingProxyType(dict(self._records))

    def get_record(
        self,
        memory_id: str,
    ) -> MemoryRecord | None:
        """
        Return one canonical Memory Record by identity.
        """

        return self._records.get(memory_id)

    def retain(
        self,
        *,
        memory_id: str,
        evidence: object | None,
        evidence_state: MemoryEvidenceState,
        provenance: MemoryProvenance,
        references: tuple[MemoryReference, ...] = (),
        metadata: Mapping[str, str] | None = None,
        retained_at: datetime | None = None,
    ) -> MemoryRecord:
        """
        Retain a new immutable Memory Record.

        Existing identities cannot be silently overwritten.
        """

        if memory_id in self._records:
            raise ValueError(
                "Conflicting memory mutation: "
                f"memory '{memory_id}' already exists."
            )

        record = MemoryRecord(
            memory_id=memory_id,
            evidence=evidence,
            evidence_state=evidence_state,
            provenance=provenance,
            retained_at=(
                retained_at
                if retained_at is not None
                else datetime.now(timezone.utc)
            ),
            references=references,
            metadata=(
                {}
                if metadata is None
                else metadata
            ),
        )

        self._records[memory_id] = record
        return record
