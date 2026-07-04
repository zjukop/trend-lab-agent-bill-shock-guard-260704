from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass

TOKEN_PRICE_PER_1K = 0.003
BLOAT_HINTS = (".lock", ".log", "node_modules", "dist/", "build/", ".venv")


@dataclass(frozen=True)
class SpendEstimate:
    tokens: int
    dollars: float
    warnings: list[str]


def estimate_spend(command: list[str]) -> SpendEstimate:
    text = " ".join(command)
    tokens = max(1, len(text) // 4)
    dollars = tokens / 1000 * TOKEN_PRICE_PER_1K
    warnings: list[str] = []

    repeated = [part for part in set(command) if command.count(part) >= 3]
    if repeated:
        warnings.append("possible runaway loop: repeated command fragments detected")

    if any(hint in text for hint in BLOAT_HINTS):
        warnings.append("context bloat: avoid sending logs, lockfiles, builds, or dependencies")

    return SpendEstimate(tokens=tokens, dollars=dollars, warnings=warnings)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guard coding-agent sessions from surprise bills.")
    parser.add_argument("--budget", type=float, default=None, help="maximum estimated dollars for this command")
    parser.add_argument("--dry-run", action="store_true", help="show estimate without running the command")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="agent command after --")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        print("usage: agent-bill-guard [--budget USD] [--dry-run] -- <agent command>", file=sys.stderr)
        return 2

    estimate = estimate_spend(command)
    print(f"estimated_tokens={estimate.tokens} estimated_cost=${estimate.dollars:.4f}")
    for warning in estimate.warnings:
        print(f"warning: {warning}")
    print("tip: send only relevant files and prefer concise prompts for cheaper runs")

    if args.budget is not None and estimate.dollars > args.budget:
        print(f"blocked: estimate exceeds budget ${args.budget:.2f}", file=sys.stderr)
        return 3
    if args.dry_run:
        return 0
    return subprocess.call(command)


if __name__ == "__main__":
    raise SystemExit(main())
