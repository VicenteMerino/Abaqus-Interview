from django.db import models
from styleguide_example.common.models import BaseModel

class Asset(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    
class Portfolio(BaseModel):
    name = models.CharField(max_length=100, unique=True)

class Price(BaseModel):
    asset = models.ForeignKey(Asset,  on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ("asset", "date")

class Weight(BaseModel):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ("portfolio", "asset", "date")

