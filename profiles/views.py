from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import StudentProfile, Skill, InterestDomain, StudentSkill, StudentInterest
from .forms import ProfileForm, StudentSearchForm
from teams.models import ConnectionRequest


@login_required
def edit_profile(request):
    profile = get_object_or_404(StudentProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # Handle skills
            skill_names = request.POST.getlist('skill_names[]')
            skill_profs = request.POST.getlist('skill_proficiencies[]')
            skill_exps = request.POST.getlist('skill_experiences[]')
            profile.student_skills.all().delete()
            for name, prof, exp in zip(skill_names, skill_profs, skill_exps):
                if name.strip():
                    skill_obj, _ = Skill.objects.get_or_create(name=name.strip())
                    try:
                        exp_val = float(exp)
                    except (ValueError, TypeError):
                        exp_val = 0.5
                    StudentSkill.objects.create(student=profile, skill=skill_obj, proficiency=prof, years_experience=exp_val)
            # Handle interests
            domain_ids = request.POST.getlist('domain_ids[]')
            profile.interests.all().delete()
            for i, did in enumerate(domain_ids):
                try:
                    domain = InterestDomain.objects.get(id=int(did))
                    StudentInterest.objects.create(student=profile, domain=domain, is_primary=(i == 0))
                except (InterestDomain.DoesNotExist, ValueError):
                    pass
            messages.success(request, "Profile updated successfully!")
            return redirect('profiles:detail', pk=profile.pk)
    else:
        form = ProfileForm(instance=profile)
    skills = profile.student_skills.select_related('skill').all()
    all_domains = InterestDomain.objects.all()
    selected_domains = profile.interests.select_related('domain').all()
    return render(request, 'profiles/edit.html', {
        'form': form, 'profile': profile,
        'skills': skills, 'all_domains': all_domains,
        'selected_domains': selected_domains,
        'proficiency_choices': StudentSkill._meta.get_field('proficiency').choices,
    })


@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(StudentProfile, pk=pk)
    is_own = profile.user == request.user
    # Check connection status
    connection_status = None
    if not is_own:
        try:
            conn = ConnectionRequest.objects.get(
                Q(sender=request.user, recipient=profile.user) |
                Q(sender=profile.user, recipient=request.user)
            )
            connection_status = conn.status
        except ConnectionRequest.DoesNotExist:
            pass
    skills = profile.student_skills.select_related('skill').all()
    interests = profile.interests.select_related('domain').all()
    teams = profile.team_memberships.filter(is_active=True).select_related('team').all()
    return render(request, 'profiles/detail.html', {
        'profile': profile, 'is_own': is_own,
        'skills': skills, 'interests': interests, 'teams': teams,
        'connection_status': connection_status,
    })


@login_required
def student_list(request):
    form = StudentSearchForm(request.GET)
    profiles = StudentProfile.objects.exclude(user=request.user).select_related('user').prefetch_related('student_skills__skill', 'interests__domain')

    if form.is_valid():
        q = form.cleaned_data.get('q')
        skill = form.cleaned_data.get('skill')
        role = form.cleaned_data.get('role')
        year = form.cleaned_data.get('year')
        availability = form.cleaned_data.get('availability')
        domain = form.cleaned_data.get('domain')

        if q:
            profiles = profiles.filter(
                Q(full_name__icontains=q) | Q(college__icontains=q) |
                Q(branch__icontains=q) | Q(bio__icontains=q)
            )
        if skill:
            profiles = profiles.filter(student_skills__skill=skill)
        if role:
            profiles = profiles.filter(preferred_role=role)
        if year:
            profiles = profiles.filter(year=year)
        if availability:
            profiles = profiles.filter(availability=availability)
        if domain:
            profiles = profiles.filter(interests__domain=domain)

    profiles = profiles.distinct()
    return render(request, 'profiles/list.html', {'profiles': profiles, 'form': form})
