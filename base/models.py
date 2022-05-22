from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from tkinter import CASCADE
from turtle import Turtle
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
import datetime
# Create your models here.

class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    user_image = models.ImageField(null = True, blank = True, upload_to = "images", default = 'default_image.png')
    location = models.CharField(max_length=200, null = True, blank = True)
    description = models.TextField(null = True, blank = True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name

class JobSeeker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_image = models.ImageField(null = True, blank = True, upload_to = "images", default= 'default_image.png')
    user_resume = models.FileField(null = True, blank = True, upload_to ="files" )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    recent_job = models.CharField(max_length=200, null=True, blank = True)
    description= models.TextField(null = True, blank=True)
    is_active = models.BooleanField(default=True)
    def __str__(self) -> str:
        return self.user.username

class SeekerSkills(models.Model):
    seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length= 50, null = True, blank= True)

    def __str__(self) -> str:
        return self.skill_name

def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class SeekerPreviousWork(models.Model):
    seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    name = models.CharField(max_length= 150)
    description = models.TextField()
    yearStarted = models.PositiveIntegerField(
        default=1999, validators=[MinValueValidator(1984), max_value_current_year])
    yearEnded = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(1984), max_value_current_year])

    def __str__(self) -> str:
        return self.name

class Jobs(models.Model):
    company = models.ForeignKey(Company, on_delete= models.CASCADE)
    title = models.CharField(max_length=150)
    salary= models.CharField(max_length=40, null =True, blank = True)
    qualification = models.CharField(max_length=1000, null = True, blank= True)
    job_description = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    ispart_time = models.BooleanField(default= False)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    date_applied = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length = 30, default = 'Pending')

class ActivityLogs(models.Model):
    log = models.TextField()
    time = models.DateTimeField(auto_now_add = True, null = True, blank= True)