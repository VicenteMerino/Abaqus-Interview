from django.urls import include, path

from abaqus.portfolio.apis import (
    PortfolioApi,
    PortfolioValueApi,
    PortfolioWeightApi,
)

portfolio_patterns = [
    path("", PortfolioApi.as_view(), name="portfolio"),
    path("<str:portfolio_id>/value/", PortfolioValueApi.as_view(), name="value"),
    path("<str:portfolio_id>/weight/", PortfolioWeightApi.as_view(), name="weight"),
]

urlpatterns = [
    path("", include((portfolio_patterns, "portfolio"))),
]
