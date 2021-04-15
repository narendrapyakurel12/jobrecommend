from django import forms
from .models import *
from django.forms import ValidationError, widgets


class JobSeekerRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = JobSeeker
        fields = ['username', 'password', 'confirm_password', 'name', 'email', 'address',
                  'mobile', 'image', 'qualification', 'skills', 'about', 'cv']
        widgets = {'address': forms.TextInput(attrs={'class': 'form-control'}),
                   'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'mobile': forms.TextInput(attrs={'class': 'form-control'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   'qualification': forms.TextInput(attrs={'class': 'form-control'}),
                   'skills': forms.TextInput(attrs={'class': 'form-control','placeholder':'python,django,javascript,rest framework'}),
                   'about': forms.TextInput(attrs={'class': 'form-control'}),
                   'cv': forms.FileInput(attrs={'class': 'form-control'}),
                   }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        print(user, 'kkd')
        if user.exists():
            print('1')
            raise forms.ValidationError(
                f"{username} with this user name already exitst please choose different name")
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        c_password = self.cleaned_data.get('confirm_password')
        if password != c_password:
            raise forms.ValidationError('password didnot match')
        return c_password


class JobSeekerLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())


class JobApplyForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.FileInput(attrs={'class': 'form-control'})
        }




class EmployerForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Employer
        fields = ['username', 'password', 'confirm_password', 'name', 'mobile', 'email', 'address',
                  'website', 'company_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'company_image': forms.FileInput(attrs={'class': 'form-control'}),

        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = User.objects.filter(username=username)
        if user.exists():
            raise forms.ValidationError(
                'JobSeeker with this user name already exitst please choose different name')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        c_password = self.cleaned_data.get('confirm_password')
        if password != c_password:
            raise forms.ValidationError('password didnot match')
        return c_password


class JobseekerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = JobSeeker
        exclude = ['user']
        fields = ['email', 'address', 'name',
                  'mobile', 'image', 'qualification', 'skills', 'about', 'cv']
        widgets = {'address': forms.TextInput(attrs={'class': 'form-control'}),
                   'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'email': forms.EmailInput(attrs={'class': 'form-control'}),
                   'mobile': forms.TextInput(attrs={'class': 'form-control'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   'qualification': forms.TextInput(attrs={'class': 'form-control'}),
                   'skills': forms.TextInput(attrs={'class': 'form-control'}),
                   'about': forms.TextInput(attrs={'class': 'form-control'}),
                   'cv': forms.FileInput(attrs={'class': 'form-control'}),
                   }


class EmployerJobCreateForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['employer']
        fields = ['title', 'image', 'category', 'job_type', 'level', 'deadline', 'vaccncy_number',
                  'education', 'skills', 'details', 'experience', 'salary']

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control '}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   'category': forms.Select(attrs={'class': 'form-control'}),
                   'job_type': forms.Select(attrs={'class': 'form-control'}),
                   'level': forms.Select(attrs={'class': 'form-control'}),
                   'deadline': forms.DateInput(attrs={'class': 'form-control '}),
                   'vaccncy_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'education': forms.TextInput(attrs={'class': 'form-control'}),
                   'skills': forms.TextInput(attrs={'class': 'form-control'}),
                   'details': forms.TextInput(attrs={'class': 'form-control'}),
                   'experience': forms.TextInput(attrs={'class': 'form-control'}),
                   'salary': forms.TextInput(attrs={'class': 'form-control'})
                   }


class EmployerJobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['employer']
        fields = ['title', 'image', 'category', 'job_type', 'level', 'deadline', 'vaccncy_number',
                  'education', 'skills', 'details', 'experience', 'salary']

        widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                   'image': forms.FileInput(attrs={'class': 'form-control'}),
                   'category': forms.TextInput(attrs={'class': 'form-control'}),
                   'job_type': forms.Select(attrs={'class': 'form-control'}),
                   'level': forms.Select(attrs={'class': 'form-control'}),
                   'deadline': forms.DateInput(attrs={'class': 'form-control'}),
                   'vaccncy_number': forms.NumberInput(attrs={'class': 'form-control'}),
                   'education': forms.TextInput(attrs={'class': 'form-control'}),
                   'skills': forms.TextInput(attrs={'class': 'form-control'}),
                   'details': forms.TextInput(attrs={'class': 'form-control'}),
                   'experience': forms.TextInput(attrs={'class': 'form-control'}),
                   'salary': forms.TextInput(attrs={'class': 'form-control'})
                   }


class EmployerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        exclude = ['user']
        fields = ['name', 'mobile', 'email',
                  'address', 'website', 'company_image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'company_image': forms.FileInput(attrs={'class': 'form-control'}),

        }


class AdminLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
class AdminJobSatusChangeForm(forms.ModelForm):
    class Meta:
        model = Job
        fields='__all__'

class CvBuidlerForm(forms.ModelForm):
    class Meta:
        model=ResumeBuilder
        fields='__all__'

 
 

