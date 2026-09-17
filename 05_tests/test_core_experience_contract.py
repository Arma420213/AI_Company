"""
AI Company Core — Canonical Experience Contract Tests

Stdlib-only contract test suite.

Experience:
- owns canonical derived organizational knowledge;
- preserves evidence traceability;
- preserves provenance and temporal context;
- preserves uncertainty and contradiction;
- remains independent from Runtime and Integrations;
- does not become Trust, Learning, Evaluation, Selection,
  Strategic Decision, or Execution authority.
"""

from __future__ import annotations

import ast
import importlib.util
import traceback
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPERIENCE_PATH = PROJECT_ROOT / "02_core" / "experience.py"


def load_experience_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_experience",
        EXPERIENCE_PATH,
    )
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)

    import sys
    sys.modules[spec.name] = module

    spec.loader.exec_module(module)
    return module


experience = load_experience_module()


def aware_time(hour: int = 12) -> datetime:
    return datetime(
        2026,
        9,
        17,
        hour,
        0,
        tzinfo=timezone.utc,
    )


def make_provenance():
    return experience.ExperienceProvenance(
        source="memory:mem-001",
        authority="Memory Authority",
        derived_at=aware_time(13),
        derivation_method="canonical evidence synthesis",
    )


def make_temporal_context():
    return experience.ExperienceTemporalContext(
        evidence_start=aware_time(10),
        evidence_end=aware_time(11),
        derived_at=aware_time(13),
    )


def make_evidence_reference():
    return experience.ExperienceReference(
        concept="MemoryRecord",
        identity="mem-001",
        reference_kind="EVIDENCE",
    )


def make_context_reference():
    return experience.ExperienceReference(
        concept="Task",
        identity="task-001",
        reference_kind="CONTEXT",
    )


def make_record(**overrides):
    values = {
        "experience_id": "exp-001",
        "subject": "task execution",
        "scope": "AI Company runtime",
        "derived_knowledge": {
            "observation": "execution completed",
            "result": "task produced expected output",
        },
        "supporting_evidence": (
            make_evidence_reference(),
        ),
        "contextual_references": (
            make_context_reference(),
        ),
        "temporal_context": make_temporal_context(),
        "provenance": make_provenance(),
        "evidentiary_qualification": (
            "derived from preserved evidence"
        ),
        "metadata": {
            "origin": "canonical",
        },
    }

    values.update(overrides)

    return experience.ExperienceRecord(**values)


# ---------------------------------------------------------------------------
# E-01 — Single Authority
# ---------------------------------------------------------------------------

def test_e01_experience_has_single_canonical_authority():
    authority = experience.ExperienceAuthority()

    assert authority.AUTHORITY_NAME == "Experience Authority"


# ---------------------------------------------------------------------------
# E-02 — Canonical Identity
# ---------------------------------------------------------------------------

def test_e02_experience_requires_canonical_identity():
    try:
        make_record(experience_id="")
    except ValueError:
        return

    raise AssertionError(
        "Experience must reject an empty canonical identity."
    )


def test_e02_experience_collection_key_matches_identity():
    try:
        experience.ExperienceAuthority(
            initial_records={
                "wrong-id": make_record(
                    experience_id="exp-001"
                ),
            }
        )
    except ValueError:
        return

    raise AssertionError(
        "Experience collection key must match experience_id."
    )


# ---------------------------------------------------------------------------
# E-03 — Evidence Derivation
# ---------------------------------------------------------------------------

def test_e03_experience_requires_derived_knowledge():
    try:
        make_record(derived_knowledge=None)
    except ValueError:
        return

    raise AssertionError(
        "Experience must require derived knowledge."
    )


def test_e03_experience_contains_supporting_evidence():
    record = make_record()

    assert record.supporting_evidence
    assert record.supporting_evidence[0].identity == "mem-001"


# ---------------------------------------------------------------------------
# E-04 — Evidence Traceability
# ---------------------------------------------------------------------------

