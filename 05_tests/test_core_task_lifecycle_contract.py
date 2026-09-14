"""
AI Company — Task Lifecycle Contract Tests

These tests verify the canonical Task Lifecycle State Machine.

Tests do not define the contract.
The canonical contract is defined by:

    01_docs/Task_Lifecycle_State_Machine_Canonical_Definition.md
"""

from datetime import datetime, timezone

import pytest

from core.task_lifecycle import (
    TaskLifecycleAuthority,
    TaskLifecycleState,
)


def transition(
    authority: TaskLifecycleAuthority,
    next_state: TaskLifecycleState,
):
    return authority.transition(
        next_state,
        cause="test",
        provenance="canonical-test",
        evidence="test-evidence",
    )


def test_canonical_state_set():
    assert {
        state.value
        for state in TaskLifecycleState
    } == {
        "CREATED",
        "IN_PROGRESS",
        "COMPLETED",
        "CANCELLED",
    }


def test_initial_state_is_created():
    authority = TaskLifecycleAuthority("task-1")

    assert authority.state is TaskLifecycleState.CREATED
    assert authority.history == ()


def test_terminal_states_are_canonical():
    assert TaskLifecycleAuthority.TERMINAL_STATES == {
        TaskLifecycleState.COMPLETED,
        TaskLifecycleState.CANCELLED,
    }


def test_valid_transition_graph():
    expected = {
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

    assert TaskLifecycleAuthority.VALID_TRANSITIONS == expected


@pytest.mark.parametrize(
    "previous_state,next_state",
    [
        (
            TaskLifecycleState.CREATED,
            TaskLifecycleState.CREATED,
        ),
        (
            TaskLifecycleState.CREATED,
            TaskLifecycleState.COMPLETED,
        ),
        (
            TaskLifecycleState.CREATED,
            TaskLifecycleState.CANCELLED,
        ),
        (
            TaskLifecycleState.IN_PROGRESS,
            TaskLifecycleState.CREATED,
        ),
        (
            TaskLifecycleState.IN_PROGRESS,
            TaskLifecycleState.IN_PROGRESS,
        ),
        (
            TaskLifecycleState.COMPLETED,
            TaskLifecycleState.CREATED,
        ),
        (
            TaskLifecycleState.COMPLETED,
            TaskLifecycleState.IN_PROGRESS,
        ),
        (
            TaskLifecycleState.COMPLETED,
            TaskLifecycleState.CANCELLED,
        ),
        (
            TaskLifecycleState.CANCELLED,
            TaskLifecycleState.CREATED,
        ),
        (
            TaskLifecycleState.CANCELLED,
            TaskLifecycleState.IN_PROGRESS,
        ),
        (
            TaskLifecycleState.CANCELLED,
            TaskLifecycleState.COMPLETED,
        ),
        (
            TaskLifecycleState.CANCELLED,
            TaskLifecycleState.CANCELLED,
        ),
    ],
)
def test_invalid_transitions_are_rejected(
    previous_state,
    next_state,
):
    authority = TaskLifecycleAuthority("task-1")

    if previous_state is TaskLifecycleState.IN_PROGRESS:
        transition(
            authority,
            TaskLifecycleState.IN_PROGRESS,
        )

    elif previous_state is not TaskLifecycleState.CREATED:
        raise AssertionError(
            "Unexpected test setup state"
        )

    with pytest.raises(ValueError):
        transition(authority, next_state)


def test_created_to_in_progress():
    authority = TaskLifecycleAuthority("task-1")

    record = transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    assert authority.state is TaskLifecycleState.IN_PROGRESS
    assert record.previous_state is TaskLifecycleState.CREATED
    assert record.next_state is TaskLifecycleState.IN_PROGRESS


def test_in_progress_to_completed():
    authority = TaskLifecycleAuthority("task-1")

    transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    record = transition(
        authority,
        TaskLifecycleState.COMPLETED,
    )

    assert authority.state is TaskLifecycleState.COMPLETED
    assert record.previous_state is TaskLifecycleState.IN_PROGRESS
    assert record.next_state is TaskLifecycleState.COMPLETED


def test_in_progress_to_cancelled():
    authority = TaskLifecycleAuthority("task-1")

    transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    record = transition(
        authority,
        TaskLifecycleState.CANCELLED,
    )

    assert authority.state is TaskLifecycleState.CANCELLED
    assert record.previous_state is TaskLifecycleState.IN_PROGRESS
    assert record.next_state is TaskLifecycleState.CANCELLED


@pytest.mark.parametrize(
    "terminal_state",
    [
        TaskLifecycleState.COMPLETED,
        TaskLifecycleState.CANCELLED,
    ],
)
def test_terminal_states_cannot_reopen(terminal_state):
    authority = TaskLifecycleAuthority("task-1")

    transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    transition(
        authority,
        terminal_state,
    )

    for next_state in TaskLifecycleState:
        with pytest.raises(ValueError):
            transition(authority, next_state)

    assert authority.state is terminal_state
    assert len(authority.history) == 2


def test_transition_requires_cause():
    authority = TaskLifecycleAuthority("task-1")

    with pytest.raises(ValueError):
        authority.transition(
            TaskLifecycleState.IN_PROGRESS,
            cause="",
            provenance="canonical-test",
            evidence="test-evidence",
        )


def test_transition_requires_provenance():
    authority = TaskLifecycleAuthority("task-1")

    with pytest.raises(ValueError):
        authority.transition(
            TaskLifecycleState.IN_PROGRESS,
            cause="test",
            provenance="",
            evidence="test-evidence",
        )


def test_transition_requires_evidence():
    authority = TaskLifecycleAuthority("task-1")

    with pytest.raises(ValueError):
        authority.transition(
            TaskLifecycleState.IN_PROGRESS,
            cause="test",
            provenance="canonical-test",
            evidence="",
        )


def test_transition_history_is_append_only_from_public_api():
    authority = TaskLifecycleAuthority("task-1")

    first = transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    second = transition(
        authority,
        TaskLifecycleState.COMPLETED,
    )

    assert authority.history == (first, second)


def test_transition_record_contains_required_canonical_fields():
    authority = TaskLifecycleAuthority("task-1")

    record = transition(
        authority,
        TaskLifecycleState.IN_PROGRESS,
    )

    assert record.task_id == "task-1"
    assert record.previous_state is TaskLifecycleState.CREATED
    assert record.next_state is TaskLifecycleState.IN_PROGRESS
    assert record.cause == "test"
    assert record.provenance == "canonical-test"
    assert record.evidence == "test-evidence"
    assert record.validation_result == "VALID"
    assert isinstance(record.timestamp, datetime)
    assert record.timestamp.tzinfo is timezone.utc


def test_failed_execution_result_is_not_a_lifecycle_state():
    assert "FAILED" not in {
        state.value
        for state in TaskLifecycleState
    }


def test_readiness_states_are_not_lifecycle_states():
    lifecycle_values = {
        state.value
        for state in TaskLifecycleState
    }

    assert "READY" not in lifecycle_values
    assert "DEGRADED" not in lifecycle_values
    assert "BLOCKED" not in lifecycle_values
    assert "UNAVAILABLE" not in lifecycle_values
