from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError


User = get_user_model()

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Internship', 'Internship'),
    ]
    EMPLOYMENT_TYPE = [
        ('Onsite', 'Onsite'),
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=100, choices=EMPLOYMENT_TYPE)
    skills_required = models.TextField()
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    salary = models.IntegerField()
    experience = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Job.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def posted_by(self):
        return self.user.username


class JobApplication(models.Model):
    APPLICANT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Hold', 'Hold'),
        ('Accepted', 'Accepted'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.applicant.username}'s application for {self.job.title}"
    

class ContactSubmission(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"