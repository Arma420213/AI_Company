"""
AI Company Core — Strategic Decision Contract Tests

Standard-library-only architectural contract tests for the canonical
Strategic Decision nucleus.
"""

from __future__ import annotations

import ast
import importlib.util
import py_compile
import tempfile

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "02_core"

MODULE_PATH = Path(__file__).resolve().parents[1] / "02_core" / "strategic_decision.py"

def load_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_strategic_decision",
        MODULE_PATH,
    )

    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)

    sys.modules[spec.name] = module

    spec.loader.exec_module(module)

    return module


def test_module_exists():
    assert MODULE_PATH.exists()


def test_module_compiles():
    py_compile.compile(
        str(MODULE_PATH),
        doraise=True,
    )


def test_canonical_symbols_exist():
    module = load_module()

    assert hasattr(module, "DecisionProvenance")
    assert hasattr(module, "StrategicDecision")
    assert hasattr(module, "DecisionAuthority")


def test_provenance_and_decision_construction():
    module = load_module()

    timestamp = datetime.now(timezone.utc)

    provenance = module.DecisionProvenance(
        source="contract-test",
        timestamp=timestamp,
        authority="Decision Authority",
    )

    decision = module.StrategicDecision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=("objective-1",),
        strategic_direction="Improve organizational capability.",
        context={"priority": "foundation"},
        evidence={"source": "test"},
        provenance=provenance,
    )

    assert decision.decision_id == "decision-1"
    assert decision.intent_id == "intent-1"
    assert decision.objective_ids == ("objective-1",)
    assert decision.strategic_direction == "Improve organizational capability."
    assert decision.provenance is provenance


def test_required_fields_are_validated():
    module = load_module()

    provenance = module.DecisionProvenance(
        source="test",
        timestamp=datetime.now(timezone.utc),
        authority="Decision Authority",
    )

    try:
        module.StrategicDecision(
            decision_id="",
            intent_id="intent-1",
            objective_ids=(),
            strategic_direction="direction",
            context={},
            evidence={},
            provenance=provenance,
        )
    except ValueError:
        pass
    else:
        raise AssertionError("Empty decision_id must be rejected.")


def test_decision_is_immutable():
    module = load_module()

    decision = module.StrategicDecision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=("objective-1",),
        strategic_direction="direction",
        context={},
        evidence={},
        provenance=module.DecisionProvenance(
            source="test",
            timestamp=datetime.now(timezone.utc),
            authority="Decision Authority",
        ),
    )

    try:
        decision.strategic_direction = "changed"
    except FrozenInstanceError:
        pass
    else:
        raise AssertionError(
            "StrategicDecision must be immutable."
        )


def test_context_and_evidence_are_read_only():
    module = load_module()

    decision = module.StrategicDecision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=(),
        strategic_direction="direction",
        context={"a": "b"},
        evidence={"x": "y"},
        provenance=module.DecisionProvenance(
            source="test",
            timestamp=datetime.now(timezone.utc),
            authority="Decision Authority",
        ),
    )

    try:
        decision.context["a"] = "changed"
    except TypeError:
        pass
    else:
        raise AssertionError("Context must be read-only.")

    try:
        decision.evidence["x"] = "changed"
    except TypeError:
        pass
    else:
        raise AssertionError("Evidence must be read-only.")


def test_decision_authority_owns_state():
    module = load_module()

    authority = module.DecisionAuthority()

    decision = authority.set_decision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=("objective-1",),
        strategic_direction="direction",
        source="test",
    )

    assert authority.get_decision("decision-1") is decision
    assert authority.decisions["decision-1"] is decision


def test_decision_collection_is_read_only():
    module = load_module()

    authority = module.DecisionAuthority()

    authority.set_decision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=(),
        strategic_direction="direction",
        source="test",
    )

    try:
        authority.decisions["decision-2"] = authority.get_decision("decision-1")
    except TypeError:
        pass
    else:
        raise AssertionError(
            "DecisionAuthority.decisions must be read-only."
        )


