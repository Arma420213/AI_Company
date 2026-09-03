"""
AI Company — Core Objective Contract Test

Verifies the canonical behavioral and architectural contract of
02_core/objective.py.

This test intentionally uses only the Python standard library.
It does not require pytest, external providers, Runtime, Integrations,
or execution infrastructure.
"""

from __future__ import annotations

import ast
import sys
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "02_core"
OBJECTIVE_FILE = CORE_DIR / "objective.py"
INTENT_FILE = CORE_DIR / "intent.py"


def fail(message: str) -> None:
    raise AssertionError(message)


def test_module_exists() -> None:
    if not OBJECTIVE_FILE.is_file():
        fail("02_core/objective.py does not exist.")


def test_module_compiles() -> None:
    source = OBJECTIVE_FILE.read_text()
    compile(source, str(OBJECTIVE_FILE), "exec")


def load_modules():
    sys.path.insert(0, str(CORE_DIR))

    try:
        import intent
        import objective
    finally:
        sys.path.pop(0)

    return intent, objective


def build_intent(intent_module, intent_id: str = "intent-test-001"):
    return intent_module.CompanyIntent(
        intent_id=intent_id,
        purpose="Build a reliable AI Company.",
        desired_direction="Develop canonical organizational capabilities.",
        organizational_context={
            "architecture": "local-first",
        },
        provenance=intent_module.IntentProvenance(
            source="human_owner",
            timestamp=datetime.now(timezone.utc),
            authority="Intent Authority",
        ),
    )


def test_canonical_symbols() -> None:
    _, objective = load_modules()

    required = (
        "CompanyObjective",
        "ObjectiveAuthority",
        "ObjectiveProvenance",
    )

    for name in required:
        if not hasattr(objective, name):
            fail(f"Missing canonical Objective symbol: {name}")


def test_company_objective_construction_and_values() -> None:
    _, objective = load_modules()

    provenance = objective.ObjectiveProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Objective Authority",
    )

    company_objective = objective.CompanyObjective(
        objective_id="objective-test-001",
        intent_id="intent-test-001",
        desired_outcome="Establish a reliable local-first AI company.",
        provenance=provenance,
    )

    if company_objective.objective_id != "objective-test-001":
        fail("Objective identity was not preserved.")

    if company_objective.intent_id != "intent-test-001":
        fail("Intent reference was not preserved.")

    if (
        company_objective.desired_outcome
        != "Establish a reliable local-first AI company."
    ):
        fail("Objective desired outcome was not preserved.")

    if company_objective.provenance is not provenance:
        fail("Objective provenance was not preserved.")


def test_required_fields_are_validated() -> None:
    _, objective = load_modules()

    provenance = objective.ObjectiveProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Objective Authority",
    )

    invalid_cases = (
        {
            "objective_id": "   ",
            "intent_id": "intent-test-001",
            "desired_outcome": "Valid outcome",
            "provenance": provenance,
        },
        {
            "objective_id": "objective-valid",
            "intent_id": "   ",
            "desired_outcome": "Valid outcome",
            "provenance": provenance,
        },
        {
            "objective_id": "objective-valid",
            "intent_id": "intent-test-001",
            "desired_outcome": "   ",
            "provenance": provenance,
        },
    )

    for values in invalid_cases:
        try:
            objective.CompanyObjective(**values)
        except ValueError:
            pass
        else:
            fail(
                "Invalid CompanyObjective representation was accepted."
            )


def test_provenance_fields_are_validated() -> None:
    _, objective = load_modules()

    invalid_cases = (
        {
            "source": "   ",
            "timestamp": datetime.now(timezone.utc),
            "authority": "Objective Authority",
        },
        {
            "source": "human_owner",
            "timestamp": datetime.now(timezone.utc),
            "authority": "   ",
        },
    )

    for values in invalid_cases:
        try:
            objective.ObjectiveProvenance(**values)
        except ValueError:
            pass
        else:
            fail(
                "Invalid Objective provenance was accepted."
            )


def test_company_objective_is_immutable() -> None:
    _, objective = load_modules()

    provenance = objective.ObjectiveProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Objective Authority",
    )

    company_objective = objective.CompanyObjective(
        objective_id="objective-test-002",
        intent_id="intent-test-002",
        desired_outcome="Valid outcome",
        provenance=provenance,
    )

    try:
        company_objective.desired_outcome = "mutation"
    except FrozenInstanceError:
        pass
    else:
        fail("CompanyObjective permits direct field mutation.")


def test_objective_authority_owns_collection() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    created = authority.set_objective(
        objective_id="objective-test-003",
        intent=intent,
        desired_outcome="First outcome",
        source="human_owner",
    )

    if authority.get_objective("objective-test-003") is not created:
        fail(
            "ObjectiveAuthority does not own the accepted canonical "
            "Objective state."
        )

    if "objective-test-003" not in authority.objectives:
        fail("Canonical Objective collection does not expose accepted state.")

    if authority.objectives["objective-test-003"] is not created:
        fail("Canonical Objective collection returned stale state.")


