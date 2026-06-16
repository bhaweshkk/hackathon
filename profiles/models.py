from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


YEAR_CHOICES = [
    ('1', '1st Year'), ('2', '2nd Year'), ('3', '3rd Year'),
    ('4', '4th Year'), ('5', '5th Year / PG'),
]

ROLE_CHOICES = [
    ('frontend', 'Frontend Developer'), ('backend', 'Backend Developer'),
    ('fullstack', 'Full Stack Developer'), ('ml', 'AI/ML Engineer'),
    ('uiux', 'UI/UX Designer'), ('mobile', 'Mobile Developer'),
    ('blockchain', 'Blockchain Developer'), ('devops', 'DevOps Engineer'),
    ('cybersecurity', 'Cybersecurity Expert'), ('data', 'Data Analyst'),
    ('presenter', 'Presenter / Business Analyst'), ('other', 'Other'),
]

DOMAIN_CHOICES = [
    ('ai', 'Artificial Intelligence'), ('web', 'Web Development'),
    ('mobile', 'Mobile Apps'), ('cybersecurity', 'Cybersecurity'),
    ('healthtech', 'HealthTech'), ('agritech', 'AgriTech'),
    ('fintech', 'FinTech'), ('edtech', 'EdTech'), ('iot', 'IoT'),
    ('blockchain', 'Blockchain'), ('data', 'Data Science'),
    ('gaming', 'Gaming'), ('ar_vr', 'AR/VR'), ('sustainability', 'Sustainability'),
    ('social', 'Social Impact'), ('other', 'Other'),
]

PROFICIENCY_CHOICES = [
    ('beginner', 'Beginner'), ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'), ('expert', 'Expert'),
]

AVAILABILITY_CHOICES = [
    ('available', 'Available for Teams'), ('busy', 'Currently Busy'),
    ('open', 'Open to Opportunities'), ('not_available', 'Not Available'),
]


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, blank=True)
    icon = models.CharField(max_length=50, blank=True, default='code')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class InterestDomain(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, default='globe')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200)
    college = models.CharField(max_length=200)
    branch = models.CharField(max_length=200)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    phone = models.CharField(max_length=15, blank=True)
    github = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    resume_link = models.URLField(blank=True)
    bio = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    preferred_role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='backend')
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')
    preferred_team_size = models.IntegerField(default=4)
    achievements = models.TextField(blank=True)
    languages_known = models.CharField(max_length=300, blank=True, help_text="Comma-separated list")
    # Stats
    hackathons_participated = models.IntegerField(default=0)
    teams_participated = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    shortlisted = models.IntegerField(default=0)
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.college}"

    def get_absolute_url(self):
        return reverse('profiles:detail', kwargs={'pk': self.pk})

    @property
    def skill_list(self):
        return self.student_skills.select_related('skill').all()

    @property
    def domain_list(self):
        return self.interests.select_related('domain').all()

    @property
    def completion_percentage(self):
        fields = [self.full_name, self.college, self.branch, self.phone,
                  self.github, self.linkedin, self.bio, self.achievements]
        filled = sum(1 for f in fields if f)
        has_skills = self.student_skills.exists()
        has_domains = self.interests.exists()
        total = len(fields) + 2
        score = (filled + has_skills + has_domains) / total * 100
        return int(score)


class StudentSkill(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='student_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='intermediate')
    years_experience = models.FloatField(default=0.5)

    class Meta:
        unique_together = ('student', 'skill')

    def __str__(self):
        return f"{self.student.full_name} - {self.skill.name} ({self.proficiency})"


class StudentInterest(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='interests')
    domain = models.ForeignKey(InterestDomain, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'domain')

    def __str__(self):
        return f"{self.student.full_name} - {self.domain.name}"
