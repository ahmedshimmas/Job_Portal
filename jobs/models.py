from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from users.choices import UserRoles

class BaseModelManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def deleted_objs(self):
        return super().get_queryset().filter(is_deleted=True)
    

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    objects = BaseModelManager()

    class Meta:
        abstract = True

class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.code

class RolePermission(models.Model):
    role = models.CharField(max_length=20, choices=UserRoles.choices)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role} - {self.permission.code}"

class JobCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Job Category'
        verbose_name_plural = 'Job Categories'

    def __str__(self):
        return self.name


class Job(BaseModel):
    employer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'employer'})
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
    

class Application(BaseModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('users.User', on_delete=models.CASCADE, limit_choices_to={'role': 'jobseeker'} )
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    cover_letter = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    is_shortlisted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('job', 'applicant')  # prevent duplicate applications

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"