def test_multiple_objectives_are_supported() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    first = authority.set_objective(
        objective_id="objective-test-004",
        intent=intent,
        desired_outcome="First outcome",
        source="human_owner",
    )

    second = authority.set_objective(
        objective_id="objective-test-005",
        intent=intent,
        desired_outcome="Second outcome",
        source="human_owner",
    )

    if len(authority.objectives) != 2:
        fail("ObjectiveAuthority does not maintain multiple Objectives.")

    if authority.get_objective(first.objective_id) is not first:
        fail("First Objective was not retained.")

    if authority.get_objective(second.objective_id) is not second:
        fail("Second Objective was not retained.")


def test_objective_collection_is_read_only() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    authority.set_objective(
        objective_id="objective-test-006",
        intent=intent,
        desired_outcome="Valid outcome",
        source="human_owner",
    )

    try:
        authority.objectives["illegal"] = authority.objectives[
            "objective-test-006"
        ]
    except TypeError:
        pass
    else:
        fail("Objective collection permits direct external mutation.")


def test_initial_objectives_are_copied() -> None:
    _, objective = load_modules()

    provenance = objective.ObjectiveProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Objective Authority",
    )

    original = objective.CompanyObjective(
        objective_id="objective-test-007",
        intent_id="intent-test-007",
        desired_outcome="Valid outcome",
        provenance=provenance,
    )

    initial = {
        "objective-test-007": original,
    }

    authority = objective.ObjectiveAuthority(
        initial_objectives=initial,
    )

    initial.clear()

    if "objective-test-007" not in authority.objectives:
        fail("ObjectiveAuthority retained caller-owned mutable state.")


def test_conflicting_objective_creation_is_rejected() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    authority.set_objective(
        objective_id="objective-test-008",
        intent=intent,
        desired_outcome="First outcome",
        source="human_owner",
    )

    try:
        authority.set_objective(
            objective_id="objective-test-008",
            intent=intent,
            desired_outcome="Conflicting outcome",
            source="human_owner",
        )
    except ValueError:
        pass
    else:
        fail(
            "ObjectiveAuthority silently overwrote an existing Objective."
        )


def test_explicit_objective_update_is_supported() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    original = authority.set_objective(
        objective_id="objective-test-009",
        intent=intent,
        desired_outcome="Original outcome",
        source="human_owner",
    )

    updated = authority.update_objective(
        objective_id="objective-test-009",
        desired_outcome="Updated outcome",
        source="human_owner",
    )

    if updated is original:
        fail(
            "Objective update mutated the existing immutable Objective "
            "instead of creating a new canonical state."
        )

    if updated.desired_outcome != "Updated outcome":
        fail("Objective update did not apply the new desired outcome.")

    if updated.intent_id != original.intent_id:
        fail("Objective update changed the originating Intent reference.")

    if authority.get_objective("objective-test-009") is not updated:
        fail("Updated Objective was not accepted as canonical state.")


def test_update_requires_existing_objective() -> None:
    _, objective = load_modules()

    authority = objective.ObjectiveAuthority()

    try:
        authority.update_objective(
            objective_id="objective-does-not-exist",
            desired_outcome="Invalid update",
            source="human_owner",
        )
    except KeyError:
        pass
    else:
        fail(
            "ObjectiveAuthority accepted an update for a non-existing "
            "Objective."
        )


def test_objective_requires_canonical_company_intent() -> None:
    _, objective = load_modules()

    authority = objective.ObjectiveAuthority()

    try:
        authority.set_objective(
            objective_id="objective-test-010",
            intent="intent-test-010",
            desired_outcome="Invalid input",
            source="human_owner",
        )
    except TypeError:
        pass
    else:
        fail(
            "ObjectiveAuthority accepted a non-canonical Intent input."
        )


def test_objective_preserves_stable_intent_reference() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(
        intent_module,
        intent_id="intent-canonical-001",
    )

    authority = objective.ObjectiveAuthority()

    created = authority.set_objective(
        objective_id="objective-test-011",
        intent=intent,
        desired_outcome="Valid outcome",
        source="human_owner",
    )

    if created.intent_id != intent.intent_id:
        fail(
            "CompanyObjective did not preserve the canonical Intent "
            "reference."
        )


def test_provenance_is_attached_to_canonical_state() -> None:
    intent_module, objective = load_modules()

    intent = build_intent(intent_module)

    authority = objective.ObjectiveAuthority()

    created = authority.set_objective(
        objective_id="objective-test-012",
        intent=intent,
        desired_outcome="Valid outcome",
        source="human_owner",
    )

    if created.provenance.source != "human_owner":
        fail("Objective provenance source was not preserved.")

    if created.provenance.authority != "Objective Authority":
        fail("Canonical Objective Authority provenance is incorrect.")

    if not isinstance(created.provenance.timestamp, datetime):
        fail("Objective provenance timestamp is not datetime.")


