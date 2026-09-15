import ast
import importlib.util
import sys
import unittest
from datetime import datetime, timedelta, timezone
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

hardware_capability_spec = importlib.util.spec_from_file_location(
    "hardware_capability",
    CORE_ROOT / "hardware_capability.py",
)

if hardware_capability_spec is None or hardware_capability_spec.loader is None:
    raise RuntimeError(
        "Unable to load hardware_capability module."
    )

hardware_capability = importlib.util.module_from_spec(
    hardware_capability_spec
)
sys.modules["hardware_capability"] = hardware_capability
hardware_capability_spec.loader.exec_module(
    hardware_capability
)

hardware_observation_spec = importlib.util.spec_from_file_location(
    "hardware_observation",
    CORE_ROOT / "hardware_observation.py",
)

if hardware_observation_spec is None or hardware_observation_spec.loader is None:
    raise RuntimeError(
        "Unable to load hardware_observation module."
    )

hardware_observation = importlib.util.module_from_spec(
    hardware_observation_spec
)
sys.modules["hardware_observation"] = hardware_observation
hardware_observation_spec.loader.exec_module(
    hardware_observation
)


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

        self.provenance = resource_state.ResourceStateProvenance(
            source="test",
            timestamp=self.timestamp,
            authority="ResourceStateAuthority",
        )

        self.capability = hardware_capability.HardwareCapability(
            hardware_id="hardware-001",
            cpu_capability={
                "cores": "12",
                "threads": "12",
            },
            memory_capability={
                "gb": "15.58",
            },
            gpu_capability={
                "present": "true",
                "gb": "4",
            },
            storage_capability={
                "gb": "1007",
            },
            other_capabilities={},
            provenance=hardware_capability.HardwareCapabilityProvenance(
                source="test",
                timestamp=self.timestamp,
                authority="HardwareCapabilityAuthority",
            ),
        )

        self.observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation={
                "available": "8",
            },
            memory_observation={
                "available_gb": "10",
            },
            gpu_observation={
                "usable": "true",
                "gb": "3",
            },
            storage_observation={
                "available_gb": "900",
            },
            other_observations={
                "network_available": "true",
                "system_pressure": "low",
            },
            provenance=hardware_observation.HardwareObservationProvenance(
                source="test-observer",
                timestamp=self.timestamp,
                authority="HardwareObserver",
            ),
        )

        self.rules = resource_state.ResourceInterpretationRules()

        self.constraints = resource_state.ResourceConstraints.empty()

    def derive(self, **kwargs):
        authority = resource_state.ResourceStateAuthority()

        return authority.derive_state(
            self.capability,
            self.observation,
            self.rules,
            self.constraints,
            resource_state_id="resource-state-001",
            evaluated_at=self.timestamp,
            **kwargs,
        )

    # --------------------------------------------------------
    # Canonical symbols
    # --------------------------------------------------------

    def test_required_symbols_exist(self):
        required = {
            "ResourceValueStatus",
            "ResourceValue",
            "ResourceInterpretationRules",
            "ResourceConstraints",
            "ResourceStateProvenance",
            "ResourceState",
            "ResourceStateAuthority",
        }

        for name in required:
            self.assertTrue(
                hasattr(resource_state, name),
                msg=f"Missing canonical symbol: {name}",
            )

    # --------------------------------------------------------
    # Resource Value semantics
    # --------------------------------------------------------

    def test_resource_value_is_frozen(self):
        value = resource_state.ResourceValue(
            dimension="cpu",
            status=resource_state.ResourceValueStatus.KNOWN,
            quantity=8,
            unit="cores",
        )

        with self.assertRaises(Exception):
            value.quantity = 4

    def test_known_quantitative_value_requires_quantity(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceValue(
                dimension="cpu",
                status=resource_state.ResourceValueStatus.KNOWN,
            )

    def test_known_network_value_may_be_semantic(self):
        value = resource_state.ResourceValue(
            dimension="network",
            status=resource_state.ResourceValueStatus.KNOWN,
        )

        self.assertIsNone(value.quantity)

    def test_negative_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceValue(
                dimension="cpu",
                status=resource_state.ResourceValueStatus.KNOWN,
                quantity=-1,
                unit="cores",
            )

    def test_nan_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceValue(
                dimension="cpu",
                status=resource_state.ResourceValueStatus.KNOWN,
                quantity=float("nan"),
                unit="cores",
            )

    def test_infinite_quantity_is_rejected(self):
        with self.assertRaises(ValueError):
            resource_state.ResourceValue(
                dimension="cpu",
                status=resource_state.ResourceValueStatus.KNOWN,
                quantity=float("inf"),
                unit="cores",
            )

    def test_unobserved_value_has_no_quantity(self):
        value = resource_state.ResourceValue(
            dimension="cpu",
            status=resource_state.ResourceValueStatus.UNOBSERVED,
        )

        self.assertIsNone(value.quantity)

    def test_unavailable_value_has_no_quantity(self):
        value = resource_state.ResourceValue(
            dimension="cpu",
            status=resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(value.quantity)

    # --------------------------------------------------------
    # Resource State construction
    # --------------------------------------------------------

    def test_derived_state_has_canonical_dimensions(self):
        state = self.derive()

        self.assertEqual(state.cpu.dimension, "cpu")
        self.assertEqual(state.memory.dimension, "memory")
        self.assertEqual(state.gpu.dimension, "gpu")
        self.assertEqual(state.storage.dimension, "storage")
        self.assertEqual(state.network.dimension, "network")

    def test_derived_state_is_frozen(self):
        state = self.derive()

        with self.assertRaises(Exception):
            state.hardware_id = "changed"

    def test_derived_state_values_are_read_only(self):
        state = self.derive()

        values = state.values()

        self.assertIsInstance(
            values,
            MappingProxyType,
        )

        with self.assertRaises(TypeError):
            values["cpu"] = state.cpu

    def test_other_resources_are_not_inferred_from_arbitrary_metadata(self):
        state = self.derive()

        self.assertEqual(
            state.other_resources,
            {},
        )

    # --------------------------------------------------------
    # Derivation chain
    # --------------------------------------------------------

    def test_derivation_uses_capability_and_observation(self):
        state = self.derive()

        self.assertEqual(
            state.cpu.quantity,
            8,
        )

        self.assertEqual(
            state.memory.quantity,
            10,
        )

        self.assertEqual(
            state.storage.quantity,
            900,
        )

    def test_capability_ceiling_is_enforced(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation={"available": "99"},
            memory_observation={"available_gb": "99"},
            gpu_observation={"usable": "true", "gb": "99"},
            storage_observation={"available_gb": "9999"},
            other_observations={"network_available": "true"},
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="ceiling-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.cpu.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(
            state.cpu.quantity,
        )

        self.assertEqual(
            state.memory.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(
            state.memory.quantity,
        )

        self.assertEqual(
            state.storage.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(
            state.storage.quantity,
        )

    def test_constrained_network_value_may_be_semantic(self):
        value = resource_state.ResourceValue(
            dimension="network",
            status=resource_state.ResourceValueStatus.CONSTRAINED,
            limitation="network access is operationally restricted",
        )

        self.assertEqual(
            value.status,
            resource_state.ResourceValueStatus.CONSTRAINED,
        )
        self.assertIsNone(value.quantity)
        self.assertEqual(
            value.limitation,
            "network access is operationally restricted",
        )

    def test_gpu_usable_without_quantity_is_incomplete(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation=self.observation.cpu_observation,
            memory_observation=self.observation.memory_observation,
            gpu_observation={
                "usable": "true",
            },
            storage_observation=self.observation.storage_observation,
            other_observations=self.observation.other_observations,
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="gpu-incomplete-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.gpu.status,
            resource_state.ResourceValueStatus.INCOMPLETE,
        )
        self.assertIsNone(state.gpu.quantity)

    # --------------------------------------------------------
    # Unknown / unavailable / incomplete
    # --------------------------------------------------------

    def test_unknown_is_not_zero(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation={},
            memory_observation={},
            gpu_observation={},
            storage_observation={},
            other_observations={},
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="unknown-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.cpu.status,
            resource_state.ResourceValueStatus.UNOBSERVED,
        )

        self.assertIsNone(state.cpu.quantity)

    def test_incomplete_observation_is_distinct_from_unknown(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation={
                "utilization_percent": "25",
            },
            memory_observation={},
            gpu_observation={},
            storage_observation={},
            other_observations={},
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="incomplete-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.cpu.status,
            resource_state.ResourceValueStatus.INCOMPLETE,
        )

    def test_stale_observation_becomes_unavailable(self):
        rules = resource_state.ResourceInterpretationRules(
            freshness_threshold=timedelta(minutes=5),
        )

        evaluated_at = self.timestamp + timedelta(
            minutes=10,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            self.observation,
            rules,
            self.constraints,
            resource_state_id="stale-test",
            evaluated_at=evaluated_at,
        )

        self.assertEqual(
            state.cpu.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

    # --------------------------------------------------------
    # Constraints
    # --------------------------------------------------------

    def test_constraints_reduce_capacity(self):
        constraints = resource_state.ResourceConstraints(
            reserved={"cpu": 2},
            committed={"memory": 2},
            contention={"storage": 100},
            environmental_limitations={},
            operational_restrictions={},
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            self.observation,
            self.rules,
            constraints,
            resource_state_id="constraint-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(state.cpu.quantity, 6)
        self.assertEqual(state.memory.quantity, 8)
        self.assertEqual(state.storage.quantity, 800)

    def test_constraints_cannot_create_capacity(self):
        constraints = resource_state.ResourceConstraints(
            reserved={"cpu": 999},
            committed={},
            contention={},
            environmental_limitations={},
            operational_restrictions={},
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            self.observation,
            self.rules,
            constraints,
            resource_state_id="constraint-floor-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.cpu.quantity,
            0,
        )

        self.assertEqual(
            state.cpu.status,
            resource_state.ResourceValueStatus.CONSTRAINED,
        )

    # --------------------------------------------------------
    # Network semantics
    # --------------------------------------------------------

    def test_network_is_semantic_not_fake_numeric_capacity(self):
        state = self.derive()

        self.assertEqual(
            state.network.status,
            resource_state.ResourceValueStatus.KNOWN,
        )

        self.assertIsNone(
            state.network.quantity,
        )

    def test_network_unavailability_is_distinct(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation=self.observation.cpu_observation,
            memory_observation=self.observation.memory_observation,
            gpu_observation=self.observation.gpu_observation,
            storage_observation=self.observation.storage_observation,
            other_observations={
                "network_available": "false",
            },
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="network-unavailable-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.network.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(
            state.network.quantity,
        )

    # --------------------------------------------------------
    # GPU semantics
    # --------------------------------------------------------

    def test_gpu_usable_state_is_known(self):
        state = self.derive()

        self.assertEqual(
            state.gpu.status,
            resource_state.ResourceValueStatus.KNOWN,
        )

        self.assertIsNotNone(
            state.gpu.quantity,
        )

    def test_gpu_unusable_state_is_not_zero_capacity(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="hardware-001",
            observed_at=self.timestamp,
            cpu_observation=self.observation.cpu_observation,
            memory_observation=self.observation.memory_observation,
            gpu_observation={
                "usable": "false",
            },
            storage_observation=self.observation.storage_observation,
            other_observations={
                "network_available": "true",
            },
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            observation,
            self.rules,
            self.constraints,
            resource_state_id="gpu-unusable-test",
            evaluated_at=self.timestamp,
        )

        self.assertEqual(
            state.gpu.status,
            resource_state.ResourceValueStatus.UNAVAILABLE,
        )

        self.assertIsNone(
            state.gpu.quantity,
        )

    # --------------------------------------------------------
    # Provenance
    # --------------------------------------------------------

    def test_provenance_is_frozen(self):
        provenance = self.derive().provenance

        with self.assertRaises(Exception):
            provenance.source = "changed"

    def test_provenance_contains_observation_origin(self):
        provenance = self.derive().provenance

        self.assertEqual(
            provenance.observation_source,
            "test-observer",
        )

        self.assertEqual(
            provenance.observation_timestamp,
            self.timestamp,
        )

    # --------------------------------------------------------
    # Authority
    # --------------------------------------------------------

    def test_authority_records_derived_state(self):
        authority = resource_state.ResourceStateAuthority()

        state = authority.derive_state(
            self.capability,
            self.observation,
            self.rules,
            self.constraints,
            resource_state_id="authority-test",
            evaluated_at=self.timestamp,
        )

        self.assertIs(
            authority.get_state("authority-test"),
            state,
        )

    def test_authority_rejects_duplicate_state_identity(self):
        authority = resource_state.ResourceStateAuthority()

        state = self.derive()

        authority.record_state(state)

        with self.assertRaises(ValueError):
            authority.record_state(state)

    def test_authority_unknown_state_fails(self):
        authority = resource_state.ResourceStateAuthority()

        with self.assertRaises(KeyError):
            authority.get_state("unknown")

    def test_authority_history_is_read_only(self):
        authority = resource_state.ResourceStateAuthority()

        state = self.derive()

        authority.record_state(state)

        states = authority.all_states()

        self.assertIsInstance(
            states,
            MappingProxyType,
        )

        with self.assertRaises(TypeError):
            states["another"] = state

    def test_states_for_hardware_is_immutable(self):
        authority = resource_state.ResourceStateAuthority()

        state = self.derive()

        authority.record_state(state)

        states = authority.states_for("hardware-001")

        self.assertIsInstance(
            states,
            tuple,
        )

    # --------------------------------------------------------
    # Input identity
    # --------------------------------------------------------

    def test_capability_and_observation_hardware_identity_must_match(self):
        observation = hardware_observation.HardwareObservation(
            hardware_id="different-hardware",
            observed_at=self.timestamp,
            cpu_observation=self.observation.cpu_observation,
            memory_observation=self.observation.memory_observation,
            gpu_observation=self.observation.gpu_observation,
            storage_observation=self.observation.storage_observation,
            other_observations=self.observation.other_observations,
            provenance=self.observation.provenance,
        )

        authority = resource_state.ResourceStateAuthority()

        with self.assertRaises(ValueError):
            authority.derive_state(
                self.capability,
                observation,
                self.rules,
                self.constraints,
                resource_state_id="identity-test",
                evaluated_at=self.timestamp,
            )

    # --------------------------------------------------------
    # Architectural isolation
    # --------------------------------------------------------

    def test_resource_state_uses_only_stdlib_imports(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        allowed_roots = {
            "dataclasses",
            "datetime",
            "math",
            "types",
            "typing",
            "enum",
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

    def test_no_runtime_or_integration_dependencies(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden = (
            "03_runtime",
            "04_integrations",
            "runtime",
            "integrations",
            "weft",
            "psutil",
            "GPUtil",
            "cuda",
            "rocm",
            "requests",
            "httpx",
            "sqlalchemy",
            "subprocess",
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [
                    alias.name
                    for alias in node.names
                ]

                for name in names:
                    self.assertFalse(
                        name.startswith(forbidden),
                        msg=f"Forbidden import: {name}",
                    )

            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""

                self.assertFalse(
                    module.startswith(forbidden),
                    msg=f"Forbidden import: {module}",
                )

    def test_no_task_agent_selection_or_execution_logic(self):
        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        forbidden = {
            "task_feasible",
            "task_feasibility",
            "resource_fit",
            "selected_agent",
            "agent_selection",
            "execution_ready",
            "execution_readiness",
            "authorize_execution",
            "execute_task",
            "execute_work",
            "allocate_task_resources",
            "schedule",
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                self.assertNotIn(node.id, forbidden)

            elif isinstance(node, ast.Attribute):
                self.assertNotIn(node.attr, forbidden)


if __name__ == "__main__":
    unittest.main()
