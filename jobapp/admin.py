from django.contrib import admin
from .models import *
admin.site.register([Admin,Employer,JobSeeker,Job,JobApplication,JobCategory,ResumeBuilder])

# Register your models here.
