from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils import timezone
from .models import Team, TeamMembership, TeamInvite, ConnectionRequest
from .forms import TeamForm, TeamInviteForm
from profiles.models import StudentProfile
from messaging.models import Notification


def _notify(recipient, sender, notif_type, title, msg, link=''):
    Notification.objects.create(
        recipient=recipient, sender=sender,
        notification_type=notif_type, title=title, message=msg, link=link
    )


@login_required
def team_list(request):
    teams = Team.objects.filter(is_open=True).prefetch_related('memberships').order_by('-created_at')
    domain = request.GET.get('domain', '')
    if domain:
        teams = teams.filter(domain_focus=domain)
    my_teams = Team.objects.filter(memberships__profile__user=request.user, memberships__is_active=True)
    return render(request, 'teams/list.html', {'teams': teams, 'my_teams': my_teams, 'selected_domain': domain})


@login_required
def team_create(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.leader = request.user
            team.save()
            profile = get_object_or_404(StudentProfile, user=request.user)
            TeamMembership.objects.create(
                team=team, profile=profile,
                role_in_team=profile.preferred_role, team_role='leader'
            )
            profile.teams_participated = profile.team_memberships.filter(is_active=True).count()
            profile.save()
            messages.success(request, f"Team '{team.name}' created!")
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamForm()
    return render(request, 'teams/create.html', {'form': form})


@login_required
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    memberships = team.memberships.filter(is_active=True).select_related('profile__user')
    is_member = memberships.filter(profile__user=request.user).exists()
    is_leader = team.leader == request.user
    pending_invites = TeamInvite.objects.filter(team=team, status='pending') if is_leader else []
    applications = team.applications.select_related('hackathon').all()
    return render(request, 'teams/detail.html', {
        'team': team, 'memberships': memberships,
        'is_member': is_member, 'is_leader': is_leader,
        'pending_invites': pending_invites, 'applications': applications,
    })


@login_required
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk, leader=request.user)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            messages.success(request, "Team updated!")
            return redirect('teams:detail', pk=team.pk)
    else:
        form = TeamForm(instance=team)
    return render(request, 'teams/edit.html', {'form': form, 'team': team})


@login_required
def invite_member(request, team_pk, user_pk):
    team = get_object_or_404(Team, pk=team_pk, leader=request.user)
    recipient = get_object_or_404(User, pk=user_pk)
    if TeamMembership.objects.filter(team=team, profile__user=recipient, is_active=True).exists():
        messages.warning(request, "This student is already in your team.")
        return redirect('teams:detail', pk=team_pk)
    invite, created = TeamInvite.objects.get_or_create(
        team=team, sender=request.user, recipient=recipient,
        defaults={'status': 'pending'}
    )
    if created:
        _notify(recipient, request.user, 'invite',
                f"Team Invite: {team.name}",
                f"{request.user.username} invited you to join {team.name}",
                f"/teams/{team_pk}/")
        messages.success(request, f"Invite sent to {recipient.username}!")
    else:
        messages.info(request, "Invite already sent.")
    return redirect(request.META.get('HTTP_REFERER', 'teams:detail'))


@login_required
def respond_invite(request, invite_pk, action):
    invite = get_object_or_404(TeamInvite, pk=invite_pk, recipient=request.user, status='pending')
    if action == 'accept':
        invite.status = 'accepted'
        invite.responded_at = timezone.now()
        invite.save()
        profile = get_object_or_404(StudentProfile, user=request.user)
        if not TeamMembership.objects.filter(team=invite.team, profile=profile).exists():
            TeamMembership.objects.create(
                team=invite.team, profile=profile,
                role_in_team=profile.preferred_role, team_role='member'
            )
            profile.teams_participated = profile.team_memberships.filter(is_active=True).count()
            profile.save()
        _notify(invite.sender, request.user, 'invite',
                f"{request.user.username} accepted your invite",
                f"{request.user.username} joined {invite.team.name}", f"/teams/{invite.team.pk}/")
        messages.success(request, f"You joined {invite.team.name}!")
    else:
        invite.status = 'rejected'
        invite.responded_at = timezone.now()
        invite.save()
        messages.info(request, "Invite declined.")
    return redirect('teams:my_invites')


@login_required
def my_invites(request):
    invites = TeamInvite.objects.filter(recipient=request.user, status='pending').select_related('team', 'sender')
    return render(request, 'teams/invites.html', {'invites': invites})


@login_required
def leave_team(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if team.leader == request.user:
        messages.error(request, "Team leader cannot leave. Transfer leadership or disband the team.")
        return redirect('teams:detail', pk=pk)
    membership = get_object_or_404(TeamMembership, team=team, profile__user=request.user, is_active=True)
    membership.is_active = False
    membership.save()
    profile = get_object_or_404(StudentProfile, user=request.user)
    profile.teams_participated = profile.team_memberships.filter(is_active=True).count()
    profile.save()
    messages.success(request, f"You left {team.name}.")
    return redirect('teams:list')


@login_required
def send_connection(request, user_pk):
    recipient = get_object_or_404(User, pk=user_pk)
    if recipient == request.user:
        messages.error(request, "You can't connect with yourself.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    conn, created = ConnectionRequest.objects.get_or_create(
        sender=request.user, recipient=recipient,
        defaults={'status': 'pending'}
    )
    if created:
        _notify(recipient, request.user, 'connection',
                "New Connection Request",
                f"{request.user.username} wants to connect with you.",
                f"/profiles/{recipient.profile.pk}/")
        messages.success(request, "Connection request sent!")
    else:
        messages.info(request, "Request already sent.")
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def respond_connection(request, conn_pk, action):
    conn = get_object_or_404(ConnectionRequest, pk=conn_pk, recipient=request.user, status='pending')
    conn.status = 'accepted' if action == 'accept' else 'rejected'
    conn.save()
    if action == 'accept':
        messages.success(request, f"Connected with {conn.sender.username}!")
    return redirect(request.META.get('HTTP_REFERER', '/'))
