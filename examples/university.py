"""Run Case 10. This evaluates an opportunity; it implements no university system."""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from opportunity_cookbook.analysis import analyze
from opportunity_cookbook.economics import (annual_support_cost,
    effective_contribution_per_solutions_hour, implementation_delivery_cost,
    recurring_support_contribution, reuse_percentage, solutions_contribution,
    solutions_hours)
from opportunity_cookbook.tourism_attraction import implemented_case_comparison
from opportunity_cookbook.university import (approved_exports_only_case,
    baseline_case, case_nine_vs_ten, centrally_sponsored_case,
    department_only_champion_case, existing_bi_tool_case,
    higher_contract_value_case, high_reuse_unique_governance_case)


def money(value): return f"${value:,.2f}"


case = baseline_case(); scenario = case.scenario
print("CASE 10 — THE UNIVERSITY DEPARTMENT\n" + "=" * 35)
print("Fictional educational scenario:\nJames River University — Continuing Education")
print("The institution, department, people, operations, and all figures are entirely fictional.")
print("\nBUSINESS PROBLEM")
print("Inquiry → program/course → registration → participant record → schedule → instructor/delivery → completion → finance/reporting")
print("A fictional 24-person department repeatedly reconciles enterprise systems, local tools, forms, email, and spreadsheets.")
print("Instruction and educational outcomes are excluded from recoverable burden.")
print("\nAUTHORITY MAP")
for label, value in (("Problem owner", case.authority.problem_owner),
        ("Budget authority", case.authority.budget_owner), ("System owner", case.authority.system_owner),
        ("Data owner", case.authority.data_owner), ("Security approver", case.authority.security_approver),
        ("Integration approver", case.authority.integration_approver),
        ("Procurement", case.authority.procurement), ("End users", case.authority.end_users)):
    print(f"{label:28} {value}")
print("REACHABLE USER ≠ REACHABLE BUYER ≠ AUTHORIZED SYSTEM OWNER")
print("\nCURRENT-STATE BURDEN")
for item in case.burdens:
    print(f"{item.name:40} {item.annual_units} × {money(item.cost_per_unit):>9} = {money(item.annual_burden):>12}")
print(f"{'Total annual burden':40} {money(case.total_burden):>38}")
print("\nRECOVERABLE VALUE")
for item in case.burdens:
    print(f"{item.name + ' × ' + str(item.improvement_rate * 100) + '%':40} {money(item.recoverable):>14}")
print(f"{'Total recoverable value':40} {money(case.recoverable_value):>14}")
print("No enrollment, retention, tuition, or educational-outcome uplift is assumed.")
print("\nCUSTOMER ECONOMICS")
print("Implementation / annual fee:", money(scenario.customer.implementation_price), "/", money(scenario.customer.recurring_annual_fee))
print("\nDELIVERY")
print("Engineering hours:", case.engineering.total_hours)
print("Integration/security/accessibility effort:", case.engineering.security_access_hours)
print("Direct delivery cost:", money(implementation_delivery_cost(scenario.delivery)))
print("\nSALES / GOVERNANCE")
print("Department discovery / central IT / procurement:", case.governance.department_discovery,
      case.governance.central_it_coordination, case.governance.procurement_support)
print("Total solutions hours:", solutions_hours(scenario.solutions))
print("Contribution / contribution per solutions hour:",
      money(solutions_contribution(scenario.customer, scenario.delivery, scenario.solutions)), "/",
      money(effective_contribution_per_solutions_hour(scenario.customer, scenario.delivery, scenario.solutions)))
print("\nBUILD VS. BUY\n" + scenario.build_vs_buy.note)
print("Baseline favors narrow custom under fictional costs; the existing-BI scenario returns BUY / CONFIGURE.")
print("No SIS, LMS, registration, identity, finance, CRM, ERP, advising system, or portal is replaced.")
print("\nSUPPORT")
print("Restricted hosting/deployment, monitoring, export/API and identity changes, security, accessibility, reporting rules, user support, documentation, and change control.")
print("Annual revenue / cost / contribution:", money(scenario.customer.recurring_annual_fee), "/",
      money(annual_support_cost(scenario.delivery)), "/", money(recurring_support_contribution(scenario.customer, scenario.delivery)))
result = analyze(scenario)
print("\nVERDICT\n-------\n" + result.verdict.value + "\nWHY")
for reason in result.reasons: print("-", reason)
print("Customer desire does not create data, integration, security, procurement, or implementation authority.")
print("\nSCENARIOS")
for name, factory in (("Baseline", baseline_case), ("Central sponsorship", centrally_sponsored_case),
        ("Department-only champion", department_only_champion_case),
        ("Approved exports only", approved_exports_only_case), ("Existing BI tool", existing_bi_tool_case),
        ("Higher contract value", higher_contract_value_case),
        ("Reusable code / unique governance", high_reuse_unique_governance_case)):
    item = factory()
    print(f"{name:38} {analyze(item.scenario).verdict.value} (reuse {reuse_percentage(item.scenario.delivery):.0%})")
print("Reduce scope before violating governance. Unauthorized access and shadow IT are never options.")
comparison = case_nine_vs_ten()
print("\nCASE 9 VS. CASE 10")
print("Local government — solutions/cycle/permission:", comparison.government_solutions_hours,
      comparison.government_sales_cycle_months, comparison.government_permission_difficulty, "→", comparison.government_verdict)
print("University — solutions/cycle/permission:", comparison.university_solutions_hours,
      comparison.university_sales_cycle_months, comparison.university_permission_difficulty, "→", comparison.university_verdict)
print("Case 9 emphasizes difficult procurement; Case 10 adds lack of control over delivery-critical systems.")
print("\nIMPLEMENTED-CASE COMPARISON")
for row in implemented_case_comparison():
    print(f"{row.name:28} value {money(row.recoverable_value):>13} | delivery {row.delivery_difficulty:8} | procurement {row.sales_procurement_difficulty:8} | reuse {row.reuse:.0%} | {row.verdict}")
