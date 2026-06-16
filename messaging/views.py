from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q, Max
from .models import Message, Notification
from .forms import MessageForm
from teams.models import Team, TeamMembership


@login_required
def inbox(request):
    """Show conversation threads (DMs)"""
    user = request.user
    # Get distinct conversation partners
    sent_to = Message.objects.filter(sender=user, team=None).values_list('recipient_id', flat=True).distinct()
    received_from = Message.objects.filter(recipient=user, team=None).values_list('sender_id', flat=True).distinct()
    partner_ids = set(list(sent_to) + list(received_from))

    conversations = []
    for pid in partner_ids:
        partner = User.objects.get(pk=pid)
        last_msg = Message.objects.filter(
            Q(sender=user, recipient=partner) | Q(sender=partner, recipient=user),
            team=None
        ).order_by('-created_at').first()
        unread = Message.objects.filter(sender=partner, recipient=user, is_read=False, team=None).count()
        conversations.append({'partner': partner, 'last_msg': last_msg, 'unread': unread})

    conversations.sort(key=lambda x: x['last_msg'].created_at if x['last_msg'] else 0, reverse=True)
    return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
def conversation(request, user_pk):
    partner = get_object_or_404(User, pk=user_pk)
    user = request.user
    msgs = Message.objects.filter(
        Q(sender=user, recipient=partner) | Q(sender=partner, recipient=user),
        team=None
    ).order_by('created_at')
    # Mark as read
    msgs.filter(sender=partner, is_read=False).update(is_read=True)

    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Message.objects.create(sender=user, recipient=partner, content=form.cleaned_data['content'])
        return redirect('messaging:conversation', user_pk=user_pk)

    return render(request, 'messaging/conversation.html', {'partner': partner, 'messages': msgs, 'form': form})


@login_required
def team_chat(request, team_pk):
    team = get_object_or_404(Team, pk=team_pk)
    if not TeamMembership.objects.filter(team=team, profile__user=request.user, is_active=True).exists():
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("Not a team member.")

    msgs = Message.objects.filter(team=team).select_related('sender').order_by('created_at')

    form = MessageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        Message.objects.create(sender=request.user, team=team, content=form.cleaned_data['content'])
        return redirect('messaging:team_chat', team_pk=team_pk)

    return render(request, 'messaging/team_chat.html', {'team': team, 'messages': msgs, 'form': form})


@login_required
def notifications(request):
    qs = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    # mark unread as read on the full queryset, then slice for display
    qs.filter(is_read=False).update(is_read=True)
    notifs = qs[:50]
    return render(request, 'messaging/notifications.html', {'notifications': notifs})


@login_required
def mark_all_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('messaging:notifications')
