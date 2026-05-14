from chanta_core.cli.main import main


def test_cli_observe_digest_ecosystem_snapshot_safety_gaps_manifest(capsys) -> None:
    assert main(["observe-digest", "ecosystem", "snapshot"]) == 0
    snapshot_out = capsys.readouterr().out
    assert "Observation/Digestion Ecosystem" in snapshot_out
    assert "observation_skill_count=" in snapshot_out
    assert "executable_external_candidate_count=0" in snapshot_out

    assert main(["observe-digest", "ecosystem", "safety"]) == 0
    safety_out = capsys.readouterr().out
    assert "shell_allowed=false" in safety_out
    assert "network_allowed=false" in safety_out
    assert "write_allowed=false" in safety_out

    assert main(["observe-digest", "ecosystem", "gaps", "--limit", "5"]) == 0
    gaps_out = capsys.readouterr().out
    assert "Observation/Digestion Gap Register" in gaps_out
    assert "full external adapters" in gaps_out

    assert main(["observe-digest", "ecosystem", "manifest"]) == 0
    manifest_out = capsys.readouterr().out
    assert "v0.19.0" in manifest_out
    assert "v0.19.9" in manifest_out

