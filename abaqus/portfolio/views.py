from collections import Counter

import plotly.express as px
from django.shortcuts import render

from abaqus.portfolio.models import Portfolio, PortfolioValue


def line_chart(request):
    portfolio_1 = Portfolio.objects.first()
    portfolio_values = (
        PortfolioValue.objects.filter(portfolio=portfolio_1)
        .order_by("date")
        .values("date", "value")
    )

    fig = px.line(portfolio_values, x="date", y="value")
    fig.update_layout(
        title="Portfolio Value",
        xaxis_title="Date",
        yaxis_title="Value",
        font=dict(family="Courier New, monospace", size=18, color="#7f7f7f"),
    )
    chart = fig.to_html(full_html=False, default_height=500, default_width=700)
    return render(request, "line_chart.html", context={"chart": chart})
