from django.contrib import admin
from .models import Job,JobApplication,ContactSubmission


admin.site.register(Job)
admin.site.register(JobApplication)
admin.site.register(ContactSubmission)