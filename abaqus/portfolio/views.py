import plotly.express as px
from django.shortcuts import render

from abaqus.portfolio.models import Portfolio, PortfolioValue
from abaqus.portfolio.forms import DateAndPortfolioForm


def line_chart(request):
    portfolio_id = request.GET.get("portfolio")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    if portfolio_id:
        portfolio_values = (
            PortfolioValue.objects.filter(portfolio=portfolio_id)
            .order_by("date")
            .values("date", "value")
        )
        if start_date:
            portfolio_values = portfolio_values.filter(date__gte=start_date)
        if end_date:
            portfolio_values = portfolio_values.filter(date__lte=end_date)

        if portfolio_values.count() == 0:
            fig = px.line()
        else:
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
    return render(
        request, "line_chart.html", context={"chart": chart, "form": DateAndPortfolioForm()}
    )
