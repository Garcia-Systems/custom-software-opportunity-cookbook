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
python examples/independent_restaurant.py
python examples/restaurant_group.py
python examples/independent_hotel.py
python examples/hotel_group.py
python examples/tourism_attraction.py
python examples/multi_location_retail.py
python examples/construction_trades.py
python examples/professional_services.py
python examples/local_government.py
python examples/university.py
python examples/healthcare.py
python examples/buy_dont_build.py
```

The editable installation makes the `src/` package importable by the example. Tests can also run directly from a checkout because pytest's path is configured in `pyproject.toml`.

## Chapters

- [Chapter 0 — How to Evaluate a Custom Software Opportunity](chapters/00-opportunity-framework.md) — implemented
- [Case 1 — The Independent Restaurant](chapters/01-independent-restaurant.md) — implemented
- [Case 2 — The Five-Location Restaurant Group](chapters/02-restaurant-group.md) — implemented
- [Case 3 — The Independent Hotel](chapters/03-independent-hotel.md) — implemented
- [Case 4 — The Small Hotel Group](chapters/04-hotel-group.md) — implemented
- [Case 5 — The Tourism / Attraction Operator](chapters/05-tourism-attraction.md) — implemented
- [Case 6 — The Multi-Location Retailer](chapters/06-multi-location-retail.md) — implemented
- [Case 7 — The Construction / Trades Company](chapters/07-construction-trades.md) — implemented
- [Case 8 — The Professional Services Firm](chapters/08-professional-services.md) — implemented
- [Case 9 — The Local Government Department](chapters/09-local-government.md) — implemented
- [Case 10 — The University Department](chapters/10-university.md) — implemented
- [Case 11 — The Healthcare Organization](chapters/11-healthcare.md) — implemented
- [Case 12 — The Perfect-Looking Deal That Isn't](chapters/12-buy-dont-build.md) — implemented
- Cases 13–14 — planned, **not implemented**

## Package map

- `models.py`: frozen assumption records and explicit categories.
- `economics.py`: deterministic `Decimal` calculations.
- `analysis.py`: ordered decision gates and traceable reasons.
- `verdicts.py`: stable machine identifiers with readable labels.
- `examples/opportunity_framework.py`: one tiny, fictional demonstration—not a numbered case.
- `independent_restaurant.py`: immutable Case 1 assumptions and scenario variants.
- `examples/independent_restaurant.py`: executable Case 1 analysis.
- `scaling.py`: reusable fixed/shared, per-unit, and exception delivery/support assumptions.
- `restaurant_group.py`: immutable Case 2 assumptions, variants, and calculated Case 1 comparison.
- `examples/restaurant_group.py`: executable Case 2 analysis.
- `independent_hotel.py`: immutable Case 3 burden assumptions and integration-access variants.
- `examples/independent_hotel.py`: executable Case 3 analysis and implemented-case comparison.
- `hotel_group.py`: immutable Case 4 group burden, standardization, scaling, support, and comparison assumptions.
- `examples/hotel_group.py`: executable Case 4 analysis and four-case comparison.
- `tourism_attraction.py`: immutable seasonal Case 5 burdens, context, delivery variants, and calculated implemented-case comparison.
- `examples/tourism_attraction.py`: executable Case 5 analysis and implemented-case comparison.
- `multi_location_retail.py`: immutable Case 6 burden, alternative economics, multi-location delivery, support, and scenario assumptions.
- `examples/multi_location_retail.py`: executable Case 6 analysis and six-case comparison.
- `construction_trades.py`: immutable Case 7 handoff, billing-timing, reliability, support, alternatives, and scenario assumptions.
- `examples/construction_trades.py`: executable Case 7 analysis and seven-case comparison.
- `professional_services.py`: immutable Case 8 administrative burden, configuration alternative, delivery, support, scenario, and Case 7 comparison assumptions.
- `examples/professional_services.py`: executable Case 8 analysis and eight-case comparison.
- `local_government.py`: immutable Case 9 public-service burden, procurement, delivery, support, access, alternative, and scenario assumptions.
- `examples/local_government.py`: executable Case 9 analysis, Case 7 comparison, and nine-case comparison.
- `university.py`: immutable Case 10 administrative burden, authority map, governance, delivery, support, alternatives, scenarios, and Case 9 comparison assumptions.
- `examples/university.py`: executable Case 10 analysis and ten-case comparison.
- `healthcare.py`: immutable Case 11 administrative burden, security/privacy, validation, uncertainty, support, alternatives, scenarios, and cross-case assumptions.
- `examples/healthcare.py`: executable Case 11 analysis and eleven-case comparison.
- `buy_dont_build.py`: immutable Case 12 two-stage discovery, residual-burden, four-option, edge, break-even, and scenario assumptions.
- `examples/buy_dont_build.py`: executable Case 12 analysis and twelve-case comparison using the fully discovered verdict.

The tool evaluates opportunities; it does not implement a fictional customer's workflow.
