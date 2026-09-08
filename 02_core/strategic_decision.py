"""
AI Company Core — Strategic Decision

Canonical representation and ownership of Strategic Decisions.

Strategic Decision transforms organizational intent and objectives into
organizational direction.

This module owns only the canonical meaning and mutable state of Strategic
Decisions. It does not execute work, authorize execution, select agents,
evaluate tasks, manage tasks, or depend on external infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class DecisionProvenance:
    """Provenance attached to a canonical Strategic Decision."""

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("Decision provenance source must be non-empty.")

        if not isinstance(self.authority, str) or not self.authority.strip():
            raise ValueError("Decision provenance authority must be non-empty.")

        if not isinstance(self.timestamp, datetime):
            raise TypeError("Decision provenance timestamp must be a datetime.")


@dataclass(frozen=True)
class StrategicDecision:
    """
    Immutable canonical representation of a Strategic Decision.

    A Strategic Decision expresses organizational direction derived from
    canonical Intent and Objectives. It is not an execution instruction and
    does not authorize execution.
    """

    decision_id: str
    intent_id: str
    objective_ids: tuple[str, ...]
    strategic_direction: str
    context: Mapping[str, str]
    evidence: Mapping[str, str]
    provenance: DecisionProvenance

    def __post_init__(self) -> None:
        if not isinstance(self.decision_id, str) or not self.decision_id.strip():
            raise ValueError("Strategic Decision id must be non-empty.")

        if not isinstance(self.intent_id, str) or not self.intent_id.strip():
            raise ValueError("Strategic Decision intent_id must be non-empty.")

        if not isinstance(self.strategic_direction, str) or not self.strategic_direction.strip():
            raise ValueError("Strategic direction must be non-empty.")

        if not isinstance(self.objective_ids, tuple):
            raise TypeError("objective_ids must be a tuple.")

        for objective_id in self.objective_ids:
            if not isinstance(objective_id, str) or not objective_id.strip():
                raise ValueError("Every objective_id must be non-empty.")

        if not isinstance(self.provenance, DecisionProvenance):
            raise TypeError(
                "Strategic Decision provenance must be DecisionProvenance."
            )

        object.__setattr__(
            self,
            "context",
            MappingProxyType(dict(self.context)),
        )

        object.__setattr__(
            self,
            "evidence",
            MappingProxyType(dict(self.evidence)),
        )


class DecisionAuthority:
    """
    Sole canonical owner of mutable Strategic Decision state.

    DecisionAuthority owns Strategic Decision state transitions only.
    It does not create Tasks, select Agents, authorize execution, execute
    work, or communicate with external infrastructure.
    """

    def __init__(
        self,
        initial_decisions: Mapping[str, StrategicDecision] | None = None,
    ) -> None:
        if initial_decisions is None:
            self._decisions: dict[str, StrategicDecision] = {}
        else:
            self._decisions = dict(initial_decisions)

        for decision_id, decision in self._decisions.items():
            if not isinstance(decision_id, str) or not decision_id.strip():
                raise ValueError("Decision ids must be non-empty.")

            if not isinstance(decision, StrategicDecision):
                raise TypeError(
                    "DecisionAuthority can contain only StrategicDecision values."
                )

    @property
    def decisions(self) -> Mapping[str, StrategicDecision]:
        """Read-only view of the canonical Strategic Decision collection."""
        return MappingProxyType(dict(self._decisions))

    def get_decision(self, decision_id: str) -> StrategicDecision | None:
        """Return a canonical Strategic Decision by identity."""
        return self._decisions.get(decision_id)

    def set_decision(
        self,
        *,
        decision_id: str,
        intent_id: str,
        objective_ids: tuple[str, ...],
        strategic_direction: str,
        context: Mapping[str, str] | None = None,
        evidence: Mapping[str, str] | None = None,
        source: str,
        authority: str = "Decision Authority",
        timestamp: datetime | None = None,
    ) -> StrategicDecision:
        """
        Create and own a new canonical Strategic Decision.

        A decision identity cannot be silently replaced. Conflicting state
        requires an explicit update through update_decision().
        """
        if decision_id in self._decisions:
            raise ValueError(
                f"Strategic Decision '{decision_id}' already exists."
            )

        decision = StrategicDecision(
            decision_id=decision_id,
            intent_id=intent_id,
            objective_ids=tuple(objective_ids),
            strategic_direction=strategic_direction,
            context={} if context is None else context,
            evidence={} if evidence is None else evidence,
            provenance=DecisionProvenance(
                source=source,
                timestamp=(
                    datetime.now(timezone.utc)
                    if timestamp is None
                    else timestamp
                ),
                authority=authority,
            ),
        )

        self._decisions[decision_id] = decision
        return decision

    def update_decision(
        self,
        *,
        decision_id: str,
        strategic_direction: str | None = None,
        context: Mapping[str, str] | None = None,
        evidence: Mapping[str, str] | None = None,
        source: str | None = None,
        authority: str | None = None,
        timestamp: datetime | None = None,
    ) -> StrategicDecision:
        """
        Replace canonical Strategic Decision state with a new immutable value.

        Identity and canonical Intent/Objectives references remain stable.
        """
        existing = self._decisions.get(decision_id)

        if existing is None:
            raise KeyError(
                f"Strategic Decision '{decision_id}' does not exist."
            )

        if (
            strategic_direction is None
            and context is None
            and evidence is None
            and source is None
            and authority is None
            and timestamp is None
        ):
            raise ValueError("No Strategic Decision fields were provided.")

        updated = StrategicDecision(
            decision_id=existing.decision_id,
            intent_id=existing.intent_id,
            objective_ids=existing.objective_ids,
            strategic_direction=(
                existing.strategic_direction
                if strategic_direction is None
                else strategic_direction
            ),
            context=(
                existing.context
                if context is None
                else context
            ),
            evidence=(
                existing.evidence
                if evidence is None
                else evidence
            ),
            provenance=DecisionProvenance(
                source=(
                    existing.provenance.source
                    if source is None
                    else source
                ),
                timestamp=(
                    datetime.now(timezone.utc)
                    if timestamp is None
                    else timestamp
                ),
                authority=(
                    existing.provenance.authority
                    if authority is None
                    else authority
                ),
            ),
        )

        self._decisions[decision_id] = updated
        return updated
