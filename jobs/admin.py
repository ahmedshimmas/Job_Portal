from django.contrib import admin
from jobs import models
# Register your models here.

admin.site.register(
    [
        models.JobCategory,
        models.Job,
        models.Application,
        models.Permission,
        models.RolePermission
    ]
)