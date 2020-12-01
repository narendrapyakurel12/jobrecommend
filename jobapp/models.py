from django.db import models
from django.contrib.auth.models import User, Group
from datetime import datetime
from .validators import validate_file

# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Admin(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='admin')
    name = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='admin')
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Employer(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100)
    image = models.ImageField(upload_to='employer')
    website = models.CharField(max_length=100)
    compnay = models.CharField(max_length=100)
    company_image = models.ImageField(upload_to='employer/')

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='employer')
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class JobSeeker(TimeStamp):
    user = models.OneToOneField(User, on_delete=models.CharField)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jobseeker')
    qualification = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    cv = models.FileField(upload_to='jobseeker', validators=[validate_file])

    def save(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='jobseeker')
        self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class JobCategory(TimeStamp):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jobcategory')

    def __str__(self):
        return self.title


JOB_TYPE = (('full_time', 'Full Time'), ('part_time', 'Part Time'),
            ('contact', 'Contact'), ('internship', 'Internship'),)
LEVEL = (('junior', 'Junior'), ('mid', 'Mid'), ('seneior', 'Seneior'),)


class Job(TimeStamp):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='job')
    category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    job_type = models.CharField(max_length=100, choices=JOB_TYPE)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    level = models.CharField(max_length=50, choices=LEVEL)
    deadline = models.DateTimeField(default=datetime.now())
    vaccncy_number = models.PositiveIntegerField()
    education = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    details = models.TextField()
    experience = models.CharField(max_length=100, null=True, blank=True)
    salary = models.CharField(max_length=100, null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class JobApplication(TimeStamp):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    cover_letter = models.FileField(upload_to='jobapplication')

    def __str__(self):
        return self.jobseeker.user.username