def test_e04_supporting_evidence_is_explicitly_referenced():
    record = make_record()

    reference = record.supporting_evidence[0]

    assert reference.concept == "MemoryRecord"
    assert reference.identity == "mem-001"
    assert reference.reference_kind == "EVIDENCE"


def test_e04_context_references_are_distinct_from_evidence():
    record = make_record()

    assert (
        record.contextual_references[0].reference_kind
        == "CONTEXT"
    )

    assert (
        record.supporting_evidence[0].reference_kind
        == "EVIDENCE"
    )


# ---------------------------------------------------------------------------
# E-05 — Interpretation Separation
# ---------------------------------------------------------------------------

def test_e05_experience_does_not_expose_trust_or_learning_fields():
    record = make_record()

    assert not hasattr(record, "trust")
    assert not hasattr(record, "learning")
    assert not hasattr(record, "trust_score")
    assert not hasattr(record, "learning_score")


# ---------------------------------------------------------------------------
# E-06 — Provenance
# ---------------------------------------------------------------------------

def test_e06_provenance_requires_source_authority_and_method():
    invalid_values = (
        {
            "source": "",
            "authority": "Memory Authority",
            "derived_at": aware_time(),
            "derivation_method": "synthesis",
        },
        {
            "source": "memory:mem-001",
            "authority": "",
            "derived_at": aware_time(),
            "derivation_method": "synthesis",
        },
        {
            "source": "memory:mem-001",
            "authority": "Memory Authority",
            "derived_at": aware_time(),
            "derivation_method": "",
        },
    )

    for values in invalid_values:
        try:
            experience.ExperienceProvenance(**values)
        except ValueError:
            continue

        raise AssertionError(
            "Invalid Experience provenance was accepted."
        )


def test_e06_provenance_requires_timezone_aware_derivation_time():
    try:
        experience.ExperienceProvenance(
            source="memory:mem-001",
            authority="Memory Authority",
            derived_at=datetime(
                2026,
                9,
                17,
                13,
            ),
            derivation_method="synthesis",
        )
    except ValueError:
        return

    raise AssertionError(
        "Experience provenance must require timezone-aware time."
    )


# ---------------------------------------------------------------------------
# E-07 — Temporal Integrity
# ---------------------------------------------------------------------------

def test_e07_temporal_context_preserves_evidence_period_and_derivation_time():
    context = make_temporal_context()

    assert context.evidence_start == aware_time(10)
    assert context.evidence_end == aware_time(11)
    assert context.derived_at == aware_time(13)


def test_e07_temporal_context_rejects_reversed_evidence_period():
    try:
        experience.ExperienceTemporalContext(
            evidence_start=aware_time(11),
            evidence_end=aware_time(10),
            derived_at=aware_time(13),
        )
    except ValueError:
        return

    raise AssertionError(
        "Experience must reject reversed evidence periods."
    )


# ---------------------------------------------------------------------------
# E-08 — Uncertainty Preservation
# ---------------------------------------------------------------------------

def test_e08_evidentiary_qualification_is_optional_and_non_numeric():
    record = make_record(
        evidentiary_qualification="incomplete evidence"
    )

    assert (
        record.evidentiary_qualification
        == "incomplete evidence"
    )

    assert not hasattr(record, "confidence")
    assert not hasattr(record, "confidence_score")


def test_e08_empty_evidentiary_qualification_is_rejected():
    try:
        make_record(
            evidentiary_qualification="   "
        )
    except ValueError:
        return

    raise AssertionError(
        "Empty evidentiary qualification must be rejected."
    )


# ---------------------------------------------------------------------------
# E-09 — Contradiction Preservation
# ---------------------------------------------------------------------------

