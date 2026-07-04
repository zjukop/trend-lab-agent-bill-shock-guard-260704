# Agent Bill Shock Guard

A tiny local CLI wrapper that estimates token spend, warns about runaway agent loops, and suggests cheaper context choices before launching coding agents.

## Install

```bash
pip install -e .
```

## Usage

```bash
agent-bill-guard --budget 1.50 -- claude "fix the tests"
agent-bill-guard --budget 0.25 --dry-run -- codex "explain this repo"
```

The tool is intentionally local-only and stores no data by default.

## Development

```bash
pip install -e '.[dev]'
pytest
```
