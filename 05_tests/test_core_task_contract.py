"""
AI Company — Canonical Task Contract Tests

Python standard-library only.
No pytest dependency.

These tests verify the canonical Task contract defined by:
    00_architecture/AI_Company_Canonical_Architecture.md
    01_docs/AI_Company_Core_Contract_Specification.md
    01_docs/AI_Company_Core_Module_Derivation.md

Task is the canonical definition of intended work.

Task is NOT:
- lifecycle state
- execution attempt
- execution result
- observation
- learning evidence
- queue state
- task evaluation
- agent selection
- execution readiness
- execution authorization
"""

from __future__ import annotations

import ast
import dataclasses
import datetime
import sys
from pathlib import Path
from types import MappingProxyType


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "02_core"
TASK_FILE = CORE / "task.py"

if str(CORE) not in sys.path:
    sys.path.insert(0, str(CORE))

from task import Task, TaskAuthority, TaskProvenance


def expect_exception(exception_type, callable_obj):
    try:
        callable_obj()
    except exception_type:
        return
    except Exception as exc:
        raise AssertionError(
            f"Expected {exception_type.__name__}, "
            f"got {type(exc).__name__}: {exc}"
        ) from exc

    raise AssertionError(
        f"Expected {exception_type.__name__}, but no exception was raised"
    )


def test_canonical_symbols_exist():
    assert dataclasses.is_dataclass(Task)
    assert dataclasses.is_dataclass(TaskProvenance)
    assert isinstance(TaskAuthority, type)


def test_task_exact_fields():
    expected = (
        "task_id",
        "intent",
        "requirements",
        "constraints",
        "priority",
        "metadata",
        "provenance",
    )

    actual = tuple(field.name for field in dataclasses.fields(Task))

    assert actual == expected, (
        f"Unexpected Task fields: {actual}"
    )


def test_task_provenance_exact_fields():
    expected = (
        "source",
        "timestamp",
        "authority",
    )

    actual = tuple(
        field.name for field in dataclasses.fields(TaskProvenance)
    )

    assert actual == expected, (
        f"Unexpected TaskProvenance fields: {actual}"
    )


def build_provenance():
    return TaskProvenance(
        source="test",
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        authority="Test Authority",
    )


def build_task():
    return Task(
        task_id="task-001",
        intent="Test canonical work",
        requirements={"skill": "python"},
        constraints={"scope": "local"},
        priority="normal",
        metadata={"origin": "test"},
        provenance=build_provenance(),
    )


def test_task_construction():
    task = build_task()

    assert task.task_id == "task-001"
    assert task.intent == "Test canonical work"
    assert task.priority == "normal"
    assert task.provenance.authority == "Test Authority"


def test_task_is_frozen():
    task = build_task()

    expect_exception(
        dataclasses.FrozenInstanceError,
        lambda: setattr(task, "priority", "high"),
    )


def test_task_provenance_is_frozen():
    provenance = build_provenance()

    expect_exception(
        dataclasses.FrozenInstanceError,
        lambda: setattr(provenance, "source", "changed"),
    )


def test_task_mappings_are_immutable():
    task = build_task()

    assert isinstance(task.requirements, MappingProxyType)
    assert isinstance(task.constraints, MappingProxyType)
    assert isinstance(task.metadata, MappingProxyType)

    def mutate_requirements():
        task.requirements["new"] = "value"

    def mutate_constraints():
        task.constraints["new"] = "value"

    def mutate_metadata():
        task.metadata["new"] = "value"

    expect_exception(TypeError, mutate_requirements)
    expect_exception(TypeError, mutate_constraints)
    expect_exception(TypeError, mutate_metadata)


def test_task_mapping_defensive_copy():
    requirements = {"skill": "python"}
    constraints = {"scope": "local"}
    metadata = {"origin": "test"}

    task = Task(
        task_id="task-002",
        intent="Defensive copy test",
        requirements=requirements,
        constraints=constraints,
        priority="normal",
        metadata=metadata,
        provenance=build_provenance(),
    )

    requirements["skill"] = "changed"
    constraints["scope"] = "changed"
    metadata["origin"] = "changed"

    assert task.requirements["skill"] == "python"
    assert task.constraints["scope"] == "local"
    assert task.metadata["origin"] == "test"


