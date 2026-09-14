"""
AI Company — Canonical Task Lifecycle Authority

Owns the canonical lifecycle state of a Task.

This module is subordinate to:
    00_architecture/AI_Company_Canonical_Architecture.md

and:
    01_docs/Task_Lifecycle_State_Machine_Canonical_Definition.md

The Task Lifecycle Authority owns:
- current Task lifecycle state;
- valid lifecycle transitions;
- transition validation;
- terminal-state protection;
- lifecycle history;
- transition causality.

It does NOT own:
- Task definition;
- Queue state;
- Execution Readiness;
- Execution Authorization;
- Execution Attempt state;
- Execution Result;
- Runtime state;
- Integration state.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum


class TaskLifecycleState(str, Enum):
    CREATED = "CREATED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


@dataclass(frozen=True)
class TaskLifecycleTransition:
    task_id: str
    previous_state: TaskLifecycleState
    next_state: TaskLifecycleState
    cause: str
    provenance: str
    evidence: str
    validation_result: str
    timestamp: datetime


class TaskLifecycleAuthority:
    """
    Canonical owner of Task Lifecycle State.
    """

    INITIAL_STATE = TaskLifecycleState.CREATED

    TERMINAL_STATES = frozenset(
        {
            TaskLifecycleState.COMPLETED,
            TaskLifecycleState.CANCELLED,
        }
    )

    VALID_TRANSITIONS = frozenset(
        {
            (
                TaskLifecycleState.CREATED,
                TaskLifecycleState.IN_PROGRESS,
            ),
            (
                TaskLifecycleState.IN_PROGRESS,
                TaskLifecycleState.COMPLETED,
            ),
            (
                TaskLifecycleState.IN_PROGRESS,
                TaskLifecycleState.CANCELLED,
            ),
        }
    )

    def __init__(self, task_id: str):
        if not task_id:
            raise ValueError("task_id must not be empty")

        self._task_id = task_id
        self._state = self.INITIAL_STATE
        self._history = []

    @property
    def task_id(self) -> str:
        return self._task_id

    @property
    def state(self) -> TaskLifecycleState:
        return self._state

    @property
    def history(self) -> tuple[TaskLifecycleTransition, ...]:
        return tuple(self._history)

    def can_transition(
        self,
        next_state: TaskLifecycleState,
    ) -> bool:
        return (self._state, next_state) in self.VALID_TRANSITIONS

    def transition(
        self,
        next_state: TaskLifecycleState,
        *,
        cause: str,
        provenance: str,
        evidence: str,
    ) -> TaskLifecycleTransition:
        if not cause:
            raise ValueError("cause must not be empty")

        if not provenance:
            raise ValueError("provenance must not be empty")

        if not evidence:
            raise ValueError("evidence must not be empty")

        previous_state = self._state

        if not self.can_transition(next_state):
            raise ValueError(
                f"invalid Task lifecycle transition: "
                f"{previous_state.value} -> {next_state.value}"
            )

        timestamp = datetime.now(timezone.utc)

        record = TaskLifecycleTransition(
            task_id=self._task_id,
            previous_state=previous_state,
            next_state=next_state,
            cause=cause,
            provenance=provenance,
            evidence=evidence,
            validation_result="VALID",
            timestamp=timestamp,
        )

        self._state = next_state
        self._history.append(record)

        return record
