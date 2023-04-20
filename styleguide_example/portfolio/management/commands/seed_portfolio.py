from django.core.management.base import BaseCommand

from styleguide_example.portfolio.services import (
    ETLService,
    PortfolioUpdateService,
    initial_portfolio_amount_update,
)


class Command(BaseCommand):
    help = "Seed portfolio data from excel file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        file = options["file"]
        ETLService(file).extract()
        initial_portfolio_amount_update()
        PortfolioUpdateService.update_amount()
        PortfolioUpdateService.update_value()
        PortfolioUpdateService.update_weight()
