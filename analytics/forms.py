from django import forms
from profiles.models import InterestDomain, StudentProfile


class DashboardFilterForm(forms.Form):
    from_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    to_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    domain = forms.ModelChoiceField(queryset=InterestDomain.objects.all(), required=False, empty_label='All Domains')
    year = forms.ChoiceField(
        choices=[('', 'All Years')] + list(StudentProfile._meta.get_field('year').choices),
        required=False
    )