def test_task_rejects_empty_task_id():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="",
            intent="test",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_task_rejects_blank_task_id():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="   ",
            intent="test",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_task_rejects_empty_intent():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="task-invalid",
            intent="",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_task_rejects_blank_intent():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="task-invalid",
            intent="   ",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_task_rejects_empty_priority():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="task-invalid",
            intent="test",
            requirements={},
            constraints={},
            priority="",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_task_rejects_blank_priority():
    expect_exception(
        ValueError,
        lambda: Task(
            task_id="task-invalid",
            intent="test",
            requirements={},
            constraints={},
            priority="   ",
            metadata={},
            provenance=build_provenance(),
        ),
    )


def test_provenance_rejects_empty_source():
    expect_exception(
        ValueError,
        lambda: TaskProvenance(
            source="",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            authority="Test Authority",
        ),
    )


def test_provenance_rejects_blank_source():
    expect_exception(
        ValueError,
        lambda: TaskProvenance(
            source="   ",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            authority="Test Authority",
        ),
    )


def test_provenance_rejects_empty_authority():
    expect_exception(
        ValueError,
        lambda: TaskProvenance(
            source="test",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            authority="",
        ),
    )


def test_provenance_rejects_blank_authority():
    expect_exception(
        ValueError,
        lambda: TaskProvenance(
            source="test",
            timestamp=datetime.datetime.now(datetime.timezone.utc),
            authority="   ",
        ),
    )


def test_provenance_requires_timezone_aware_timestamp():
    expect_exception(
        ValueError,
        lambda: TaskProvenance(
            source="test",
            timestamp=datetime.datetime.now(),
            authority="Test Authority",
        ),
    )


def test_task_authority_creates_and_owns_tasks():
    authority = TaskAuthority()

    task = authority.create_task(
        task_id="authority-task-001",
        intent="Authority creation test",
        requirements={"skill": "python"},
        constraints={"scope": "local"},
        priority="high",
        metadata={"origin": "test"},
        source="test",
    )

    assert isinstance(task, Task)
    assert authority.get_task(task.task_id) is task
    assert task.provenance.authority == "Task Authority"


def test_task_authority_exposes_read_only_collection():
    authority = TaskAuthority()

    authority.create_task(
        task_id="authority-task-002",
        intent="Read-only collection test",
        requirements={},
        constraints={},
        priority="normal",
        metadata={},
        source="test",
    )

    tasks = authority.tasks

    assert isinstance(tasks, MappingProxyType)
    assert tasks["authority-task-002"].task_id == "authority-task-002"

    def mutate_tasks():
        tasks["other"] = build_task()

    expect_exception(TypeError, mutate_tasks)


def test_task_authority_rejects_duplicate_identity():
    authority = TaskAuthority()

    authority.create_task(
        task_id="duplicate-task",
        intent="First task",
        requirements={},
        constraints={},
        priority="normal",
        metadata={},
        source="test",
    )

    expect_exception(
        ValueError,
        lambda: authority.create_task(
            task_id="duplicate-task",
            intent="Second task",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            source="test",
        ),
    )


def test_task_authority_unknown_task():
    authority = TaskAuthority()

    assert authority.get_task("does-not-exist") is None


FORBIDDEN_TASK_FIELDS = {
    # Lifecycle
    "lifecycle_state",
    "state",
    "status",
    "lifecycle_history",
    "transition_history",

    # Execution
    "execution_attempt",
    "execution_attempts",
    "attempt",
    "attempts",
    "execution_context",
    "execution_result",
    "execution_results",

    # Readiness / authorization
    "execution_readiness",
    "readiness",
    "execution_authorization",
    "authorization",

    # Observation / learning
    "observation",
    "observations",
    "learning_evidence",
    "learning",

    # Queue
    "queue",
    "queue_state",
    "queue_position",

    # Evaluation / selection
    "task_evaluation",
    "evaluation",
    "evaluation_score",
    "agent_selection",
    "selected_agent",
    "selected_agent_id",

    # Execution/resource decision semantics
    "resource_fit",
    "resource_allocation",
    "feasibility",
    "task_feasible",
}


def test_task_has_no_forbidden_semantic_fields():
    actual = {
        field.name
        for field in dataclasses.fields(Task)
    }

    overlap = actual & FORBIDDEN_TASK_FIELDS

    assert not overlap, (
        f"Task contains forbidden semantic fields: {sorted(overlap)}"
    )


