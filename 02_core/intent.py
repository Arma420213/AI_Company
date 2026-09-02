"""
AI Company Core — Company Intent

Canonical representation and ownership of Company Intent.

Company Intent represents the organizational purpose and desired direction
of AI Company.

This module belongs to the canonical Core layer.

It must remain independent of:
- Runtime
- Integrations
- Tools
- external providers
- workflow engines
- persistence systems
- execution infrastructure

Intent Authority is the sole owner of mutable canonical Company Intent state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class IntentProvenance:
    """
    Canonical provenance attached to an accepted Company Intent state.

    Provider-specific identifiers do not become canonical identity.
    """

    source: str
    timestamp: datetime
    authority: str


@dataclass(frozen=True)
class CompanyIntent:
    """
    Immutable canonical representation of Company Intent.

    Company Intent expresses organizational purpose and desired direction.
    It is not a Task, Objective, Strategic Decision, or execution instruction.
    """

    intent_id: str
    purpose: str
    desired_direction: str
    organizational_context: Mapping[str, str]
    provenance: IntentProvenance

    def __post_init__(self) -> None:
        if not self.intent_id.strip():
            raise ValueError("Company Intent requires a canonical identity.")

        if not self.purpose.strip():
            raise ValueError("Company Intent requires an organizational purpose.")

        if not self.desired_direction.strip():
            raise ValueError(
                "Company Intent requires a desired organizational direction."
            )

        if not self.provenance.source.strip():
            raise ValueError("Company Intent provenance requires a source.")

        if not self.provenance.authority.strip():
            raise ValueError("Company Intent provenance requires an authority.")


class IntentAuthority:
    """
    Sole canonical owner of mutable Company Intent state.

    The authority validates and replaces Company Intent state.

    It does not:
    - create Objectives
    - create Tasks
    - make Strategic Decisions
    - select Agents
    - authorize execution
    - execute work
    - persist state
    - communicate with external systems
    """

    def __init__(self, initial_intent: CompanyIntent | None = None) -> None:
        self._current_intent = initial_intent

    @property
    def current_intent(self) -> CompanyIntent | None:
        """Return the current canonical Company Intent."""
        return self._current_intent

    def set_intent(
        self,
        *,
        intent_id: str,
        purpose: str,
        desired_direction: str,
        organizational_context: Mapping[str, str],
        source: str,
    ) -> CompanyIntent:
        """
        Establish or replace the canonical Company Intent.

        State mutation is explicit and remains owned by Intent Authority.
        """

        intent = CompanyIntent(
            intent_id=intent_id,
            purpose=purpose,
            desired_direction=desired_direction,
            organizational_context=MappingProxyType(
                dict(organizational_context)
            ),
            provenance=IntentProvenance(
                source=source,
                timestamp=datetime.now(timezone.utc),
                authority="Intent Authority",
            ),
        )

        self._current_intent = intent
        return intent
