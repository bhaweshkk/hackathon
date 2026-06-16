from django.contrib import admin
from .models import MatchScore

@admin.register(MatchScore)
class MatchScoreAdmin(admin.ModelAdmin):
    list_display = ['student_a', 'student_b', 'total_score', 'computed_at']
