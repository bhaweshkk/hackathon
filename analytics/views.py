from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from profiles.models import StudentProfile
from teams.models import Team, TeamMembership
from hackathons.models import Hackathon, HackathonApplication
from messaging.models import Notification
from teams.models import TeamInvite
import json


def landing(request):
    if request.user.is_authenticated:
        return redirect('analytics:dashboard')

    student_count = StudentProfile.objects.count()
    team_count = Team.objects.count()
    hackathon_count = Hackathon.objects.count()
    featured_hackathon = Hackathon.objects.filter(status__in=['upcoming', 'ongoing']).order_by('-is_featured', 'registration_deadline').first()

    return render(request, 'landing.html', {
        'student_count': student_count,
        'team_count': team_count,
        'hackathon_count': hackathon_count,
        'featured_hackathon': featured_hackathon,
    })


@login_required
def dashboard(request):
    try:
        profile = StudentProfile.objects.get(user=request.user)
    except StudentProfile.DoesNotExist:
        return redirect('profiles:edit')

    # Stats
    my_teams = TeamMembership.objects.filter(profile=profile, is_active=True).select_related('team')
    my_applications = HackathonApplication.objects.filter(
        team__memberships__profile=profile, team__memberships__is_active=True
    ).select_related('hackathon', 'team').distinct()

    active_teams = my_teams.filter(team__status__in=['forming', 'active'])
    recent_hackathons = Hackathon.objects.filter(status__in=['upcoming', 'ongoing']).order_by('registration_deadline')[:4]
    pending_invites = TeamInvite.objects.filter(recipient=request.user, status='pending').count()
    recent_notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:5]

    # Skill chart data
    skill_data = [
        {'skill': ss.skill.name, 'level': {'beginner': 25, 'intermediate': 50, 'advanced': 75, 'expert': 100}.get(ss.proficiency, 50)}
        for ss in profile.student_skills.select_related('skill').all()[:8]
    ]

    # Application status breakdown
    app_stats = {
        'applied': my_applications.filter(status='applied').count(),
        'shortlisted': my_applications.filter(status='shortlisted').count(),
        'winner': my_applications.filter(status='winner').count(),
        'rejected': my_applications.filter(status='rejected').count(),
    }

    return render(request, 'analytics/dashboard.html', {
        'profile': profile,
        'my_teams': my_teams,
        'active_teams': active_teams,
        'my_applications': my_applications[:5],
        'recent_hackathons': recent_hackathons,
        'pending_invites': pending_invites,
        'recent_notifications': recent_notifications,
        'skill_data_json': json.dumps(skill_data),
        'app_stats': app_stats,
        'total_teams': my_teams.count(),
        'total_hackathons': my_applications.count(),
    })


@login_required
def leaderboard(request):
    profiles = StudentProfile.objects.annotate(
        total_teams=Count('team_memberships', distinct=True),
    ).order_by('-hackathons_participated', '-wins', '-teams_participated')[:20]
    return render(request, 'analytics/leaderboard.html', {'profiles': profiles})
