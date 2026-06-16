from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import StudentProfile
from .engine import compute_match_score, get_team_recommendations, get_skill_gaps
from .forms import MatchFilterForm


@login_required
def recommendations(request):
    try:
        my_profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('profiles:edit')

    form = MatchFilterForm(request.GET)
    all_profiles = (
        StudentProfile.objects
        .exclude(user=request.user)
        .filter(availability__in=['available', 'open'])
        .prefetch_related('student_skills__skill', 'interests__domain')
    )

    if form.is_valid():
        if form.cleaned_data.get('q'):
            q = form.cleaned_data['q']
            all_profiles = all_profiles.filter(
                full_name__icontains=q
            )
        if form.cleaned_data.get('role'):
            all_profiles = all_profiles.filter(preferred_role=form.cleaned_data['role'])
        if form.cleaned_data.get('domain'):
            all_profiles = all_profiles.filter(interests__domain=form.cleaned_data['domain'])
        if form.cleaned_data.get('availability'):
            all_profiles = all_profiles.filter(availability=form.cleaned_data['availability'])

    scored = []
    for p in all_profiles:
        result = compute_match_score(my_profile, p)
        scored.append((p, result))
    scored.sort(key=lambda x: x[1]['total'], reverse=True)
    top_matches = scored[:12]

    skill_gaps = get_skill_gaps(my_profile)
    team_suggestion = get_team_recommendations(my_profile, all_profiles)

    return render(request, 'matching/recommendations.html', {
        'my_profile': my_profile,
        'top_matches': top_matches,
        'skill_gaps': skill_gaps,
        'team_suggestion': team_suggestion,
        'form': form,
    })


@login_required
def match_detail(request, profile_pk):
    my_profile = get_object_or_404(StudentProfile, user=request.user)
    other_profile = get_object_or_404(StudentProfile, pk=profile_pk)
    result = compute_match_score(my_profile, other_profile)
    score_breakdown = [
        ('Skill Complementarity', result['skill_score'], 30),
        ('Domain Overlap',        result['domain_score'], 20),
        ('Role Balance',          result['role_score'],   20),
        ('Experience',            result['experience_score'], 10),
        ('Availability',          result['availability_score'], 10),
        ('Collaboration Fit',     result['collab_score'],  10),
    ]
    return render(request, 'matching/match_detail.html', {
        'my_profile': my_profile,
        'other_profile': other_profile,
        'result': result,
        'score_breakdown': score_breakdown,
    })
