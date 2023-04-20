from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from abaqus.portfolio.models import Portfolio, PortfolioValue, PortfolioAsset


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
        fecha_inicio = serializers.DateField(required=False)
        fecha_fin = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = PortfolioValue
            fields = ("value", "date")

    def get(self, request, portfolio_id):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        portfolio_values_data = self.OutputSerializer(
            portfolio.portfolio_values.filter(
                date__gte=filters_serializer.validated_data["fecha_inicio"],
                date__lte=filters_serializer.validated_data["fecha_fin"],
            ).order_by("date"),
            many=True,
        ).data
        return Response(portfolio_values_data)


class PortfolioWeightApi(APIView):
    class FilterSerializer(serializers.Serializer):
        fecha_inicio = serializers.DateField(required=False)
        fecha_fin = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        asset = serializers.CharField(source="asset.name")

        class Meta:
            model = PortfolioAsset
            fields = ("asset", "weight", "date")

    def get(self, request, portfolio_id):
        portfolio = Portfolio.objects.get(id=portfolio_id)
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        portfolio_assets_data = self.OutputSerializer(
            portfolio.portfolio_assets.filter(
                date__gte=filters_serializer.validated_data["fecha_inicio"],
                date__lte=filters_serializer.validated_data["fecha_fin"],
            ).order_by("date"),
            many=True,
        ).data
        return Response(portfolio_assets_data)
