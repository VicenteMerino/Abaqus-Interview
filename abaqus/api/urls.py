from django.urls import include, path

urlpatterns = [
    path("portfolio/", include(("abaqus.portfolio.urls", "portfolio"))),
]
