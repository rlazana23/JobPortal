from email.mime import application
from genericpath import exists
from importlib.metadata import files
from multiprocessing import context
from re import U
from turtle import title
from urllib.request import Request
from wsgiref.util import request_uri
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . forms import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.mail import send_mail
import sweetify
# Create your views here.

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        getemail = User.objects.values().filter(email = username)

        if getemail:
            username = getemail[0]['username']
        checkactive = User.objects.filter(username = username)
        if checkactive:
            checkactive = User.objects.get(username = username)
            if checkactive.is_active:
                user = authenticate(request,username = username, password = password)
                if user is not None:
                    login(request, user)
                    return redirect('gettingstarted')
                else:
                    sweetify.error(request, 'Login Error', text='Invalid Account', persistent='Okay', )
                    messages.add_message(request, messages.ERROR, 'Invalid Username or Password')
            else:
                sweetify.error(request, 'Account Disabled', text='Disabled Account', persistent='Okay', )
                messages.add_message(request, messages.ERROR, 'Your Account Has Been Disabled')
        else:
            sweetify.error(request, 'Login Error', text='Invalid Account', persistent='Okay', )
    return render(request, 'base/login.html')

def logoutConfirm(request):
    return render(request, 'base/user-logout-confirm.html')
def logoutPage(request):
    logout(request)
    return redirect('login')

def registerPage(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email = email).exists():
                print("existing")
                alert = 0
                # messages.add_message(request,messages.ERROR, 'Email Already Registered')
                sweetify.error(request, 'Registration Error', text='Email already registered!', persistent='Okay')
            else:
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                form.save()
                new_user = authenticate(username = username, password = password)
                sweetify.success(request, 'Registration Success', text='', persistent='Okay', )
                form = RegisterForm()
                context = {'form': form}
                return render(request, 'base/register.html', context)
                # if new_user is not None:
                #     login(request, new_user)
                #     return redirect('gettingstarted')
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'base/register.html', context)

@login_required(login_url='login')
def home(request):
    user = JobSeeker.objects.get(user_id =request.user)
    #GET Q
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q == 'Full':
        jobs = Jobs.objects.filter(ispart_time = False)
    elif q == 'Part':
        jobs = Jobs.objects.filter(ispart_time = True)
    else:
        jobs = Jobs.objects.filter(Q(company__name__icontains = q) | Q(title__icontains = q)|
        Q(qualification__icontains = q) | Q(job_description__icontains = q)|
        Q(company__location__icontains =q),is_active = True, company__user__is_active = True)

    #for pagination
    paginator = Paginator(jobs,4)
    page_number =request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    page = 'jobseeker'
    context = {'u':user, 'page': page, 'jobs':jobs, 'page_obj':page_obj, 'q':q}
    return render(request, 'base/home.html', context)