def test_e09_derived_knowledge_can_preserve_explicit_contradictory_evidence():
    contradictory_knowledge = {
        "evidence_a": "completed",
        "evidence_b": "failed",
        "status": "inconsistent",
    }

    record = make_record(
        derived_knowledge=contradictory_knowledge,
        evidentiary_qualification=(
            "contradictory evidence preserved"
        ),
    )

    assert record.derived_knowledge["evidence_a"] == "completed"
    assert record.derived_knowledge["evidence_b"] == "failed"
    assert record.derived_knowledge["status"] == "inconsistent"


# ---------------------------------------------------------------------------
# E-10 — Ownership Isolation
# ---------------------------------------------------------------------------

def test_e10_experience_authority_owns_experience_records():
    authority = experience.ExperienceAuthority()

    record = authority.retain(
        experience_id="exp-001",
        subject="task execution",
        scope="AI Company runtime",
        derived_knowledge={
            "result": "completed"
        },
        supporting_evidence=(
            make_evidence_reference(),
        ),
        temporal_context=make_temporal_context(),
        provenance=make_provenance(),
    )

    assert authority.get_experience("exp-001") is record


# ---------------------------------------------------------------------------
# E-11 — No Trust Leakage
# ---------------------------------------------------------------------------

def test_e11_experience_does_not_calculate_or_mutate_trust():
    authority = experience.ExperienceAuthority()

    record = authority.retain(
        experience_id="exp-001",
        subject="task execution",
        scope="AI Company runtime",
        derived_knowledge={
            "result": "completed"
        },
        supporting_evidence=(
            make_evidence_reference(),
        ),
        temporal_context=make_temporal_context(),
        provenance=make_provenance(),
    )

    assert not hasattr(authority, "calculate_trust")
    assert not hasattr(authority, "assign_trust")
    assert not hasattr(authority, "update_trust")
    assert not hasattr(record, "trust_score")


# ---------------------------------------------------------------------------
# E-12 — No Learning Leakage
# ---------------------------------------------------------------------------

def test_e12_experience_does_not_execute_learning():
    authority = experience.ExperienceAuthority()

    assert not hasattr(authority, "learn")
    assert not hasattr(authority, "train")
    assert not hasattr(authority, "update_model")


# ---------------------------------------------------------------------------
# E-13 — No Decision Leakage
# ---------------------------------------------------------------------------

def test_e13_experience_does_not_make_strategic_decisions():
    authority = experience.ExperienceAuthority()

    assert not hasattr(authority, "decide")
    assert not hasattr(authority, "make_decision")
    assert not hasattr(authority, "recommend_decision")


# ---------------------------------------------------------------------------
# E-14 — No Selection Leakage
# ---------------------------------------------------------------------------

def test_e14_experience_does_not_select_agents():
    authority = experience.ExperienceAuthority()

    assert not hasattr(authority, "select_agent")
    assert not hasattr(authority, "rank_agents")
    assert not hasattr(authority, "score_agent")


# ---------------------------------------------------------------------------
# E-15 — No Execution Authority
# ---------------------------------------------------------------------------

def test_e15_experience_does_not_execute_tasks():
    authority = experience.ExperienceAuthority()

    assert not hasattr(authority, "execute")
    assert not hasattr(authority, "dispatch")
    assert not hasattr(authority, "authorize_execution")


# ---------------------------------------------------------------------------
# E-16 — No Duplicate Models
# ---------------------------------------------------------------------------

def test_e16_experience_does_not_define_forbidden_domain_models():
    source = EXPERIENCE_PATH.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)

    forbidden_names = {
        "MemoryRecord",
        "MemoryAuthority",
        "TrustModel",
        "TrustRecord",
        "LearningModel",
        "LearningRecord",
        "AgentSelection",
        "StrategicDecision",
    }

    defined_names = {
        node.name
        for node in ast.walk(tree)
        if isinstance(
            node,
            (
                ast.ClassDef,
                ast.FunctionDef,
                ast.AsyncFunctionDef,
            ),
        )
    }

    overlap = defined_names.intersection(
        forbidden_names
    )

    assert not overlap, (
        "Experience defines forbidden duplicate models: "
        + ", ".join(sorted(overlap))
    )


