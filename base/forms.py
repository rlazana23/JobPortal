from dataclasses import field, fields
from pyexpat import model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker, Company, SeekerPreviousWork, SeekerSkills, Jobs
from django.forms import ModelForm


class UserCompanyPasswordChangeForm(PasswordChangeForm):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'required':'Please Enter Password',
            'name': 'old_password',
            'id' : 'old_password',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'Old Password',
            'maxlength' : '30',
        })
        self.fields['new_password1'].widget.attrs.update({
            'required':'Please Enter Password',
            'name': 'new_password1',
            'id' : 'id_new_password1',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'New Password',
            'maxlength' : '30',
        })
        self.fields['new_password2'].widget.attrs.update({
            'required':'Please enter confirm  password',
            'name': 'new_password2',
            'id' : 'id_new_password2',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'Confirm  New Password',
            'maxlength' : '30',
        })
        self.fields['old_password'].label = ''
        self.fields['new_password1'].label = ''
        self.fields['new_password2'].label = ''
        self.fields['old_password'].help_text =  None
        self.fields['new_password1'].help_text =  None
        self.fields['new_password2'].help_text =  None
class UserPasswordResetForm(PasswordResetForm):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'required':'Please Enter your Email',
            'name': 'email',
            'id' : 'email',
            'type': 'email',
            'class': 'form-input',
            'placeholder': 'Email Address',
            'maxlength' : '30',
        })

class UserPasswordChangeForm(SetPasswordForm):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'required':'Please Enter Password',
            'name': 'new_password1',
            'id' : 'id_new_password1',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'New Password',
            'maxlength' : '30',
        })
        self.fields['new_password2'].widget.attrs.update({
            'required':'Please enter confirm  password',
            'name': 'new_password2',
            'id' : 'id_new_password2',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'Confirm  New Password',
            'maxlength' : '30',
        })

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            'unique': 'Username Already Exist',
            'required':'Please enter a valid username',
            'help_texts' : 'Please enter a valid Username',
            'name': 'username',
            'id' : 'username',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Username',
            'maxlength' : '16',
            'minlength' : '6'
        })
        
        self.fields["email"].widget.attrs.update({
            'unique': 'Email Already Exist',
            'required':'Please enter a valid email address',
            'name': 'email',
            'id' : 'email',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Email Address',
            'maxlength' : '60',
        })
        self.fields["password1"].widget.attrs.update({
            'name': 'password',
            'id' : 'password',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'Password',
            'maxlength' : '16',
            'minlength' :  '8'
        })
        self.fields["password2"].widget.attrs.update({
            'name': 'confirm-password',
            'id' : 'confirm-password',
            'type': 'password',
            'class': 'form-input',
            'placeholder': 'Confirm Password',
            'maxlength' : '16',
            'minlength' :  '8'
        })
        self.fields["username"].help_text = None
        self.fields["password1"].help_text = None
        self.fields["password2"].help_text = None
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SeekerForm(ModelForm):

    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'required':'Please Enter your firstname',
            'name': 'first_name',
            'id' : 'first_name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'First Name',
            'maxlength' : '30',
        })
        self.fields['last_name'].widget.attrs.update({
            'required':'Please Enter your lastname',
            'name': 'last_name',
            'id' : 'last_name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Last Name',
            'maxlength' : '30',
        })
    class Meta:
        model = JobSeeker
        fields = ['first_name', 'last_name']

class UploadImageForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['user_image'].label = ''
    class Meta:
        model = JobSeeker
        fields = ['user_image']

class UploadImageCompanyForm(ModelForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['user_image'].label = ''
    class Meta:
        model = Company
        fields = ['user_image']

class UploadFileForm(ModelForm):
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['user_resume'].widget.attrs.update({
            'accept': '.doc, .docx',
            'name' : 'user_resume',
            'id' : 'user_resume',
        })
        self.fields['user_resume'].label = ''
    class Meta:
        model = JobSeeker
        fields = ['user_resume']

class EditSeekerForm(ModelForm):
    class Meta:
        model = JobSeeker
        fields = ['first_name', 'last_name', 'description']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'required':'Please Enter your first name.',
            'name': 'first_name',
            'id' : 'first_name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'First Name',
            'maxlength' : '30',
        })
        self.fields['last_name'].widget.attrs.update({
            'required':'Please Enter your first name.',
            'name': 'last_name',
            'id' : 'last_name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Last Name',
            'maxlength' : '30',
        })
        self.fields['description'].widget.attrs.update({
            'name': 'description',
            'id' : 'description',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Description',
            'maxlength' : '500',
        })

class EditCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'description']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'name': 'name',
            'id' : 'name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Company Name',
            'maxlength' : '30',
        })
        self.fields['location'].widget.attrs.update({
            'required':'Please Enter your Company Location.',
            'name': 'location',
            'id' : 'location',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Company Location',
            'maxlength' : '30',
        })
        self.fields['description'].widget.attrs.update({
            'name': 'description',
            'id' : 'description',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Company Description',
            'maxlength' : '500',
        })

class AddSeekerSkillForm(ModelForm):
    class Meta:
        model = SeekerSkills
        fields = ['skill_name']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['skill_name'].widget.attrs.update({
            'required':'Please Enter your Skill',
            'name': 'skill_name',
            'id' : 'skill_name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Skill',
            'maxlength' : '30',
    })

class PostJob(ModelForm):
    class Meta:
        model = Jobs
        fields  = ['title','job_description','salary','qualification', 'ispart_time']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'required':'Please Enter Your Job Title',
            'name': 'title',
            'id' : 'title',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Job Title',
            'maxlength' : '30',
        })
        self.fields['job_description'].widget.attrs.update({
            'required':'Please Enter Your Job Description',
            'name': 'job_description',
            'id' : 'job_description',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Job Description',
            'maxlength' : '500',
        })
        self.fields['salary'].widget.attrs.update({
            'required':'Please Enter Your Job Salary',
            'name': 'salary',
            'id' : 'salary',
            'type': 'number',
            'class': 'form-input',
            'placeholder': 'Salary',
            'maxlength' : '30',
        })
        self.fields['qualification'].widget.attrs.update({
            'required':'Please Enter Your Job Qualification',
            'name': 'qualification',
            'id' : 'qualification',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Qualification',
            'maxlength' : '1000',
        })
        self.fields['ispart_time'].label = "Part Time?"
        

class EditJob(ModelForm):
    class Meta:
        model = Jobs
        fields  = ['title','job_description','salary','qualification', 'ispart_time', 'is_active']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'required':'Please Enter Your Job Title',
            'name': 'title',
            'id' : 'title',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Job Title',
            'maxlength' : '30',
        })
        self.fields['job_description'].widget.attrs.update({
            'required':'Please Enter Your Job Description',
            'name': 'job_description',
            'id' : 'job_description',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Job Description',
            'maxlength' : '500',
        })
        self.fields['salary'].widget.attrs.update({
            'required':'Please Enter Your Job Salary',
            'name': 'salary',
            'id' : 'salary',
            'type': 'number',
            'class': 'form-input',
            'placeholder': 'Salary',
            'maxlength' : '30',
        })
        self.fields['qualification'].widget.attrs.update({
            'required':'Please Enter Your Job Qualification',
            'name': 'qualification',
            'id' : 'qualification',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Qualification',
            'maxlength' : '1000',
        })
        self.fields['ispart_time'].label = "Part Time?"
        self.fields['ispart_time'].label = "Hiring? "

class PreviousWorkForm(ModelForm):
    class Meta:
        model = SeekerPreviousWork
        fields = ['name', 'description', 'yearStarted', 'yearEnded']
    def __init__(self,*args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'required':'Please Enter Your Work Name',
            'name': 'name',
            'id' : 'name',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Work Name',
            'maxlength' : '30',
        })
        self.fields['description'].widget.attrs.update({
            'required':'Please Enter Your Work Description',
            'name': 'description',
            'id' : 'description',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Work Description',
            'maxlength' : '500',
        })
        self.fields['yearStarted'].widget.attrs.update({
            'required':'Please Enter What Year Your Job Started',
            'name': 'yearStarted',
            'id' : 'yearStarted',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Year Started',
            'maxlength' : '4',
        })
        self.fields['yearEnded'].widget.attrs.update({
            'required':'Please Enter What Year Your Job Ended',
            'name': 'yearEnded',
            'id' : 'yearEnded',
            'type': 'text',
            'class': 'form-input',
            'placeholder': 'Year Ended',
            'maxlength' : '4',
        })