def test_objective_is_not_execution_semantics() -> None:
    _, objective = load_modules()

    forbidden_fields = {
        "execution_id",
        "attempt_id",
        "result_id",
        "authorization_id",
        "provider",
        "workflow_id",
        "queue_state",
        "task_state",
        "agent_id",
        "capability",
    }

    fields = set(objective.CompanyObjective.__dataclass_fields__)

    overlap = forbidden_fields & fields

    if overlap:
        fail(
            "Execution or runtime semantics leaked into CompanyObjective: "
            + ", ".join(sorted(overlap))
        )


def test_core_has_no_forbidden_import_dependencies() -> None:
    forbidden_prefixes = (
        "03_runtime",
        "04_integrations",
        "05_tests",
        "06_tools",
        "07_examples",
    )

    forbidden_terms = (
        "weft",
        "openai",
        "anthropic",
        "google",
        "requests",
        "httpx",
        "sqlalchemy",
        "psycopg",
        "discord",
        "slack",
        "telegram",
    )

    tree = ast.parse(
        OBJECTIVE_FILE.read_text(),
        filename=str(OBJECTIVE_FILE),
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue

        for name in names:
            normalized = name.lower()

            for prefix in forbidden_prefixes:
                if (
                    normalized == prefix.lower()
                    or normalized.startswith(prefix.lower() + ".")
                ):
                    fail(
                        f"Forbidden upper-layer import detected: {name}"
                    )

            for term in forbidden_terms:
                if term in normalized:
                    fail(
                        f"Forbidden external/provider import detected: {name}"
                    )


def test_only_canonical_objective_symbols_exist() -> None:
    expected = {
        "CompanyObjective",
        "ObjectiveAuthority",
        "ObjectiveProvenance",
    }

    matches: list[tuple[str, str, str]] = []

    search_roots = (
        ROOT / "02_core",
        ROOT / "03_runtime",
        ROOT / "04_integrations",
        ROOT / "05_tests",
        ROOT / "06_tools",
        ROOT / "07_examples",
    )

    for search_root in search_roots:
        if not search_root.exists():
            continue

        for path in search_root.rglob("*.py"):
            tree = ast.parse(
                path.read_text(),
                filename=str(path),
            )

            for node in ast.walk(tree):
                if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
                    if node.name in expected:
                        matches.append(
                            (
                                str(path.relative_to(ROOT)),
                                type(node).__name__,
                                node.name,
                            )
                        )

    canonical = [
        match
        for match in matches
        if match[0] == "02_core/objective.py"
    ]

    if len(canonical) != len(expected):
        fail(
            "Canonical Objective symbols are not all defined exactly in "
            "02_core/objective.py."
        )

    if len(matches) != len(expected):
        fail(
            "Competing Objective symbol definitions detected outside "
            "the canonical Core module."
        )


def test_intent_remains_independent_of_objective() -> None:
    tree = ast.parse(
        INTENT_FILE.read_text(),
        filename=str(INTENT_FILE),
    )

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [node.module or ""]
        else:
            continue

        for name in names:
            if "objective" in name.lower():
                fail(
                    "Intent module depends on Objective implementation: "
                    + name
                )


def test_objective_depends_only_downward_or_same_core() -> None:
    tree = ast.parse(
        OBJECTIVE_FILE.read_text(),
        filename=str(OBJECTIVE_FILE),
    )

    allowed_modules = {
        "dataclasses",
        "datetime",
        "types",
        "typing",
        "intent",
        "__future__",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name.split(".")[0] for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            names = [(node.module or "").split(".")[0]]
        else:
            continue

        for name in names:
            if name not in allowed_modules:
                fail(
                    "Objective module imports a non-canonical dependency: "
                    + name
                )


def run_all_tests() -> None:
    tests = (
        test_module_exists,
        test_module_compiles,
        test_canonical_symbols,
        test_company_objective_construction_and_values,
        test_required_fields_are_validated,
        test_provenance_fields_are_validated,
        test_company_objective_is_immutable,
        test_objective_authority_owns_collection,
        test_multiple_objectives_are_supported,
        test_objective_collection_is_read_only,
        test_initial_objectives_are_copied,
        test_conflicting_objective_creation_is_rejected,
        test_explicit_objective_update_is_supported,
        test_update_requires_existing_objective,
        test_objective_requires_canonical_company_intent,
        test_objective_preserves_stable_intent_reference,
        test_provenance_is_attached_to_canonical_state,
        test_objective_is_not_execution_semantics,
        test_core_has_no_forbidden_import_dependencies,
        test_only_canonical_objective_symbols_exist,
        test_intent_remains_independent_of_objective,
        test_objective_depends_only_downward_or_same_core,
    )

    for test in tests:
        test()
        print(f"PASS — {test.__name__}")


if __name__ == "__main__":
    run_all_tests()
    print()
    print("============================================================")
    print("===== CORE OBJECTIVE HARDENED CONTRACT TEST: PASS")
    print("============================================================")
