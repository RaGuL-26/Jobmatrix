from django import forms
from .models import Job,JobApplication

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company_name', 'salary','location','employment_type', 'experience','skills_required', 'job_type']
 
 
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['resume']