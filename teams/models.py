from django.db import models
from django.contrib.auth.models import User
from profiles.models import StudentProfile, ROLE_CHOICES, DOMAIN_CHOICES


TEAM_STATUS_CHOICES = [
    ('forming', 'Forming'), ('active', 'Active'),
    ('completed', 'Completed'), ('disbanded', 'Disbanded'),
]

MEMBERSHIP_ROLE_CHOICES = [
    ('leader', 'Team Leader'), ('member', 'Member'), ('mentor', 'Mentor'),
]

INVITE_STATUS_CHOICES = [
    ('pending', 'Pending'), ('accepted', 'Accepted'),
    ('rejected', 'Rejected'), ('cancelled', 'Cancelled'),
]


class Team(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name='led_teams')
    max_size = models.IntegerField(default=4)
    status = models.CharField(max_length=20, choices=TEAM_STATUS_CHOICES, default='forming')
    is_open = models.BooleanField(default=True)
    domain_focus = models.CharField(max_length=50, choices=DOMAIN_CHOICES, blank=True)
    looking_for_roles = models.CharField(max_length=500, blank=True, help_text="Comma-separated roles needed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def member_count(self):
        return self.memberships.filter(is_active=True).count()

    @property
    def is_full(self):
        return self.member_count >= self.max_size

    def get_member_roles(self):
        return [m.profile.preferred_role for m in self.memberships.filter(is_active=True).select_related('profile')]


class TeamMembership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='memberships')
    profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='team_memberships')
    role_in_team = models.CharField(max_length=50, choices=ROLE_CHOICES, blank=True)
    team_role = models.CharField(max_length=20, choices=MEMBERSHIP_ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('team', 'profile')

    def __str__(self):
        return f"{self.profile.full_name} in {self.team.name}"


class TeamInvite(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invites')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invites')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invites')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=INVITE_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Invite: {self.sender.username} → {self.recipient.username} for {self.team.name}"


class ConnectionRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_connections')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_connections')
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=INVITE_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'recipient')

    def __str__(self):
        return f"{self.sender.username} → {self.recipient.username}"