def test_task_does_not_embed_execution_attempts():
    field_names = {
        field.name
        for field in dataclasses.fields(Task)
    }

    assert "execution_attempt" not in field_names
    assert "execution_attempts" not in field_names
    assert "attempt" not in field_names
    assert "attempts" not in field_names


def test_task_does_not_embed_execution_results():
    field_names = {
        field.name
        for field in dataclasses.fields(Task)
    }

    assert "execution_result" not in field_names
    assert "execution_results" not in field_names


def test_task_does_not_embed_observations_or_learning():
    field_names = {
        field.name
        for field in dataclasses.fields(Task)
    }

    assert "observation" not in field_names
    assert "observations" not in field_names
    assert "learning_evidence" not in field_names
    assert "learning" not in field_names


def test_task_does_not_embed_queue_state():
    field_names = {
        field.name
        for field in dataclasses.fields(Task)
    }

    assert "queue" not in field_names
    assert "queue_state" not in field_names
    assert "queue_position" not in field_names


def test_task_does_not_embed_evaluation_or_selection():
    field_names = {
        field.name
        for field in dataclasses.fields(Task)
    }

    assert "task_evaluation" not in field_names
    assert "evaluation" not in field_names
    assert "evaluation_score" not in field_names
    assert "agent_selection" not in field_names
    assert "selected_agent" not in field_names
    assert "selected_agent_id" not in field_names


def test_task_has_no_dynamic_semantic_extension():
    task = build_task()

    expect_exception(
        dataclasses.FrozenInstanceError,
        lambda: setattr(task, "execution_result", "forbidden"),
    )


def collect_import_roots(tree):
    imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split(".")[0])

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module.split(".")[0])

    return imports


def test_task_core_module_uses_only_allowed_standard_library_imports():
    source = TASK_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    imports = collect_import_roots(tree)

    allowed = {
        "__future__",
        "dataclasses",
        "datetime",
        "types",
        "typing",
    }

    unexpected = imports - allowed

    assert not unexpected, (
        f"Unexpected Task module imports: {sorted(unexpected)}"
    )


FORBIDDEN_MODULE_NAMES = {
    "weft",
    "runtime",
    "integration",
    "integrations",
    "workflow",
    "executor",
    "execution_engine",
    "agent_platform",
    "openrouter",
    "anthropic",
    "openai",
    "tavily",
    "elevenlabs",
}


def test_task_core_module_has_no_external_execution_dependencies():
    source = TASK_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    imports = collect_import_roots(tree)

    forbidden = imports & FORBIDDEN_MODULE_NAMES

    assert not forbidden, (
        f"Forbidden external/execution imports: {sorted(forbidden)}"
    )


def test_task_module_does_not_define_parallel_canonical_authorities():
    source = TASK_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    class_names = {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }

    forbidden_classes = {
        "TaskQueue",
        "TaskLifecycle",
        "ExecutionAttempt",
        "ExecutionResult",
        "ExecutionReadiness",
        "ExecutionAuthorization",
        "AgentSelection",
        "TaskEvaluation",
    }

    overlap = class_names & forbidden_classes

    assert not overlap, (
        f"Parallel canonical authorities found: {sorted(overlap)}"
    )


def test_task_authority_is_the_only_task_storage_owner():
    source = TASK_FILE.read_text(encoding="utf-8")
    tree = ast.parse(source)

    task_authority_classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and node.name == "TaskAuthority"
    ]

    assert len(task_authority_classes) == 1

    task_classes = [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and node.name == "Task"
    ]

    assert len(task_classes) == 1


def test_no_semantic_extension_via_normal_instance_assignment():
    task = build_task()

    expect_exception(
        dataclasses.FrozenInstanceError,
        lambda: setattr(task, "new_semantic_field", "forbidden"),
    )


def run_all_tests():
    tests = [
        obj
        for name, obj in sorted(globals().items())
        if name.startswith("test_")
        and callable(obj)
    ]

    passed = 0
    failed = 0

    print("=" * 60)
    print("AI COMPANY — CANONICAL TASK CONTRACT TESTS")
    print("Python standard library only")
    print("=" * 60)

    for test in tests:
        try:
            test()
        except Exception as exc:
            failed += 1
            print(f"FAIL  {test.__name__}: {exc}")
        else:
            passed += 1
            print(f"PASS  {test.__name__}")

    print("=" * 60)
    print(f"RESULT: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    run_all_tests()
