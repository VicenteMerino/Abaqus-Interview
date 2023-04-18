from django.core.management.base import BaseCommand

from styleguide_example.portfolio.services import ETLService


class Command(BaseCommand):
    help = "Seed portfolio data from excel file"

    def add_arguments(self, parser):
        parser.add_argument("file", type=str)

    def handle(self, *args, **options):
        file = options["file"]
        ETLService(file).extract()
