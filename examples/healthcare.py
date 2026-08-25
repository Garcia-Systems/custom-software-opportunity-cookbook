"""Run Case 11. This evaluates fictional administrative economics, not care."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    effective_contribution_per_solutions_hour, implementation_delivery_cost,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.healthcare import (CASE_NINE_TEN_ELEVEN_PROGRESSION,
    baseline_case, case_seven_vs_eleven, difficult_proprietary_integration_case,
    high_customer_value_case, high_reuse_high_validation_case,
    narrow_read_only_case, underpriced_support_case,
    vendor_supported_interfaces_case, vendor_supported_product_case)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison


def money(value): return f"${value:,.2f}"


case = baseline_case(); scenario = case.scenario; e = case.engineering
print("CASE 11 — THE HEALTHCARE ORGANIZATION\n" + "=" * 38)
print("Fictional educational scenario:\nJames River Specialty Clinic Group")
print("Several fictional outpatient specialty clinics; centralized administration; approximately 80 employees.")
print("All people, systems, operations, and figures are invented assumptions, not benchmarks.")
print("\nSCOPE\nAdministrative / operational integration only")
print("Appointment → scheduling/registration → administrative status → service-completion signal → billing workflow → payment/reconciliation → management reporting")
print("The model processes no records and assigns no clinical or patient outcome value.")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens:
    print(f"{item.name:40} {item.annual_units} × {money(item.cost_per_unit):>9} = {money(item.annual_burden):>13}")
print(f"{'Total annual administrative burden':40} {money(case.total_burden):>25}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':40} {money(item.recoverable):>14}")
print(f"{'Total recoverable value':40} {money(case.recoverable_value):>14}")
print("No diagnosis, treatment, medical prioritization, clinical outcome, or clinical revenue benefit is included.")
print("\nDELIVERY")
for label, value in (("Base engineering", e.base_engineering_hours),
        ("Integration-access validation", e.integration_validation),
        ("Security/privacy implementation", e.security_privacy),
        ("Validation/testing", e.validation_reconciliation + e.testing),
        ("Deployment/monitoring", e.deployment_monitoring),
        ("Rework reserve", e.rework_reserve),
        ("Integration uncertainty reserve", e.integration_uncertainty_reserve),
        ("Total engineering hours", e.total_hours)):
    print(f"{label:40} {value:>10}")
print("Direct delivery cost:", money(implementation_delivery_cost(scenario.delivery)))
print("Reusable / customer-specific core hours:", scenario.delivery.reusable_engineering_hours,
      "/", scenario.delivery.customer_specific_engineering_hours)
print("Reusable adapters, normalization, validation, idempotency, audit, monitoring, secure configuration, and deployment patterns do not eliminate customer-specific verification.")
print("\nDATA MINIMIZATION\nNEED DATA? NO → DO NOT INGEST IT | YES → USE MINIMUM NECESSARY FICTIONAL ADMINISTRATIVE FIELDS")
print("Existing scheduling, practice-management, clinical-record, billing, communication, staffing, and reporting systems remain authoritative.")
print("\nCUSTOMER ECONOMICS")
print("Implementation / annual fee:", money(scenario.customer.implementation_price), "/",
      money(scenario.customer.recurring_annual_fee))
print("\nSOLUTIONS ECONOMICS")
print("Prospecting, discovery, workflow mapping, stakeholder interviews, security/privacy discovery, vendor validation, design, scoping, coordination, and acceptance planning.")
print("Total solutions hours:", solutions_hours(scenario.solutions))
print("Implementation contribution / per solutions hour:",
      money(solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions)), "/",
      money(effective_contribution_per_solutions_hour(scenario.customer, scenario.delivery, scenario.solutions)))
print("\nSUPPORT")
print("Monitoring, failures, interface and credential changes, security updates, incident expectations, mappings, data quality, support, maintenance, and periodic validation.")
print("Recurring fee / direct cost / contribution:", money(scenario.customer.recurring_annual_fee), "/",
      money(annual_support_cost(scenario.delivery)), "/",
      money(recurring_support_contribution(scenario.customer, scenario.delivery)))
print("\nBUILD VS. BUY\n" + scenario.build_vs_buy.note)
print("A supported option can be superior despite a higher sticker price because risk and retained burden are explicit.")
print("No clinical system, billing platform, portal, scheduling system, or patient-facing application is built or replaced.")
result = analyze(scenario)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("High customer value does not cancel high delivery cost.")
print("\nSCENARIOS")
factories = (("Baseline", baseline_case),
    ("Vendor-supported interfaces", vendor_supported_interfaces_case),
    ("Difficult proprietary integration", difficult_proprietary_integration_case),
    ("High customer value", high_customer_value_case),
    ("Vendor-supported product", vendor_supported_product_case),
    ("Underpriced support", underpriced_support_case),
    ("Narrow read-only scope", narrow_read_only_case),
    ("High reuse / high validation", high_reuse_high_validation_case))
for name, factory in factories:
    item = factory()
    print(f"{name:36} {analyze(item.scenario).verdict.value:34} value {money(item.recoverable_value):>13} | delivery {item.engineering.total_hours:>5}h")
deep, narrow = baseline_case(), narrow_read_only_case()
print("\nSCOPE REDUCTION")
print("Deep multi-system: value / delivery / support", money(deep.recoverable_value),
      deep.engineering.total_hours, money(annual_support_cost(deep.scenario.delivery)), "→", analyze(deep.scenario).verdict.value)
print("Narrow read-only: value / delivery / support", money(narrow.recoverable_value),
      narrow.engineering.total_hours, money(annual_support_cost(narrow.scenario.delivery)), "→", analyze(narrow.scenario).verdict.value)
comparison = case_seven_vs_eleven()
print("\nCASE 7 VS. CASE 11")
print("Construction — value / integration / support / verdict:", money(comparison.construction_value),
      comparison.construction_integration, money(comparison.construction_support_cost), comparison.construction_verdict)
print("Healthcare — value / integration / support / verdict:", money(comparison.healthcare_value),
      comparison.healthcare_integration, money(comparison.healthcare_support_cost), comparison.healthcare_verdict)
print("At what point does added value stop compensating for added delivery complexity? No composite score answers that question.")
print("\nCASE 9 → 10 → 11")
for line in CASE_NINE_TEN_ELEVEN_PROGRESSION: print(line)
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} value {money(row.recoverable_value):>13} | delivery {row.delivery_difficulty:8} | procurement {row.sales_procurement_difficulty:8} | reuse {row.reuse:.0%} | support in case model | {row.verdict}")
