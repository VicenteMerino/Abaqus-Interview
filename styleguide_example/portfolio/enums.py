from enum import Enum


class PortfolioDateRange(Enum):
    """Enum for the date range options for the portfolio page."""

    INITIAL_DATE = "2022-02-15"
    LAST_DATE = "2023-02-16"


class PortfolioSpecialAmounts(Enum):
    """Enum for the special amounts used in the portfolio page."""

    INITIAL_PORTFOLIO_AMOUNT = 1000000000
