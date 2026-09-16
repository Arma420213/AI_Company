"""
AI Company Core — Canonical Memory Contract Tests

These tests verify the canonical Memory contract without importing or
depending on Runtime, Integrations, persistence systems, providers,
workflow engines, or OS-specific infrastructure.
"""

from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEMORY_PATH = ROOT / "02_core" / "memory.py"


def load_memory_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_memory_contract",
        MEMORY_PATH,
    )

    if spec is None or spec.loader is None:
        raise AssertionError("Unable to load canonical memory module.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


memory = load_memory_module()

MemoryAuthority = memory.MemoryAuthority
MemoryEvidenceState = memory.MemoryEvidenceState
MemoryProvenance = memory.MemoryProvenance
MemoryReference = memory.MemoryReference
MemoryRecord = memory.MemoryRecord


NOW = datetime.now(timezone.utc)


def provenance(**overrides):
    values = {
        "source": "contract-test",
        "authority": "Test Authority",
        "evidence_timestamp": NOW,
        "source_type": "test",
        "originating_concept": "TestEvidence",
        "originating_identity": "evidence-001",
    }
    values.update(overrides)
    return MemoryProvenance(**values)


def known_record(memory_id: str = "memory-001"):
    return MemoryRecord(
        memory_id=memory_id,
        evidence={
            "status": "completed",
            "attempts": 1,
            "events": ["started", "completed"],
        },
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(),
        retained_at=NOW,
    )


def test_memory_authority_is_canonical_owner():
    authority = MemoryAuthority()

    assert authority.AUTHORITY_NAME == "Memory Authority"
    assert authority.records == {}


def test_memory_record_identity_is_required():
    try:
        MemoryRecord(
            memory_id="",
            evidence="evidence",
            evidence_state=MemoryEvidenceState.KNOWN,
            provenance=provenance(),
            retained_at=NOW,
        )
    except ValueError:
        return

    raise AssertionError("MemoryRecord accepted an empty identity.")


def test_memory_provenance_requires_valid_source_and_authority():
    for field, value in (
        ("source", ""),
        ("authority", ""),
    ):
        values = {
            "source": "source",
            "authority": "authority",
            "evidence_timestamp": NOW,
        }
        values[field] = value

        try:
            MemoryProvenance(**values)
        except ValueError:
            continue

        raise AssertionError(
            f"MemoryProvenance accepted invalid {field}."
        )


def test_memory_provenance_timestamp_is_timezone_aware():
    try:
        MemoryProvenance(
            source="source",
            authority="authority",
            evidence_timestamp=datetime.now(),
        )
    except ValueError:
        return

    raise AssertionError(
        "MemoryProvenance accepted a naive evidence timestamp."
    )


def test_memory_temporal_semantics_are_explicit():
    retained_at = datetime(
        2026,
        9,
        16,
        20,
        0,
        tzinfo=timezone.utc,
    )
    evidence_at = datetime(
        2026,
        9,
        16,
        19,
        0,
        tzinfo=timezone.utc,
    )

    record = MemoryRecord(
        memory_id="memory-time",
        evidence="historical evidence",
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(
            evidence_timestamp=evidence_at,
        ),
        retained_at=retained_at,
    )

    assert record.provenance.evidence_timestamp == evidence_at
    assert record.retained_at == retained_at
    assert (
        record.provenance.evidence_timestamp
        != record.retained_at
    )


def test_memory_reference_does_not_transfer_ownership():
    reference = MemoryReference(
        concept="Task",
        identity="task-001",
    )

    assert reference.concept == "Task"
    assert reference.identity == "task-001"


def test_memory_reference_requires_identity_and_concept():
    for values in (
        {"concept": "", "identity": "id"},
        {"concept": "Task", "identity": ""},
    ):
        try:
            MemoryReference(**values)
        except ValueError:
            continue

        raise AssertionError(
            "MemoryReference accepted an invalid identity/concept."
        )


def test_known_evidence_requires_content():
    try:
        MemoryRecord(
            memory_id="memory-known",
            evidence=None,
            evidence_state=MemoryEvidenceState.KNOWN,
            provenance=provenance(),
            retained_at=NOW,
        )
    except ValueError:
        return

    raise AssertionError(
        "KNOWN evidence was accepted without evidence content."
    )


def test_uncertainty_states_are_distinct_and_preserved():
    expected = {
        "KNOWN",
        "UNAVAILABLE",
        "UNOBSERVED",
        "INCOMPLETE",
        "INCONSISTENT",
    }

    actual = {
        state.value
        for state in MemoryEvidenceState
    }

    assert actual == expected
    assert (
        MemoryEvidenceState.UNAVAILABLE
        != MemoryEvidenceState.UNOBSERVED
    )


def test_structured_evidence_is_preserved_without_semantic_interpretation():
    authority = MemoryAuthority()

    record = authority.retain(
        memory_id="memory-structured",
        evidence={
            "status": "completed",
            "details": {
                "attempts": 2,
                "result": "accepted",
            },
            "events": ["started", "completed"],
        },
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(),
        retained_at=NOW,
    )

    assert record.evidence["status"] == "completed"
    assert record.evidence["details"]["attempts"] == 2
    assert record.evidence["events"] == (
        "started",
        "completed",
    )


def test_structured_evidence_is_immutable():
    authority = MemoryAuthority()

    record = authority.retain(
        memory_id="memory-immutable-structured",
        evidence={
            "status": "completed",
            "details": {
                "attempts": 1,
            },
        },
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(),
        retained_at=NOW,
    )

    try:
        record.evidence["status"] = "changed"
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Memory evidence mapping is mutable."
        )

    try:
        record.evidence["details"]["attempts"] = 99
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Nested Memory evidence mapping is mutable."
        )