# ---------------------------------------------------------------------------
# E-17 — Core Isolation
# ---------------------------------------------------------------------------

def test_e17_experience_uses_only_allowed_standard_library_imports():
    source = EXPERIENCE_PATH.read_text(
        encoding="utf-8"
    )

    tree = ast.parse(source)

    allowed_modules = {
        "__future__",
        "dataclasses",
        "datetime",
        "types",
        "typing",
    }

    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(
                alias.name.split(".")[0]
                for alias in node.names
            )

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(
                    node.module.split(".")[0]
                )

    unexpected = set(imports) - allowed_modules

    assert not unexpected, (
        "Experience contains forbidden imports: "
        + ", ".join(sorted(unexpected))
    )


def test_e17_experience_has_no_runtime_or_integration_imports():
    source = EXPERIENCE_PATH.read_text(
        encoding="utf-8"
    )

    forbidden_tokens = (
        "02_company_runtime",
        "04_integrations",
        "requests",
        "httpx",
        "sqlalchemy",
        "sqlite3",
        "ollama",
        "weft",
        "fastapi",
        "boto3",
        "openai",
    )

    for token in forbidden_tokens:
        assert token not in source, (
            f"Forbidden infrastructure dependency found: {token}"
        )


# ---------------------------------------------------------------------------
# E-18 — Persistence Independence
# ---------------------------------------------------------------------------

def test_e18_experience_has_no_persistence_dependency():
    authority = experience.ExperienceAuthority()

    assert not hasattr(authority, "save")
    assert not hasattr(authority, "load")
    assert not hasattr(authority, "persist")
    assert not hasattr(authority, "database")


# ---------------------------------------------------------------------------
# E-19 — Historical Integrity
# ---------------------------------------------------------------------------

def test_e19_existing_experience_identity_cannot_be_silently_rewritten():
    authority = experience.ExperienceAuthority()

    original = authority.retain(
        experience_id="exp-001",
        subject="task execution",
        scope="AI Company runtime",
        derived_knowledge={
            "result": "completed"
        },
        supporting_evidence=(
            make_evidence_reference(),
        ),
        temporal_context=make_temporal_context(),
        provenance=make_provenance(),
    )

    try:
        authority.retain(
            experience_id="exp-001",
            subject="task execution",
            scope="AI Company runtime",
            derived_knowledge={
                "result": "different"
            },
            supporting_evidence=(
                make_evidence_reference(),
            ),
            temporal_context=make_temporal_context(),
            provenance=make_provenance(),
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Existing Experience identity was silently rewritten."
        )

    assert authority.get_experience("exp-001") is original

    assert (
        authority
        .get_experience("exp-001")
        .derived_knowledge["result"]
        == "completed"
    )


# ---------------------------------------------------------------------------
# E-20 — Reference Ownership
# ---------------------------------------------------------------------------

def test_e20_experience_references_do_not_transfer_ownership():
    evidence_reference = make_evidence_reference()
    context_reference = make_context_reference()

    record = make_record(
        supporting_evidence=(
            evidence_reference,
        ),
        contextual_references=(
            context_reference,
        ),
    )

    assert (
        record.supporting_evidence[0]
        is evidence_reference
    )

    assert (
        record.contextual_references[0]
        is context_reference
    )

    assert (
        record.supporting_evidence[0].concept
        == "MemoryRecord"
    )

    assert (
        record.contextual_references[0].concept
        == "Task"
    )


# ---------------------------------------------------------------------------
# Additional structural integrity tests
# ---------------------------------------------------------------------------

def test_experience_record_is_immutable():
    record = make_record()

    try:
        record.subject = "changed"
    except (AttributeError, TypeError):
        return

    raise AssertionError(
        "ExperienceRecord is mutable."
    )


