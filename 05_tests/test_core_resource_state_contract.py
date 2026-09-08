import ast
import importlib.util
import inspect
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import MappingProxyType


CORE_ROOT = Path(__file__).resolve().parents[1] / "02_core"
MODULE_PATH = CORE_ROOT / "resource_state.py"


def load_resource_state_module():
    spec = importlib.util.spec_from_file_location(
        "resource_state",
        MODULE_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Unable to load resource_state module."
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules["resource_state"] = module
    spec.loader.exec_module(module)

    return module


resource_state = load_resource_state_module()


class ResourceStateContractTests(unittest.TestCase):

    def setUp(self):
        self.timestamp = datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=timezone.utc,
        )

        self.provenance = (
            resource_state.ResourceStateProvenance(
                source="test",
                timestamp=self.timestamp,
                authority="ResourceStateAuthority",
            )
        )

        self.state = resource_state.ResourceState(
            resource_state_id="resource-state-001",
            hardware_id="hardware-001",
            evaluated_at=self.timestamp,
            cpu_state={
                "usable_cores": "8",
                "utilization_percent": "25",
            },
            memory_state={
                "usable_gb": "10",
                "available_gb": "12",
            },
            gpu_state={
                "usable": "false",
            },
            storage_state={
                "usable_gb": "900",
                "available_gb": "950",
            },
            network_state={
                "available": "true",
            },
            other_resource_state={
                "system_pressure": "low",
            },
            provenance=self.provenance,
        )

    def test_required_symbols_exist(self):
        self.assertTrue(
            hasattr(
                resource_state,
                "ResourceStateProvenance",
            )
        )

        self.assertTrue(
            hasattr(
                resource_state,
                "ResourceState",
            )
        )

        self.assertTrue(
            hasattr(
                resource_state,
                "ResourceStateAuthority",
            )
        )

    def test_resource_state_is_frozen(self):
        with self.assertRaises(Exception):
            self.state.resource_state_id = "changed"

    def test_provenance_is_frozen(self):
        with self.assertRaises(Exception):
            self.provenance.source = "changed"

    def test_resource_state_mappings_are_read_only(self):
        self.assertIsInstance(
            self.state.cpu_state,
            MappingProxyType,
        )

        self.assertIsInstance(
            self.state.memory_state,
            MappingProxyType,
        )

        self.assertIsInstance(
            self.state.gpu_state,
            MappingProxyType,
        )

        self.assertIsInstance(
            self.state.storage_state,
            MappingProxyType,
        )

        self.assertIsInstance(
            self.state.network_state,
            MappingProxyType,
        )

        self.assertIsInstance(
            self.state.other_resource_state,
            MappingProxyType,
        )

        with self.assertRaises(TypeError):
            self.state.cpu_state["usable_cores"] = "1"

    def test_empty_resource_state_id_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceState(
                resource_state_id="",
                hardware_id="hardware-001",
                evaluated_at=self.timestamp,
                cpu_state={},
                memory_state={},
                gpu_state={},
                storage_state={},
                network_state={},
                other_resource_state={},
                provenance=self.provenance,
            )

    def test_empty_hardware_id_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceState(
                resource_state_id="resource-state-001",
                hardware_id="",
                evaluated_at=self.timestamp,
                cpu_state={},
                memory_state={},
                gpu_state={},
                storage_state={},
                network_state={},
                other_resource_state={},
                provenance=self.provenance,
            )

    def test_naive_evaluation_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceState(
                resource_state_id="resource-state-001",
                hardware_id="hardware-001",
                evaluated_at=datetime(2026, 1, 1, 12, 0),
                cpu_state={},
                memory_state={},
                gpu_state={},
                storage_state={},
                network_state={},
                other_resource_state={},
                provenance=self.provenance,
            )

    def test_naive_provenance_timestamp_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceStateProvenance(
                source="test",
                timestamp=datetime(2026, 1, 1, 12, 0),
                authority="ResourceStateAuthority",
            )

    def test_empty_provenance_source_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceStateProvenance(
                source="",
                timestamp=self.timestamp,
                authority="ResourceStateAuthority",
            )

    def test_empty_provenance_authority_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceStateProvenance(
                source="test",
                timestamp=self.timestamp,
                authority="",
            )

    def test_authority_records_state(self):
        authority = resource_state.ResourceStateAuthority()

        returned = authority.record_state(self.state)

        self.assertIs(returned, self.state)
        self.assertIs(
            authority.get_state("resource-state-001"),
            self.state,
        )

    def test_authority_rejects_duplicate_state_identity(self):
        authority = resource_state.ResourceStateAuthority()

        authority.record_state(self.state)

        with self.assertRaises(ValueError):
            authority.record_state(self.state)

    def test_authority_get_unknown_state_fails(self):
        authority = resource_state.ResourceStateAuthority()

        with self.assertRaises(KeyError):
            authority.get_state("unknown")

    def test_states_for_hardware_returns_immutable_collection(self):
        authority = resource_state.ResourceStateAuthority()

        authority.record_state(self.state)

        states = authority.states_for("hardware-001")

        self.assertEqual(
            states,
            (self.state,),
        )

        self.assertIsInstance(
            states,
            tuple,
        )

    def test_states_for_unknown_hardware_is_empty(self):
        authority = resource_state.ResourceStateAuthority()

        self.assertEqual(
            authority.states_for("unknown"),
            (),
        )

    def test_all_states_returns_read_only_mapping(self):
        authority = resource_state.ResourceStateAuthority()

        authority.record_state(self.state)

        states = authority.all_states()

        self.assertIsInstance(
            states,
            MappingProxyType,
        )

        self.assertEqual(
            states["resource-state-001"],
            self.state,
        )

        with self.assertRaises(TypeError):
            states["another"] = self.state

    def test_authority_owns_mutable_state(self):
        authority = resource_state.ResourceStateAuthority()

        self.assertTrue(
            hasattr(authority, "_states")
        )

        self.assertIsInstance(
            authority._states,
            dict,
        )

    def test_resource_state_does_not_import_forbidden_modules(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden_roots = {
            "psutil",
            "GPUtil",
            "cuda",
            "rocm",
            "subprocess",
            "requests",
            "httpx",
            "sqlalchemy",
            "weft",
        }

        imported_modules = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_modules.extend(
                    alias.name
                    for alias in node.names
                )

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_modules.append(node.module)

        for module_name in imported_modules:
            root = module_name.split(".")[0]

            self.assertNotIn(
                root.lower(),
                {
                    dependency.lower()
                    for dependency in forbidden_roots
                },
                msg=f"Forbidden dependency detected: {module_name}",
            )

    def test_resource_state_has_no_runtime_or_integration_imports(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden_prefixes = (
            "03_runtime",
            "04_integrations",
            "runtime",
            "integrations",
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported = [
                    alias.name
                    for alias in node.names
                ]

                for name in imported:
                    self.assertFalse(
                        name.startswith(forbidden_prefixes),
                        msg=f"Forbidden import detected: {name}",
                    )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                self.assertFalse(
                    module.startswith(forbidden_prefixes),
                    msg=f"Forbidden import detected: {module}",
                )

    def test_resource_state_does_not_define_task_or_agent_selection_logic(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden_identifiers = {
            "task_feasible",
            "task_feasibility",
            "resource_fit",
            "selected_agent",
            "agent_selection",
            "execution_ready",
            "execution_readiness",
            "authorization",
            "authorize_execution",
            "execute_task",
            "execute_work",
            "allocate_task_resources",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                self.assertNotIn(
                    node.id,
                    forbidden_identifiers,
                )

            if isinstance(node, ast.Attribute):
                self.assertNotIn(
                    node.attr,
                    forbidden_identifiers,
                )

    def test_resource_state_does_not_execute_external_work(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden_calls = {
            "system",
            "run",
            "Popen",
            "call",
            "check_call",
            "check_output",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(
                        node.func.id,
                        forbidden_calls,
                    )

                if isinstance(node.func, ast.Attribute):
                    self.assertNotIn(
                        node.func.attr,
                        forbidden_calls,
                    )

    def test_resource_state_has_expected_fields(self):
        fields = resource_state.ResourceState.__dataclass_fields__

        expected = {
            "resource_state_id",
            "hardware_id",
            "evaluated_at",
            "cpu_state",
            "memory_state",
            "gpu_state",
            "storage_state",
            "network_state",
            "other_resource_state",
            "provenance",
        }

        self.assertEqual(
            set(fields),
            expected,
        )

    def test_provenance_has_expected_fields(self):
        fields = (
            resource_state
            .ResourceStateProvenance
            .__dataclass_fields__
        )

        self.assertEqual(
            set(fields),
            {
                "source",
                "timestamp",
                "authority",
            },
        )

    def test_authority_has_expected_api(self):
        expected_methods = {
            "record_state",
            "get_state",
            "states_for",
            "all_states",
        }

        for method_name in expected_methods:
            self.assertTrue(
                hasattr(
                    resource_state.ResourceStateAuthority,
                    method_name,
                ),
                msg=f"Missing authority method: {method_name}",
            )

    def test_resource_state_module_uses_only_stdlib_imports(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        allowed_roots = {
            "dataclasses",
            "datetime",
            "types",
            "typing",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    self.assertIn(root, allowed_roots)

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root = node.module.split(".")[0]
                    self.assertIn(root, allowed_roots)


if __name__ == "__main__":
    unittest.main()
