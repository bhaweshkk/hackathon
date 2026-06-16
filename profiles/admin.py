from django.contrib import admin
from .models import StudentProfile, Skill, InterestDomain, StudentSkill, StudentInterest


class StudentSkillInline(admin.TabularInline):
    model = StudentSkill
    extra = 1


class StudentInterestInline(admin.TabularInline):
    model = StudentInterest
    extra = 1


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'college', 'branch', 'year', 'preferred_role', 'availability', 'hackathons_participated']
    list_filter = ['year', 'preferred_role', 'availability', 'college']
    search_fields = ['full_name', 'college', 'branch', 'user__email']
    inlines = [StudentSkillInline, StudentInterestInline]
    list_per_page = 25


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']


@admin.register(InterestDomain)
class InterestDomainAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
