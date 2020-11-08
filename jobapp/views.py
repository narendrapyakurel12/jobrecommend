from django.views.generic import *
from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse, reverse_lazy

from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout


class EmployerRequiredMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='employer').exists():
            pass
        else:
            return redirect('/login/')

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
        context['jobcategorys'] = JobCategory.objects.all()

        context['jobs'] = Job.objects.all().order_by('-id')
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
            return reverse('jobapp:jobseekerhome')
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


class JobSeekerJobApplyView(CreateView):
    template_name = 'jobseekertemplates/jobseekerjobapply.html'
    form_class = JobApplyForm
    success_url = reverse_lazy('jobapp:jobseekerprofile')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='jobseeker').exists():
            pass
        else:
            return redirect('jobapp:jobseekerlogin')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        job_id = self.kwargs['pk']
        job = Job.objects.get(id=job_id)
        user = self.request.user
        job_seeker = JobSeeker.objects.get(user=user)
        form.instance.job = job
        form.instance.jobseeker = job_seeker
        return super().form_valid(form)


class JobSeekerProfileView(TemplateView):
    template_name = 'jobseekertemplates/jobseekerprofile.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.groups.filter(name='jobseeker'):
            pass
        else:
            return redirect('jobapp:jobseekerlogin')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logged_user = self.request.user
        jobseeker = JobSeeker.objects.get(user=logged_user)
        print(jobseeker, 'jobseeker')
        context['jobseeker'] = jobseeker
        return context


class JobseekerProfileUpdateView(UpdateView):
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
    model = Job
    context_object_name = 'jobobject'

    
class AdminJobDetailView(DetailView):
    template_name = 'admintemplates/adminjobdetail.html'
    model = Job
    context_object_name = 'jobdetailobject'


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