def companyHome(request):
    user = Company.objects.get(user_id = request.user)
    if request.method == 'POST':
        form = PostJob(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            job_description = form.cleaned_data.get('job_description')
            ispart_time = form.cleaned_data.get('ispart_time')
            salary = form.cleaned_data.get('salary')
            qualification = form.cleaned_data.get('qualification')
            job = Jobs.objects.create(
                company = user,
                title = title,
                salary = salary,
                qualification = qualification,
                job_description = job_description,
                ispart_time = ispart_time,
            )

            #sending email after posting of jobs
            seekers = JobSeeker.objects.all()

            for seeker in seekers:
                skills = SeekerSkills.objects.filter(seeker_id = seeker)

                for skill in skills:
                    if skill.skill_name in title or skill.skill_name in qualification or skill.skill_name in job_description:
                        companyname = Company.objects.get(user_id = request.user)
                        useremail = User.objects.get(username = seeker.user)
                        send_mail(
                            'JOB ALERT',
                            'A Job offering for ' + skill.skill_name + ' is being offered by ' + companyname.name
                            +'\n Title: ' + title
                            +'\n Description: ' + job_description
                            +'\n Qualification: '+ qualification,
                            'rlazana23@gmail.com',
                            [useremail.email],
                            fail_silently=False,
                        )
                        break

            # for activity logs
            log = (f"{user} created a job named {title}.")
            logs = ActivityLogs.objects.create(
                log = log
            )    
            sweetify.success(request, 'Job Posted', text='New job is now available', persistent='Okay', )        
            # messages.add_message(request, messages.SUCCESS, 'Job Posted!')
            return redirect('company')
    else:
        form = PostJob()
    
    page = 'company'
    jobs = Jobs.objects.filter(company_id = user)
    context = {'u': user, 'page': page, 'form':form, 'jobs':jobs}
    return render(request, 'base/home_company.html', context)
@login_required(login_url='login')
def userProfile(request):
    user = JobSeeker.objects.get(user_id =request.user)
    #code for updating images
    if request.method == 'POST':
        requestname = request.POST.get('action')
        #form for uploading profile  picture
        if 'change_profile_picture' == requestname:
            file = request.FILES.get('user_image')
            user = JobSeeker.objects.get(user_id = request.user.id)
            form = UploadImageForm(request.POST, request.FILES, instance= user)
            if file:
                sweetify.success(request, 'Profile Picture Updated', text='', persistent='Okay', )
                form.save()
            else:
                sweetify.error(request, 'File is empty', text='Upload your photo', persistent='Okay', )
            # if form.is_valid():
            #     form.save()
        #form for uploading  resume
        elif 'upload-profile-resume' == requestname:
            file = request.FILES.get('user_resume')
            user = JobSeeker.objects.get(user_id = request.user.id)
            form = UploadFileForm(request.POST, request.FILES, instance = user)
            if not file:
                sweetify.error(request, 'File is empty', text='Upload your resume', persistent='Okay', )
            else:
                sweetify.success(request, 'Resume Uploaded', text='', persistent='Okay', )
                form.save()
        # code for adding skill        
        elif 'user-add-skill' == requestname:
            user = JobSeeker.objects.get(user_id = request.user.id)
            skilltoAdd = request.POST.get('skill_name')
            skill = SeekerSkills.objects.create(
                    seeker = user,
                    skill_name = skilltoAdd,
                )
            sweetify.success(request, 'Skill Added', text='', persistent='Okay',)
        
        elif 'user-add-previous-work' == requestname:
            user = JobSeeker.objects.get(user_id = request.user.id)
            name = request.POST.get('name')
            description = request.POST.get('description')
            yearStarted = request.POST.get('yearStarted')
            yearEnded = request.POST.get('yearEnded')
            work = SeekerPreviousWork.objects.create(
                    seeker = user,
                    name = name,
                    description =description,
                    yearStarted = yearStarted,
                    yearEnded = yearEnded
            )
            sweetify.success(request, 'Previous Job Added', text='', persistent='Okay', )

        elif 'user-edit-profile' == requestname:
            form =EditSeekerForm(request.POST, instance= user)
            if form.is_valid():
                form.save()

                log = (f"{user} updated their profile.")
                logs = ActivityLogs.objects.create(
                log = log
            )      
            # messages.add_message(request, messages.SUCCESS, 'Profile Successfully Updated!')
            sweetify.info(request, 'Profile Updated', text='', persistent='Okay', )
            return redirect('user_profile')
            

        return redirect('user_profile')
    else:
        form_change_profile = UploadImageForm()
        form_upload_resume = UploadFileForm()
        form_add_skill = AddSeekerSkillForm()
        form_add_work = PreviousWorkForm()
        form_edit_profile = EditSeekerForm(instance=user)
    skills = SeekerSkills.objects.filter(seeker_id = user)
    works =SeekerPreviousWork.objects.filter(seeker_id = user)
    page = 'jobseeker'
    context = {'form_edit_profile':form_edit_profile,'form_add_work': form_add_work,'form_add_skill': form_add_skill,'form_profile_picture': form_change_profile, 'form_upload_resume': form_upload_resume, 'u':user, 'skills':skills, 'page': page ,'works':works}
    return render(request, 'base/user-profile.html', context)

def companyProfile(request):
    user = Company.objects.get(user_id = request.user)
    if request.method == 'POST':
        requestname = request.POST.get('action')
        if 'change_profile_picture' == requestname:
            file = request.FILES.get('user_image')
            user = Company.objects.get(user_id = request.user)
            form = UploadImageCompanyForm(request.POST, request.FILES, instance=user)
            if file:
                sweetify.success(request, 'Company Picture Updated', text='', persistent='Okay', )
                form.save()
            else:
                sweetify.error(request, 'File is empty', text='Upload your company photo', persistent='Okay', )
        if 'user-edit-profile' == requestname:
            form = EditCompanyForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                log = (f"{user} updated their profile.")
                logs = ActivityLogs.objects.create(
                log = log
            )      
            sweetify.success(request, 'Company Information Updated', text='', persistent='Okay',)
            # messages.add_message(request, messages.SUCCESS, 'Profile Successfully Updated!')
            return redirect('company_profile')
        return redirect('company_profile')
    else:
        form_change_profile = UploadImageCompanyForm()
        form_edit_profile = EditCompanyForm(instance=user)
    page = 'company'
    
    context = {'form_edit_profile':form_edit_profile,'form_profile_picture': form_change_profile, 'u' : user, 'page':page}
    return render(request, 'base/user-profile.html', context)

def seekerViewApplications(request):
    user = JobSeeker.objects.get(user_id = request.user)
    page = 'jobseeker'
    applications = JobApplication.objects.filter(seeker = user)
    context = {'u':user, 'page':page, 'applications':applications}
    return render(request, 'base/user-view-applications.html', context)

def seekerCancelRemoveApplication(request, pk):
    sweetify.info(request, 'Application Removed', text='', persistent='Okay', )
    applications = JobApplication.objects.get(id = pk)
    applications.delete()

    log = (f"{applications.seeker} removed their application for {applications.job}.")
    logs = ActivityLogs.objects.create(
        log = log
    )      
    # messages.add_message(request, messages.SUCCESS, 'Application Removed')
    return redirect('seeker_view_applications')

def seekerViewCompany(request, pk):
    user = JobSeeker.objects.get(user_id = request.user)
    company = Company.objects.get(id = pk)
    jobs = Jobs.objects.filter(company= company)
    page = 'jobseeker'
    context = {'u':user, 'company':company, 'page':page, 'jobs':jobs}
    return render(request, 'base/view_user_profile.html', context)

def companyViewSeeker(request, pk):
    user = Company.objects.get(user_id = request.user)
    seeker = JobSeeker.objects.get(id = pk)
    skills = SeekerSkills.objects.filter(seeker_id = seeker)
    works = SeekerPreviousWork.objects.filter(seeker_id = seeker)
    page = 'company'
    context = {'u':user, 'seeker':seeker, 'page':page, 'skills':skills, 'works':works}
    return render(request, 'base/view_user_profile.html', context)

def companyEditJob(request,pk):
    user = Company.objects.get(user_id = request.user)
    job = Jobs.objects.get(id = pk)
    if request.method == 'POST':
        form = EditJob(request.POST, instance=job)
        if form.is_valid():
            form.save()
            log = (f"{job.company} updated {job.title}")
            logs = ActivityLogs.objects.create(
                log = log
            )  
            # messages.add_message(request, messages.SUCCESS, 'Job Successfully Updated!')
            sweetify.success(request, 'Job Updated', text='Job information is now updated', persistent='Okay', )
            return redirect('company')
    else:
        form = EditJob(instance=job)
    page = 'company'
    context = {'u':user, 'form':form, 'page':page, 'key': pk}
    return render(request, 'base/company_edit_job.html', context)

def companyDeletejob(request,pk):
    job = Jobs.objects.get(id = pk)
    log = (f"{job.company} removed {job.title}")
    logs = ActivityLogs.objects.create(
        log = log
    )  
    job.delete()
    sweetify.error(request, 'Job Removed', text='Job offer will no longer be available', persistent='Okay', )
        # messages.add_message(request, messages.SUCCESS, 'Job Deleted!')
    return redirect('company')

def companyViewApplications(request, pk):
    applications = JobApplication.objects.filter(job_id = pk , seeker__user__is_active = True)
    job = Jobs.objects.get(id = pk)
    user = Company.objects.get(user_id = request.user)
    page = 'company'
    context = {'u':user, 'page':page, 'applications':applications, 'job':job}
    return render(request, 'base/company_view_applications.html', context)

def companyRejectApplication(request, pk, application_id):
    jobapplication = JobApplication.objects.get(id = application_id)
    jobapplication.application_status = 'Rejected'
    jobapplication.save()
    log = (f"{jobapplication.job.company} rejected {jobapplication.seeker}")
    logs = ActivityLogs.objects.create(
        log = log
    )  
    sweetify.error(request, 'Applicant Rejected', text='', persistent='Okay', )
    return redirect('company_view_applications', pk = pk)
def companyAcceptApplication(request,pk, application_id):
    jobapplication = JobApplication.objects.get(id = application_id)
    jobapplication.application_status = 'Accepted'
    jobapplication.save()
    log = (f"{jobapplication.job.company} accepted {jobapplication.seeker}")
    logs = ActivityLogs.objects.create(
        log = log
    ) 
    sweetify.success(request, 'Applicant Accepted', text='', persistent='Okay', ) 
    # messages.add_message(request, messages.SUCCESS, 'You have accepted an application!')
    return redirect('company_view_applications', pk = pk)
def companyRevokeAction(request, pk, application_id):
    jobapplication = JobApplication.objects.get(id = application_id)
    jobapplication.application_status = 'Pending'
    jobapplication.save()
    log = (f"{jobapplication.job.company} Action Revoked for {jobapplication.seeker}")
    logs = ActivityLogs.objects.create(
        log = log
    ) 
    sweetify.success(request, 'ActionRevoked', text='', persistent='Okay', ) 
    # messages.add_message(request, messages.SUCCESS, 'You have accepted an application!')
    return redirect('company_view_applications', pk = pk)
def seekerRemoveSkills(request, pk):
    skill = SeekerSkills.objects.get(id = pk)
    skill.delete()
    sweetify.error(request, 'Skill Removed', text='', persistent='Okay', )
    return redirect('user_profile')

def seekerRemoveWork(request, pk):
    work = SeekerPreviousWork.objects.get(id = pk)
    work.delete()
    sweetify.error(request, 'Previous Job Removed', text='', persistent='Okay', )
    return redirect('user_profile')

def viewJob(request, pk):
    job = Jobs.objects.get(id = pk)
    seeker = JobSeeker.objects.get(user_id = request.user)
    page = 'jobseeker'
    if request.method == 'POST':
        job_id = request.POST.get('job_id')
        seeker_id = request.POST.get('seeker_id')
        if JobApplication.objects.filter(seeker_id = seeker_id, job_id = job_id).exists():
            return redirect('home')
        else:
            application = JobApplication.objects.create(
                seeker_id = seeker_id,
                job_id = job_id
            )
            log = (f"{application.seeker} applied for {application.job}.")
            logs = ActivityLogs.objects.create(
                log = log
            )     
            sweetify.success(request, 'Applied for this position', text='', persistent='Okay', )
            # messages.add_message(request, messages.SUCCESS, 'JOB APPLIED!')

    applied = JobApplication.objects.filter(job_id = job, seeker_id =seeker)

    if applied:
        applied = JobApplication.objects.get(job_id = job, seeker_id=seeker)
    user = JobSeeker.objects.get(user_id = request.user)
    context = {'page': page, 'job':job, 'u':user, 'applied': applied}
    return render(request, 'base/user-view-job.html', context)

def gettingStarted(request):

    if JobSeeker.objects.filter(user_id = request.user.id).exists():
        u = JobSeeker.objects.get(user_id = request.user.id)
        return redirect('home')
    elif Company.objects.filter(user_id = request.user.id).exists():
        u = Company.objects.get(user_id = request.user)
        return redirect('company')
    return render(request, 'base/gettingstarted.html')

def seekerForm(request):

    if request.method == 'POST':
        form = SeekerForm(request.POST, request.FILES)
        if form.is_valid():
            firstname = form.cleaned_data.get('first_name')
            lastname = form.cleaned_data.get('last_name')
            user = JobSeeker.objects.create(
                user = request.user,
                first_name = firstname,
                last_name = lastname,
            )
            log = (f"{user} registered as a jobseeker.")
            logs = ActivityLogs.objects.create(
                log = log
            )   
            return redirect('home')
    else:
        form = SeekerForm()
    
    context = {'form':form}

    return render(request, 'base/form_seeker.html', context)

def companyForm(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        company_location = request.POST.get('company_location')
        if Company.objects.filter(name = company_name).exists():
            messages.add_message(request, messages.ERROR, 'Company already exists!')
        else:
            add_company = Company.objects.create(
                user = request.user,
                name = company_name,
                location = company_location,
            )
            log = (f"{add_company} registered as a company.")
            logs = ActivityLogs.objects.create(
                log = log
            )   
            return redirect('company')
    
    return render(request, 'base/form_company.html')

def deleteAccount(request):
            user = User.objects.get(username = request.user)
            logout(request)
            log = (f"{user} deleted  their account.")
            logs = ActivityLogs.objects.create(
                log = log
            )  
            user.delete()
            messages.add_message(request, messages.SUCCESS, 'Account Deleted.')
            return redirect('login')

def backtoProfile(request):
    user = JobSeeker.objects.filter(user_id = request.user)
    if user:
        return redirect('user_profile')
    else:
        return redirect('company_profile')