def test_experience_reference_is_immutable():
    reference = make_evidence_reference()

    try:
        reference.identity = "changed"
    except (AttributeError, TypeError):
        return

    raise AssertionError(
        "ExperienceReference is mutable."
    )


def test_experience_provenance_is_immutable():
    provenance = make_provenance()

    try:
        provenance.source = "changed"
    except (AttributeError, TypeError):
        return

    raise AssertionError(
        "ExperienceProvenance is mutable."
    )


def test_experience_temporal_context_is_immutable():
    context = make_temporal_context()

    try:
        context.derived_at = aware_time(15)
    except (AttributeError, TypeError):
        return

    raise AssertionError(
        "ExperienceTemporalContext is mutable."
    )


def test_derived_knowledge_is_structurally_immutable():
    original = {
        "nested": {
            "value": "original",
        },
        "items": [
            "a",
            "b",
        ],
    }

    record = make_record(
        derived_knowledge=original
    )

    original["nested"]["value"] = "changed"
    original["items"].append("c")

    assert (
        record.derived_knowledge["nested"]["value"]
        == "original"
    )

    assert (
        record.derived_knowledge["items"]
        == ("a", "b")
    )


def test_metadata_is_read_only():
    record = make_record()

    assert isinstance(
        record.metadata,
        MappingProxyType,
    )

    try:
        record.metadata["new"] = "value"
    except TypeError:
        return

    raise AssertionError(
        "Experience metadata is mutable."
    )


def test_records_collection_is_read_only():
    authority = experience.ExperienceAuthority()

    authority.retain(
        experience_id="exp-001",
        subject="task execution",
        scope="AI Company runtime",
        derived_knowledge={
            "result": "completed"
        },
        supporting_evidence=(
            make_evidence_reference(),
        ),
        temporal_context=make_temporal_context(),
        provenance=make_provenance(),
    )

    records = authority.records

    assert isinstance(
        records,
        MappingProxyType,
    )

    try:
        records["exp-002"] = make_record(
            experience_id="exp-002"
        )
    except TypeError:
        return

    raise AssertionError(
        "Experience records collection is mutable."
    )


def test_invalid_supporting_reference_kind_is_rejected():
    invalid_reference = experience.ExperienceReference(
        concept="Task",
        identity="task-001",
        reference_kind="CONTEXT",
    )

    try:
        make_record(
            supporting_evidence=(
                invalid_reference,
            )
        )
    except ValueError:
        return

    raise AssertionError(
        "Invalid supporting evidence reference was accepted."
    )


def test_invalid_context_reference_kind_is_rejected():
    invalid_reference = experience.ExperienceReference(
        concept="MemoryRecord",
        identity="mem-001",
        reference_kind="EVIDENCE",
    )

    try:
        make_record(
            contextual_references=(
                invalid_reference,
            )
        )
    except ValueError:
        return

    raise AssertionError(
        "Invalid contextual reference was accepted."
    )


def test_initial_records_require_experience_record_instances():
    try:
        experience.ExperienceAuthority(
            initial_records={
                "exp-001": object()
            }
        )
    except TypeError:
        return

    raise AssertionError(
        "Experience Authority accepted a non-ExperienceRecord."
    )


# ---------------------------------------------------------------------------
# Simple stdlib test runner
# ---------------------------------------------------------------------------

def run_tests():
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_")
        and callable(value)
    ]

    tests.sort(key=lambda function: function.__name__)

    passed = 0
    failed = 0

    print("=" * 72)
    print("AI COMPANY — EXPERIENCE CONTRACT TESTS")
    print("stdlib-only runner")
    print("=" * 72)

    for test in tests:
        try:
            test()
        except Exception:
            failed += 1
            print(f"FAIL  {test.__name__}")
            traceback.print_exc()
        else:
            passed += 1
            print(f"PASS  {test.__name__}")

    print("=" * 72)
    print(
        f"RESULT: {passed} passed, {failed} failed, "
        f"{len(tests)} total"
    )
    print("=" * 72)

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    run_tests()
