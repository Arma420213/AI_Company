from __future__ import annotations

import re
import unittest
from datetime import datetime, timezone
from importlib import import_module
from pathlib import Path
from types import MappingProxyType


_task_evaluation = import_module("02_core.task_evaluation")

EvaluationCondition = _task_evaluation.EvaluationCondition
EvaluationConclusion = _task_evaluation.EvaluationConclusion
EvaluationContext = _task_evaluation.EvaluationContext
EvaluationEvidence = _task_evaluation.EvaluationEvidence
EvaluationReference = _task_evaluation.EvaluationReference
EvaluationRules = _task_evaluation.EvaluationRules
EvidenceState = _task_evaluation.EvidenceState
TaskEvaluation = _task_evaluation.TaskEvaluation
TaskEvaluationAuthority = _task_evaluation.TaskEvaluationAuthority
TaskEvaluationProvenance = _task_evaluation.TaskEvaluationProvenance


def make_reference(
    concept: str = "Task",
    identity: str = "task-001",
    reference_kind: str = "canonical",
) -> EvaluationReference:
    return EvaluationReference(
        concept=concept,
        identity=identity,
        reference_kind=reference_kind,
    )


def make_context() -> EvaluationContext:
    return EvaluationContext(
        strategic_context=(
            make_reference("Strategic Decision", "decision-001"),
        ),
        capability_context=(
            make_reference("Capability", "python"),
        ),
        agent_context=(
            make_reference("Agent", "agent-001"),
        ),
        resource_state_context=(
            make_reference("Resource State", "resource-state-001"),
        ),
        experience_context=(
            make_reference("Experience", "experience-001"),
        ),
        trust_context=(
            make_reference("Trust", "trust-001"),
        ),
        risk_context={
            "level": "known",
        },
        cost_context={
            "class": "bounded",
        },
        environmental_context={
            "availability": "observed",
        },
    )


def make_rules() -> EvaluationRules:
    return EvaluationRules(
        rules_id="task-evaluation-rules",
        version="1.0",
        description="Canonical Task Evaluation semantic rules.",
    )


def make_provenance(
    evaluation_id: str = "evaluation-001",
) -> TaskEvaluationProvenance:
    return TaskEvaluationProvenance(
        source="canonical-core",
        timestamp=datetime.now(timezone.utc),
        authority=TaskEvaluationAuthority.AUTHORITY_NAME,
        derivation_method="evidence-grounded evaluation",
        rules_id="task-evaluation-rules",
        context_references=(
            make_reference(
                "Task Evaluation Context",
                evaluation_id,
            ),
        ),
    )


def make_evaluation(
    conclusion: EvaluationConclusion = EvaluationConclusion.SUITABLE,
    evaluation_id: str = "evaluation-001",
    reason: str | None = None,
    conditions: tuple[EvaluationCondition, ...] = (),
) -> TaskEvaluation:
    return TaskEvaluation(
        evaluation_id=evaluation_id,
        task_id="task-001",
        conclusion=conclusion,
        context=make_context(),
        evidence=(
            EvaluationEvidence(
                dimension="capability",
                state=EvidenceState.KNOWN,
                reference=make_reference(
                    "Capability",
                    "python",
                ),
                detail="Required capability is known.",
            ),
        ),
        rules=make_rules(),
        provenance=make_provenance(evaluation_id),
        reason=reason,
        conditions=conditions,
    )


