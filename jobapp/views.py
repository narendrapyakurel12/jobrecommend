from django.http.response import HttpResponseRedirect
from django.views.generic import *

from django.contrib import messages
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from jobapp.jobrecommend import *
import itertools
from itertools import chain
from operator import attrgetter



class EmployerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='employer').exists():
            pass
        else:
            return redirect('/login/')

        return super().dispatch(request, *args, **kwargs)
class JobSeekerRequiredMixin(object):
    
    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and request.user.groups.filter(name='jobseeker').exists():
            pass
        else:
            return redirect('jobapp:jobseekerlogin')
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            pass
        else:
            return redirect('jobapp:adminlogin')
        return super().dispatch(request, *args, **kwargs)


class JobseekerHomeView(TemplateView):
    template_name = 'jobseekertemplates/jobseekerhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context['jobcategorys'] = JobCategory.objects.all()
        context['employers'] = Employer.objects.order_by('-id')

        context['jobs'] = Job.objects.filter(status='completed').order_by('-id')
        return context


class JobSeekerRegistrationView(CreateView):
    template_name = 'jobseekertemplates/jobseekerregistration.html'
    form_class = JobSeekerRegistrationForm
    success_url = reverse_lazy('jobapp:jobseekerlogin')

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = User.objects.create_user(uname, '', pword)
        form.instance.user = user
        return super().form_valid(form)


class JobSeekerLoginView(FormView):
    template_name = 'jobseekertemplates/jobseekerlogin.html'
    form_class = JobSeekerLoginForm
    success_url = '/'

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = authenticate(username=uname, password=pword)
        self.thisuser = user
        if user is not None and user.groups.exists():
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {'form': form, 'error': 'you are not authorized'})
        return super().form_valid(form)

    def get_success_url(self):
        user = self.thisuser
        if user.groups.filter(name='jobseeker').exists():
            return reverse('jobapp:jobseekerprofile')
        elif user.groups.filter(name='employer').exists():
            return reverse('jobapp:employerhome')
        elif user.groups.filter(name='admin').exists():
            return reverse('jobapp:adminhome')
        else:
            return reverse('jobapp:jobseekerlogin')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/')


class JobDetailView(DetailView):
    template_name = 'jobseekertemplates/jobdetail.html'
    model = Job
    context_object_name = 'jobdetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.all().order_by('-id')
        return context


class JobSeekerJobApplyView(JobSeekerRequiredMixin,CreateView):
    template_name = 'jobseekertemplates/jobseekerjobapply.html'
    form_class = JobApplyForm
    success_url = reverse_lazy('jobapp:jobseekerprofile')

    def form_valid(self, form):
        job_id = self.kwargs['pk']
        job = Job.objects.get(id=job_id)
        user = self.request.user
        job_seeker=JobSeeker.objects.get(user=user)
        print(job_seeker,'kkk')
        applicant=JobApplication.objects.filter(jobseeker=job_seeker,job_id=job_id)
        print(applicant)
        if applicant.exists():
            print('ok')
            messages.info(self.request,"you already applied for this job")
            return render(self.request,self.template_name,{'form':form})
        job_seeker = JobSeeker.objects.get(user=user)
        form.instance.job = job
        form.instance.jobseeker = job_seeker
        form.instance.is_applied=True
        form.save()
        messages.success(self.request,'successfully applied')
        return redirect(self.success_url)
        return super().form_valid(form)



class JobSeekerProfileView(JobSeekerRequiredMixin,TemplateView):
    template_name = 'jobseekertemplates/jobseekerprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        jobseeker = JobSeeker.objects.get(user=logged_user)
        text1=jobseeker.skills
        jobs=Job.objects.filter(status='completed')

        match_jobs=[]
        # match=[]
        for job in jobs:

            match_value=match_job(text1,job.skills)
            print(type(match_value))
            if match_value>0.5:
                match_jobs.append(job)
                job.match_value =match_value
        #         for i in [job.match_value]:
        #             match.append(i)
        #             match.sort(reverse=True)
        # context['match']=match
        # print(context['match'])
        
        context['jobrecommend']=match_jobs
        context['match_value']=match_value
        context['jobseeker'] = jobseeker
        return context


class JobseekerProfileUpdateView(JobSeekerRequiredMixin,UpdateView):
    template_name = 'jobseekertemplates/jobseekerprofileupdate.html'
    model = JobSeeker
    form_class = JobseekerProfileUpdateForm
    success_url = reverse_lazy('jobapp:jobseekerprofile')

    def form_valid(self, form):
        user = self.request.user
        form.save()

        return super().form_valid(form)


