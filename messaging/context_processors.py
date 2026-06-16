from .models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        return {'unread_notification_count': count}
    return {'unread_notification_count': 0}


def pending_invites(request):
    if request.user.is_authenticated:
        from teams.models import TeamInvite
        count = TeamInvite.objects.filter(recipient=request.user, status='pending').count()
        return {'pending_invite_count': count}
    return {'pending_invite_count': 0}
