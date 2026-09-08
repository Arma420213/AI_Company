"""
AI Company Core — Agent Contract Tests

Standard-library-only architectural contract tests for the canonical
Agent nucleus.
"""

from __future__ import annotations

import importlib.util
import unittest
from dataclasses import FrozenInstanceError
from datetime import datetime, timezone
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "02_core" / "agent.py"


def load_module():
    spec = importlib.util.spec_from_file_location(
        "ai_company_core_agent",
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


def make_agent(module):
    provenance = module.AgentProvenance(
        source="contract-test",
        timestamp=datetime.now(timezone.utc),
        authority="Agent Authority",
    )

    return module.Agent(
        agent_id="agent-1",
        name="Python Engineer",
        description="An organizational participant capable of Python work.",
        role="Software Engineer",
        agent_type="AI",
        capability_ids=(
            "python-development",
            "runtime-development",
        ),
        availability_state="AVAILABLE",
        requirements={
            "environment": "python",
        },
        execution_characteristics={
            "execution_mode": "local",
        },
        provenance=provenance,
    )


class AgentContractTests(unittest.TestCase):

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

        self.assertTrue(hasattr(module, "AgentProvenance"))
        self.assertTrue(hasattr(module, "Agent"))
        self.assertTrue(hasattr(module, "AgentAuthority"))

    def test_agent_construction(self):
        module = load_module()

        agent = make_agent(module)

        self.assertEqual(agent.agent_id, "agent-1")
        self.assertEqual(agent.name, "Python Engineer")
        self.assertEqual(agent.role, "Software Engineer")
        self.assertEqual(agent.agent_type, "AI")
        self.assertEqual(
            agent.capability_ids,
            (
                "python-development",
                "runtime-development",
            ),
        )
        self.assertEqual(
            agent.availability_state,
            "AVAILABLE",
        )

    def test_agent_is_immutable(self):
        module = load_module()

        agent = make_agent(module)

        with self.assertRaises(FrozenInstanceError):
            agent.name = "Changed"

    def test_agent_capability_ids_are_immutable(self):
        module = load_module()

        agent = make_agent(module)

        self.assertIsInstance(agent.capability_ids, tuple)

        with self.assertRaises(AttributeError):
            agent.capability_ids.append("new-capability")

    def test_agent_requirements_are_immutable(self):
        module = load_module()

        agent = make_agent(module)

        with self.assertRaises(TypeError):
            agent.requirements["environment"] = "changed"

    def test_agent_execution_characteristics_are_immutable(self):
        module = load_module()

        agent = make_agent(module)

        with self.assertRaises(TypeError):
            agent.execution_characteristics[
                "execution_mode"
            ] = "remote"

    def test_agent_authority_owns_identity(self):
        module = load_module()

        authority = module.AgentAuthority()
        agent = make_agent(module)

        stored = authority.set_agent(agent)

        self.assertEqual(stored, agent)
        self.assertEqual(
            authority.get_agent("agent-1"),
            agent,
        )

    def test_agent_authority_rejects_duplicate_identity(self):
        module = load_module()

        authority = module.AgentAuthority()
        agent = make_agent(module)

        authority.set_agent(agent)

        replacement = module.Agent(
            agent_id="agent-1",
            name="Different Agent",
            description="Another organizational participant.",
            role="Software Engineer",
            agent_type="AI",
            capability_ids=("python-development",),
            availability_state="AVAILABLE",
            requirements={
                "environment": "python",
            },
            execution_characteristics={
                "execution_mode": "local",
            },
            provenance=module.AgentProvenance(
                source="contract-test-replacement",
                timestamp=datetime.now(timezone.utc),
                authority="Agent Authority",
            ),
        )

        with self.assertRaises(ValueError):
            authority.set_agent(replacement)

        self.assertEqual(
            authority.get_agent("agent-1"),
            agent,
        )

    def test_agent_authority_can_update_existing_agent(self):
        module = load_module()

        authority = module.AgentAuthority()
        agent = make_agent(module)

        authority.set_agent(agent)

        updated = module.Agent(
            agent_id="agent-1",
            name="Senior Python Engineer",
            description="Updated organizational participant.",
            role="Senior Software Engineer",
            agent_type="AI",
            capability_ids=agent.capability_ids,
            availability_state=agent.availability_state,
            requirements=agent.requirements,
            execution_characteristics=agent.execution_characteristics,
            provenance=module.AgentProvenance(
                source="contract-test-update",
                timestamp=datetime.now(timezone.utc),
                authority="Agent Authority",
            ),
        )

        stored = authority.update_agent(updated)

        self.assertEqual(stored, updated)
        self.assertEqual(
            authority.get_agent("agent-1"),
            updated,
        )

    def test_agent_authority_can_update_availability(self):
        module = load_module()

        authority = module.AgentAuthority()
        agent = make_agent(module)

        authority.set_agent(agent)

        updated = authority.set_availability(
            "agent-1",
            "UNAVAILABLE",
        )

        self.assertEqual(
            updated.agent_id,
            agent.agent_id,
        )

        self.assertEqual(
            updated.name,
            agent.name,
        )

        self.assertEqual(
            updated.availability_state,
            "UNAVAILABLE",
        )

        self.assertEqual(
            authority.get_agent("agent-1"),
            updated,
        )

    def test_agent_authority_collection_is_read_only(self):
        module = load_module()

        authority = module.AgentAuthority()
        agents = authority.all_agents()

        with self.assertRaises(TypeError):
            agents["agent-1"] = make_agent(module)

    def test_unknown_agent_returns_key_error(self):
        module = load_module()

        authority = module.AgentAuthority()

        with self.assertRaises(KeyError):
            authority.get_agent("does-not-exist")

    def test_agent_rejects_empty_identity(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.Agent(
                agent_id="",
                name="Python Engineer",
                description="Participant.",
                role="Engineer",
                agent_type="AI",
                capability_ids=("python-development",),
                availability_state="AVAILABLE",
                requirements={},
                execution_characteristics={},
                provenance=module.AgentProvenance(
                    source="contract-test",
                    timestamp=datetime.now(timezone.utc),
                    authority="Agent Authority",
                ),
            )

    def test_agent_rejects_empty_availability(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.Agent(
                agent_id="agent-1",
                name="Python Engineer",
                description="Participant.",
                role="Engineer",
                agent_type="AI",
                capability_ids=("python-development",),
                availability_state="",
                requirements={},
                execution_characteristics={},
                provenance=module.AgentProvenance(
                    source="contract-test",
                    timestamp=datetime.now(timezone.utc),
                    authority="Agent Authority",
                ),
            )

    def test_agent_rejects_duplicate_capability_ids(self):
        module = load_module()

        with self.assertRaises(ValueError):
            module.Agent(
                agent_id="agent-1",
                name="Python Engineer",
                description="Participant.",
                role="Engineer",
                agent_type="AI",
                capability_ids=(
                    "python-development",
                    "python-development",
                ),
                availability_state="AVAILABLE",
                requirements={},
                execution_characteristics={},
                provenance=module.AgentProvenance(
                    source="contract-test",
                    timestamp=datetime.now(timezone.utc),
                    authority="Agent Authority",
                ),
            )

    def test_agent_does_not_import_runtime_or_integrations(self):
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

    def test_agent_does_not_own_execution_or_authorization(self):
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

    def test_agent_does_not_define_trust_or_experience_scores(self):
        source = MODULE_PATH.read_text(encoding="utf-8")

        forbidden_terms = (
            "trust_score",
            "experience_score",
            "selection_score",
            "evaluation_score",
        )

        for forbidden in forbidden_terms:
            self.assertNotIn(
                forbidden,
                source,
            )


if __name__ == "__main__":
    unittest.main()
