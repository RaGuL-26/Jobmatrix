from .models import *
from django import forms
    

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    dob = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = User
        
        fields =['username','email','password', 'number', 'dob', 'user_type']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','password']
    
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'field_of_study','percentage', 'started_year', 'ended_year']
        widgets = {
            'started_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2100'}),
            'ended_year': forms.NumberInput(attrs={'class': 'form-control', 'min': '1900', 'max': '2100'}),
            'percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['project_name', 'description', 'start_date', 'end_date', 'url']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }        

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_name', 'issuing_organization', 'issue_date', 'credential_url']
        widgets = {
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }       
         
class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']