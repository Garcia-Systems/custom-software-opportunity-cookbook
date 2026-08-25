# Custom Software Opportunity Cookbook

A compact, executable casebook for deciding where custom software might make economic sense—and where it does not. The code models assumptions, calculates three-party economics, and produces a verdict with readable reasons rather than an opaque score.

## What this repository is

A compact executable casebook for evaluating where custom software makes economic sense. It combines immutable fictional assumptions, `Decimal` economics, explicit verdict gates, runnable cases, and a transparent cross-case synthesis.

## What it is not

It is not a market study, an industry benchmark source, a CRM, an ERP, a domain application, or proof that any modeled market is attractive.

## Conceptual progression

```text
Restaurant Technology Lab                 What could we build?
                    ↓
Custom Software Deal Economics            Would the deal make economic sense?
                    ↓
Custom Software Opportunity Cookbook      Where should we look for these deals?
```

> **Fiction notice:** All businesses, operational metrics, financial values, labor assumptions, delivery estimates, sales assumptions, and support costs in this repository are fictional educational modeling assumptions unless explicitly cited otherwise. A modeled result is a hypothesis, not market validation or financial advice.

## Start here

Python 3.11 or newer is required.

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[test]'
pytest
python examples/opportunity_framework.py
# Run any individual case (shown here with Case 1):
python examples/independent_restaurant.py
# Compare all 14 framework-generated baselines:
python examples/compare_opportunities.py
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
- [Case 13 — Great Customer Value, Bad Delivery Economics](chapters/13-bad-delivery-economics.md) — implemented
- [Case 14 — Great Product, Bad Sales Motion](chapters/14-bad-sales-motion.md) — implemented
- [Chapter 15 — Where Custom Software Deserves to Exist](chapters/15-cross-case-synthesis.md) — final cross-case synthesis (not Case 15)

**The book is complete: Chapter 0, Cases 1–14, and the Chapter 15 synthesis are implemented; no additional industry case is planned.**

### Compact book structure

| Part | Purpose |
|---|---|
| Chapter 0 | Reusable opportunity, economics, alternative, authority, support, sales, and verdict framework |
| Cases 1–5 | Single-site, multi-site, hospitality, and seasonal reporting economics |
| Cases 6–8 | Standardized categories, alternatives, and operational handoffs |
| Cases 9–11 | Procurement, governance, authority, security, and validation |
| Cases 12–14 | Isolated alternative, delivery, and acquisition failure modes |
| Chapter 15 | Cross-case patterns, hypotheses, funnel, and non-scored screening checklist |

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
- `bad_delivery_economics.py`: immutable Case 13 burden, delivery decomposition, price-corridor, redesign, and scenario assumptions.
- `examples/bad_delivery_economics.py`: executable Case 13 analysis and fourteen-case comparison.
- `bad_sales_motion.py`: immutable Case 14 acquisition motion, contribution, channel, corridor, sensitivity, and scenario assumptions.
- `examples/bad_sales_motion.py`: executable Case 14 analysis and final fourteen-case comparison.
- `comparison.py`: canonical baseline registry, common transparent economics, verdict grouping, structural pattern sets, and fixed rendering—without a composite score.
- `examples/compare_opportunities.py`: canonical executable comparison of all fourteen baselines.
- `chapters/15-cross-case-synthesis.md`: final good-project/good-market synthesis, discovery hypotheses, failure patterns, funnel, and practical checklist.

The tool evaluates opportunities; it does not implement a fictional customer's workflow.


## Final casebook synthesis

Read [Chapter 15 — Where Custom Software Deserves to Exist](chapters/15-cross-case-synthesis.md), then reproduce its evidence with:

```bash
python examples/compare_opportunities.py
```

The fourteen cases expose failure modes directly rather than compressing them into a composite score:

| Observable failure | Framework implication |
|---|---|
| **Problem too small** | insufficient value |
| **Better existing product** | **BUY / CONFIGURE** |
| **Delivery too expensive** | **NO DEAL** |
| **Sales / procurement too expensive** | **POOR TARGET CUSTOMER** |
| **Authority / access missing** | redesign, poor target, or pass |
| **Support unsustainable** | redesign or **NO DEAL** |
| **Low reuse** | possibly **ONE-OFF CUSTOM PROJECT** |

The positive hypothesis is equally transparent:

```text
MEANINGFUL PROBLEM
+ MEASURABLE VALUE
+ INSUFFICIENT OFF-THE-SHELF SOLUTION
+ AUTHORIZED / ACCESSIBLE BUYER
+ FEASIBLE INTEGRATION
+ SUSTAINABLE DELIVERY
+ SUSTAINABLE SUPPORT
+ EFFICIENT SALES MOTION
+ USEFUL REPEATABILITY
= PROMISING — VALIDATE IN DISCOVERY
```

The strongest pattern combines customer value, technical feasibility, authority, sustainable implementation/support, efficient acquisition, and both engineering and sales repeatability. The weakest opportunities fail a decisive gate even when another dimension looks excellent: Case 12 has an excellent-looking problem but a better product exists; Case 13 has value but cannot be built economically; Case 14 is a good referred project but a poor outbound market. These remain explainable dimensions, never an opaque opportunity score.

## Final principle

The goal is not to prove that custom software should be sold. The goal is to learn where custom software deserves to exist.
