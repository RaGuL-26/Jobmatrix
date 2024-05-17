from django.shortcuts import render,redirect,get_object_or_404
from .forms import RegisterForm,LoginForm,EducationForm,ProjectForm,CertificateForm,SkillForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import UserProfile,User,Education,Project,Certificate,Skill
from django.urls import reverse



# Create your views here.
def main_page(request):
    return render(request,'index.html')


def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user =form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            form.save()
            messages.success(request,'Registered Successfully..!')
            return redirect('mainpage')
    else:
        form = RegisterForm()
    return render(request,'register.html')

def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,'LoggedIn SuccessFully')
                return redirect('mainpage')
            else:
                messages.error(request, "Invalid email or password.")
        else:
            form = LoginForm()
    return render(request,'login.html')
    
def logout_page(request):
    logout(request)
    messages.success(request,'LoggedOut SuccessFully..!')
    return redirect('mainpage')
            
@login_required(login_url='loginpage')
def profile_page(request,slug):
    user = get_object_or_404(User, slug=slug)
    education_list = Education.objects.filter(user=user).order_by('-started_year')
    project_list = Project.objects.filter(user=user).order_by('-start_date')
    certificate_list = Certificate.objects.filter(user=user).order_by('-issue_date')
    skill_list = Skill.objects.filter(user=user)

    context = {
        'user': user,
        'education_list': education_list,
        'project_list':project_list,
        'certificate_list':certificate_list,
        'skill_list':skill_list,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='loginpage')
def edit_image(request, slug):
    user = get_object_or_404(User, slug=slug)
    user_data, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        if request.FILES:
            user_data.profile_pic = request.FILES['profile_pic']
            user_data.save()
            return redirect('profile', slug=user.slug)
    
    context = {'user': user, 'user_data': user_data}
    return render(request, 'editprofile.html', context)


@login_required(login_url='loginpage')
def remove_pic(request, slug):
    user = get_object_or_404(User, slug=slug)
    user_data, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == 'POST':
        user_data.profile_pic = None
        user_data.save()
        return redirect('profile', slug=user.slug)
    
    context = {'user': user, 'user_data': user_data}
    return render(request, 'editprofile.html', context)


@login_required(login_url='loginpage')
def add_education(request, slug):
    user = get_object_or_404(User, slug=slug)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            education = form.save(commit=False)
            education.user = user
            education.save()
            return redirect('profile', slug=user.slug)
    else:
        form = EducationForm()
    return render(request, 'addeducation.html', {'form': form})

@login_required(login_url='loginpage')
def edit_education(request, slug, id):
    user = get_object_or_404(User, slug=slug)
    education = get_object_or_404(Education, id=id, user=user)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=user.slug)
    else:
        form = EducationForm(instance=education)
    return render(request, 'editeducation.html', {'form': form})


@login_required(login_url='loginpage')
def delete_education(request, education_id, slug):
    education = get_object_or_404(Education, id=education_id)
    if education.user == request.user:

        education.delete()
    return redirect('profile', slug=slug)


@login_required(login_url='loginpage')
def add_project(request, slug):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('profile', slug=request.user.slug)
    else:
        form = ProjectForm()
    return render(request, 'addproject.html', {'form': form})

@login_required(login_url='loginpage')
def delete_project(request, slug, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)
    if project.user == request.user:
        project.delete()
    return redirect('profile', slug=slug)


@login_required(login_url='loginpage')
def add_certificate(request,slug):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save(commit=False)
            certificate.user = request.user
            certificate.save()
            return redirect('profile',slug=request.user.slug)
    else:
        form = CertificateForm()
    return render(request, 'addcertificate.html', {'form': form})

@login_required(login_url='loginpage')
def delete_certificate(request, slug, certificate_id):
    project = get_object_or_404(Certificate, id=certificate_id, user=request.user)
    if project.user == request.user:
        project.delete()
    return redirect('profile', slug=slug)

@login_required(login_url='loginpage')
def add_skill(request,slug):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            return redirect('profile',slug=request.user.slug)
    else:
        form = SkillForm()
    return render(request, 'addskills.html', {'form': form})

@login_required(login_url='loginpage')
def delete_skill(request, slug, skill_id):
    skill = get_object_or_404(Skill, id=skill_id, user=request.user)
    if skill.user == request.user:
        skill.delete()
    return redirect('profile', slug=slug)
