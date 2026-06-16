from django import forms
from .models import Hackathon, HackathonApplication


class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = [
            'title', 'organizer', 'description', 'domain', 'mode',
            'start_date', 'end_date', 'registration_deadline',
            'min_team_size', 'max_team_size', 'eligibility',
            'prize_pool', 'website', 'tags', 'is_featured',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'registration_deadline': forms.DateInput(attrs={'type': 'date'}),
        }


class HackathonFilterForm(forms.Form):
    q = forms.CharField(required=False, label='Search')
    domain = forms.ChoiceField(required=False, choices=[])
    mode = forms.ChoiceField(required=False, choices=[
        ('', 'All Modes'), ('online', 'Online'), ('offline', 'Offline'), ('hybrid', 'Hybrid')
    ])
    status = forms.ChoiceField(required=False, choices=[
        ('', 'All'), ('upcoming', 'Upcoming'), ('ongoing', 'Ongoing')
    ])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from profiles.models import DOMAIN_CHOICES
        self.fields['domain'].choices = [('', 'All Domains')] + list(DOMAIN_CHOICES)
