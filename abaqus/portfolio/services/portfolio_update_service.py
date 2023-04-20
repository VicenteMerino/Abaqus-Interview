from collections import defaultdict
from django.db.models import OuterRef, Subquery, F, Sum, Case, FloatField, When, ExpressionWrapper

from abaqus.portfolio.constants import (
    INITIAL_DATE,
)
from abaqus.portfolio.models import PortfolioAsset, PortfolioValue
import logging

logger = logging.getLogger(__name__)


class PortfolioUpdateService:
    @classmethod
    def update_amount(cls):
        subquery = PortfolioAsset.objects.filter(
            date=INITIAL_DATE, portfolio_id=OuterRef("portfolio_id"), asset_id=OuterRef("asset_id")
        ).values("amount")[:1]
        PortfolioAsset.objects.filter(date__gt=INITIAL_DATE).annotate(
            initial_amount=Subquery(subquery)
        ).update(amount=F("initial_amount"))
        logging.info("Portfolio amount updated")

    @classmethod
    def update_value(cls):
        portfolio_assets = (
            PortfolioAsset.objects.all().annotate(
                price=Sum(
                    Case(
                        When(
                            asset__prices__date=F("date"),
                            then=F("asset__prices__value"),
                        ),
                        default=0,
                        output_field=FloatField(),
                    )
                ),
                asset_valuation=ExpressionWrapper(
                    F("amount") * F("price"), output_field=FloatField()
                ),
            )
        ).values("portfolio_id", "date", "asset_valuation")

        portfolio_values_dict = defaultdict(int)
        for portfolio_asset in portfolio_assets:
            portfolio_values_dict[
                (portfolio_asset["portfolio_id"], portfolio_asset["date"])
            ] += portfolio_asset["asset_valuation"]
        portfolio_values = []
        for (portfolio_id, date), value in portfolio_values_dict.items():
            portfolio_values.append(
                PortfolioValue(portfolio_id=portfolio_id, date=date, value=value)
            )

        PortfolioValue.objects.bulk_create(portfolio_values)
        logging.info("Portfolio value updated")

    @classmethod
    def update_weight(cls):
        portfolio_assets = PortfolioAsset.objects.all().annotate(
            price=Sum(
                Case(
                    When(
                        asset__prices__date=F("date"),
                        then=F("asset__prices__value"),
                    ),
                    default=0,
                    output_field=FloatField(),
                )
            ),
            asset_valuation=ExpressionWrapper(F("amount") * F("price"), output_field=FloatField()),
            portfolio_valuation=Subquery(
                PortfolioValue.objects.filter(
                    portfolio_id=OuterRef("portfolio_id"), date=OuterRef("date")
                ).values("value")[:1]
            ),
        )

        for portfolio_asset in portfolio_assets:
            if not portfolio_asset.portfolio_valuation:
                continue
            portfolio_asset.weight = (
                portfolio_asset.asset_valuation / portfolio_asset.portfolio_valuation
            )
            portfolio_asset.save()
        logging.info("Portfolio weight updated")
