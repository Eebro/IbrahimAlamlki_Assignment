from typing import List
from enums import RoleType, AccessType, ResourceType
from custom_resource import Resource

class Role:
    @staticmethod
    def get_env_policy(r: RoleType) -> str:
        if r == RoleType.TELLER:
            return "As a teller, this user can only access the system between 9 a.m. and 5 p.m. \n As a teller, this user can only access client accounts with their permission."
        elif r == RoleType.TECH_SUPPORT:
            return "Technical support can only access client accounts with their permission"
        else:
            return ""

    @staticmethod
    def create_capability_list(r: RoleType) -> List[Resource]:
        resources = [Resource(ResourceType.CLIENT_INFO, AccessType.VIEW)]

        if r == RoleType.PREMIUM_CLIENT:
            resources.extend([
                Resource(ResourceType.INVESTMENTS_PORTFOLIO, AccessType.MODIFY),
                Resource(ResourceType.CD_FP, AccessType.VIEW),
                Resource(ResourceType.CD_IA, AccessType.VIEW),
            ])
        elif r == RoleType.REGULAR_CLIENT:
            resources.extend([
                Resource(ResourceType.ACCOUNT_BALANCE, AccessType.VIEW),
                Resource(ResourceType.CD_FA, AccessType.VIEW),
                Resource(ResourceType.INVESTMENTS_PORTFOLIO, AccessType.VIEW),
            ])

        elif r == RoleType.FINANCIAL_PLANNER:
            resources.append(Resource(ResourceType.MONEY_MARKET_I, AccessType.VIEW))

        elif r == RoleType.FINANCIAL_ADVISOR:
            resources.extend([
                Resource(ResourceType.ACCOUNT_BALANCE, AccessType.VIEW),
                Resource(ResourceType.INVESTMENTS_PORTFOLIO, AccessType.MODIFY),
                Resource(ResourceType.PRVT_CONSUMER_INSTRUMENTS, AccessType.VIEW),
            ])

        elif r == RoleType.INVESTMENT_ANALYST:
            resources.extend([
                Resource(ResourceType.ACCOUNT_BALANCE, AccessType.VIEW),
                Resource(ResourceType.INVESTMENTS_PORTFOLIO, AccessType.MODIFY),
                Resource(ResourceType.MONEY_MARKET_I, AccessType.VIEW),
                Resource(ResourceType.DERIVATIVES_TRADING, AccessType.VIEW),
                Resource(ResourceType.INTEREST_INSTRUMENTS, AccessType.VIEW),
                Resource(ResourceType.PRVT_CONSUMER_INSTRUMENTS, AccessType.VIEW),
            ])

        elif r == RoleType.COMPLIANCE_OFFICER:
            resources.extend([
                Resource(ResourceType.ACCOUNT_BALANCE, AccessType.VIEW),
                Resource(ResourceType.INVESTMENTS_PORTFOLIO, AccessType.VALIDATE),
            ])

        elif r == RoleType.TELLER:
            resources.append(Resource(ResourceType.SYSTEM, AccessType.CONDITIONAL))

        elif r == RoleType.TECH_SUPPORT:
            resources.append(Resource(ResourceType.CLIENT_INFO, AccessType.CONDITIONAL))

        return resources
