from django.db.models import Case, DecimalField, F, Sum, When

from styleguide_example.portfolio.enums import (
    PortfolioDateRange,
    PortfolioSpecialAmounts,
)
from styleguide_example.portfolio.models import PortfolioAsset


def initial_portfolio_amount_update():
    portfolio_assets = PortfolioAsset.objects.filter(date=PortfolioDateRange.INITIAL_DATE).annotate(
        price=Sum(
            Case(
                When(
                    asset__prices__date=PortfolioDateRange.INITIAL_DATE,
                    then=F("asset__prices__value"),
                ),
                default=0,
                output_field=DecimalField(),
            )
        )
    )

    for portfolio_asset in portfolio_assets:
        portfolio_asset.amount = (
            portfolio_asset.weight
            * PortfolioSpecialAmounts.INITIAL_PORTFOLIO_AMOUNT
            / portfolio_asset.price
        )
        portfolio_asset.save()
