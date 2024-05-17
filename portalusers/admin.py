from django.contrib import admin

# Register your models here.
from .models import User,UserProfile,Education,Project,Certificate,Skill

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Education)
admin.site.register(Project)
admin.site.register(Certificate)
admin.site.register(Skill)