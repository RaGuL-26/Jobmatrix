from django.shortcuts import render,redirect
from .forms import JobForm,JobApplicationForm
from .models import Job,JobApplication,ContactSubmission
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

@login_required(login_url='loginpage')
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.success(request,'Job Added SuccessFully...!')
            return redirect('mainpage')  
    else:
        form = JobForm()  
    return render(request, 'addjob.html', {'form': form})

@login_required(login_url='loginpage')
def job_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(description__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'joblist.html', {'jobs': jobs})

@login_required(login_url='loginpage')
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    return render(request, 'jobdetail.html', {'job': job})

@login_required(login_url='loginpage')
def apply_for_job(request, slug):
    job = get_object_or_404(Job, slug=slug)
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            job_application = form.save(commit=False)
            job_application.job = job  
            job_application.applicant = request.user  
            job_application.save()
            messages.success(request,"Applied For The Job SuccessFully...!")
            return redirect('jobdetail', slug=slug)  
    else:
        form = JobApplicationForm()
    return render(request, 'applyjob.html', {'form': form, 'job': job})
@login_required(login_url='loginpage')
def view_job_applications(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'jobapplications.html', {'jobs': jobs})


@login_required(login_url='loginpage')
def update_application_status(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        return redirect('jobapplications')

@login_required(login_url='loginpage')
def my_applications(request):
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'myapplications.html', {'applications': applications})

@login_required(login_url='loginpage')
def jobs_list(request):
    query = request.GET.get('q')
    if query:
        jobs = Job.objects.filter(title__icontains=query)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobapplications.html', {'jobs': jobs})



def main_page(request):
    return render(request,'index.html')


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactSubmission.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Your message has been sent!')
        return redirect('mainpage')
    return render(request, 'index.html')

@login_required(login_url='loginpage')
def view_submissions(request):
    submissions = ContactSubmission.objects.order_by('-submitted_at')
    return render(request, 'viewcomment.html', {'submissions': submissions})


@login_required(login_url='loginpage')
def delete_comment(request,comment_id=None):
    comment_delete = ContactSubmission.objects.get(id=comment_id)
    comment_delete.delete()
    messages.success(request,'Comment Deleted')
    return redirect('comments')

@login_required(login_url='loginpage')
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    if job.user == request.user:
        job.delete()
        messages.success(request,'Job Deleted SuccessFully...!')
    return redirect('jobposted')


@login_required(login_url='loginpage')
def my_posted_jobs(request):
    jobs = Job.objects.filter(user=request.user)
    return render(request, 'jobposted.html', {'jobs': jobs})