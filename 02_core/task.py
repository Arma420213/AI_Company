"""
AI Company Core — Canonical Task

Canonical representation and ownership of Company Tasks.

A Task represents the canonical definition of intended company work.

This module belongs to the canonical Core layer.

A Task contains only:
- Task Identity
- Task Intent
- Task Requirements
- Task Constraints
- Task Priority
- Task Metadata

The following are deliberately separate domains and are NOT part of
the canonical Task definition:
- Task Lifecycle State
- Execution Attempts
- Execution Context
- Execution Authorization
- Execution Results
- Observations
- Learning Evidence

This module must remain independent of:
- Runtime
- Integrations
- Tools
- Weft
- external providers
- workflow engines
- persistence systems
- execution infrastructure

Task Authority is the sole owner of mutable canonical Task state.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from types import MappingProxyType
from typing import Mapping


@dataclass(frozen=True)
class TaskProvenance:
    """
    Canonical provenance attached to a Task definition.

    Provider-specific identifiers do not become canonical Task identity.
    """

    source: str
    timestamp: datetime
    authority: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Task provenance requires a source."
            )

        if not self.authority.strip():
            raise ValueError(
                "Task provenance requires an authority."
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Task provenance timestamp must be timezone-aware."
            )


@dataclass(frozen=True)
class Task:
    """
    Immutable canonical representation of intended company work.

    Task is the canonical definition of work.

    Task is not:
    - Task Lifecycle State
    - a Task Queue entry
    - an Execution Attempt
    - an Execution Context
    - an Execution Authorization
    - an Execution Result
    - an Observation
    - Learning Evidence
    """

    task_id: str
    intent: str
    requirements: Mapping[str, str]
    constraints: Mapping[str, str]
    priority: str
    metadata: Mapping[str, str]
    provenance: TaskProvenance

    def __post_init__(self) -> None:
        if not self.task_id.strip():
            raise ValueError(
                "Task requires a canonical identity."
            )

        if not self.intent.strip():
            raise ValueError(
                "Task requires a canonical intent."
            )

        if not self.priority.strip():
            raise ValueError(
                "Task requires a canonical priority."
            )

        object.__setattr__(
            self,
            "requirements",
            MappingProxyType(dict(self.requirements)),
        )

        object.__setattr__(
            self,
            "constraints",
            MappingProxyType(dict(self.constraints)),
        )

        object.__setattr__(
            self,
            "metadata",
            MappingProxyType(dict(self.metadata)),
        )


class TaskAuthority:
    """
    Sole canonical authority for mutable Task state.

    Task Authority owns the canonical collection of Task definitions.

    It does not:
    - manage Task lifecycle
    - queue Tasks
    - evaluate Task feasibility
    - select Agents
    - determine execution readiness
    - authorize execution
    - execute work
    - create Execution Attempts
    - create Execution Results
    - persist state
    - communicate with external systems
    """

    def __init__(
        self,
        initial_tasks: Mapping[str, Task] | None = None,
    ) -> None:
        if initial_tasks is None:
            self._tasks: dict[str, Task] = {}
        else:
            self._tasks = dict(initial_tasks)

    @property
    def tasks(self) -> Mapping[str, Task]:
        """
        Return the canonical Task collection read-only.
        """
        return MappingProxyType(dict(self._tasks))

    def get_task(
        self,
        task_id: str,
    ) -> Task | None:
        """
        Return one canonical Task by identity.
        """
        return self._tasks.get(task_id)

    def create_task(
        self,
        *,
        task_id: str,
        intent: str,
        requirements: Mapping[str, str],
        constraints: Mapping[str, str],
        priority: str,
        metadata: Mapping[str, str],
        source: str,
    ) -> Task:
        """
        Establish a new canonical Task definition.

        Existing Task identities cannot be silently overwritten.
        """

        if task_id in self._tasks:
            raise ValueError(
                "Conflicting task mutation: "
                f"task '{task_id}' already exists."
            )

        task = Task(
            task_id=task_id,
            intent=intent,
            requirements=requirements,
            constraints=constraints,
            priority=priority,
            metadata=metadata,
            provenance=TaskProvenance(
                source=source,
                timestamp=datetime.now(timezone.utc),
                authority="Task Authority",
            ),
        )

        self._tasks[task_id] = task
        return task
