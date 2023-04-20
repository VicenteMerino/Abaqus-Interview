from django.shortcuts import render

from abaqus.portfolio.forms import DateAndPortfolioForm
from abaqus.portfolio.utils.charts import (
    generate_line_chart,
    generate_stacked_area_chart,
)


def graphs(request):
    line_chart = generate_line_chart(request)
    stacked_area_chart = generate_stacked_area_chart(request)
    context = {"line_chart": line_chart, "form": DateAndPortfolioForm(
        initial={"start_date": "2022-02-15", "end_date": "2022-02-16"}
    ), "stacked_area_chart": stacked_area_chart}
    return render(
        request, "graphs.html", context=context
    )
