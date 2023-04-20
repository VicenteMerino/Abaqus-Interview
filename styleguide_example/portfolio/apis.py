from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from styleguide_example.portfolio.models import Portfolio, PortfolioValue


class PortfolioApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Portfolio
            fields = ("id", "name")

    def get(self, request):
        portfolios = Portfolio.objects.all()
        portfolios_data = self.OutputSerializer(portfolios, many=True).data
        return Response(portfolios_data)


class PortfolioValueApi(APIView):
    class FilterSerializer(serializers.Serializer):
        begin_date = serializers.DateField(required=False)
        end_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PortfolioValue
            fields = ("value", "date")

    def get(self, request, portfolio_id):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        portfolio_values_data = self.OutputSerializer(
            portfolio.portfolio_values.order_by("date"), many=True
        ).data
        return Response(portfolio_values_data)
