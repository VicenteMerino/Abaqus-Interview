import os

from django.db import transaction
from openpyxl import load_workbook
from logging import getLogger
from abaqus.portfolio.models import Asset, Portfolio, PortfolioAsset, AssetPrice
import pandas as pd

logger = getLogger(__name__)


class ETLService:
    """
    This class is responsible for extracting, transforming and loading data from
    excel files into the database.
    """

    def __init__(self, file):
        self.file = file
        self.weights_df = None
        self.prices_worksheet_df = None
        self.assets_dict = {}
        self.portfolios_list = []

    def _is_valid_path(self):
        return os.path.exists(self.file) and (self.file.endswith(".xlsx"))

    def extract(self):
        if not self._is_valid_path():
            raise FileNotFoundError("File not found")
        self.prices_worksheet_df = pd.read_excel(self.file, sheet_name="Precios", header=0)
        self.weights_df = pd.read_excel(self.file, sheet_name="weights", header=0)
        logger.info(f"Extracted data from {self.file}")
        return self

    def transform(self):
        # No need to transform data
        logger.info(f"Weights types are:\n\n {self.weights_df.dtypes}")
        logger.info(f"Prices types are:\n\n {self.prices_worksheet_df.dtypes}")
        logger.info(f"No need to transform data")
        logger.info(self.weights_df.head())
        logger.info(self.prices_worksheet_df.head())
        return self

    def _load_portfolios(self):
        portfolios = []
        for element in self.weights_df.columns[2:]:
            portfolios.append(Portfolio(name=element))
        portfolios_objs = Portfolio.objects.bulk_create(portfolios)
        self.portfolios_list.extend(portfolios_objs)
        for portfolio in portfolios_objs:
            logger.info(f"Created portfolio {portfolio}")

    def _load_assets(self):
        assets = []
        for element in self.weights_df["activos"]:
            assets.append(Asset(name=element))
        assets_objs = Asset.objects.bulk_create(assets)
        for asset in assets_objs:
            logger.info(f"Created asset {asset}")
            self.assets_dict[asset.name] = asset

    def _load_weights(self):
        portfolio_assets = []
        for portfolio in self.portfolios_list:
            for _index, row in self.weights_df.iterrows():
                asset_name = row["activos"]
                weight = row[portfolio.name]
                date = row["Fecha"]
                portfolio_assets.append(
                    PortfolioAsset(
                        portfolio=portfolio,
                        asset=self.assets_dict[asset_name],
                        weight=weight,
                        date=date,
                    )
                )

        portfolio_assets_objs = PortfolioAsset.objects.bulk_create(portfolio_assets)
        for portfolio_asset in portfolio_assets_objs:
            logger.info(
                f"Created portfolio asset {portfolio_asset} with weight {portfolio_asset.weight}"
            )

    def _load_prices(self):
        asset_prices = []
        for _index, row in self.prices_worksheet_df.iterrows():
            for asset in self.assets_dict.values():
                date = row["Dates"]
                price = row[asset.name]
                asset_prices.append(AssetPrice(asset=asset, date=date, value=price))
        asset_prices_objs = AssetPrice.objects.bulk_create(asset_prices)
        for asset_price in asset_prices_objs:
            logger.info(f"Created asset price {asset_price} with value {asset_price.value}")

    def _load_missing_portfolio_assets(self):
        current_portfolio_dates = PortfolioAsset.objects.values_list("date", flat=True).distinct(
            "date"
        )
        missing_portfolio_dates = (
            AssetPrice.objects.exclude(date__in=current_portfolio_dates)
            .values_list("date", flat=True)
            .distinct("date")
        )

        missing_portfolio_assets = []
        for date in missing_portfolio_dates:
            for portfolio in self.portfolios_list:
                for asset in self.assets_dict.values():
                    missing_portfolio_assets.append(
                        PortfolioAsset(portfolio=portfolio, asset=asset, date=date)
                    )
        portfolio_assets_objs = PortfolioAsset.objects.bulk_create(missing_portfolio_assets)
        for portfolio_asset in portfolio_assets_objs:
            logger.info(f"Created portfolio asset for {portfolio_asset}")

    @transaction.atomic
    def load(self):
        if PortfolioAsset.objects.exists():
            logger.warning("Initial data already exists in the database")
        else:
            self._load_portfolios()
            self._load_assets()
            self._load_weights()
            self._load_prices()
            self._load_missing_portfolio_assets()
            logger.info("Finished extracting and loading data")
