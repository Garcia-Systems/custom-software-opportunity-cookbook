"""Case 14: excellent reusable delivery undermined by acquisition economics."""

from dataclasses import dataclass, replace
from decimal import Decimal as D

from .analysis import OpportunityAnalysis, analyze
from .economics import (acquisition_adjusted_minimum_price, annual_support_cost,
    customer_contribution_after_acquisition, customer_contribution_before_acquisition,
    customer_maximum_economic_price, expected_acquisition_cost,
    expected_sales_hours_per_win, has_feasible_price_corridor,
    implementation_contribution, implementation_delivery_cost,
    recurring_support_contribution)
from .models import (AlternativeFinding, AlternativeType, BuildVsBuy,
    CustomerEconomics, DeliveryEconomics, Feasibility, Level,
    OpportunityScenario, SalesCharacteristics, SolutionsEconomics,
    TechnicalCharacteristics)
from .verdicts import Verdict


@dataclass(frozen=True)
class Burden:
    name: str
    annual_hours: D
    hourly_cost: D
    recovery_rate: D

    def __post_init__(self):
        if self.annual_hours < 0 or self.hourly_cost < 0:
            raise ValueError("burden assumptions cannot be negative")
        if not D("0") <= self.recovery_rate <= D("1"):
            raise ValueError("recovery_rate must be between 0 and 1")

    @property
    def annual_burden(self): return self.annual_hours * self.hourly_cost
    @property
    def recoverable_value(self): return self.annual_burden * self.recovery_rate


@dataclass(frozen=True)
class AcquisitionMotion:
    hours_per_qualified_opportunity: D
    close_probability: D
    sales_cycle_months: D
    channel_cost: D = D("0")
    sales_reuse: D = D(".25")

    def __post_init__(self):
        if min(self.hours_per_qualified_opportunity, self.sales_cycle_months,
               self.channel_cost) < 0:
            raise ValueError("acquisition assumptions cannot be negative")
        expected_sales_hours_per_win(self.hours_per_qualified_opportunity,
                                     self.close_probability)
        if not D("0") <= self.sales_reuse <= D("1"):
            raise ValueError("sales_reuse must be between 0 and 1")


@dataclass(frozen=True)
class BadSalesMotionCase:
    burdens: tuple[Burden, ...]
    scenario: OpportunityScenario
    acquisition: AcquisitionMotion
    required_contribution: D = D("2000")
    required_retained_benefit: D = D("3400")

    def __post_init__(self):
        if min(self.required_contribution, self.required_retained_benefit) < 0:
            raise ValueError("commercial assumptions cannot be negative")

    @property
    def total_burden(self): return sum((b.annual_burden for b in self.burdens), D("0"))
    @property
    def recoverable_value(self): return sum((b.recoverable_value for b in self.burdens), D("0"))
    @property
    def delivery_cost(self): return implementation_delivery_cost(self.scenario.delivery)
    @property
    def implementation_contribution(self):
        return implementation_contribution(self.scenario.customer.implementation_price,
                                           self.delivery_cost)
    @property
    def support_cost(self): return annual_support_cost(self.scenario.delivery)
    @property
    def recurring_contribution(self):
        return recurring_support_contribution(self.scenario.customer, self.scenario.delivery)
    @property
    def expected_sales_hours(self):
        return expected_sales_hours_per_win(self.acquisition.hours_per_qualified_opportunity,
                                            self.acquisition.close_probability)
    @property
    def acquisition_cost(self):
        return expected_acquisition_cost(self.expected_sales_hours,
            self.scenario.solutions.hourly_cost, self.acquisition.channel_cost)
    @property
    def contribution_before_acquisition(self):
        return customer_contribution_before_acquisition(self.implementation_contribution,
                                                        self.recurring_contribution)
    @property
    def contribution_after_acquisition(self):
        return customer_contribution_after_acquisition(self.contribution_before_acquisition,
                                                       self.acquisition_cost)
    @property
    def customer_maximum_price(self):
        return customer_maximum_economic_price(self.recoverable_value,
            self.scenario.customer.recurring_annual_fee, self.required_retained_benefit)
    @property
    def acquisition_adjusted_minimum_price(self):
        return acquisition_adjusted_minimum_price(self.delivery_cost, self.acquisition_cost,
            self.required_contribution, self.recurring_contribution)
    @property
    def feasible_corridor(self):
        return has_feasible_price_corridor(self.acquisition_adjusted_minimum_price,
                                           self.customer_maximum_price)
    @property
    def result(self):
        base = analyze(self.scenario)
        if base.verdict not in (Verdict.PROMISING, Verdict.POOR_TARGET): return base
        if self.contribution_after_acquisition < self.required_contribution or not self.feasible_corridor:
            return OpportunityAnalysis(Verdict.POOR_TARGET, (
                "Expected customer acquisition effort is too high relative to contract value.",
                "Contribution after expected acquisition cost is below the required contribution.",
                "The acquisition-adjusted minimum price exceeds the customer's economic maximum.",))
        return OpportunityAnalysis(Verdict.PROMISING, (
            "Customer value, reusable delivery, support, and acquisition economics work under the assumptions.",
            "Promising remains a hypothesis to validate in discovery.",))


