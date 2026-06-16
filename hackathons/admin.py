from django.contrib import admin
from .models import Hackathon, HackathonApplication, HackathonBookmark


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'mode', 'status', 'domain', 'registration_deadline', 'is_featured']
    list_filter = ['status', 'mode', 'domain', 'is_featured']
    search_fields = ['title', 'organizer']
    list_editable = ['is_featured', 'status']


@admin.register(HackathonApplication)
class HackathonApplicationAdmin(admin.ModelAdmin):
    list_display = ['team', 'hackathon', 'status', 'applied_at']
    list_filter = ['status']
