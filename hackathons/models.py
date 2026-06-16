from django.db import models
from django.contrib.auth.models import User
from teams.models import Team
from profiles.models import DOMAIN_CHOICES


MODE_CHOICES = [('online', 'Online'), ('offline', 'Offline'), ('hybrid', 'Hybrid')]
STATUS_CHOICES = [('upcoming', 'Upcoming'), ('ongoing', 'Ongoing'), ('ended', 'Ended')]
APP_STATUS_CHOICES = [
    ('applied', 'Applied'), ('shortlisted', 'Shortlisted'),
    ('rejected', 'Rejected'), ('winner', 'Winner'), ('participant', 'Participant'),
]


class Hackathon(models.Model):
    title = models.CharField(max_length=300)
    organizer = models.CharField(max_length=200)
    description = models.TextField()
    domain = models.CharField(max_length=50, choices=DOMAIN_CHOICES, blank=True)
    mode = models.CharField(max_length=10, choices=MODE_CHOICES, default='online')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    start_date = models.DateField()
    end_date = models.DateField()
    registration_deadline = models.DateField()
    min_team_size = models.IntegerField(default=2)
    max_team_size = models.IntegerField(default=5)
    eligibility = models.CharField(max_length=300, blank=True)
    prize_pool = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    image = models.ImageField(upload_to='hackathons/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    class Meta:
        ordering = ['registration_deadline']


class HackathonApplication(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='applications')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='applications')
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APP_STATUS_CHOICES, default='applied')
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('hackathon', 'team')

    def __str__(self):
        return f"{self.team.name} → {self.hackathon.title}"


class HackathonBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hackathon')