class TaskEvaluationContractTests(unittest.TestCase):

    # -----------------------------------------------------------------------
    # TE-01 — Canonical Authority
    # -----------------------------------------------------------------------

    def test_te01_single_canonical_authority(self) -> None:
        self.assertEqual(
            TaskEvaluationAuthority.AUTHORITY_NAME,
            "Task Evaluation Authority",
        )

    # -----------------------------------------------------------------------
    # TE-02 — Canonical Evaluation Identity
    # -----------------------------------------------------------------------

    def test_te02_evaluation_requires_canonical_identity(self) -> None:
        with self.assertRaises(ValueError):
            make_evaluation(evaluation_id="")

    # -----------------------------------------------------------------------
    # TE-03 — Canonical Task Identity
    # -----------------------------------------------------------------------

    def test_te03_evaluation_requires_task_identity(self) -> None:
        with self.assertRaises(ValueError):
            TaskEvaluation(
                evaluation_id="evaluation-001",
                task_id="",
                conclusion=EvaluationConclusion.SUITABLE,
                context=make_context(),
                evidence=(),
                rules=make_rules(),
                provenance=make_provenance(),
            )

    # -----------------------------------------------------------------------
    # TE-04 — Immutable Evaluation Snapshot
    # -----------------------------------------------------------------------

    def test_te04_evaluation_is_immutable(self) -> None:
        evaluation = make_evaluation()

        with self.assertRaises(AttributeError):
            evaluation.conclusion = EvaluationConclusion.UNSUITABLE  # type: ignore[misc]

    # -----------------------------------------------------------------------
    # TE-05 — Four Canonical Conclusions
    # -----------------------------------------------------------------------

    def test_te05_four_canonical_conclusions(self) -> None:
        self.assertEqual(
            {
                EvaluationConclusion.SUITABLE,
                EvaluationConclusion.UNSUITABLE,
                EvaluationConclusion.CONDITIONALLY_SUITABLE,
                EvaluationConclusion.INDETERMINATE,
            },
            set(EvaluationConclusion),
        )

    # -----------------------------------------------------------------------
    # TE-06 — Conditional Suitability Requires Conditions
    # -----------------------------------------------------------------------

    def test_te06_conditional_suitability_requires_conditions(self) -> None:
        with self.assertRaises(ValueError):
            make_evaluation(
                conclusion=EvaluationConclusion.CONDITIONALLY_SUITABLE,
            )

    def test_te06_conditional_suitability_accepts_explicit_conditions(
        self,
    ) -> None:
        condition = EvaluationCondition(
            condition_id="condition-001",
            description="Required resource evidence must remain available.",
        )

        evaluation = make_evaluation(
            conclusion=EvaluationConclusion.CONDITIONALLY_SUITABLE,
            conditions=(condition,),
        )

        self.assertEqual(evaluation.conditions, (condition,))

    # -----------------------------------------------------------------------
    # TE-07 — Indeterminate Requires Explainable Reason
    # -----------------------------------------------------------------------

    def test_te07_indeterminate_requires_reason(self) -> None:
        with self.assertRaises(ValueError):
            make_evaluation(
                conclusion=EvaluationConclusion.INDETERMINATE,
            )

    def test_te07_indeterminate_preserves_reason(self) -> None:
        evaluation = make_evaluation(
            conclusion=EvaluationConclusion.INDETERMINATE,
            reason="Required evidence is incomplete.",
        )

        self.assertEqual(
            evaluation.reason,
            "Required evidence is incomplete.",
        )

    # -----------------------------------------------------------------------
    # TE-08 — Evidence State Is Separate From Conclusion
    # -----------------------------------------------------------------------

    def test_te08_evidence_state_is_separate_from_conclusion(self) -> None:
        evidence = EvaluationEvidence(
            dimension="resource availability",
            state=EvidenceState.UNAVAILABLE,
            reference=make_reference(
                "Resource State",
                "resource-state-001",
            ),
        )

        evaluation = TaskEvaluation(
            evaluation_id="evaluation-001",
            task_id="task-001",
            conclusion=EvaluationConclusion.INDETERMINATE,
            context=make_context(),
            evidence=(evidence,),
            rules=make_rules(),
            provenance=make_provenance(),
            reason="Resource evidence is unavailable.",
        )

        self.assertEqual(
            evidence.state,
            EvidenceState.UNAVAILABLE,
        )
        self.assertEqual(
            evaluation.conclusion,
            EvaluationConclusion.INDETERMINATE,
        )

    # -----------------------------------------------------------------------
    # TE-09 — Unknown Evidence Must Not Become Unsuitable
    # -----------------------------------------------------------------------

    def _assert_te09_unknown_evidence_is_not_implicitly_unsuitable(
        self,
        state: EvidenceState,
    ) -> None:
        evidence = EvaluationEvidence(
            dimension="resource availability",
            state=state,
        )

        evaluation = TaskEvaluation(
            evaluation_id="evaluation-001",
            task_id="task-001",
            conclusion=EvaluationConclusion.INDETERMINATE,
            context=make_context(),
            evidence=(evidence,),
            rules=make_rules(),
            provenance=make_provenance(),
            reason="Evidence is insufficient for a suitability conclusion.",
        )

        self.assertNotEqual(
            evaluation.conclusion,
            EvaluationConclusion.UNSUITABLE,
        )

    def test_te09_unavailable_evidence_is_not_implicitly_unsuitable(
        self,
    ) -> None:
        self._assert_te09_unknown_evidence_is_not_implicitly_unsuitable(
            EvidenceState.UNAVAILABLE,
        )

    def test_te09_unobserved_evidence_is_not_implicitly_unsuitable(
        self,
    ) -> None:
        self._assert_te09_unknown_evidence_is_not_implicitly_unsuitable(
            EvidenceState.UNOBSERVED,
        )

    def test_te09_incomplete_evidence_is_not_implicitly_unsuitable(
        self,
    ) -> None:
        self._assert_te09_unknown_evidence_is_not_implicitly_unsuitable(
            EvidenceState.INCOMPLETE,
        )

    def test_te09_inconsistent_evidence_is_not_implicitly_unsuitable(
        self,
    ) -> None:
        self._assert_te09_unknown_evidence_is_not_implicitly_unsuitable(
            EvidenceState.INCONSISTENT,
        )

    # -----------------------------------------------------------------------
    # TE-10 — Explicit Evaluation Context
    # -----------------------------------------------------------------------

    def test_te10_context_preserves_canonical_references(self) -> None:
        context = make_context()

        self.assertEqual(
            context.strategic_context[0].concept,
            "Strategic Decision",
        )
        self.assertEqual(
            context.capability_context[0].concept,
            "Capability",
        )
        self.assertEqual(
            context.agent_context[0].concept,
            "Agent",
        )
        self.assertEqual(
            context.resource_state_context[0].concept,
            "Resource State",
        )
        self.assertEqual(
            context.experience_context[0].concept,
            "Experience",
        )
        self.assertEqual(
            context.trust_context[0].concept,
            "Trust",
        )

    # -----------------------------------------------------------------------
    # TE-11 — Explicit Evidence References
    # -----------------------------------------------------------------------

    def test_te11_evidence_preserves_reference(self) -> None:
        reference = make_reference(
            "Capability",
            "python",
        )

        evidence = EvaluationEvidence(
            dimension="capability",
            state=EvidenceState.KNOWN,
            reference=reference,
        )

        self.assertEqual(evidence.reference, reference)

    # -----------------------------------------------------------------------
    # TE-12 — Provenance
    # -----------------------------------------------------------------------

    def test_te12_provenance_is_explicit(self) -> None:
        provenance = make_provenance()

        self.assertEqual(provenance.source, "canonical-core")
        self.assertEqual(
            provenance.authority,
            TaskEvaluationAuthority.AUTHORITY_NAME,
        )
        self.assertEqual(
            provenance.rules_id,
            "task-evaluation-rules",
        )
        self.assertIsNotNone(provenance.timestamp.tzinfo)

    # -----------------------------------------------------------------------
    # TE-13 — Temporal Integrity
    # -----------------------------------------------------------------------

    def test_te13_naive_timestamp_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            TaskEvaluationProvenance(
                source="canonical-core",
                timestamp=datetime.now(),
                authority=TaskEvaluationAuthority.AUTHORITY_NAME,
                derivation_method="evidence-grounded evaluation",
                rules_id="task-evaluation-rules",
            )

    # -----------------------------------------------------------------------
    # TE-14 — Task Is Referenced, Not Owned
    # -----------------------------------------------------------------------

    def test_te14_task_is_represented_by_identity_reference(self) -> None:
        evaluation = make_evaluation()

        self.assertEqual(evaluation.task_id, "task-001")
        self.assertFalse(hasattr(evaluation, "task"))

    # -----------------------------------------------------------------------
    # TE-15 — Resource State Is Context, Not Ownership
    # -----------------------------------------------------------------------

    def test_te15_resource_state_is_context_reference(self) -> None:
        evaluation = make_evaluation()

        self.assertEqual(
            evaluation.context.resource_state_context[0].concept,
            "Resource State",
        )
        self.assertFalse(hasattr(evaluation, "resource_state"))

    # -----------------------------------------------------------------------
    # TE-16 — No Agent Selection Leakage
    # -----------------------------------------------------------------------

    def test_te16_no_agent_selection_api(self) -> None:
        evaluation = make_evaluation()

        self.assertFalse(hasattr(evaluation, "select_agent"))
        self.assertFalse(hasattr(evaluation, "rank_agents"))
        self.assertFalse(hasattr(evaluation, "assign_agent"))

    # -----------------------------------------------------------------------
    # TE-17 — No Trust / Experience Mutation
    # -----------------------------------------------------------------------

    def test_te17_trust_and_experience_are_references_only(self) -> None:
        evaluation = make_evaluation()

        self.assertEqual(
            evaluation.context.experience_context[0].concept,
            "Experience",
        )
        self.assertEqual(
            evaluation.context.trust_context[0].concept,
            "Trust",
        )

        self.assertFalse(hasattr(evaluation, "update_trust"))
        self.assertFalse(hasattr(evaluation, "mutate_trust"))
        self.assertFalse(hasattr(evaluation, "update_experience"))
        self.assertFalse(hasattr(evaluation, "mutate_experience"))

    # -----------------------------------------------------------------------
    # TE-18 — No Numeric Score Requirement
    # -----------------------------------------------------------------------

    def test_te18_numeric_score_is_not_canonical_contract(self) -> None:
        evaluation = make_evaluation()

        field_names = set(evaluation.__dataclass_fields__)

        self.assertNotIn("score", field_names)
        self.assertNotIn("confidence_score", field_names)
        self.assertNotIn("ranking_score", field_names)

    # -----------------------------------------------------------------------
    # TE-19 — No Readiness / Authorization / Execution Leakage
    # -----------------------------------------------------------------------

    def test_te19_no_execution_responsibilities(self) -> None:
        evaluation = make_evaluation()

        forbidden_methods = (
            "determine_readiness",
            "check_readiness",
            "authorize",
            "authorize_execution",
            "execute",
            "execute_task",
        )

        for method_name in forbidden_methods:
            self.assertFalse(hasattr(evaluation, method_name))

    # -----------------------------------------------------------------------
    # TE-20 — Authority Owns Evaluation State Only
    # -----------------------------------------------------------------------

    def test_te20_authority_records_immutable_evaluations(self) -> None:
        authority = TaskEvaluationAuthority()

        evaluation = make_evaluation()

        recorded = authority.record_evaluation(evaluation)

        self.assertIs(recorded, evaluation)
        self.assertIs(
            authority.get_evaluation("evaluation-001"),
            evaluation,
        )
        self.assertIs(
            authority.evaluations["evaluation-001"],
            evaluation,
        )

        with self.assertRaises(ValueError):
            authority.record_evaluation(evaluation)

    def test_te20_authority_mapping_is_read_only(self) -> None:
        authority = TaskEvaluationAuthority()
        evaluation = make_evaluation()

        authority.record_evaluation(evaluation)

        with self.assertRaises(TypeError):
            authority.evaluations["evaluation-002"] = evaluation  # type: ignore[index]

    # -----------------------------------------------------------------------
    # TE-21 — Initial Evaluation Collection Preserves Identity
    # -----------------------------------------------------------------------

    def test_te21_initial_evaluations_require_matching_identity(self) -> None:
        evaluation = make_evaluation()

        authority = TaskEvaluationAuthority(
            initial_evaluations={
                "evaluation-001": evaluation,
            }
        )

        self.assertIs(
            authority.get_evaluation("evaluation-001"),
            evaluation,
        )

    def test_te21_initial_evaluations_reject_identity_mismatch(self) -> None:
        evaluation = make_evaluation()

        with self.assertRaises(ValueError):
            TaskEvaluationAuthority(
                initial_evaluations={
                    "different-id": evaluation,
                }
            )

    # -----------------------------------------------------------------------
    # TE-22 — Context Mapping Is Immutable
    # -----------------------------------------------------------------------

    def test_te22_context_mappings_are_immutable(self) -> None:
        context = make_context()

        self.assertIsInstance(
            context.risk_context,
            MappingProxyType,
        )

        with self.assertRaises(TypeError):
            context.risk_context["new"] = "value"  # type: ignore[index]

    # -----------------------------------------------------------------------
    # TE-23 — Conditions Are Immutable
    # -----------------------------------------------------------------------

    def test_te23_conditions_are_immutable(self) -> None:
        condition = EvaluationCondition(
            condition_id="condition-001",
            description="Required evidence remains available.",
        )

        evaluation = make_evaluation(
            conclusion=EvaluationConclusion.CONDITIONALLY_SUITABLE,
            conditions=(condition,),
        )

        with self.assertRaises(AttributeError):
            evaluation.conditions = ()  # type: ignore[misc]

    # -----------------------------------------------------------------------
    # TE-24 — No Runtime / Integration Import Contract
    # -----------------------------------------------------------------------

    def test_te24_module_declares_no_runtime_or_integration_imports(
        self,
    ) -> None:
        source = Path("02_core/task_evaluation.py").read_text()

        forbidden_imports = (
            "from 03_runtime",
            "import 03_runtime",
            "from 04_integrations",
            "import 04_integrations",
            "import weft",
            "from weft",
        )

        for forbidden in forbidden_imports:
            self.assertNotIn(forbidden, source)

    # -----------------------------------------------------------------------
    # TE-25 — No External Dependency Contract
    # -----------------------------------------------------------------------

    def test_te25_module_uses_standard_library_only(self) -> None:
        source = Path("02_core/task_evaluation.py").read_text()

        imports = re.findall(
            r"^(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)",
            source,
            flags=re.MULTILINE,
        )

        standard_library_modules = {
            "__future__",
            "dataclasses",
            "datetime",
            "enum",
            "types",
            "typing",
        }

        self.assertTrue(
            set(imports).issubset(standard_library_modules),
            msg=f"Non-standard imports detected: "
                f"{set(imports) - standard_library_modules}",
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
