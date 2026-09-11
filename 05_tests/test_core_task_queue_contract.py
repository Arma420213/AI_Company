"""
AI Company Core — Canonical Task Queue Contract Tests

These tests verify the Task Queue against the canonical architecture.

The tests validate:
- Queue Authority ownership
- queue/Task separation
- explicit ordering policy
- ordering
- retrieval
- duplicate handling
- read-only queue inspection
- Task immutability
- lifecycle isolation
- execution/authorization isolation
- dependency isolation
- absence of competing queue authorities
"""

from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
import sys
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "02_core"
QUEUE_PATH = CORE / "task_queue.py"
TASK_PATH = CORE / "task.py"


def load_core_modules():
    """
    Load task.py and task_queue.py without requiring package installation.
    """
    package = types.ModuleType("ai_company_core_test_package")
    package.__path__ = [str(CORE)]
    sys.modules[package.__name__] = package

    task_spec = importlib.util.spec_from_file_location(
        f"{package.__name__}.task",
        TASK_PATH,
    )
    task_module = importlib.util.module_from_spec(task_spec)
    sys.modules[task_spec.name] = task_module
    task_spec.loader.exec_module(task_module)

    queue_spec = importlib.util.spec_from_file_location(
        f"{package.__name__}.task_queue",
        QUEUE_PATH,
    )
    queue_module = importlib.util.module_from_spec(queue_spec)
    sys.modules[queue_spec.name] = queue_module
    queue_spec.loader.exec_module(queue_module)

    return task_module, queue_module


TaskModule, QueueModule = load_core_modules()

Task = TaskModule.Task
TaskAuthority = TaskModule.TaskAuthority
TaskProvenance = TaskModule.TaskProvenance

TaskQueue = QueueModule.TaskQueue
QueueAuthority = QueueModule.QueueAuthority
QueueProvenance = QueueModule.QueueProvenance


def make_task(task_id: str):
    authority = TaskAuthority()

    return authority.create_task(
        task_id=task_id,
        intent=f"Intent for {task_id}",
        requirements={"capability": "test"},
        constraints={},
        priority="normal",
        metadata={},
        source="contract-test",
    )


def fifo_policy(tasks):
    return tuple(tasks)


