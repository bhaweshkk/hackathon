from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Hackathon, HackathonApplication, HackathonBookmark
from .forms import HackathonForm, HackathonFilterForm
from teams.models import Team, TeamMembership
from profiles.models import StudentProfile
from messaging.models import Notification


def hackathon_list(request):
    form = HackathonFilterForm(request.GET)
    hackathons = Hackathon.objects.all().order_by('registration_deadline')
    if form.is_valid():
        q = form.cleaned_data.get('q')
        domain = form.cleaned_data.get('domain')
        mode = form.cleaned_data.get('mode')
        status = form.cleaned_data.get('status')
        if q:
            hackathons = hackathons.filter(Q(title__icontains=q) | Q(organizer__icontains=q))
        if domain:
            hackathons = hackathons.filter(domain=domain)
        if mode:
            hackathons = hackathons.filter(mode=mode)
        if status:
            hackathons = hackathons.filter(status=status)

    bookmarked_ids = set()
    applied_hackathon_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(HackathonBookmark.objects.filter(user=request.user).values_list('hackathon_id', flat=True))
        applied_hackathon_ids = set(
            HackathonApplication.objects.filter(team__leader=request.user)
            .values_list('hackathon_id', flat=True)
        )
    return render(request, 'hackathons/list.html', {
        'hackathons': hackathons, 'form': form,
        'bookmarked_ids': bookmarked_ids,
        'applied_hackathon_ids': applied_hackathon_ids,
    })


def hackathon_detail(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    is_bookmarked = False
    user_teams = []
    applied_team = None
    if request.user.is_authenticated:
        is_bookmarked = HackathonBookmark.objects.filter(user=request.user, hackathon=hackathon).exists()
        user_teams = Team.objects.filter(leader=request.user, is_open=True)
        try:
            applied_team = HackathonApplication.objects.get(hackathon=hackathon, team__leader=request.user)
        except HackathonApplication.DoesNotExist:
            pass
    return render(request, 'hackathons/detail.html', {
        'hackathon': hackathon, 'is_bookmarked': is_bookmarked,
        'user_teams': user_teams, 'applied_team': applied_team,
    })


@login_required
def apply_hackathon(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    team_id = request.POST.get('team_id')
    if not team_id:
        messages.error(request, "Select a team to apply.")
        return redirect('hackathons:detail', pk=pk)
    team = get_object_or_404(Team, pk=team_id, leader=request.user)
    app, created = HackathonApplication.objects.get_or_create(
        hackathon=hackathon, team=team,
        defaults={'applied_by': request.user, 'status': 'applied'}
    )
    if created:
        # Update participation stats for all team members
        for membership in team.memberships.filter(is_active=True):
            p = membership.profile
            p.hackathons_participated = HackathonApplication.objects.filter(
                team__memberships__profile=p, team__memberships__is_active=True
            ).values('hackathon').distinct().count()
            p.save()
        messages.success(request, f"Applied to {hackathon.title} with team {team.name}!")
    else:
        messages.info(request, "Already applied.")
    return redirect('hackathons:detail', pk=pk)


@login_required
def toggle_bookmark(request, pk):
    hackathon = get_object_or_404(Hackathon, pk=pk)
    bm, created = HackathonBookmark.objects.get_or_create(user=request.user, hackathon=hackathon)
    if not created:
        bm.delete()
        messages.info(request, "Bookmark removed.")
    else:
        messages.success(request, "Hackathon bookmarked!")
    return redirect(request.META.get('HTTP_REFERER', 'hackathons:list'))


@login_required
def hackathon_create(request):
    if not request.user.is_staff:
        messages.error(request, "Only admins can add hackathons.")
        return redirect('hackathons:list')
    if request.method == 'POST':
        form = HackathonForm(request.POST, request.FILES)
        if form.is_valid():
            h = form.save(commit=False)
            h.created_by = request.user
            h.save()
            messages.success(request, "Hackathon added!")
            return redirect('hackathons:detail', pk=h.pk)
    else:
        form = HackathonForm()
    return render(request, 'hackathons/create.html', {'form': form})
