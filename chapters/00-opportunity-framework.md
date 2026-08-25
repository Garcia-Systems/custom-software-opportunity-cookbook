# Chapter 0 — How to Evaluate a Custom Software Opportunity

> What separates an interesting business problem from an economically viable custom-software opportunity?

This framework turns stated assumptions into an **economic hypothesis**. It is a gate-by-gate field guide, not an opportunity score. Every rejection and every encouraging result must name its reasons.

## The sequence

1. Establish a meaningful problem. If none exists: **NO DEAL**.
2. Measure current burden and recoverable value. If material facts are missing: **INVESTIGATE**.
3. examine SaaS, configuration, automation, spreadsheets/process change, and doing nothing. If buying is adequate and materially preferable: **BUY / CONFIGURE**.
4. Check feasibility, delivery contribution, customer return, and support coverage. A failed gate means **NO DEAL**.
5. Check access, procurement, close friction, and cycle. Excessive friction means **POOR TARGET CUSTOMER**.
6. Distinguish customer-specific work from demonstrated common work. Viable with low reuse is a **ONE-OFF CUSTOM PROJECT**; viable with substantial reuse is **PROMISING — VALIDATE IN DISCOVERY**.

The implementation documents two deliberately simple operating rules: customer benefit must repay implementation within one year, and at least 40% of core engineering hours must be demonstrably reusable for `PROMISING`. These are editable screening policies, not universal truths.

## Ten lessons

### 1. A problem is not automatically a software opportunity

An annoying manual process may cost less than a responsible custom build. First estimate the current-state **annual burden**: avoidable labor, errors, delay, and other explicitly defensible costs. If it is immaterial, pass.

### 2. Technical feasibility is not economic viability

Buildable software can still fail customer payback, partner cost, sales effort, or support coverage. “We can build it” answers only one gate.

### 3. Value, price, and cost are different

```text
Customer value ≠ customer price ≠ delivery cost
```

| Term | Definition |
|---|---|
| Current-state annual burden | Measured annual cost of the problem before a solution |
| Recoverable annual value | Realistic portion of that burden the solution can remove |
| Implementation price | One-time amount paid by the customer |
| Recurring annual fee | Annual amount paid for support/service |
| Customer retained benefit | Recoverable value − recurring annual fee |
| Direct delivery cost | Engineering, QA, deployment, reserve, and other direct implementation costs |

The simple screening calculations are:

```text
first-year ROI = (retained annual benefit − implementation price)
                 / (implementation price + recurring annual fee)
payback months = implementation price / retained annual benefit × 12
```

ROI is undefined when first-year spend is zero. Payback is undefined when retained benefit is zero or negative. These are one-year, undiscounted estimates—not forecasts.

### 4. Custom software competes with alternatives

Compare custom work with existing SaaS, SaaS configuration, automation tools, spreadsheets, process improvement, and doing nothing. Custom wins only when those choices are inadequate and its incremental cost and risk make sense. An incomplete alternatives review means **INVESTIGATE**, not “build.”

### 5. Three parties must have workable economics

```text
CUSTOMER
Business value, retained benefit, budget, and payback
        ↕
SOLUTIONS ORGANIZATION
Prospecting, discovery, design, coordination, and contribution
        ↕
ENGINEERING PARTNER
Implementation, integration, testing, deployment, and maintenance
```

Implementation contribution is price less direct delivery cost and modeled solutions labor. Contribution per solutions hour makes a small contract's coordination burden visible.

### 6. Sales economics matter

An economically attractive $8,000 implementation can remain a poor target if acquisition takes months. Record prospecting hours, cycle length, accessibility, procurement difficulty, and close friction; do not disguise them in a probability score.

### 7. Support economics matter

Recurring revenue is not pure profit. Annual support contribution is recurring fee minus support engineering hours times support cost. Negative coverage requires redesign or **NO DEAL**.

### 8. Reuse matters

```text
COMMON / DEMONSTRABLY REUSABLE WORK + CUSTOMER-SPECIFIC WORK
```

Reuse percentage is reusable core engineering hours divided by reusable plus customer-specific core hours. QA, deployment, and reserves affect delivery cost but are excluded from this narrow reuse ratio. The distinction is crucial:

```text
Good project: this customer's economics work.
Good market: a meaningful pattern can repeat across customers.
```

Theoretical portability is not evidence of reuse.

### 9. Integration-first thinking

```text
Existing System A ──┐
Existing System B ──┼──→ Custom Integration Layer
Existing System C ──┘             ↓
                            Useful workflow /
                            management signal
```

Connecting systems can preserve prior investments, reduce training and scope, and target the valuable gap. It is often more realistic than replacing an entire stack—but permissions, data access, security, and compliance remain explicit assumptions.

### 10. Discovery remains mandatory

```text
CASE MODEL → Economic hypothesis → Target customer profile
           → Real discovery → Actual numbers → Recalculate
           → Prototype only if justified
```

`PROMISING` means only that the modeled gates passed. It never means a market has been validated. Interview buyers and users, verify alternatives and integration rights, replace fictional inputs, and recalculate before prototyping.

## Run the tiny demonstration

After following the [README setup](../README.md#start-here):

```bash
python examples/opportunity_framework.py
```

The local-service scenario is intentionally small and wholly fictional. It demonstrates calculations and reason traceability; it is not Case 1 or evidence about an industry.

[Book home](../README.md) · [Next: Case 1 — The Independent Restaurant →](01-independent-restaurant.md)
