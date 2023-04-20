from django import forms
from abaqus.portfolio.models import Portfolio


class DateAndPortfolioForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    end_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}), required=False)
    portfolio = forms.ModelChoiceField(
        queryset=Portfolio.objects.all(),
        required=False,
        to_field_name="id",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
