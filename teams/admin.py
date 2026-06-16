from django.contrib import admin
from .models import Team, TeamMembership, TeamInvite, ConnectionRequest


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'leader', 'member_count', 'status', 'is_open', 'domain_focus', 'created_at']
    list_filter = ['status', 'is_open', 'domain_focus']
    search_fields = ['name', 'leader__username']
    inlines = [TeamMembershipInline]


@admin.register(TeamInvite)
class TeamInviteAdmin(admin.ModelAdmin):
    list_display = ['team', 'sender', 'recipient', 'status', 'created_at']
    list_filter = ['status']


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'status', 'created_at']
