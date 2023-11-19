from enum import Enum

# Define AccessType enum for access permission levels
class AccessType(Enum):
    VIEW = 1
    MODIFY = 2
    VALIDATE = 3
    CONDITIONAL = 4

# Define ResourceType enum for different types of system resources
class ResourceType(Enum):
    CLIENT_INFO = 1
    ACCOUNT_BALANCE = 2
    INVESTMENTS_PORTFOLIO = 3
    CD_FA = 4
    CD_FP = 5
    CD_IA = 6
    MONEY_MARKET_I = 7
    DERIVATIVES_TRADING = 8
    INTEREST_INSTRUMENTS = 9
    PRVT_CONSUMER_INSTRUMENTS = 10
    SYSTEM = 11


# Define RoleType enum for different user roles
class RoleType(Enum):
    REGULAR_CLIENT = 0
    PREMIUM_CLIENT = 1
    FINANCIAL_ADVISOR = 2
    FINANCIAL_PLANNER = 3
    TELLER = 4
    INVESTMENT_ANALYST = 5
    COMPLIANCE_OFFICER = 6
    TECH_SUPPORT = 7
