"""
AI Company Core — Canonical Task Queue

Canonical representation and ownership of pending Task Queue State.

The Task Queue owns only:
- pending-work membership
- pending-work ordering
- pending-work retrieval

The Task Queue does NOT own:
- Task definition
- Task lifecycle state
- Task evaluation
- Agent selection
- execution readiness
- execution authorization
- execution
- strategic decisions
- execution attempts
- execution results

Task definitions remain owned by Task Authority.

Queue ordering is governed by an explicit queue policy. The Queue does
not infer queue policy from Task semantics such as priority.

This module belongs to the canonical Core layer and must remain
independent of:
- Runtime
- Integrations
- Tools
- Weft
- external providers
- workflow engines
- persistence systems
- execution infrastructure
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable, Mapping

from .task import Task


TaskOrderingPolicy = Callable[[tuple[Task, ...]], tuple[Task, ...]]


@dataclass(frozen=True)
class QueueProvenance:
    """
    Provenance describing the creation of a Queue Authority instance.
    """

    source: str

    def __post_init__(self) -> None:
        if not self.source.strip():
            raise ValueError(
                "Queue provenance requires a source."
            )


class TaskQueue:
    """
    Canonical pending-work queue.

    TaskQueue owns queue membership and ordering only.

    It never mutates a Task definition.
    """

    def __init__(
        self,
        *,
        ordering_policy: TaskOrderingPolicy,
        provenance: QueueProvenance,
    ) -> None:
        if not callable(ordering_policy):
            raise TypeError(
                "Task Queue requires an explicit ordering policy."
            )

        self._ordering_policy = ordering_policy
        self._provenance = provenance
        self._pending: dict[str, Task] = {}

    @property
    def provenance(self) -> QueueProvenance:
        """
        Return queue provenance.
        """
        return self._provenance

    @property
    def pending(self) -> Mapping[str, Task]:
        """
        Return pending queue state as a read-only mapping.
        """
        return MappingProxyType(dict(self._pending))

    @property
    def size(self) -> int:
        """
        Return the number of pending Tasks.
        """
        return len(self._pending)

    def enqueue(self, task: Task) -> None:
        """
        Add an existing canonical Task to pending queue state.

        Queue membership does not transfer Task-definition ownership.
        """
        if not isinstance(task, Task):
            raise TypeError(
                "Task Queue accepts canonical Task instances only."
            )

        if task.task_id in self._pending:
            raise ValueError(
                "Duplicate queue entry: "
                f"task '{task.task_id}' is already queued."
            )

        self._pending[task.task_id] = task

    def peek(self) -> Task | None:
        """
        Return the next pending Task without changing queue state.
        """
        ordered = self._ordered_pending()

        if not ordered:
            return None

        return ordered[0]

    def dequeue(self) -> Task | None:
        """
        Remove and return the next pending Task.

        Dequeue changes only Queue State.
        It does not mutate Task lifecycle state.
        """
        task = self.peek()

        if task is None:
            return None

        del self._pending[task.task_id]
        return task

    def contains(self, task_id: str) -> bool:
        """
        Return whether a Task identity is currently pending.
        """
        return task_id in self._pending

    def _ordered_pending(self) -> tuple[Task, ...]:
        """
        Apply the explicit queue ordering policy.

        The policy receives an immutable snapshot and must return an
        ordered tuple of the same canonical Tasks.
        """
        snapshot = tuple(self._pending.values())
        ordered = self._ordering_policy(snapshot)

        if not isinstance(ordered, tuple):
            raise TypeError(
                "Queue ordering policy must return a tuple of Tasks."
            )

        expected_ids = {
            task.task_id
            for task in snapshot
        }

        actual_ids = {
            task.task_id
            for task in ordered
        }

        if actual_ids != expected_ids:
            raise ValueError(
                "Queue ordering policy must preserve queue membership."
            )

        if len(ordered) != len(snapshot):
            raise ValueError(
                "Queue ordering policy must not duplicate Tasks."
            )

        return ordered


class QueueAuthority:
    """
    Sole canonical authority for mutable Task Queue State.

    Queue Authority owns pending-work membership and ordering retrieval.

    It does not:
    - redefine Tasks
    - mutate Task definitions
    - mutate Task lifecycle state
    - evaluate Tasks
    - select Agents
    - determine readiness
    - authorize execution
    - execute work
    - make strategic decisions
    - create execution attempts
    - create execution results
    - persist state
    - communicate with external systems
    """

    def __init__(
        self,
        *,
        ordering_policy: TaskOrderingPolicy,
        source: str,
    ) -> None:
        self._queue = TaskQueue(
            ordering_policy=ordering_policy,
            provenance=QueueProvenance(source=source),
        )

    @property
    def queue_state(self) -> Mapping[str, Task]:
        """
        Return the canonical queue state as read-only data.

        The mutable TaskQueue remains internal to Queue Authority.
        Callers cannot bypass Queue Authority to mutate queue state.
        """
        return self._queue.pending

    def enqueue(self, task: Task) -> None:
        """
        Add a canonical Task to pending queue state.
        """
        self._queue.enqueue(task)

    def peek(self) -> Task | None:
        """
        Return the next pending Task without removing it.
        """
        return self._queue.peek()

    def dequeue(self) -> Task | None:
        """
        Remove and return the next pending Task.
        """
        return self._queue.dequeue()

    def contains(self, task_id: str) -> bool:
        """
        Return whether a Task is pending.
        """
        return self._queue.contains(task_id)

    @property
    def size(self) -> int:
        """
        Return the number of pending Tasks.
        """
        return self._queue.size

    @property
    def pending(self) -> Mapping[str, Task]:
        """
        Return pending queue state as read-only data.
        """
        return self._queue.pending
