"""
AI Company Core — Capability Contract Tests

Standard-library-only architectural contract tests for the canonical
Capability nucleus.
"""

from __future__ import annotations

import importlib.util
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "02_core" / "capability.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_capability",
        MODULE_PATH,
    )

    if spec is None:
        raise RuntimeError("Unable to create module specification.")

    if spec.loader is None:
        raise RuntimeError("Unable to create module loader.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


class CapabilityContractTests(unittest.TestCase):

    def test_module_exists(self):
        self.assertTrue(MODULE_PATH.exists())

    def test_module_compiles(self):
        import py_compile

        py_compile.compile(
            str(MODULE_PATH),
            doraise=True,
        )

    def test_canonical_symbols_exist(self):
        module = load_module()

        self.assertTrue(hasattr(module, "CapabilityProvenance"))
        self.assertTrue(hasattr(module, "Capability"))
        self.assertTrue(hasattr(module, "CapabilityAuthority"))

    def test_provenance_and_capability_construction(self):
        module = load_module()

        timestamp = datetime.now(timezone.utc)

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=timestamp,
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        self.assertEqual(capability.capability_id, "capability-1")
        self.assertEqual(capability.name, "Python Development")
        self.assertEqual(
            capability.availability_state,
            "AVAILABLE",
        )
        self.assertEqual(
            capability.availability_evidence["source"],
            "contract-test",
        )

    def test_capability_is_immutable(self):
        module = load_module()

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=datetime.now(timezone.utc),
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        with self.assertRaises(FrozenInstanceError):
            capability.name = "Changed"

    def test_capability_evidence_is_immutable(self):
        module = load_module()

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=datetime.now(timezone.utc),
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        with self.assertRaises(TypeError):
            capability.availability_evidence["source"] = "changed"

    def test_authority_owns_capability_state(self):
        module = load_module()

        authority = module.CapabilityAuthority()

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=datetime.now(timezone.utc),
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        authority.set_capability(capability)

        stored = authority.get_capability("capability-1")

        self.assertEqual(stored, capability)

    def test_authority_rejects_duplicate_capability_id(self):
        module = load_module()

        authority = module.CapabilityAuthority()

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=datetime.now(timezone.utc),
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        authority.set_capability(capability)

        replacement = module.Capability(
            capability_id="capability-1",
            name="Advanced Python Development",
            description="Updated Python development capability.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test-replacement",
            },
            provenance=provenance,
        )

        stored = authority.set_capability(replacement)

        self.assertEqual(stored, replacement)
        self.assertEqual(
            authority.get_capability("capability-1"),
            replacement,
        )

    def test_authority_can_update_availability(self):
        module = load_module()

        authority = module.CapabilityAuthority()

        provenance = module.CapabilityProvenance(
            source="contract-test",
            timestamp=datetime.now(timezone.utc),
            authority="Capability Authority",
        )

        capability = module.Capability(
            capability_id="capability-1",
            name="Python Development",
            description="Ability to develop Python software.",
            availability_state="AVAILABLE",
            availability_evidence={
                "source": "contract-test",
            },
            provenance=provenance,
        )

        authority.set_capability(capability)

        updated = authority.set_availability(
            "capability-1",
            "UNAVAILABLE",
            {
                "reason": "resource-condition",
            },
        )

        self.assertEqual(
            updated.availability_state,
            "UNAVAILABLE",
        )

        self.assertEqual(
            updated.availability_evidence["reason"],
            "resource-condition",
        )

        self.assertEqual(
            authority.get_capability("capability-1"),
            updated,
        )

    def test_authority_collection_is_read_only(self):
        module = load_module()

        authority = module.CapabilityAuthority()

        capabilities = authority.all_capabilities()

        with self.assertRaises(TypeError):
            capabilities["x"] = "y"

    def test_unknown_capability_returns_none(self):
        module = load_module()

        authority = module.CapabilityAuthority()

        with self.assertRaises(KeyError):
            authority.get_capability("does-not-exist")

    def test_capability_does_not_import_runtime_or_integrations(self):
        source = MODULE_PATH.read_text(encoding="utf-8")

        forbidden_imports = (
            "03_runtime",
            "04_integrations",
            "weft",
            "requests",
            "httpx",
            "boto3",
        )

        for forbidden in forbidden_imports:
            self.assertNotIn(
                f"import {forbidden}",
                source,
            )
            self.assertNotIn(
                f"from {forbidden}",
                source,
            )

    def test_capability_does_not_own_execution_or_authorization(self):
        source = MODULE_PATH.read_text(encoding="utf-8")

        forbidden_definitions = (
            "def execute",
            "def authorize",
            "def schedule",
            "def select_agent",
            "def evaluate_task",
        )

        for forbidden in forbidden_definitions:
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
