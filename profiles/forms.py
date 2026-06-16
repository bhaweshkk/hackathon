from django import forms
from .models import StudentProfile, StudentSkill, StudentInterest, Skill, InterestDomain


class ProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name', 'college', 'branch', 'year', 'phone',
            'github', 'linkedin', 'resume_link', 'bio', 'avatar',
            'preferred_role', 'availability', 'preferred_team_size',
            'achievements', 'languages_known',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'achievements': forms.Textarea(attrs={'rows': 3}),
        }


class SkillForm(forms.ModelForm):
    skill_name = forms.CharField(max_length=100, label='Skill Name')

    class Meta:
        model = StudentSkill
        fields = ['proficiency', 'years_experience']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['skill_name'].initial = self.instance.skill.name


class StudentSearchForm(forms.Form):
    q = forms.CharField(required=False, label='Search', widget=forms.TextInput(attrs={'placeholder': 'Search students...'}))
    skill = forms.ModelChoiceField(queryset=Skill.objects.all(), required=False, empty_label='All Skills')
    role = forms.ChoiceField(choices=[('', 'All Roles')] + StudentProfile._meta.get_field('preferred_role').choices, required=False)
    year = forms.ChoiceField(choices=[('', 'All Years')] + StudentProfile._meta.get_field('year').choices, required=False)
    availability = forms.ChoiceField(choices=[('', 'All')] + StudentProfile._meta.get_field('availability').choices, required=False)
    domain = forms.ModelChoiceField(queryset=InterestDomain.objects.all(), required=False, empty_label='All Domains')
