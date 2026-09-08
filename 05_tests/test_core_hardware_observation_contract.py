import importlib.util
import sys
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "02_core"
    / "hardware_observation.py"
)


def load_module():
    spec = importlib.util.spec_from_file_location(
        "hardware_observation",
        MODULE_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Unable to load hardware_observation.py"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


MODULE = load_module()


class HardwareObservationContractTests(unittest.TestCase):

    def make_provenance(self):
        return MODULE.HardwareObservationProvenance(
            source="test-observer",
            timestamp=datetime.now(timezone.utc),
            authority="Hardware Observer",
        )

    def make_observation(self):
        return MODULE.HardwareObservation(
            hardware_id="hardware-1",
            observed_at=datetime.now(timezone.utc),
            cpu_observation={
                "utilization_percent": "37.4",
                "temperature_c": "52.0",
            },
            memory_observation={
                "used_gb": "4.20",
                "available_gb": "11.38",
            },
            gpu_observation={
                "present": "false",
            },
            storage_observation={
                "used_gb": "56.00",
                "available_gb": "951.00",
            },
            other_observations={
                "network_state": "connected",
            },
            provenance=self.make_provenance(),
        )

    def test_module_compiles(self):
        source = MODULE_PATH.read_text()
        compile(source, str(MODULE_PATH), "exec")

    def test_required_symbols_exist(self):
        self.assertTrue(
            hasattr(MODULE, "HardwareObservationProvenance")
        )
        self.assertTrue(
            hasattr(MODULE, "HardwareObservation")
        )
        self.assertTrue(
            hasattr(MODULE, "HardwareObserver")
        )

    def test_observation_constructs(self):
        observation = self.make_observation()

        self.assertEqual(
            observation.hardware_id,
            "hardware-1",
        )

        self.assertEqual(
            observation.cpu_observation[
                "utilization_percent"
            ],
            "37.4",
        )

    def test_provenance_is_frozen(self):
        provenance = self.make_provenance()

        with self.assertRaises(FrozenInstanceError):
            provenance.source = "changed"

    def test_observation_is_frozen(self):
        observation = self.make_observation()

        with self.assertRaises(FrozenInstanceError):
            observation.hardware_id = "changed"

    def test_observation_mappings_are_read_only(self):
        observation = self.make_observation()

        with self.assertRaises(TypeError):
            observation.cpu_observation[
                "new"
            ] = "value"

        with self.assertRaises(TypeError):
            observation.memory_observation[
                "new"
            ] = "value"

        with self.assertRaises(TypeError):
            observation.gpu_observation[
                "new"
            ] = "value"

        with self.assertRaises(TypeError):
            observation.storage_observation[
                "new"
            ] = "value"

        with self.assertRaises(TypeError):
            observation.other_observations[
                "new"
            ] = "value"

    def test_observer_records_observation(self):
        observer = MODULE.HardwareObserver()
        observation = self.make_observation()

        result = observer.record_observation(
            observation
        )

        self.assertIs(
            result,
            observation,
        )

        self.assertIs(
            observer.get_observation(
                "hardware-1",
                observation.observed_at,
            ),
            observation,
        )

    def test_observations_for_returns_tuple(self):
        observer = MODULE.HardwareObserver()
        observation = self.make_observation()

        observer.record_observation(observation)

        result = observer.observations_for(
            "hardware-1"
        )

        self.assertIsInstance(
            result,
            tuple,
        )

        self.assertEqual(
            result,
            (observation,),
        )

    def test_all_observations_is_read_only(self):
        observer = MODULE.HardwareObserver()
        observation = self.make_observation()

        observer.record_observation(observation)

        result = observer.all_observations()

        with self.assertRaises(TypeError):
            result["hardware-2"] = ()

    def test_unknown_observation_raises_key_error(self):
        observer = MODULE.HardwareObserver()

        with self.assertRaises(KeyError):
            observer.get_observation(
                "unknown",
                datetime.now(timezone.utc),
            )

    def test_unknown_hardware_returns_empty_tuple(self):
        observer = MODULE.HardwareObserver()

        self.assertEqual(
            observer.observations_for(
                "unknown"
            ),
            (),
        )

    def test_provenance_source_required(self):
        with self.assertRaises(ValueError):
            MODULE.HardwareObservationProvenance(
                source="",
                timestamp=datetime.now(timezone.utc),
                authority="Hardware Observer",
            )

    def test_provenance_authority_required(self):
        with self.assertRaises(ValueError):
            MODULE.HardwareObservationProvenance(
                source="test",
                timestamp=datetime.now(timezone.utc),
                authority="",
            )

    def test_provenance_timestamp_must_be_timezone_aware(self):
        with self.assertRaises(ValueError):
            MODULE.HardwareObservationProvenance(
                source="test",
                timestamp=datetime.now(),
                authority="Hardware Observer",
            )

    def test_observation_timestamp_must_be_timezone_aware(self):
        with self.assertRaises(ValueError):
            MODULE.HardwareObservation(
                hardware_id="hardware-1",
                observed_at=datetime.now(),
                cpu_observation={},
                memory_observation={},
                gpu_observation={},
                storage_observation={},
                other_observations={},
                provenance=self.make_provenance(),
            )

    def test_hardware_id_required(self):
        with self.assertRaises(ValueError):
            MODULE.HardwareObservation(
                hardware_id="",
                observed_at=datetime.now(timezone.utc),
                cpu_observation={},
                memory_observation={},
                gpu_observation={},
                storage_observation={},
                other_observations={},
                provenance=self.make_provenance(),
            )

    def test_no_external_imports(self):
        source = MODULE_PATH.read_text()

        forbidden = (
            "03_runtime",
            "04_integrations",
            "weft",
            "psutil",
            "GPUtil",
            "cuda",
            "rocm",
            "subprocess",
            "requests",
            "httpx",
            "boto3",
        )

        lowered = source.lower()

        for dependency in forbidden:
            self.assertNotIn(
                dependency.lower(),
                lowered,
                dependency,
            )

    def test_no_os_specific_imports(self):
        source = MODULE_PATH.read_text()

        forbidden_imports = (
            "import os",
            "from os ",
            "import win32",
            "from win32",
            "import wmi",
            "from wmi",
            "import ctypes",
            "from ctypes",
            "import psutil",
            "from psutil",
        )

        lowered = source.lower()

        for forbidden in forbidden_imports:
            self.assertNotIn(
                forbidden.lower(),
                lowered,
                forbidden,
            )

    def test_no_resource_state_authority(self):
        self.assertFalse(
            hasattr(
                MODULE,
                "ResourceStateAuthority",
            )
        )

    def test_no_hardware_capability_authority(self):
        self.assertFalse(
            hasattr(
                MODULE,
                "HardwareCapabilityAuthority",
            )
        )

    def test_no_task_evaluation(self):
        source = MODULE_PATH.read_text().lower()

        forbidden = (
            "taskevaluationauthority",
            "task_evaluation",
            "evaluate_task",
            "resource_fit",
            "task_feasible",
        )

        for item in forbidden:
            self.assertNotIn(
                item,
                source,
            )

    def test_no_agent_selection(self):
        source = MODULE_PATH.read_text().lower()

        forbidden = (
            "agentselectionauthority",
            "agent_selection",
            "select_agent",
            "agent_score",
        )

        for item in forbidden:
            self.assertNotIn(
                item,
                source,
            )

    def test_no_execution_authorization(self):
        import ast

        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }

        method_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }

        forbidden_classes = {
            "ExecutionAuthorization",
            "ExecutionAuthorizationAuthority",
        }

        forbidden_methods = {
            "authorize_execution",
            "authorize",
            "execution_authority",
        }

        self.assertTrue(
            forbidden_classes.isdisjoint(class_names)
        )

        self.assertTrue(
            forbidden_methods.isdisjoint(method_names)
        )

    def test_no_allocation(self):
        import ast

        tree = ast.parse(
            MODULE_PATH.read_text(),
            filename=str(MODULE_PATH),
        )

        class_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        }

        method_names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }

        forbidden_classes = {
            "ResourceAllocation",
            "ResourceAllocationAuthority",
        }

        forbidden_methods = {
            "allocate",
            "allocate_resources",
            "allocation",
        }

        self.assertTrue(
            forbidden_classes.isdisjoint(class_names)
        )

        self.assertTrue(
            forbidden_methods.isdisjoint(method_names)
        )

    def test_no_current_resource_state_fields(self):
        fields = MODULE.HardwareObservation.__dataclass_fields__

        forbidden = {
            "resource_state",
            "resource_capacity",
            "resource_fit",
            "execution_capacity",
            "task_feasible",
            "allocated_resources",
        }

        self.assertTrue(
            forbidden.isdisjoint(fields.keys())
        )


if __name__ == "__main__":
    unittest.main()
