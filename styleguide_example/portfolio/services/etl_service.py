import os

from django.db import transaction
from openpyxl import load_workbook

from styleguide_example.portfolio.models import Asset, Portfolio, Price, Weight


class ETLService:
    """
    This class is responsible for extracting, transforming and loading data from
    excel files into the database.
    """

    def __init__(self, file):
        self.file = file
        self.workbook = load_workbook(file)
        self.assets = []
        self.weights = []
        self.prices = []

    def _is_valid_path(self):
        return os.path.exists(self.file) and self.file.endswith(".xlsx")

    def _extract_assets(self):
        weights_worksheet = self.workbook["weights"]
        for row in weights_worksheet.iter_rows(min_row=2):
            asset_name = row[1].value
            if asset_name is None:
                continue
            self.assets.append(Asset(name=asset_name))
        Asset.objects.bulk_create(self.assets)

    def _extract_weights(self):
        weights_worksheet = self.workbook["weights"]
        portfolio_1 = Portfolio.objects.get(name="Portfolio 1")
        portfolio_2 = Portfolio.objects.get(name="Portfolio 2")
        for row in weights_worksheet.iter_rows(min_row=2):
            date = row[0].value
            if date is None:
                continue
            asset = Asset.objects.get(name=row[1].value)
            portfolio_1_weight = row[2].value
            portfolio_2_weight = row[3].value
            self.weights.append(
                Weight(
                    date=date,
                    portfolio=portfolio_1,
                    asset=asset,
                    value=portfolio_1_weight,
                )
            )
            self.weights.append(
                Weight(
                    date=date,
                    portfolio=portfolio_2,
                    asset=asset,
                    value=portfolio_2_weight,
                )
            )
        Weight.objects.bulk_create(self.weights)

    def _extract_prices(self):
        prices_worksheet = self.workbook["Precios"]
        assets = []

        for cell in prices_worksheet[1][1:]:
            if cell.value is None:
                continue
            assets.append(Asset.objects.get(name=cell.value))
        for row in prices_worksheet.iter_rows(min_row=2):
            if row[0].value is None:
                continue
            date = row[0].value
            for i, cell in enumerate(row[1:]):
                self.prices.append(
                    Price(
                        date=date,
                        asset=assets[i],
                        value=cell.value,
                    )
                )
        Price.objects.bulk_create(self.prices)

    @transaction.atomic
    def extract(self):
        if not self._is_valid_path():
            raise FileNotFoundError("File not found")
        
        self._extract_assets()
        self._extract_weights()
        self._extract_prices()
