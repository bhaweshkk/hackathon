from django.contrib import admin
from .models import ParticipationRecord

@admin.register(ParticipationRecord)
class ParticipationRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'event_type', 'description', 'created_at']
    list_filter = ['event_type']
