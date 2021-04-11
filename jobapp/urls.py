from django.urls import path
from .views import *
from .import views

app_name = 'jobapp'
urlpatterns = [
     # jobseekers
    path('', JobseekerHomeView.as_view(), name='jobseekerhome'),
    path('jobseeker/registration/',
         JobSeekerRegistrationView.as_view(), name='jobseekerregistration'),
    path('login/', JobSeekerLoginView.as_view(), name='jobseekerlogin'),
    path('job/<int:pk>/detail/',
         JobDetailView.as_view(), name='jobdetails'),
    path('job/<int:pk>/apply/', JobSeekerJobApplyView.as_view(),
         name='jobseekerjobapply'),
    path('jobseeker/profile/', JobSeekerProfileView.as_view(),
         name='jobseekerprofile'),
    path('jobseeker/cv_builder', CVBuilderView.as_view(), name="cv_builder"),

    #employer
    path('employer/registration', EmployerRegistrationView.as_view(),
         name='employerregistration'),
    path('employer/home/', EmployerHomeView.as_view(), name='employerhome'),
    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('jobseeker/profile/<int:pk>/update/',
         JobseekerProfileUpdateView.as_view(), name='jobseekerprofileupdate'),
    path('employer/profile/', EmployerProfileView.as_view(), name='employerprofile'),
    path('employer/job/<int:pk>/detail/',
         EmployerJobDetailView.as_view(), name='employerjobdetail'),
    path('employer/job/post/', EmployerJobCreateView.as_view(),
         name='employerjobcreate'),
    path('employer/profile/<int:pk>/update/',
         EmployerProfileUpdateView.as_view(), name='employerprofileupdate'),
    path('employer/job/<int:pk>/update/',
         EmployerJobUpdateView.as_view(), name='employerjobupdate'),

         #admin
    path('job-admin/', AdminHomeView.as_view(), name='adminhome'),
    path('admin/employer/list/', AdminEmployerListView.as_view(),
         name='adminemployerlist'),
    path('admin/employer/<int:pk>/detail/',
         AdminEmployerDetailView.as_view(), name='adminemployerdetail'),
    path('admin/jobseeker/list/', AdminJobseekerListView.as_view(),
         name='adminjobseekerlist'),
    path('admin/jobseeker/<int:pk>/detail/',
         AdminJobSeekerDetailView.as_view(), name='adminjobseekerdetail'),
    path('admin/job/list/', AdminJobListView.as_view(), name='adminjoblist'),
    path('admin/job/<int:pk>/detail/',
         AdminJobDetailView.as_view(), name='adminjobdetail'),
    path('admin/job/status/<int:pk>/change',
         AdminJobStatusChange.as_view(), name='adminjobstatuschange'),

    path('logout/', LogoutView.as_view(), name='logout'), 

    #for all
    path('search/', SearchView.as_view(), name='search'),
    path('alljob/', JobView.as_view(), name='alljob'),
    path('allcompany/', CompanyView.as_view(), name='allcompany'),
    path('generate/pdf/',views.generate_pdf,name='generate_pdf'),
    
]
