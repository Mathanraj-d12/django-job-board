from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Job, JobApplication
from .forms import JobForm, JobApplicationForm

# =========================
# HOME PAGE
# =========================
def home(request):
    return render(request, 'jobs/home.html')


# =========================
# JOB LIST (Search + Pagination + Category Filter)
# =========================
from django.shortcuts import render
from .models import Job, JobApplication
from django.core.paginator import Paginator

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')

    # Filter by category if selected
    selected_category = request.GET.get('category')
    if selected_category:
        jobs = jobs.filter(category=selected_category)

    # Pagination
    paginator = Paginator(jobs, 6)  # 6 jobs per page
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    # For jobseekers, prepare applied job IDs and statuses
    applied_jobs = {}
    if request.user.is_authenticated and request.user.profile.role == 'jobseeker':
        applications = JobApplication.objects.filter(applicant=request.user.profile)
        for app in applications:
            applied_jobs[app.job.id] = app.status  # store status by job id

    context = {
        'jobs': jobs_page,
        'selected_category': selected_category,
        'applied_job_ids': applied_jobs,  # now contains {job_id: status}
    }
    return render(request, 'jobs/job_list.html', context)


# =========================
# EMPLOYER: CREATE JOB
# =========================
@login_required
def job_create(request):
    if request.user.profile.role != 'employer':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'title': 'Post Job'
    })

# =========================
# EMPLOYER: UPDATE JOB
# =========================
@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/job_form.html', {
        'form': form,
        'title': 'Edit Job'
    })

# =========================
# EMPLOYER: DELETE JOB (CONFIRM)
# =========================
@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)

    if request.method == 'POST':
        job.delete()
        return redirect('job_list')

    return render(request, 'jobs/job_confirm_delete.html', {'job': job})

# =========================
# JOBSEEKER: APPLY JOB
# =========================
@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.user.profile.role != 'jobseeker':
        return redirect('job_list')

    if request.method == 'POST':
        form = JobApplicationForm(request.POST)  # ✅ REMOVED request.FILES
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user.profile
            application.save()

            return redirect('job_list')
    else:
        form = JobApplicationForm()

    return render(request, 'jobs/job_apply.html', {
        'form': form,
        'job': job
    })


# # =========================
# # EMPLOYER: VIEW APPLICATIONS
# # =========================
# @login_required
# def employer_applications(request):
#     if request.user.profile.role != 'employer':
#         return redirect('job_list')

#     applications = JobApplication.objects.filter(
#         job__employer=request.user
#     ).order_by('-applied_at')

#     return render(request, 'jobs/employer_applications.html', {
#         'applications': applications
#     })

# =========================
# JOBSEEKER: WITHDRAW APPLICATION
# =========================
@login_required
def withdraw_application(request, job_id):
    if request.user.profile.role != 'jobseeker':
        return redirect('job_list')

    application = JobApplication.objects.filter(
        job_id=job_id,
        applicant=request.user.profile
    ).first()

    if application:
        application.delete()

    # ✅ HERE BRO
    return redirect('my_applications')






# =========================
# ABOUT PAGE
# =========================
def about(request):
    success = False

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Email content
        subject = f"Contact Form Message from {name}"
        message_body = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [settings.EMAIL_HOST_USER]  # send to your Gmail

        try:
            send_mail(subject, message_body, from_email, recipient_list, fail_silently=False)
            success = True
        except Exception as e:
            print("Error sending email:", e)
            success = False

    return render(request, 'jobs/about.html', {'success': success})




# # =========================
# # EMPLOYER: VIEW APPLICATIONS
# # =========================

@login_required
def employer_applications(request):
    if request.user.profile.role != 'employer':
        return redirect('job_list')

    applications = JobApplication.objects.filter(
        job__employer=request.user
    ).order_by('-applied_at')

    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        action = request.POST.get('action')  # accept / reject / delete

        application = get_object_or_404(
            JobApplication,
            id=app_id,
            job__employer=request.user
        )

        # ✅ HANDLE ACTIONS HERE 👇
        if action == 'accept':
            application.status = 'accepted'
            application.save()

        elif action == 'reject':
            application.status = 'rejected'
            application.save()

        elif action == 'delete':
            application.delete()

        return redirect('employer_applications')

    return render(request, 'jobs/employer_applications.html', {
        'applications': applications
    })



# jobseeker application
@login_required
def my_applications(request):
    if request.user.profile.role != 'jobseeker':
        return redirect('job_list')

    applications = JobApplication.objects.filter(
        applicant=request.user.profile
    ).order_by('-applied_at')

    return render(request, 'jobs/my_applications.html', {
        'applications': applications
    })




# jobseeker delete button
@login_required
def delete_application(request, app_id):
    if request.user.profile.role != 'jobseeker':
        return redirect('job_list')

    application = get_object_or_404(
        JobApplication,
        id=app_id,
        applicant=request.user.profile
    )

    application.delete()
    return redirect('my_applications')
