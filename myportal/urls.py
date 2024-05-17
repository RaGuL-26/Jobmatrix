"""
URL configuration for myportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from portalusers import views as PortalViews
from django.conf import settings
from django.conf.urls.static import static
from jobusers import views as JobViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',PortalViews.main_page,name='mainpage'),
    path('register',PortalViews.register_page,name='register'),
    path('loginpage',PortalViews.login_page,name='loginpage'),
    path('logout',PortalViews.logout_page,name='logout'),
    path('submit',JobViews.contact_view,name='submit'),
    path('comments',JobViews.view_submissions,name='comments'),
    path('deletecom/<comment_id>',JobViews.delete_comment,name='deletecom'),
    path('addjob',JobViews.add_job,name='addjob'),
    path('joblist',JobViews.job_list,name='joblist'),
    path('jobposted',JobViews.my_posted_jobs,name='jobposted'),
    path('jobslist', JobViews.jobs_list, name='jobslist'),
    path('delete_job/<int:job_id>/', JobViews.delete_job, name='deletejob'),
    path('myapplications', JobViews.my_applications, name='myapplications'),
    path('jobapplications', JobViews.view_job_applications, name='jobapplications'),
    path('jobdetail/<slug:slug>', JobViews.job_detail, name='jobdetail'),
    path('applyjob/<slug:slug>',JobViews.apply_for_job,name='applyjob'),
    path('updatestatus/<int:application_id>/', JobViews.update_application_status, name='updatestatus'),
    path('<slug:slug>',PortalViews.profile_page,name='profile'),
    path('<slug:slug>/editdp',PortalViews.edit_image,name='editdp'),
    path('<slug:slug>/removedp',PortalViews.remove_pic,name='removedp'),
    path('<slug:slug>/education/add', PortalViews.add_education, name='addeducation'),
    path('<slug:slug>/education/delete/<education_id>/', PortalViews.delete_education, name='deleteeducation'),
    path('<slug:slug>/projects/add/', PortalViews.add_project, name='addproject'),
    path('<slug:slug>/projects/delete/<int:project_id>/', PortalViews.delete_project, name='deleteproject'),
    path('<slug:slug>/certificate/add/', PortalViews.add_certificate, name='addcertificate'),
    path('<slug:slug>/certificate/delete/<int:certificate_id>/', PortalViews.delete_project, name='deletecertificate'),
    path('<slug:slug>/skill/add/', PortalViews.add_skill, name='addskill'),
    path('<slug:slug>/skill/delete/<int:skill_id>/', PortalViews.delete_skill, name='deleteskill'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
