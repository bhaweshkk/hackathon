from django.db import models
from profiles.models import StudentProfile


class MatchScore(models.Model):
    student_a = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='match_as_a')
    student_b = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='match_as_b')
    total_score = models.FloatField(default=0)
    skill_score = models.FloatField(default=0)
    domain_score = models.FloatField(default=0)
    role_score = models.FloatField(default=0)
    experience_score = models.FloatField(default=0)
    availability_score = models.FloatField(default=0)
    match_reason = models.TextField(blank=True)
    computed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student_a', 'student_b')

    def __str__(self):
        return f"{self.student_a} ↔ {self.student_b}: {self.total_score:.1f}"
