from access_control import AccessControl
from environment import Environment
from enums import RoleType, AccessType, ResourceType

class AccessControlTest:
    def __init__(self):
        self.accessControl = AccessControl()

    def set_permission(self, permission):
        self.accessControl.client_permission = permission

    def set_validation_required(self, validate):
        self.accessControl.validation_required = validate

    # Roles: REGULAR_CLIENT, PREMIUM_CLIENT, FINANCIAL_ADVISOR, FINANCIAL_PLANNER, TELLER, INVESTMENT_ANALYST, COMPLIANCE_OFFICER, TECH_SUPPORT
    # Resources: CLIENT_INFO, ACCOUNT_BALANCE, INVESTMENTS_PORTFOLIO, CD_FA, CD_FP, CD_IA, MONEY_MARKET_I, DERIVATIVES_TRADING, INTEREST_INSTRUMENTS, PRVT_CONSUMER_INSTRUMENTS, SYSTEM

    def tester(self, t, a, r, expected):
        actual = self.accessControl.check_access(t, a, r)
        print(f"Testing {a.name} access to {r.name}. Expected: {expected}. Actual: {actual}")

if __name__ == "__main__":
    test = AccessControlTest()

    # Teller
    print("\nTELLER:")
    test.tester(RoleType.TELLER, AccessType.VIEW, ResourceType.INVESTMENTS_PORTFOLIO, False)
    curr_time = Environment.get_curr_hour()
    b = 9 <= curr_time <= 17
    test.tester(RoleType.TELLER, AccessType.CONDITIONAL, ResourceType.SYSTEM, b)

    # REGULAR CLIENT
    print("\nREGULAR CLIENT:")
    test.tester(RoleType.REGULAR_CLIENT, AccessType.VIEW, ResourceType.INVESTMENTS_PORTFOLIO, True)
    test.tester(RoleType.REGULAR_CLIENT, AccessType.MODIFY, ResourceType.INVESTMENTS_PORTFOLIO, False)

    # PREMIUM CLIENT
    print("\nPREMIUM CLIENT:")
    test.tester(RoleType.PREMIUM_CLIENT, AccessType.VIEW, ResourceType.CD_FA, True)
    test.tester(RoleType.PREMIUM_CLIENT, AccessType.MODIFY, ResourceType.INVESTMENTS_PORTFOLIO, True)

    # FINANCIAL ADVISOR
    print("\nFINANCIAL ADVISOR:")
    test.tester(RoleType.FINANCIAL_ADVISOR, AccessType.MODIFY, ResourceType.INVESTMENTS_PORTFOLIO, True)
    test.tester(RoleType.FINANCIAL_ADVISOR, AccessType.VALIDATE, ResourceType.INVESTMENTS_PORTFOLIO, False)

    # FINANCIAL PLANNER
    print("\nFINANCIAL PLANNER:")
    test.tester(RoleType.FINANCIAL_PLANNER, AccessType.VIEW, ResourceType.MONEY_MARKET_I, True)
    test.tester(RoleType.FINANCIAL_PLANNER, AccessType.MODIFY, ResourceType.PRVT_CONSUMER_INSTRUMENTS, False)

    # INVESTMENT ANALYST
    print("\nINVESTMENT ANALYST:")
    test.tester(RoleType.INVESTMENT_ANALYST, AccessType.MODIFY, ResourceType.INVESTMENTS_PORTFOLIO, True)
    test.tester(RoleType.INVESTMENT_ANALYST, AccessType.MODIFY, ResourceType.DERIVATIVES_TRADING, False)

    # COMPLIANCE OFFICER
    print("\nCOMPLIANCE OFFICER:")
    test.set_validation_required(True)
    test.tester(RoleType.COMPLIANCE_OFFICER, AccessType.VALIDATE, ResourceType.INVESTMENTS_PORTFOLIO, True)
    test.set_validation_required(False)
    test.tester(RoleType.COMPLIANCE_OFFICER, AccessType.VALIDATE, ResourceType.INVESTMENTS_PORTFOLIO, False)

    # TECHNICAL SUPPORT
    print("\nTECHNICAL SUPPORT:")
    test.set_permission(True)
    test.tester(RoleType.TECH_SUPPORT, AccessType.CONDITIONAL, ResourceType.CLIENT_INFO, True)
    test.set_permission(False)
    test.tester(RoleType.TECH_SUPPORT, AccessType.CONDITIONAL, ResourceType.CLIENT_INFO, False)
