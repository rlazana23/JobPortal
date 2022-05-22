from django.contrib import admin
from .models import *
from datetime import datetime
# Register your models here.

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

#code for costumizing Company Tab
class CompanyAdminSite(admin.ModelAdmin):
    model = Company
    list_display = ['name', 'user', 'location' ,'is_active']
    actions = ['generateReport']
    #Code for deleting default actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
    
        return actions

    def generateReport(modeladmin,request,queryset):
        buf = io.BytesIO()
        c= canvas.Canvas(buf, pagesize=letter,bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)

        lines  = []
        lines.append("LIST OF COMPANIES\n")
        for company in queryset:
            lines.append("User: "+ company.user.username)
            lines.append("Company Name: "+ company.name)
            lines.append("Location: " + company.location)
            if company.description == None:
                lines.append("Description: N/A")
            else:
                lines.append("Description:" + company.description)
            lines.append('----------------')
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='listOfCompany.pdf')

class JobSeekerAdminSite(admin.ModelAdmin):
    model = JobSeeker
    list_display = ['user', 'first_name', 'last_name', 'is_active']
    actions = ['generateReport']
    #Code for deleting default actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
    
        return actions

    def generateReport(modeladmin,request,queryset):
        buf = io.BytesIO()
        c= canvas.Canvas(buf, pagesize=letter,bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)

        lines  = []
        lines.append("LIST OF USERS\n")
        for jobseeker in queryset:
            lines.append("User: "+ jobseeker.user.username)
            lines.append("Name: "+ jobseeker.first_name + ' ' + jobseeker.last_name)
            if jobseeker.is_active:
                lines.append("Status: Active")
            else:
                lines.append("Status: Disabled")
            lines.append('----------------')
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='listofUsers.pdf')

class JobAdminSite(admin.ModelAdmin):
    model = Jobs
    actions = ['generateReport']
    list_display = ['company', 'title', 'date_posted', 'is_active']
    #Code for deleting default actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
    
        return actions

    def generateReport(modeladmin,request,queryset):
        buf = io.BytesIO()
        c= canvas.Canvas(buf, pagesize=letter,bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)

        lines  = []
        lines.append("LIST OF JOBS")
        lines.append("")
        for jobs in queryset:
            lines.append("User: "+ jobs.company.user.username)
            lines.append("Title: "+ jobs.title)
            lines.append("Date Posted: " + jobs.date_posted.strftime('%Y-%m-%d'))
            if jobs.ispart_time:
                lines.append("Job Type: Part Time")
            else:
                lines.append("Job Type: Full Time")
            if jobs.is_active:
                lines.append("Status: Hiring")
            else:
                lines.append("Status: Closed")
            lines.append('----------------')
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='listofJobs.pdf')

class JobApplicationSite(admin.ModelAdmin):
    model = JobApplication
    list_display = ['seeker','job','date_applied', 'application_status']

class ActivityLogSite(admin.ModelAdmin):
    model = ActivityLogs
    list_display = ['log','time']
    actions = ['generateReport']
    #Code for deleting default actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
    
        return actions

    def generateReport(modeladmin,request,queryset):
        buf = io.BytesIO()
        c= canvas.Canvas(buf, pagesize=letter,bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)

        lines  = []
        lines.append("Activity Log")
        lines.append("")
        for log in queryset:
            lines.append('Log: '+ log.log)
            lines.append('Date: ' + log.time.strftime('%Y-%m-%d'))
            lines.append('----------------')
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='ActivityLogs.pdf')


class UserAdminSite(admin.ModelAdmin):
    model = User
    list_display = ['id', 'username', 'email']
    actions = ['generateReport']
    #Code for deleting default actions
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
    
        return actions

    def generateReport(modeladmin,request,queryset):
        buf = io.BytesIO()
        c= canvas.Canvas(buf, pagesize=letter,bottomup=0)
        textob = c.beginText()
        textob.setTextOrigin(inch,inch)
        textob.setFont("Helvetica",14)

        lines  = []
        lines.append("List Of Users")
        lines.append("")
        for log in queryset:
            if not log.is_staff:
                lines.append('ID: '+ str(log.id))
                lines.append('Username: '+ log.username)
                lines.append('Email: ' + log.email)

                user = JobSeeker.objects.filter(user_id = log)

                if user:
                    lines.append('Account Type: JobSeeker')
                else:
                    lines.append('Account Type: Company')
                if log.is_active:
                    lines.append('Status: Active')
                else:
                    lines.append('Status: Disabled')
                lines.append('----------------')
        for line in lines:
            textob.textLine(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='ListOfUsers.pdf')
admin.site.unregister(User)
admin.site.register(User, UserAdminSite)
admin.site.register(Company, CompanyAdminSite)
admin.site.register(JobSeeker, JobSeekerAdminSite)
admin.site.register(Jobs, JobAdminSite)
admin.site.register(JobApplication, JobApplicationSite)
admin.site.register(ActivityLogs, ActivityLogSite)