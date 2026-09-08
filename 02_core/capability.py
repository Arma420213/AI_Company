"""
AI Company — Canonical Capability Core Contract

Capability defines what can potentially be performed and its
canonical availability semantics.

This module belongs to the Core layer.

It does not:
- execute Tasks
- schedule Tasks
- select Agents
- authorize execution
- make strategic decisions
- depend on Runtime
- depend on Integrations
- depend on external providers
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class CapabilityProvenance:
    """
    Provenance describing where the capability information came from.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError("Capability provenance source must not be empty.")

        if not self.authority.strip():
            raise ValueError("Capability provenance authority must not be empty.")

        if self.timestamp.tzinfo is None:
            raise ValueError("Capability provenance timestamp must be timezone-aware.")


@dataclass(frozen=True)
class Capability:
    """
    Canonical representation of an organizational capability.

    A Capability describes potential ability.

    Capability is deliberately separated from:
    - Agent identity
    - execution
    - readiness
    - authorization
    """

    capability_id: str
    name: str
    description: str
    availability_state: str
    availability_evidence: Mapping[str, str]
    provenance: CapabilityProvenance

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("Capability ID must not be empty.")

        if not self.name.strip():
            raise ValueError("Capability name must not be empty.")

        if not self.description.strip():
            raise ValueError("Capability description must not be empty.")

        if not self.availability_state.strip():
            raise ValueError("Capability availability state must not be empty.")

        object.__setattr__(
            self,
            "availability_evidence",
            MappingProxyType(dict(self.availability_evidence)),
        )


class CapabilityAuthority:
    """
    Sole canonical authority for Capability semantics and availability.

    The authority owns the mutable collection of canonical capabilities
    while individual Capability objects remain immutable.

    It does not execute work, schedule work, authorize execution,
    or make strategic decisions.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}

    def get_capability(self, capability_id: str) -> Capability:
        """
        Return the canonical Capability identified by capability_id.
        """
        try:
            return self._capabilities[capability_id]
        except KeyError as exc:
            raise KeyError(
                f"Unknown capability: {capability_id}"
            ) from exc

    def set_capability(self, capability: Capability) -> Capability:
        """
        Register or replace a canonical Capability.

        Replacement returns the new immutable Capability state.
        """
        self._capabilities[capability.capability_id] = capability
        return capability

    def set_availability(
        self,
        capability_id: str,
        availability_state: str,
        availability_evidence: Mapping[str, str] | None = None,
    ) -> Capability:
        """
        Update canonical capability availability.

        The existing Capability definition is preserved while a new
        immutable Capability state is created.
        """
        if not availability_state.strip():
            raise ValueError("Capability availability state must not be empty.")

        current = self.get_capability(capability_id)

        evidence = (
            current.availability_evidence
            if availability_evidence is None
            else availability_evidence
        )

        updated = Capability(
            capability_id=current.capability_id,
            name=current.name,
            description=current.description,
            availability_state=availability_state,
            availability_evidence=evidence,
            provenance=CapabilityProvenance(
                source="capability_authority",
                timestamp=datetime.now(timezone.utc),
                authority="CapabilityAuthority",
            ),
        )

        self._capabilities[capability_id] = updated
        return updated

    def all_capabilities(self) -> Mapping[str, Capability]:
        """
        Return a read-only view of canonical capabilities.
        """
        return MappingProxyType(self._capabilities)
