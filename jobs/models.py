from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Profile


class Job(models.Model):
    EMPLOYMENT_TYPE = (
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('internship', 'Internship'),
    )

    CATEGORY_CHOICES = (
        ('Software Development', 'Software Development'),
        ('Data & Analytics', 'Data & Analytics'),
        ('Design & UI', 'Design & UI'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Customer Support', 'Customer Support'),
    )

    employer = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.employer.username}"


class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    passout_year = models.IntegerField()
    dob = models.DateField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # ✅ new field

    def __str__(self):
        return f"{self.applicant.user.username} → {self.job.title} ({self.status})"