def test_memory_record_is_immutable():
    record = known_record()

    try:
        record.memory_id = "changed"
    except Exception:
        pass
    else:
        raise AssertionError(
            "MemoryRecord is mutable."
        )


def test_memory_records_collection_is_read_only():
    authority = MemoryAuthority(
        {"memory-001": known_record()}
    )

    records = authority.records

    assert records["memory-001"].memory_id == "memory-001"

    try:
        records["memory-002"] = known_record("memory-002")
    except TypeError:
        pass
    else:
        raise AssertionError(
            "Memory records collection is mutable."
        )


def test_memory_authority_rejects_duplicate_identity():
    authority = MemoryAuthority(
        {"memory-001": known_record()}
    )

    try:
        authority.retain(
            memory_id="memory-001",
            evidence="replacement",
            evidence_state=MemoryEvidenceState.KNOWN,
            provenance=provenance(),
        )
    except ValueError:
        return

    raise AssertionError(
        "Memory Authority silently overwrote historical evidence."
    )


def test_memory_authority_rejects_non_memory_records():
    try:
        MemoryAuthority(
            {"memory-001": object()}
        )
    except TypeError:
        return

    raise AssertionError(
        "Memory Authority accepted a non-MemoryRecord value."
    )


def test_initial_record_key_must_match_identity():
    record = known_record("memory-001")

    try:
        MemoryAuthority(
            {"different-key": record}
        )
    except ValueError:
        return

    raise AssertionError(
        "Memory Authority accepted mismatched collection identity."
    )


def test_memory_get_record_returns_canonical_record():
    record = known_record()

    authority = MemoryAuthority(
        {"memory-001": record}
    )

    assert authority.get_record("memory-001") is record
    assert authority.get_record("missing") is None


