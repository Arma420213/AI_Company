"""
AI Company Core — Hardware Capability Contract Tests

Standard-library-only architectural contract tests for the canonical
Hardware Capability nucleus.
"""

from __future__ import annotations

import importlib.util
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "02_core" / "hardware_capability.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_hardware_capability",
        MODULE_PATH,
    )

    if spec is None:
        raise RuntimeError(
            "Unable to create module specification."
        )

    if spec.loader is None:
        raise RuntimeError(
            "Unable to create module loader."
        )

    module = importlib.util.module_from_spec(spec)

    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def make_capability(module):
    provenance = module.HardwareCapabilityProvenance(
        source="contract-test",
        timestamp=datetime.now(timezone.utc),
        authority="Hardware Capability Authority",
    )

    return module.HardwareCapability(
        hardware_id="hardware-1",
        cpu_capability={
            "architecture": "x86_64",
            "core_count": "12",
            "thread_count": "24",
        },
        memory_capability={
            "total_gb": "15.58",
        },
        gpu_capability={
            "present": "false",
        },
        storage_capability={
            "total_gb": "1007",
        },
        other_capabilities={
            "virtualization": "supported",
        },
        provenance=provenance,
    )


class HardwareCapabilityContractTests(unittest.TestCase):

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

        self.assertTrue(
            hasattr(
                module,
                "HardwareCapabilityProvenance",
            )
        )

        self.assertTrue(
            hasattr(
                module,
                "HardwareCapability",
            )
        )

        self.assertTrue(
            hasattr(
                module,
                "HardwareCapabilityAuthority",
            )
        )

    def test_hardware_capability_construction(self):
        module = load_module()

        capability = make_capability(module)

        self.assertEqual(
            capability.hardware_id,
            "hardware-1",
        )

        self.assertEqual(
            capability.cpu_capability["architecture"],
            "x86_64",
        )

        self.assertEqual(
            capability.cpu_capability["core_count"],
            "12",
        )

        self.assertEqual(
            capability.memory_capability["total_gb"],
            "15.58",
        )

        self.assertEqual(
            capability.gpu_capability["present"],
            "false",
        )

        self.assertEqual(
            capability.storage_capability["total_gb"],
            "1007",
        )

    def test_hardware_capability_is_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(FrozenInstanceError):
            capability.hardware_id = "changed"

    def test_cpu_capability_is_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(TypeError):
            capability.cpu_capability[
                "core_count"
            ] = "999"

    def test_memory_capability_is_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(TypeError):
            capability.memory_capability[
                "total_gb"
            ] = "9999"

    def test_gpu_capability_is_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(TypeError):
            capability.gpu_capability[
                "present"
            ] = "true"

    def test_storage_capability_is_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(TypeError):
            capability.storage_capability[
                "total_gb"
            ] = "9999"

    def test_other_capabilities_are_immutable(self):
        module = load_module()

        capability = make_capability(module)

        with self.assertRaises(TypeError):
            capability.other_capabilities[
                "new"
            ] = "value"

    def test_authority_owns_capability(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()
        capability = make_capability(module)

        stored = authority.set_capability(
            capability
        )

        self.assertEqual(
            stored,
            capability,
        )

        self.assertEqual(
            authority.get_capability("hardware-1"),
            capability,
        )

    def test_authority_can_replace_existing_profile(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()

        original = make_capability(module)
        authority.set_capability(original)

        replacement = module.HardwareCapability(
            hardware_id="hardware-1",
            cpu_capability={
                "architecture": "x86_64",
                "core_count": "16",
                "thread_count": "32",
            },
            memory_capability={
                "total_gb": "31.16",
            },
            gpu_capability={
                "present": "true",
            },
            storage_capability={
                "total_gb": "2000",
            },
            other_capabilities={
                "virtualization": "supported",
            },
            provenance=module.HardwareCapabilityProvenance(
                source="contract-test-replacement",
                timestamp=datetime.now(timezone.utc),
                authority="Hardware Capability Authority",
            ),
        )

        stored = authority.set_capability(
            replacement
        )

        self.assertEqual(
            stored,
            replacement,
        )

        self.assertEqual(
            authority.get_capability("hardware-1"),
            replacement,
        )

    def test_authority_can_update_existing_profile(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()

        original = make_capability(module)
        authority.set_capability(original)

        updated = module.HardwareCapability(
            hardware_id="hardware-1",
            cpu_capability={
                "architecture": "x86_64",
                "core_count": "14",
                "thread_count": "28",
            },
            memory_capability={
                "total_gb": "15.58",
            },
            gpu_capability={
                "present": "false",
            },
            storage_capability={
                "total_gb": "1007",
            },
            other_capabilities={
                "virtualization": "supported",
            },
            provenance=module.HardwareCapabilityProvenance(
                source="contract-test-update",
                timestamp=datetime.now(timezone.utc),
                authority="Hardware Capability Authority",
            ),
        )

        stored = authority.update_capability(
            updated
        )

        self.assertEqual(
            stored,
            updated,
        )

        self.assertEqual(
            authority.get_capability("hardware-1"),
            updated,
        )

    def test_update_unknown_profile_fails(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()
        capability = make_capability(module)

        with self.assertRaises(KeyError):
            authority.update_capability(
                capability
            )

    def test_authority_collection_is_read_only(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()
        capabilities = authority.all_capabilities()

        with self.assertRaises(TypeError):
            capabilities[
                "hardware-1"
            ] = make_capability(module)

    def test_unknown_hardware_capability_returns_key_error(self):
        module = load_module()

        authority = module.HardwareCapabilityAuthority()

        with self.assertRaises(KeyError):
            authority.get_capability(
                "does-not-exist"
            )

    def test_empty_hardware_identity_is_rejected(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.HardwareCapability(
                hardware_id="",
                cpu_capability={},
                memory_capability={},
                gpu_capability={},
                storage_capability={},
                other_capabilities={},
                provenance=module.HardwareCapabilityProvenance(
                    source="contract-test",
                    timestamp=datetime.now(timezone.utc),
                    authority="Hardware Capability Authority",
                ),
            )

    def test_empty_provenance_source_is_rejected(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.HardwareCapabilityProvenance(
                source="",
                timestamp=datetime.now(timezone.utc),
                authority="Hardware Capability Authority",
            )

    def test_empty_provenance_authority_is_rejected(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.HardwareCapabilityProvenance(
                source="contract-test",
                timestamp=datetime.now(timezone.utc),
                authority="",
            )

    def test_naive_provenance_timestamp_is_rejected(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.HardwareCapabilityProvenance(
                source="contract-test",
                timestamp=datetime.now(),
                authority="Hardware Capability Authority",
            )

    def test_module_has_no_runtime_or_integration_imports(self):
        source = MODULE_PATH.read_text(
            encoding="utf-8"
        )

        forbidden_imports = (
            "03_runtime",
            "04_integrations",
            "weft",
            "requests",
            "httpx",
            "boto3",
            "psutil",
            "GPUtil",
            "torch",
            "cuda",
            "rocm",
            "subprocess",
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

    def test_module_does_not_own_hardware_observation(self):
        source = MODULE_PATH.read_text(
            encoding="utf-8"
        )

        forbidden_definitions = (
            "def observe",
            "def measure",
            "def sample",
            "def probe",
            "def inspect_hardware",
            "def detect_hardware",
        )

        for forbidden in forbidden_definitions:
            self.assertNotIn(
                forbidden,
                source,
            )

    def test_module_does_not_own_resource_state(self):
        source = MODULE_PATH.read_text(
            encoding="utf-8"
        )

        forbidden_runtime_definitions = (
            "def get_utilization",
            "def measure_utilization",
            "def current_utilization",
            "def get_current_usage",
            "def measure_current_usage",
            "def get_available_resources",
            "def allocate_resources",
        )

        forbidden_resource_types = (
            "ResourceState",
        )

        for forbidden in forbidden_runtime_definitions:
            self.assertNotIn(
                forbidden,
                source,
            )

        for forbidden in forbidden_resource_types:
            self.assertNotIn(
                forbidden,
                source,
            )

    def test_hardware_capability_contains_no_current_state_fields(self):
        module = load_module()

        capability = make_capability(module)

        forbidden_fields = (
            "available_gb",
            "current_usage",
            "current_load",
            "utilization",
            "allocated_resources",
            "free_resources",
        )

        for field_name in forbidden_fields:
            self.assertNotIn(
                field_name,
                capability.__dict__,
            )

    def test_module_does_not_own_execution_or_decision_semantics(self):
        source = MODULE_PATH.read_text(
            encoding="utf-8"
        )

        forbidden_definitions = (
            "def execute",
            "def authorize",
            "def schedule",
            "def select_agent",
            "def evaluate_task",
            "def allocate",
        )

        for forbidden in forbidden_definitions:
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
