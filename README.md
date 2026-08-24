# Custom Software Opportunity Cookbook

A compact, executable casebook for deciding where custom software might make economic sense—and where it does not. The code models assumptions, calculates three-party economics, and produces a verdict with readable reasons rather than an opaque score.

```text
Restaurant Technology Lab                 What could we build?
                    ↓
Custom Software Deal Economics            Would the deal make economic sense?
                    ↓
Custom Software Opportunity Cookbook      Where should we look for these deals?
```

> **Fiction notice:** Every business, operational assumption, and financial figure in this repository is fictional and educational unless explicitly cited otherwise. A modeled result is a hypothesis, not market validation or financial advice.

## Start here

Python 3.11 or newer is required.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
pytest
python examples/opportunity_framework.py
```

The editable installation makes the `src/` package importable by the example. Tests can also run directly from a checkout because pytest's path is configured in `pyproject.toml`.

## Chapters

- [Chapter 0 — How to Evaluate a Custom Software Opportunity](chapters/00-opportunity-framework.md) — implemented
- Cases 1–14 — planned, **not implemented**

## Package map

- `models.py`: frozen assumption records and explicit categories.
- `economics.py`: deterministic `Decimal` calculations.
- `analysis.py`: ordered decision gates and traceable reasons.
- `verdicts.py`: stable machine identifiers with readable labels.
- `examples/opportunity_framework.py`: one tiny, fictional demonstration—not a numbered case.

The tool evaluates opportunities; it does not implement a fictional customer's workflow.
