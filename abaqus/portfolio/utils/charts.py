import plotly.express as px
from django.http import HttpRequest

from abaqus.portfolio.apis import PortfolioValueApi, PortfolioWeightApi


def generate_line_chart(request):
    portfolio_id = request.GET.get("portfolio")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if portfolio_id and start_date and end_date:
        portfolio_request = HttpRequest()
        portfolio_request.method = "GET"
        portfolio_request.GET = {"fecha_inicio": start_date, "fecha_fin": end_date}
        portfolio_values = PortfolioValueApi.as_view()(portfolio_request, portfolio_id).data
        fig = px.line(portfolio_values, x="date", y="value")
    else:
        fig = px.line()
    fig.update_layout(
        title="Portfolio Value",
        xaxis_title="Date",
        yaxis_title="Value",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    chart = fig.to_html()
    return chart

def generate_stacked_area_chart(request):
    portfolio_id = request.GET.get("portfolio")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if portfolio_id and start_date and end_date:
        portfolio_request = HttpRequest()
        portfolio_request.method = "GET"
        portfolio_request.GET = {"fecha_inicio": start_date, "fecha_fin": end_date}
        portfolio_weights = PortfolioWeightApi.as_view()(portfolio_request, portfolio_id).data
        df = px.data.gapminder()
        fig = px.area(portfolio_weights, x="date", y="weight", color="asset")
    else:
        fig = px.area()
    fig.update_layout(
        title="Portfolio Weights",
        xaxis_title="Date",
        yaxis_title="Weight",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    chart = fig.to_html()
    return chart