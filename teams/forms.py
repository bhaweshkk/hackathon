from django import forms
from .models import Team, TeamMembership


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'description', 'max_size', 'domain_focus', 'looking_for_roles', 'is_open']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'looking_for_roles': forms.TextInput(attrs={'placeholder': 'e.g. frontend, ml, uiux'}),
        }


class TeamInviteForm(forms.Form):
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        label='Personal message (optional)'
    )