class TestCanonicalTaskQueueContract(unittest.TestCase):

    def test_single_canonical_queue_authority_symbols(self):
        self.assertTrue(hasattr(QueueModule, "TaskQueue"))
        self.assertTrue(hasattr(QueueModule, "QueueAuthority"))
        self.assertTrue(hasattr(QueueModule, "QueueProvenance"))

        source = QUEUE_PATH.read_text(encoding="utf-8")
        tree = ast.parse(source)

        class_names = [
            node.name
            for node in tree.body
            if isinstance(node, ast.ClassDef)
        ]

        self.assertEqual(
            class_names.count("TaskQueue"),
            1,
        )

        self.assertEqual(
            class_names.count("QueueAuthority"),
            1,
        )

    def test_queue_has_explicit_ordering_policy(self):
        task_a = make_task("task-a")

        with self.assertRaises(TypeError):
            TaskQueue(
                ordering_policy=None,
                provenance=QueueProvenance(
                    source="test",
                ),
            )

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task_a)

        self.assertIs(queue.peek(), task_a)

    def test_queue_preserves_task_definition(self):
        task = make_task("task-1")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)

        self.assertEqual(queue.peek(), task)
        self.assertEqual(task.task_id, "task-1")
        self.assertEqual(task.intent, "Intent for task-1")

    def test_queue_does_not_mutate_task(self):
        task = make_task("task-immutable")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)

        with self.assertRaises((AttributeError, TypeError)):
            task.intent = "changed"

        self.assertEqual(
            queue.peek().intent,
            "Intent for task-immutable",
        )

    def test_ordering(self):
        tasks = [
            make_task("task-1"),
            make_task("task-2"),
            make_task("task-3"),
        ]

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        for task in tasks:
            queue.enqueue(task)

        self.assertEqual(
            queue.dequeue().task_id,
            "task-1",
        )

        self.assertEqual(
            queue.dequeue().task_id,
            "task-2",
        )

        self.assertEqual(
            queue.dequeue().task_id,
            "task-3",
        )

        self.assertIsNone(queue.dequeue())

    def test_custom_ordering_policy_is_respected(self):
        tasks = [
            make_task("task-1"),
            make_task("task-2"),
            make_task("task-3"),
        ]

        def reverse_policy(items):
            return tuple(reversed(items))

        queue = TaskQueue(
            ordering_policy=reverse_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        for task in tasks:
            queue.enqueue(task)

        self.assertEqual(
            queue.dequeue().task_id,
            "task-3",
        )

        self.assertEqual(
            queue.dequeue().task_id,
            "task-2",
        )

        self.assertEqual(
            queue.dequeue().task_id,
            "task-1",
        )

    def test_peek_does_not_change_queue_state(self):
        task = make_task("task-peek")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)

        self.assertEqual(queue.size, 1)
        self.assertIs(queue.peek(), task)
        self.assertEqual(queue.size, 1)
        self.assertTrue(queue.contains("task-peek"))

    def test_dequeue_changes_only_queue_state(self):
        task = make_task("task-dequeue")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)
        result = queue.dequeue()

        self.assertIs(result, task)
        self.assertEqual(queue.size, 0)
        self.assertFalse(queue.contains("task-dequeue"))

        self.assertEqual(
            task.task_id,
            "task-dequeue",
        )

    def test_duplicate_queue_entry_is_rejected(self):
        task = make_task("task-duplicate")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)

        with self.assertRaises(ValueError):
            queue.enqueue(task)

    def test_only_canonical_tasks_can_be_queued(self):
        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        with self.assertRaises(TypeError):
            queue.enqueue("not-a-task")

    def test_pending_state_is_read_only(self):
        task = make_task("task-read-only")

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task)

        pending = queue.pending

        with self.assertRaises(TypeError):
            pending["other"] = task

        self.assertEqual(queue.size, 1)

    def test_queue_authority_owns_queue_state(self):
        authority = QueueAuthority(
            ordering_policy=fifo_policy,
            source="contract-test",
        )

        task = make_task("task-authority")

        authority.enqueue(task)

        self.assertEqual(authority.size, 1)
        self.assertTrue(authority.contains("task-authority"))
        self.assertIs(
            authority.peek(),
            task,
        )

    def test_queue_authority_does_not_expose_mutable_queue(self):
        authority = QueueAuthority(
            ordering_policy=fifo_policy,
            source="contract-test",
        )

        self.assertFalse(
            hasattr(authority, "queue"),
        )

        self.assertTrue(
            hasattr(authority, "queue_state"),
        )

        task = make_task("task-ownership-boundary")

        authority.enqueue(task)

        state = authority.queue_state

        with self.assertRaises(TypeError):
            state["other"] = task

        self.assertEqual(authority.size, 1)
        self.assertTrue(
            authority.contains("task-ownership-boundary"),
        )

    def test_queue_authority_does_not_own_task_definition(self):
        task_authority = TaskAuthority()
        queue_authority = QueueAuthority(
            ordering_policy=fifo_policy,
            source="contract-test",
        )

        task = task_authority.create_task(
            task_id="task-owner-separation",
            intent="owned by Task Authority",
            requirements={},
            constraints={},
            priority="normal",
            metadata={},
            source="task-authority",
        )

        queue_authority.enqueue(task)

        self.assertIs(
            task_authority.get_task("task-owner-separation"),
            task,
        )

    def test_empty_queue_retrieval(self):
        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        self.assertIsNone(queue.peek())
        self.assertIsNone(queue.dequeue())
        self.assertEqual(queue.size, 0)

    def test_queue_provenance(self):
        provenance = QueueProvenance(
            source="contract-test",
        )

        queue = TaskQueue(
            ordering_policy=fifo_policy,
            provenance=provenance,
        )

        self.assertEqual(
            queue.provenance.source,
            "contract-test",
        )

    def test_invalid_provenance_is_rejected(self):
        with self.assertRaises(ValueError):
            QueueProvenance(source="")

    def test_policy_must_preserve_membership(self):
        task_a = make_task("task-policy-a")
        task_b = make_task("task-policy-b")

        def invalid_policy(_):
            return (task_a,)

        queue = TaskQueue(
            ordering_policy=invalid_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task_a)
        queue.enqueue(task_b)

        with self.assertRaises(ValueError):
            queue.peek()

    def test_policy_must_not_duplicate_tasks(self):
        task_a = make_task("task-policy-duplicate")

        def invalid_policy(_):
            return (task_a, task_a)

        queue = TaskQueue(
            ordering_policy=invalid_policy,
            provenance=QueueProvenance(
                source="test",
            ),
        )

        queue.enqueue(task_a)

        with self.assertRaises(ValueError):
            queue.peek()

    def test_core_dependency_is_task_only(self):
        tree = ast.parse(
            QUEUE_PATH.read_text(encoding="utf-8")
        )

        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "")

        forbidden_fragments = (
            "runtime",
            "integration",
            "weft",
            "requests",
            "httpx",
            "sqlalchemy",
            "ollama",
            "openai",
        )

        for imported in imports:
            lowered = imported.lower()

            for forbidden in forbidden_fragments:
                self.assertNotIn(
                    forbidden,
                    lowered,
                    msg=(
                        "Forbidden dependency in Task Queue: "
                        f"{imported}"
                    ),
                )

        self.assertIn(
            "dataclasses",
            imports,
        )

        self.assertIn(
            "typing",
            imports,
        )

    def test_forbidden_responsibilities_are_not_defined(self):
        source = QUEUE_PATH.read_text(
            encoding="utf-8"
        ).lower()

        forbidden_symbols = (
            "execute_task",
            "authorize_execution",
            "select_agent",
            "evaluate_task",
            "transition_task",
            "change_lifecycle",
        )

        for symbol in forbidden_symbols:
            self.assertNotIn(
                symbol,
                source,
            )


if __name__ == "__main__":
    unittest.main()
