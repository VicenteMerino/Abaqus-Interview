from django.db import models
from abaqus.common.models import BaseModel


class Asset(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Portfolio(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    assets = models.ManyToManyField(Asset, related_name="portfolios", through="PortfolioAsset")

    def __str__(self):
        return self.name


class PortfolioValue(BaseModel):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="portfolio_values"
    )
    date = models.DateField()
    value = models.FloatField(default=0)

    def __str__(self):
        return f"{self.portfolio.name} - {self.date} - {self.value}"

    class Meta:
        unique_together = ("portfolio", "date")


class PortfolioAsset(BaseModel):
    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="portfolio_assets"
    )
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="portfolio_assets")
    amount = models.FloatField(default=0)
    weight = models.FloatField(default=0)
    date = models.DateField()

    def __str__(self):
        return f"{self.portfolio.name} - {self.asset.name} - {self.date}"

    class Meta:
        unique_together = ("portfolio", "asset", "date")


class AssetPrice(BaseModel):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="prices")
    date = models.DateField()
    value = models.FloatField()

    def __str__(self):
        return f"{self.asset.name} - {self.date}"

    class Meta:
        unique_together = ("asset", "date")
