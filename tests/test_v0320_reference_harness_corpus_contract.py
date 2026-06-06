import pytest

from chanta_core.external_harness import (
    ExternalHarnessProfileKind,
    ReferenceCorpusNoExecutionGuarantee,
    ReferenceCorpusSnapshot,
    ReferenceFileInventory,
    ReferenceFileInventoryEntry,
    ReferenceFileInventoryPolicy,
    ReferenceHarnessCorpus,
    ReferenceHarnessCorpusPolicy,
    ReferenceHarnessSource,
    ReferenceHarnessSourceKind,
    V0320ReadinessReport,
    build_reference_corpus_no_execution_guarantee,
    build_reference_corpus_policy,
    build_reference_corpus_snapshot,
    build_reference_file_inventory,
    build_reference_file_inventory_entry,
    build_reference_file_inventory_policy,
    build_reference_harness_corpus,
    build_reference_harness_source,
    build_v0320_readiness_report,
    reference_corpus_policy_preserves_read_only,
    reference_inventory_preserves_no_execution,
    reference_snapshot_is_not_runtime,
    v0320_readiness_report_is_not_runtime_ready,
)


def test_reference_source_kind_taxonomy() -> None:
    assert {item.value for item in ReferenceHarnessSourceKind} >= {
        "local_reference_directory",
        "local_reference_file",
        "local_reference_manifest",
        "local_reference_documentation",
        "local_reference_config",
        "sanitized_manifest",
        "manual_reference",
        "unknown",
    }


def test_reference_corpus_policy_is_read_only_and_non_executable() -> None:
    policy = build_reference_corpus_policy()

    assert isinstance(policy, ReferenceHarnessCorpusPolicy)
    assert reference_corpus_policy_preserves_read_only(policy)
    assert policy.read_only is True
    assert policy.prohibit_execution is True
    assert policy.prohibit_install is True
    assert policy.prohibit_import_runtime is True
    assert policy.prohibit_network is True
    assert policy.prohibit_credentials is True
    assert policy.prohibit_command_execution is True
    assert policy.prohibit_provider_invocation is True
    assert policy.prohibit_browser_automation is True
    assert policy.prohibit_rpa_control is True
    assert policy.prohibit_gateway_control is True
    assert policy.prohibit_packet_send is True
    assert policy.prohibit_secret_file_read is True

    with pytest.raises(ValueError):
        ReferenceHarnessCorpusPolicy(policy_id="bad-policy", read_only=False)
    with pytest.raises(ValueError):
        ReferenceHarnessCorpusPolicy(policy_id="bad-policy", prohibit_execution=False)
    with pytest.raises(ValueError):
        ReferenceHarnessCorpusPolicy(policy_id="bad-policy", prohibit_credentials=False)
    with pytest.raises(ValueError):
        ReferenceHarnessCorpusPolicy(policy_id="bad-policy", prohibit_secret_file_read=False)


def test_reference_source_and_corpus_are_path_refs_only() -> None:
    source = build_reference_harness_source(
        source_id="source:opencode",
        source_kind=ReferenceHarnessSourceKind.LOCAL_REFERENCE_DIRECTORY,
        harness_kind=ExternalHarnessProfileKind.OPENCODE_STYLE,
        local_path_ref="references/opencode",
        display_name="OpenCode-style local reference",
        description="Path reference only for static observation.",
    )
    corpus = build_reference_harness_corpus(
        corpus_id="corpus:references",
        sources=[source],
        root_path_ref="references",
    )

    assert isinstance(source, ReferenceHarnessSource)
    assert source.local_path_ref == "references/opencode"
    assert source.executable_source is False
    assert isinstance(corpus, ReferenceHarnessCorpus)
    assert corpus.ready_for_static_observation is True
    assert corpus.ready_for_execution is False
    assert corpus.runtime_corpus is False

    with pytest.raises(ValueError):
        ReferenceHarnessSource(
            source_id="source:bad",
            source_kind=ReferenceHarnessSourceKind.LOCAL_REFERENCE_DIRECTORY,
            harness_kind=ExternalHarnessProfileKind.UNKNOWN,
            local_path_ref="references/bad",
            display_name="Bad",
            description="Bad metadata.",
            metadata={"executable_source": True},
        )


