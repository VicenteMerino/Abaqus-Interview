from django.urls import include, path

from styleguide_example.portfolio.apis import (
    PortfolioApi,
    PortfolioValueApi,
)

portfolio_patterns = [
    path("", PortfolioApi.as_view(), name="portfolio"),
    path("<str:portfolio_id>/value/", PortfolioValueApi.as_view(), name="value"),
]

urlpatterns = [
    path("", include((portfolio_patterns, "portfolio"))),
]