class AdminLoginView(FormView):
    template_name = 'admintemplates/login.html'
    form_class = AdminLoginForm
    success_url = reverse_lazy('jobapp:adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = authenticate(username=uname, password=pword)
        if user is not None:
            login(self.request, user)
        else:
            return render(self.request, self.template_name, {'form': form, 'error': 'you are not authorized'})

        return super().form_valid(form)


class CVBuilderView(CreateView):
    template_name = "jobseekertemplates/cv_builder.html"
    form_class = CvBuidlerForm
    success_url=reverse_lazy('jobapp:generate_pdf')





class EmployerRegistrationView(CreateView):
    template_name = 'employertemplates/employerregistration.html'
    form_class = EmployerForm
    success_url = reverse_lazy('jobapp:jobseekerlogin')

    def form_valid(self, form):
        uname = form.cleaned_data['username']
        pword = form.cleaned_data['password']
        user = User.objects.create_user(uname, '', pword)
        form.instance.user = user

        return super().form_valid(form)


class EmployerHomeView(EmployerRequiredMixin, TemplateView):
    template_name = 'employertemplates/employerhome.html'


class EmployerProfileView(EmployerRequiredMixin, TemplateView):

    template_name = 'employertemplates/employerprofile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        employer = Employer.objects.get(user=logged_user)
        context['employer'] = employer
        return context


class EmployerJobCreateView(EmployerRequiredMixin, CreateView):
    template_name = 'employertemplates/employerjobcreate.html'
    form_class = EmployerJobCreateForm
    success_url = reverse_lazy('jobapp:employerprofile')

    def form_valid(self, form):
        employer = Employer.objects.get(user=self.request.user)
        form.instance.employer = employer
        return super().form_valid(form)


class EmployerJobDetailView(EmployerRequiredMixin, DetailView):
    template_name = 'employertemplates/employerjobdetail.html'
    model = Job
    context_object_name = 'jobobject'


   


class EmployerProfileUpdateView(EmployerRequiredMixin, UpdateView):
    template_name = 'employertemplates/employerprofileupdate.html'
    form_class = EmployerProfileUpdateForm
    model = Employer
    success_url = reverse_lazy('jobapp:employerprofile')

    def form_valid(self, form):
        user = self.request.user
        print(user)
        form.save()

        return super().form_valid(form)


class EmployerJobUpdateView(EmployerRequiredMixin, UpdateView):
    template_name = 'employertemplates/employerjobupdate.html'
    form_class = EmployerJobUpdateForm
    model = Job
    success_url = reverse_lazy('jobapp:employerprofile')

    def form_valid(self, form):
        user = self.request.user
        print(user)
        form.save()

        return super().form_valid(form)
class EmployerJobDeleteView(EmployerRequiredMixin,DeleteView):
    template_name='employertemplates/employerjobdelete.html'
    model=Job
    success_url=reverse_lazy('jobapp:employerprofile')


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'admintemplates/adminhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allemployers'] = Employer.objects.all()
        context['alljobs'] = Job.objects.all()
        context['alljobseekers'] = JobSeeker.objects.all()
        context['allapplications'] = JobApplication.objects.all()
        return context


class AdminEmployerListView(AdminRequiredMixin, ListView):
    template_name = 'admintemplates/adminemployerlist.html'
    model = Employer
    context_object_name = 'adminemployer'


class AdminEmployerDetailView(DetailView):
    template_name = 'admintemplates/adminemployerdetail.html'
    model = Employer
    context_object_name = 'adminemployerobject'

class AdminJobseekerListView(ListView):
    template_name = 'admintemplates/adminjobseekerlist.html'
    model = JobSeeker
    context_object_name = 'jobseekerobject'


class AdminJobSeekerDetailView(DetailView):
    template_name = 'admintemplates/adminjobseekerdetail.html'
    model = JobSeeker
    context_object_name = 'jobseekerdetailobject'


class AdminJobListView(ListView):
    template_name = 'admintemplates/adminjoblist.html'
    model=Job
    context_object_name = 'jobobject'

    def get_queryset(self):
        job=Job.objects.all().order_by('-id')
        return job


class AdminJobDetailView(DetailView):
    template_name = 'admintemplates/adminjobdetail.html'
    model = Job
    context_object_name = 'jobdetailobject'
class AdminJobStatusChange(UpdateView):
    template_name = 'admintemplates/adminjobstatuschange.html'
    model = Job
    form_class = AdminJobSatusChangeForm
    success_url = reverse_lazy('jobapp:adminjoblist')




class SearchView(TemplateView):
    template_name = 'jobseekertemplates/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        keyword = self.request.GET.get('search')
        keyword1 = self.request.GET.get('location')
        keyword1 = keyword1.strip()
        print(keyword1)

        submits = self.request.GET.get('submit')
        print(submits)

        result = Job.objects.filter(Q(
            title__contains=keyword) | Q(category__title__iexact=keyword), employer__address__contains=keyword1)
        context['submits'] = submits

        context['results'] = result

        return context


class JobView(TemplateView):
    template_name = 'jobseekertemplates/job.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs = Job.objects.filter(status='completed').order_by('-id')
        paginator = Paginator(jobs, 3)
        context['jobs'] = jobs

        return context



class CompanyView(TemplateView):
    template_name = 'jobseekertemplates/company.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Employer.objects.all().order_by('-id')
        return context   

def generate_pdf(request):
    last_cv_builder_user=ResumeBuilder.objects.last()
    html_string=render_to_string('jobseekertemplates/home_page.html',{'last_cv_builder':last_cv_builder_user})
    html=HTML(string=html_string)
    result=html.write_pdf()
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=your_cv.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response

class AdminSearchView(TemplateView):
    template_name='admintemplates/search.html'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        keyword=self.request.GET.get('q')
        jobseeker=JobSeeker.objects.filter(name__icontains=keyword)
        employer=Employer.objects.filter(name__icontains=keyword)
        inbox = sorted(chain(employer,jobseeker), key=attrgetter('name'))
        context['results']=inbox
        return context

class AdminJobseekerDeleteView(DeleteView):
    template_name='admintemplates/delete.html'
    model=JobSeeker
    success_url=reverse_lazy('jobapp:adminjobseekerlist')


class AdminEmployerDeleteView(DeleteView):
    template_name='admintemplates/employerdelete.html'
    model=Employer
    success_url=reverse_lazy('jobapp:adminemployerlist')

