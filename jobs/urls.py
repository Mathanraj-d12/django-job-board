from django.urls import path
from .views import (
    home, job_list, job_create,
    job_update, job_delete,
    apply_job, employer_applications,
    withdraw_application, about,my_applications,delete_application
)

urlpatterns = [
    path('', home, name='home'),
    path('jobs/', job_list, name='job_list'),

    # Employer
    path('job/create/', job_create, name='job_create'),
    path('job/edit/<int:pk>/', job_update, name='job_update'),
    path('job/delete/<int:pk>/', job_delete, name='job_delete'),
    path('update/<int:pk>/', job_update, name='job_update'),


    # Jobseeker
    path('apply/<int:pk>/', apply_job, name='apply_job'),
    path('withdraw/<int:job_id>/', withdraw_application, name='withdraw_application'),

    # Employer applications
    path('employer/applications/', employer_applications, name='employer_applications'),

    # Static pages
    path('about/', about, name='about'),

    # job seeker applications
    path('my-applications/', my_applications, name='my_applications'),
    path('delete-application/<int:app_id>/', delete_application, name='delete_application'),


]