def test_memory_preserves_historical_record_identity():
    authority = MemoryAuthority()

    first = authority.retain(
        memory_id="memory-history-001",
        evidence="original evidence",
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(),
        retained_at=NOW,
    )

    assert authority.get_record(
        "memory-history-001"
    ) is first

    try:
        authority.retain(
            memory_id="memory-history-001",
            evidence="new evidence",
            evidence_state=MemoryEvidenceState.KNOWN,
            provenance=provenance(),
            retained_at=NOW,
        )
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Historical Memory evidence was silently overwritten."
        )

    assert authority.get_record(
        "memory-history-001"
    ).evidence == "original evidence"


def test_memory_provenance_origin_identity_requires_concept():
    try:
        MemoryProvenance(
            source="source",
            authority="authority",
            evidence_timestamp=NOW,
            originating_identity="id",
        )
    except ValueError:
        return

    raise AssertionError(
        "Originating identity was accepted without originating concept."
    )


def test_memory_retain_defaults_to_current_utc_retention_time():
    authority = MemoryAuthority()

    record = authority.retain(
        memory_id="memory-retention-time",
        evidence="evidence",
        evidence_state=MemoryEvidenceState.KNOWN,
        provenance=provenance(),
    )

    assert record.retained_at.tzinfo is not None
    assert record.retained_at.utcoffset() is not None


def test_core_memory_module_has_no_forbidden_infrastructure_imports():
    source = MEMORY_PATH.read_text(encoding="utf-8")

    forbidden_tokens = (
        "requests",
        "httpx",
        "sqlalchemy",
        "sqlite3",
        "boto3",
        "google.cloud",
        "azure",
        "ollama",
        "fastapi",
        "flask",
        "redis",
    )

    for token in forbidden_tokens:
        assert token not in source.lower(), (
            f"Forbidden infrastructure dependency detected: {token}"
        )


def test_memory_contract_has_no_runtime_or_integration_imports():
    source = MEMORY_PATH.read_text(encoding="utf-8").lower()

    forbidden_import_patterns = (
        "02_company_runtime",
        "04_integrations",
        "runtime",
        "integration",
    )

    for pattern in forbidden_import_patterns:
        assert f"import {pattern}" not in source
        assert f"from {pattern}" not in source


def test_memory_preserves_unavailable_without_interpreting_it_as_false():
    authority = MemoryAuthority()

    record = authority.retain(
        memory_id="memory-unavailable",
        evidence=None,
        evidence_state=MemoryEvidenceState.UNAVAILABLE,
        provenance=provenance(),
    )

    assert record.evidence is None
    assert record.evidence_state is MemoryEvidenceState.UNAVAILABLE


def test_memory_preserves_unobserved_without_interpreting_it_as_false():
    authority = MemoryAuthority()

    record = authority.retain(
        memory_id="memory-unobserved",
        evidence=None,
        evidence_state=MemoryEvidenceState.UNOBSERVED,
        provenance=provenance(),
    )

    assert record.evidence is None
    assert record.evidence_state is MemoryEvidenceState.UNOBSERVED


def test_memory_preserves_incomplete_and_inconsistent_evidence_states():
    authority = MemoryAuthority()

    incomplete = authority.retain(
        memory_id="memory-incomplete",
        evidence="partial evidence",
        evidence_state=MemoryEvidenceState.INCOMPLETE,
        provenance=provenance(),
    )

    inconsistent = authority.retain(
        memory_id="memory-inconsistent",
        evidence={
            "sources": ["A", "B"],
            "values": [1, 2],
        },
        evidence_state=MemoryEvidenceState.INCONSISTENT,
        provenance=provenance(),
    )

    assert incomplete.evidence_state is MemoryEvidenceState.INCOMPLETE
    assert inconsistent.evidence_state is (
        MemoryEvidenceState.INCONSISTENT
    )


def run_all_tests() -> None:
    tests = [
        value
        for name, value in globals().items()
        if name.startswith("test_")
        and callable(value)
    ]

    for test in sorted(tests, key=lambda item: item.__name__):
        test()
        print(f"OK: {test.__name__}")


if __name__ == "__main__":
    run_all_tests()