def test_duplicate_decision_identity_is_rejected():
    module = load_module()

    authority = module.DecisionAuthority()

    authority.set_decision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=(),
        strategic_direction="direction",
        source="test",
    )

    try:
        authority.set_decision(
            decision_id="decision-1",
            intent_id="intent-2",
            objective_ids=(),
            strategic_direction="other",
            source="test",
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Duplicate Strategic Decision identity must be rejected."
        )


def test_update_creates_new_immutable_state():
    module = load_module()

    authority = module.DecisionAuthority()

    original = authority.set_decision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=("objective-1",),
        strategic_direction="original",
        source="test",
    )

    updated = authority.update_decision(
        decision_id="decision-1",
        strategic_direction="updated",
        source="test-update",
    )

    assert updated is not original
    assert updated.decision_id == original.decision_id
    assert updated.intent_id == original.intent_id
    assert updated.objective_ids == original.objective_ids
    assert updated.strategic_direction == "updated"
    assert authority.get_decision("decision-1") is updated


def test_provenance_is_attached():
    module = load_module()

    authority = module.DecisionAuthority()

    timestamp = datetime.now(timezone.utc)

    decision = authority.set_decision(
        decision_id="decision-1",
        intent_id="intent-1",
        objective_ids=(),
        strategic_direction="direction",
        source="contract-test",
        authority="Decision Authority",
        timestamp=timestamp,
    )

    assert decision.provenance.source == "contract-test"
    assert decision.provenance.authority == "Decision Authority"
    assert decision.provenance.timestamp == timestamp


def test_forbidden_dependencies_are_absent():
    tree = ast.parse(
        MODULE_PATH.read_text(encoding="utf-8-sig")
    )

    forbidden_terms = {
        "runtime",
        "integration",
        "integrations",
        "weft",
        "provider",
        "providers",
        "tool",
        "tools",
        "execution",
        "authorization",
        "agent_selection",
        "task_evaluation",
    }

    violations = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.lower() for alias in node.names]
            violations.extend(
                name
                for name in names
                if any(term in name for term in forbidden_terms)
            )

        elif isinstance(node, ast.ImportFrom):
            name = (node.module or "").lower()
            if any(term in name for term in forbidden_terms):
                violations.append(name)

    assert not violations, (
        "Strategic Decision has forbidden dependencies: "
        + ", ".join(violations)
    )


def test_no_second_decision_authority_is_defined_in_core():
    symbol = "DecisionAuthority"
    occurrences = []

    for path in CORE.rglob("*.py"):
        if path.name == "strategic_decision.py":
            continue

        try:
            tree = ast.parse(
                path.read_text(encoding="utf-8-sig")
            )
        except (OSError, UnicodeDecodeError, SyntaxError):
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == symbol:
                occurrences.append(path)

    assert not occurrences, (
        "Competing canonical DecisionAuthority definitions found: "
        + ", ".join(str(path) for path in occurrences)
    )


def test_strategic_decision_has_no_execution_semantics():
    tree = ast.parse(
        MODULE_PATH.read_text(encoding="utf-8-sig")
    )

    forbidden_fields = {
        "execute",
        "execution",
        "execution_id",
        "authorization",
        "authorized",
        "agent",
        "agent_id",
        "task_id",
        "result",
        "status",
    }

    fields = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            fields.add(node.target.id)

    assert not (fields & forbidden_fields), (
        "Strategic Decision contains execution-related canonical fields: "
        + ", ".join(sorted(fields & forbidden_fields))
    )


def run_all_tests():
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_") and callable(value)
    ]

    failures = []

    for test in sorted(tests, key=lambda function: function.__name__):
        try:
            test()
        except Exception as exc:
            failures.append((test.__name__, exc))

    if failures:
        for name, exc in failures:
            print(f"FAIL: {name}: {exc}")
        raise SystemExit(1)

    print(f"PASS: {len(tests)} Strategic Decision contract tests")


if __name__ == "__main__":
    run_all_tests()
