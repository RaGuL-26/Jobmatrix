from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
import hashlib


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, dob=None, user_type=None):
        if not email:
            raise ValueError('Enter a valid email')
        if not username:
            raise ValueError('Enter a correct username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            dob=dob,
            user_type=user_type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, dob=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            dob=dob,
            user_type = User.SEEKER
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    SEEKER = 'Jobseeker'
    HIRER = 'JobHirer'
    USER_TYPES = [
        (SEEKER, 'Jobseeker'),
        (HIRER, 'JobHirer'),
    ]

    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    number = models.CharField(max_length=15)
    dob = models.DateField(null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default=SEEKER)
    slug = models.SlugField(unique=True, blank=True)

    date_join = models.DateTimeField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = f"{self.username}-{self.email}"
            self.slug = slugify(base_slug)
        
        # Ensure uniqueness by adding a hash if the slug already exists
            original_slug = self.slug
            queryset = User.objects.filter(slug=self.slug).exists()
            counter = 1
            while queryset:
                self.slug = f"{original_slug}-{hashlib.md5((self.email + str(counter)).encode()).hexdigest()[:5]}"
                queryset = User.objects.filter(slug=self.slug).exists()
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
    
    

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='')

    def __str__(self):
        return self.user.username


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    started_year = models.IntegerField()
    ended_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} in {self.field_of_study}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.project_name
    
    
class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=100)
    issuing_organization = models.CharField(max_length=100)
    issue_date = models.DateField()
    credential_url = models.URLField(blank=True)

    def __str__(self):
        return self.certificate_name

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=100)

    def __str__(self):
        return self.skill_name