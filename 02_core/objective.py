"""
AI Company Core — Company Objective

Canonical representation and ownership of Company Objectives.

Company Objective represents a desired organizational outcome derived from
Company Intent and organizational direction.

This module belongs to the canonical Core layer.

It must remain independent of:
- Runtime
- Integrations
- Tools
- external providers
- workflow engines
- persistence systems
- execution infrastructure

Objective Authority is the sole owner of mutable canonical Company
Objective state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping

from intent import CompanyIntent


@dataclass(frozen=True)
class ObjectiveProvenance:
    """
    Canonical provenance attached to an accepted Company Objective state.

    Provider-specific identifiers do not become canonical identity.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Company Objective provenance requires a source."
            )

        if not self.authority.strip():
            raise ValueError(
                "Company Objective provenance requires an authority."
            )


@dataclass(frozen=True)
class CompanyObjective:
    """
    Immutable canonical representation of a Company Objective.

    A Company Objective represents a desired organizational outcome.

    The originating Company Intent is represented through its stable
    canonical identity.

    It is not:
    - Company Intent
    - a Strategic Decision
    - a Task
    - an Execution Proposal
    - an Execution Authorization
    - an Execution Attempt
    - an Execution Result
    """

    objective_id: str
    intent_id: str
    desired_outcome: str
    provenance: ObjectiveProvenance

    def __post_init__(self) -> None:
        if not self.objective_id.strip():
            raise ValueError(
                "Company Objective requires a canonical identity."
            )

        if not self.intent_id.strip():
            raise ValueError(
                "Company Objective requires a canonical Intent reference."
            )

        if not self.desired_outcome.strip():
            raise ValueError(
                "Company Objective requires a desired organizational outcome."
            )


class ObjectiveAuthority:
    """
    Sole canonical owner of mutable Company Objective state.

    Objective Authority owns the canonical collection of Company Objectives.

    It does not:
    - create Strategic Decisions
    - create Tasks
    - evaluate Tasks
    - select Agents
    - authorize execution
    - execute work
    - persist state
    - communicate with external systems

    Objective creation and updates are explicit state transitions.
    """

    def __init__(
        self,
        initial_objectives: Mapping[str, CompanyObjective] | None = None,
    ) -> None:
        if initial_objectives is None:
            self._objectives: dict[str, CompanyObjective] = {}
        else:
            self._objectives = dict(initial_objectives)

    @property
    def objectives(self) -> Mapping[str, CompanyObjective]:
        """
        Return the canonical Company Objective collection read-only.
        """
        return MappingProxyType(dict(self._objectives))

    def get_objective(
        self,
        objective_id: str,
    ) -> CompanyObjective | None:
        """
        Return one canonical Company Objective by identity.
        """
        return self._objectives.get(objective_id)

    def set_objective(
        self,
        *,
        objective_id: str,
        intent: CompanyIntent,
        desired_outcome: str,
        source: str,
    ) -> CompanyObjective:
        """
        Establish a new canonical Company Objective.

        A Company Intent object is required as the semantic input.

        Existing objective identities cannot be silently overwritten.
        """

        if not isinstance(intent, CompanyIntent):
            raise TypeError(
                "Objective Authority requires a canonical CompanyIntent."
            )

        if objective_id in self._objectives:
            raise ValueError(
                "Conflicting objective mutation: "
                f"objective '{objective_id}' already exists."
            )

        objective = CompanyObjective(
            objective_id=objective_id,
            intent_id=intent.intent_id,
            desired_outcome=desired_outcome,
            provenance=ObjectiveProvenance(
                source=source,
                timestamp=datetime.now(timezone.utc),
                authority="Objective Authority",
            ),
        )

        self._objectives[objective_id] = objective
        return objective

    def update_objective(
        self,
        *,
        objective_id: str,
        desired_outcome: str,
        source: str,
    ) -> CompanyObjective:
        """
        Explicitly update an existing Company Objective.

        The originating Intent reference is immutable and is preserved.

        Updating an Objective creates a new immutable canonical state with
        fresh provenance.
        """

        existing = self._objectives.get(objective_id)

        if existing is None:
            raise KeyError(
                f"Company Objective '{objective_id}' does not exist."
            )

        updated = CompanyObjective(
            objective_id=existing.objective_id,
            intent_id=existing.intent_id,
            desired_outcome=desired_outcome,
            provenance=ObjectiveProvenance(
                source=source,
                timestamp=datetime.now(timezone.utc),
                authority="Objective Authority",
            ),
        )

        self._objectives[objective_id] = updated
        return updated
