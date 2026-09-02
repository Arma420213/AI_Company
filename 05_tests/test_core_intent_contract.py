"""
AI Company — Core Intent Contract Test

Verifies the canonical behavioral and architectural contract of
02_core/intent.py.

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
from types import MappingProxyType


ROOT = Path(__file__).resolve().parents[1]
CORE_DIR = ROOT / "02_core"
INTENT_FILE = CORE_DIR / "intent.py"


def fail(message: str) -> None:
    raise AssertionError(message)


def test_module_exists() -> None:
    if not INTENT_FILE.is_file():
        fail("02_core/intent.py does not exist.")


def test_module_compiles() -> None:
    source = INTENT_FILE.read_text()
    compile(source, str(INTENT_FILE), "exec")


def load_intent_module():
    sys.path.insert(0, str(CORE_DIR))

    try:
        import intent
    finally:
        sys.path.pop(0)

    return intent


def test_canonical_symbols() -> None:
    intent = load_intent_module()

    required = (
        "CompanyIntent",
        "IntentAuthority",
        "IntentProvenance",
    )

    for name in required:
        if not hasattr(intent, name):
            fail(f"Missing canonical Intent symbol: {name}")


def test_company_intent_construction_and_values() -> None:
    intent = load_intent_module()

    provenance = intent.IntentProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Intent Authority",
    )

    company_intent = intent.CompanyIntent(
        intent_id="intent-test-001",
        purpose="Build a useful AI company.",
        desired_direction="Develop a local-first AI company.",
        organizational_context=MappingProxyType(
            {
                "organization": "AI Company",
                "mode": "local-first",
            }
        ),
        provenance=provenance,
    )

    assert company_intent.intent_id == "intent-test-001"
    assert company_intent.purpose == "Build a useful AI company."
    assert (
        company_intent.desired_direction
        == "Develop a local-first AI company."
    )
    assert company_intent.provenance is provenance


def test_required_fields_are_validated() -> None:
    intent = load_intent_module()

    provenance = intent.IntentProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Intent Authority",
    )

    common = {
        "purpose": "Valid purpose",
        "desired_direction": "Valid direction",
        "organizational_context": MappingProxyType({}),
        "provenance": provenance,
    }

    invalid_cases = (
        {"intent_id": "   ", **common},
        {"intent_id": "valid", **{**common, "purpose": "   "}},
        {
            "intent_id": "valid",
            **{**common, "desired_direction": "   "},
        },
    )

    for values in invalid_cases:
        try:
            intent.CompanyIntent(**values)
        except ValueError:
            pass
        else:
            fail("Invalid CompanyIntent representation was accepted.")


def test_company_intent_is_immutable() -> None:
    intent = load_intent_module()

    provenance = intent.IntentProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Intent Authority",
    )

    company_intent = intent.CompanyIntent(
        intent_id="intent-test-002",
        purpose="Valid purpose",
        desired_direction="Valid direction",
        organizational_context=MappingProxyType({"scope": "company"}),
        provenance=provenance,
    )

    try:
        company_intent.purpose = "mutation"
    except FrozenInstanceError:
        pass
    else:
        fail("CompanyIntent permits direct field mutation.")


def test_organizational_context_is_deeply_immutable() -> None:
    intent = load_intent_module()

    provenance = intent.IntentProvenance(
        source="human_owner",
        timestamp=datetime.now(timezone.utc),
        authority="Intent Authority",
    )

    company_intent = intent.CompanyIntent(
        intent_id="intent-test-003",
        purpose="Valid purpose",
        desired_direction="Valid direction",
        organizational_context=MappingProxyType(
            {"scope": "company"}
        ),
        provenance=provenance,
    )

    try:
        company_intent.organizational_context["new"] = "value"
    except TypeError:
        pass
    else:
        fail("CompanyIntent organizational_context is mutable.")


def test_authority_copies_caller_context() -> None:
    intent = load_intent_module()

    authority = intent.IntentAuthority()

    caller_context = {
        "scope": "company",
    }

    created = authority.set_intent(
        intent_id="intent-test-004",
        purpose="Valid purpose",
        desired_direction="Valid direction",
        organizational_context=caller_context,
        source="human_owner",
    )

    caller_context["external_mutation"] = "must-not-leak"

    if "external_mutation" in created.organizational_context:
        fail("Caller mapping mutation leaked into CompanyIntent.")


def test_intent_authority_owns_state_transition() -> None:
    intent = load_intent_module()

    authority = intent.IntentAuthority()

    first = authority.set_intent(
        intent_id="intent-test-005",
        purpose="First purpose",
        desired_direction="First direction",
        organizational_context={"scope": "company"},
        source="human_owner",
    )

    if authority.current_intent is not first:
        fail("IntentAuthority does not expose its accepted canonical state.")

    second = authority.set_intent(
        intent_id="intent-test-006",
        purpose="Second purpose",
        desired_direction="Second direction",
        organizational_context={"scope": "company"},
        source="human_owner",
    )

    if authority.current_intent is not second:
        fail("IntentAuthority did not replace canonical state explicitly.")

    if authority.current_intent is first:
        fail("IntentAuthority retained stale canonical state.")


def test_provenance_is_attached_to_canonical_state() -> None:
    intent = load_intent_module()

    authority = intent.IntentAuthority()

    created = authority.set_intent(
        intent_id="intent-test-007",
        purpose="Valid purpose",
        desired_direction="Valid direction",
        organizational_context={"scope": "company"},
        source="human_owner",
    )

    if created.provenance.source != "human_owner":
        fail("Intent provenance source was not preserved.")

    if created.provenance.authority != "Intent Authority":
        fail("Canonical Intent Authority provenance is incorrect.")

    if not isinstance(created.provenance.timestamp, datetime):
        fail("Intent provenance timestamp is not datetime.")


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


def test_only_canonical_intent_symbols_exist() -> None:
    expected = {
        "CompanyIntent",
        "IntentAuthority",
        "IntentProvenance",
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
        if match[0] == "02_core/intent.py"
    ]

    if len(canonical) != len(expected):
        fail(
            "Canonical Intent symbols are not all defined exactly in "
            "02_core/intent.py."
        )

    if len(matches) != len(expected):
        fail(
            "Competing Intent symbol definitions detected outside the "
            "canonical Core module."
        )


def run_all_tests() -> None:
    tests = (
        test_module_exists,
        test_module_compiles,
        test_canonical_symbols,
        test_company_intent_construction_and_values,
        test_required_fields_are_validated,
        test_company_intent_is_immutable,
        test_organizational_context_is_deeply_immutable,
        test_authority_copies_caller_context,
        test_intent_authority_owns_state_transition,
        test_provenance_is_attached_to_canonical_state,
        test_core_has_no_forbidden_import_dependencies,
        test_only_canonical_intent_symbols_exist,
    )

    for test in tests:
        test()
        print(f"PASS — {test.__name__}")


if __name__ == "__main__":
    run_all_tests()
    print()
    print("============================================================")
    print("===== CORE INTENT CONTRACT TEST: PASS")
    print("============================================================")
