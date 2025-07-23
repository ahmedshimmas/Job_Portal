from django.db.models import TextChoices

class UserRoles(TextChoices):
    ADMIN = 'admin', 'ADMIN'
    EMPLOYER = 'employer', 'EMPLOYER'
    JOBSEEKER = 'jobseeker', 'JOBSEEKER'