from agent_bill_shock_guard.main import estimate_spend, main


def test_estimate_spend_returns_positive_tokens() -> None:
    estimate = estimate_spend(["claude", "fix", "tests"])
    assert estimate.tokens > 0
    assert estimate.dollars > 0


def test_dry_run_smoke(capsys) -> None:
    code = main(["--dry-run", "--", "codex", "explain", "this", "repo"])
    out = capsys.readouterr().out
    assert code == 0
    assert "estimated_tokens=" in out


def test_budget_blocks_large_command() -> None:
    code = main(["--budget", "0.0", "--dry-run", "--", "claude", "x" * 1000])
    assert code == 3
