from django import forms
from profiles.models import InterestDomain, StudentProfile


class MatchFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search teammates...'}))
    role = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Role')] + list(StudentProfile._meta.get_field('preferred_role').choices)
    )
    domain = forms.ModelChoiceField(queryset=InterestDomain.objects.all(), required=False, empty_label='Any Domain')
    availability = forms.ChoiceField(
        required=False,
        choices=[('', 'Any Availability')] + list(StudentProfile._meta.get_field('availability').choices)
    )
