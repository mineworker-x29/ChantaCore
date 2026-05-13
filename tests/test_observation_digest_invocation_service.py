import json

from chanta_core.observation_digest import OBSERVATION_DIGESTION_SKILL_IDS
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService


def _write_jsonl(path):
    path.write_bytes(
        "\n".join(
            [
                json.dumps({"role": "user", "content": "inspect this trace"}),
                json.dumps({"role": "assistant", "content": "I will inspect it"}),
                json.dumps({"tool_call": {"name": "read_file"}, "input": {"path": "trace.jsonl"}}),
                json.dumps({"tool_result": {"name": "read_file"}, "output": {"ok": True}}),
            ]
        ).encode("utf-8"),
    )


def _write_skill_dir(root):
    skill_dir = root / "external_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        "# Generic External Skill\n\nDescription: reads public fixture metadata.\n".encode("utf-8"),
    )
    return skill_dir


def test_runtime_bindings_exist_for_all_observation_digestion_skills():
    service = ObservationDigestSkillInvocationService()

    bindings = service.create_runtime_bindings()

    assert len(bindings) == 10
    assert {binding.skill_id for binding in bindings} == set(OBSERVATION_DIGESTION_SKILL_IDS)
    assert all(binding.gate_required and binding.envelope_required and binding.read_only for binding in bindings)


def test_default_policy_allows_only_observation_digestion_skills():
    service = ObservationDigestSkillInvocationService()

    policy = service.create_default_policy()

    assert policy.allowed_skill_ids == sorted(OBSERVATION_DIGESTION_SKILL_IDS)
    assert policy.allow_external_harness_execution is False
    assert policy.allow_script_execution is False
    assert policy.allow_shell is False
    assert policy.allow_network is False
    assert policy.allow_mcp is False
    assert policy.allow_plugin is False
    assert policy.allow_write is False


def test_agent_trace_observe_invokes_internal_observation_service(tmp_path):
    _write_jsonl(tmp_path / "trace.jsonl")
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(
        skill_id="skill:agent_trace_observe",
        input_payload={
            "root_path": str(tmp_path),
            "relative_path": "trace.jsonl",
            "source_runtime": "generic",
            "format_hint": "generic_jsonl",
        },
    )

    assert result.executed is True
    assert result.blocked is False
    assert result.envelope_id
    assert result.output_ref.startswith("observed_agent_run:")


def test_behavior_infer_and_process_narrative_use_read_only_models():
    observed_run = {
        "observed_run_id": "observed_agent_run:test",
        "source_id": "agent_observation_source:test",
        "batch_id": "agent_observation_batch:test",
        "inferred_runtime": "generic",
        "event_count": 2,
        "object_count": 1,
        "relation_count": 2,
        "observation_confidence": 0.7,
        "run_attrs": {"observed_activity_sequence": ["user_message_observed", "assistant_message_observed"]},
    }
    service = ObservationDigestSkillInvocationService()

    inference_result = service.invoke_skill(
        skill_id="skill:agent_behavior_infer",
        input_payload={"observed_run": observed_run},
    )

    assert inference_result.executed is True
    assert inference_result.envelope_id
    assert service.observation_service.last_inference is not None
    assert service.observation_service.last_inference.observed_run_id == "observed_agent_run:test"


def test_process_narrative_creates_narrative_from_inference_payload():
    observed_run = {"observed_run_id": "observed_agent_run:test", "event_count": 2}
    inference = {
        "inference_id": "agent_behavior_inference:test",
        "observed_run_id": "observed_agent_run:test",
        "inferred_task_type": "message_exchange",
        "inferred_action_sequence": ["user_message_observed", "assistant_message_observed"],
        "outcome_inference": "observed_without_explicit_failure",
        "inferred_goal_confidence": 0.6,
        "outcome_confidence": 0.7,
    }
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(
        skill_id="skill:agent_process_narrative",
        input_payload={"observed_run": observed_run, "inference": inference},
    )

    assert result.executed is True
    assert result.output_ref.startswith("agent_process_narrative:")


def test_external_static_digest_and_assimilation_defaults_are_safe(tmp_path):
    _write_skill_dir(tmp_path)
    service = ObservationDigestSkillInvocationService()

    profile_result = service.invoke_skill(
        skill_id="skill:external_skill_static_digest",
        input_payload={"root_path": str(tmp_path), "relative_path": "external_skill", "vendor_hint": "fixture"},
    )
    candidate_result = service.invoke_skill(
        skill_id="skill:external_skill_assimilate",
        input_payload={
            "static_profile": service.digestion_service.last_static_profile.to_dict()
        },
    )

    assert profile_result.executed is True
    assert candidate_result.executed is True
    assert candidate_result.output_preview["candidate"]["dict_keys"]
    candidate = service.digestion_service.last_candidate
    assert candidate.review_status == "pending_review"
    assert candidate.canonical_import_enabled is False
    assert candidate.execution_enabled is False


def test_external_adapter_candidate_defaults_are_safe():
    service = ObservationDigestSkillInvocationService()
    candidate = {
        "candidate_id": "external_skill_assimilation_candidate:test",
        "source_runtime": "generic",
        "source_skill_ref": "generic_skill",
        "source_kind": "external_skill",
        "proposed_chantacore_skill_id": "skill:generic_skill",
        "proposed_execution_type": "review_only_candidate",
        "adapter_candidate_ids": [],
        "risk_class": "unknown",
        "confidence": 0.5,
        "evidence_refs": [],
        "review_status": "pending_review",
        "canonical_import_enabled": False,
        "execution_enabled": False,
    }

    result = service.invoke_skill(
        skill_id="skill:external_skill_adapter_candidate",
        input_payload={"candidate": candidate},
    )

    assert result.executed is True
    adapter = service.digestion_service.last_adapter_candidate
    assert adapter.requires_review is True
    assert adapter.execution_enabled is False


def test_observation_digest_invocation_pig_counts_are_visible():
    view = OCPXProcessView(
        view_id="view:demo",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="binding:one",
                object_type="observation_digest_skill_runtime_binding",
                object_attrs={"skill_family": "observation"},
            ),
            OCPXObjectView(
                object_id="result:one",
                object_type="observation_digest_invocation_result",
                object_attrs={
                    "skill_id": "skill:agent_trace_observe",
                    "status": "completed",
                    "blocked": False,
                    "envelope_id": "execution_envelope:test",
                },
            ),
            OCPXObjectView(
                object_id="finding:one",
                object_type="observation_digest_invocation_finding",
                object_attrs={"finding_type": "missing_required_input"},
            ),
        ],
    )

    summary = PIGReportService._observation_digest_invocation_summary(
        {
            "observation_digest_skill_runtime_binding": 1,
            "observation_digest_invocation_policy": 1,
            "observation_digest_invocation_result": 1,
            "observation_digest_invocation_finding": 1,
        },
        {},
        view,
    )

    assert summary["observation_digest_runtime_binding_count"] == 1
    assert summary["observation_digest_invocation_completed_count"] == 1
    assert summary["observation_digest_invocation_envelope_count"] == 1
    assert summary["observation_digest_invocation_by_skill_id"] == {"skill:agent_trace_observe": 1}
    assert summary["observation_digest_invocation_finding_by_type"] == {"missing_required_input": 1}
