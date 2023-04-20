from django import forms
from abaqus.portfolio.models import Portfolio


class DateAndPortfolioForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    portfolio = forms.ModelChoiceField(
        queryset=Portfolio.objects.all(),
        to_field_name="id",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
