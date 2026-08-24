"""Ordered, explicit decision rules—not a weighted opportunity score."""

from dataclasses import dataclass
from decimal import Decimal
from .economics import (customer_net_annual_benefit, recurring_support_contribution,
                        reuse_percentage, solutions_contribution)
from .models import AlternativeFinding, Feasibility, Level, OpportunityScenario
from .verdicts import Verdict


@dataclass(frozen=True)
class OpportunityAnalysis:
    verdict: Verdict
    reasons: tuple[str, ...]


def analyze(s: OpportunityScenario) -> OpportunityAnalysis:
    """Apply documented gates in order and return every reason for that gate."""
    if not s.meaningful_problem:
        return OpportunityAnalysis(Verdict.NO_DEAL, ("No meaningful business problem was established.",))

    missing = []
    if s.customer.current_state_annual_burden is None:
        missing.append("Current-state annual burden has not been measured.")
    if s.customer.recoverable_value is None:
        missing.append("Recoverable value has not been validated.")
    if s.technical.feasibility is Feasibility.UNKNOWN:
        missing.append("Technical feasibility remains unresolved.")
    if s.build_vs_buy.finding is AlternativeFinding.UNKNOWN:
        missing.append("Existing alternatives have not been adequately evaluated.")
    if missing:
        return OpportunityAnalysis(Verdict.INVESTIGATE, tuple(missing))

    if s.build_vs_buy.finding is AlternativeFinding.ADEQUATE_BUY:
        return OpportunityAnalysis(Verdict.BUY_CONFIGURE, (
            "An existing buy/configure alternative adequately meets the need at materially lower cost or risk.",))
    if s.technical.feasibility is Feasibility.INFEASIBLE:
        return OpportunityAnalysis(Verdict.NO_DEAL, ("The proposed solution is not technically feasible.",))

    failures = []
    contribution = solutions_contribution(s.customer, s.delivery, s.solutions)
    if contribution <= 0:
        failures.append("Implementation price does not cover delivery and solutions labor costs.")
    net = customer_net_annual_benefit(s.customer)
    if net is not None and net <= 0:
        failures.append("Recoverable value does not exceed the annual recurring fee.")
    if net is not None and net <= s.customer.implementation_price:
        failures.append("The customer does not recover implementation price within one year.")
    if recurring_support_contribution(s.customer, s.delivery) < 0:
        failures.append("The annual recurring fee does not cover modeled support cost.")
    if failures:
        return OpportunityAnalysis(Verdict.NO_DEAL, tuple(failures))

    difficult_sales = (s.sales.procurement_difficulty is Level.HIGH
                       or s.sales.close_friction is Level.HIGH
                       or s.sales.customer_accessibility is Level.LOW
                       or s.sales.sales_cycle_months > Decimal("6"))
    if difficult_sales:
        return OpportunityAnalysis(Verdict.POOR_TARGET, (
            "Sales, access, cycle, or procurement friction is high for the modeled contract.",))

    reuse = reuse_percentage(s.delivery)
    if reuse is None or reuse < Decimal("0.40"):
        return OpportunityAnalysis(Verdict.ONE_OFF, (
            "The engagement economics work, but less than 40% of core engineering work is demonstrably reusable.",))
    return OpportunityAnalysis(Verdict.PROMISING, (
        "Customer value, delivery contribution, and recurring support economics work under the assumptions.",
        "At least 40% of core engineering work is modeled as demonstrably reusable.",
        "Promising is an economic hypothesis; market validation still requires discovery.",
    ))