BASELINE_BURDENS = (
    Burden("Event/member reconciliation", D("95"), D("32"), D(".62")),
    Burden("Duplicate entry", D("80"), D("30"), D(".70")),
    Burden("Accounting reconciliation", D("78"), D("36"), D(".55")),
    Burden("Membership-status reporting", D("65"), D("34"), D(".65")),
    Burden("Management/board reporting", D("70"), D("40"), D(".60")),
    Burden("Email-list reconciliation", D("55"), D("30"), D(".65")),
    Burden("Spreadsheet administration/rework", D("85"), D("32"), D(".60")),
)


def _build(*, burdens=BASELINE_BURDENS, price=D("7000"), fee=D("2000"),
           reusable=D("28"), specific=D("7"), qa=D("4"), deployment=D("3"),
           rework=D("2"), uncertainty=D("1"), other=D("350"), support_hours=D("10"),
           sales_hours=D("28"), close=D(".20"), cycle=D("7"), channel_cost=D("0"),
           sales_reuse=D(".25"), required_retained=D("3400")):
    total = sum((b.annual_burden for b in burdens), D("0"))
    recovery = sum((b.recoverable_value for b in burdens), D("0"))
    delivery = DeliveryEconomics(reusable, specific, D("70"), qa, deployment,
        rework, other, support_hours, D("60"), D("300"), uncertainty)
    difficult = sales_hours >= D("20") and close <= D(".25")
    scenario = OpportunityScenario("James River Professional Association", True,
        CustomerEconomics(total, recovery, price, fee), delivery,
        SolutionsEconomics(D("0"), D("0"), D("0"), D("0"), D("65")),
        SalesCharacteristics(Level.MODERATE, cycle, Level.HIGH,
                             Level.HIGH if difficult else Level.MODERATE),
        TechnicalCharacteristics(5, Level.LOW, Level.HIGH, Feasibility.FEASIBLE,
                                 Level.LOW, Level.LOW, Level.LOW),
        BuildVsBuy(AlternativeFinding.CUSTOM_JUSTIFIED,
            (AlternativeType.EXISTING_SAAS, AlternativeType.SAAS_CONFIGURATION,
             AlternativeType.AUTOMATION_TOOLING, AlternativeType.CUSTOM_INTEGRATION,
             AlternativeType.DO_NOTHING),
            "Fictional alternatives do not provide the cross-system normalized view."))
    return BadSalesMotionCase(tuple(burdens), scenario,
        AcquisitionMotion(sales_hours, close, cycle, channel_cost, sales_reuse),
        required_retained_benefit=required_retained)


def baseline_case(): return _build()
def warm_referral_case(): return _build(sales_hours=D("7"), close=D(".70"), cycle=D("2"), sales_reuse=D(".70"))
def higher_close_rate_case(): return _build(close=D(".50"), cycle=D("5"), sales_reuse=D(".55"))
def productized_sales_case(): return _build(sales_hours=D("7"), close=D(".45"), cycle=D("2.5"), sales_reuse=D(".85"))
def larger_customer_case():
    burdens = tuple(replace(b, annual_hours=b.annual_hours * D("2")) for b in BASELINE_BURDENS)
    return _build(burdens=burdens, price=D("14500"), fee=D("3500"), sales_hours=D("30"), close=D(".35"), cycle=D("6"), required_retained=D("8000"))
def higher_price_only_case(): return _build(price=D("12000"))
def very_high_reuse_case(): return _build(reusable=D("12"), specific=D("2"), qa=D("2"), deployment=D("1"), rework=D("1"), uncertainty=D("0"))
def partner_channel_case(): return _build(sales_hours=D("4"), close=D(".65"), cycle=D("3"), channel_cost=D("700"), sales_reuse=D(".75"))


def scenario_results():
    cases = (("Baseline outbound", baseline_case()), ("Warm referral", warm_referral_case()),
        ("Higher close rate", higher_close_rate_case()), ("Productized sales motion", productized_sales_case()),
        ("Larger customer", larger_customer_case()), ("Higher price only", higher_price_only_case()),
        ("Very high engineering reuse", very_high_reuse_case()), ("Partner/channel", partner_channel_case()))
    return tuple((name, case.result.verdict.value, case.contribution_after_acquisition) for name, case in cases)


def close_rate_sensitivity(rates=(D(".10"), D(".20"), D(".30"), D(".50"))):
    base = baseline_case()
    return tuple((rate, expected_sales_hours_per_win(base.acquisition.hours_per_qualified_opportunity, rate),
        expected_acquisition_cost(expected_sales_hours_per_win(base.acquisition.hours_per_qualified_opportunity, rate),
                                  base.scenario.solutions.hourly_cost)) for rate in rates)


def case_13_vs_14():
    return (("Case 13", "strong", "expensive", "weak/moderate", "manageable", "BUILD"),
            ("Case 14", "strong", "cheap", "high", "expensive", "ACQUIRE"))


def case_9_vs_14():
    return (("Case 9", "institutional procurement barrier", "procurement"),
            ("Case 14", "ordinary selling effort exceeds small contract economics", "acquisition"))