def test_reference_file_inventory_policy_and_entries_are_non_executable() -> None:
    policy = build_reference_file_inventory_policy()
    entry = build_reference_file_inventory_entry(
        entry_id="entry:package-json",
        source_id="source:opencode",
        relative_path="package.json",
        file_name="package.json",
        file_extension=".json",
        file_size_bytes=128,
        detected_kind="manifest_candidate",
    )
    skipped = build_reference_file_inventory_entry(
        entry_id="entry:env",
        source_id="source:opencode",
        relative_path=".env",
        file_name=".env",
        skipped_reason="secret-like file pattern is prohibited",
    )

    assert isinstance(policy, ReferenceFileInventoryPolicy)
    assert policy.read_only_policy is True
    assert policy.prohibit_secret_file_read is True
    assert policy.prohibit_execution is True
    assert isinstance(entry, ReferenceFileInventoryEntry)
    assert entry.file_execution is False
    assert skipped.skipped_reason is not None
    assert skipped.text_preview is None

    with pytest.raises(ValueError):
        ReferenceFileInventoryPolicy(
            inventory_policy_id="bad-inventory-policy",
            prohibit_secret_file_read=False,
        )
    with pytest.raises(ValueError):
        ReferenceFileInventoryPolicy(
            inventory_policy_id="bad-inventory-policy",
            prohibit_execution=False,
        )
    with pytest.raises(ValueError):
        build_reference_file_inventory_entry(
            entry_id="entry:bad",
            source_id="source:opencode",
            relative_path=".env",
            file_name=".env",
            text_preview="SECRET=not-allowed",
            skipped_reason="secret-like file pattern is prohibited",
        )
    with pytest.raises(ValueError):
        build_reference_file_inventory_entry(
            entry_id="entry:bad-size",
            source_id="source:opencode",
            relative_path="bad.txt",
            file_name="bad.txt",
            file_size_bytes=-1,
        )


def test_reference_file_inventory_is_manifest_candidate_contract_only() -> None:
    inventory = build_reference_file_inventory(
        inventory_id="inventory:source",
        source_id="source:opencode",
        inventory_policy_id="policy:inventory",
        manifest_candidate_paths=["package.json"],
        documentation_candidate_paths=["README.md"],
        config_candidate_paths=["config.json"],
        risk_surface_candidate_paths=["plugins/example"],
    )

    assert isinstance(inventory, ReferenceFileInventory)
    assert inventory.ready_for_manifest_extraction is True
    assert inventory.ready_for_execution is False
    assert reference_inventory_preserves_no_execution(inventory)

    with pytest.raises(ValueError):
        ReferenceFileInventory(
            inventory_id="inventory:bad",
            source_id="source",
            inventory_policy_id="policy",
            entries=[],
            summary="Bad runtime inventory.",
            ready_for_execution=True,
        )


def test_reference_snapshot_and_no_execution_guarantee_are_contract_only() -> None:
    snapshot = build_reference_corpus_snapshot(
        snapshot_id="snapshot:references",
        corpus_id="corpus:references",
        source_ids=["source:opencode"],
        inventory_ids=["inventory:source"],
        profile_seed_ids=["profile:opencode"],
    )
    guarantee = build_reference_corpus_no_execution_guarantee()

    assert isinstance(snapshot, ReferenceCorpusSnapshot)
    assert snapshot.version == "v0.32.0"
    assert snapshot.ready_for_execution is False
    assert reference_snapshot_is_not_runtime(snapshot)
    assert isinstance(guarantee, ReferenceCorpusNoExecutionGuarantee)
    assert guarantee.no_reference_code_execution is True
    assert guarantee.no_import_runtime is True
    assert guarantee.no_install is True
    assert guarantee.no_dependency_resolution is True
    assert guarantee.no_network_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_secret_file_read is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_browser_automation is True
    assert guarantee.no_rpa_control is True
    assert guarantee.no_gateway_control is True
    assert guarantee.no_packet_send is True
    assert guarantee.no_workspace_write is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True

    with pytest.raises(ValueError):
        ReferenceCorpusNoExecutionGuarantee(
            guarantee_id="bad-guarantee",
            version="v0.32.0",
            no_reference_code_execution=False,
        )


def test_v0320_readiness_report_never_implies_runtime_readiness() -> None:
    report = build_v0320_readiness_report(
        profile_set_id="profile-set:v0.32.0",
        reference_corpus_snapshot_id="snapshot:references",
    )

    assert isinstance(report, V0320ReadinessReport)
    assert report.ready_for_execution is False
    assert report.ready_for_external_harness_execution is False
    assert report.ready_for_reference_code_execution is False
    assert report.ready_for_live_scan is False
    assert v0320_readiness_report_is_not_runtime_ready(report)
    assert {
        "harness execution",
        "reference code execution",
        "source_ref fetch",
        "live scan",
        "install",
        "import runtime",
        "dependency resolution",
        "network",
        "credential",
        "secret file read",
        "command",
        "provider invocation",
        "browser",
        "rpa",
        "gateway",
        "packet send",
        "registry mutation",
        "memory mutation",
        "OCEL emission",
        "UI runtime",
    }.issubset(set(report.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        V0320ReadinessReport(
            report_id="bad-report",
            version="v0.32.0",
            profile_set_id=None,
            reference_corpus_snapshot_id=None,
            summary="Bad report.",
            ready_for_execution=True,
        )
