from django.db.models import Case, FloatField, F, Sum, When

from abaqus.portfolio.constants import (
    INITIAL_DATE,
    INITIAL_PORTFOLIO_AMOUNT,
)
from abaqus.portfolio.models import PortfolioAsset


def initial_portfolio_amount_update():
    portfolio_assets = PortfolioAsset.objects.filter(date=INITIAL_DATE).annotate(
        price=Sum(
            Case(
                When(
                    asset__prices__date=INITIAL_DATE,
                    then=F("asset__prices__value"),
                ),
                default=0,
                output_field=FloatField(),
            )
        )
    )

    for portfolio_asset in portfolio_assets:
        portfolio_asset.amount = (
            portfolio_asset.weight * INITIAL_PORTFOLIO_AMOUNT / portfolio_asset.price
        )
        portfolio_asset.save()
