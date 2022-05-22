from django.urls import path, reverse
from . import views
from .forms import *
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.loginPage, name='login'),\
    path('home/', views.home, name='home'),
    path('company_home/', views.companyHome, name='company'),
    path('gettingstarted/', views.gettingStarted, name='gettingstarted'),
    path('seeker/', views.seekerForm, name='seeker_form'),
    path('company/', views.companyForm , name = 'company_form'),
    path('logoutConfirm', views.logoutConfirm, name='logout_confirm'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('register/', views.registerPage, name = 'register'),
    path('profile/', views.userProfile, name='user_profile'),
    path('companyprofile/', views.companyProfile, name = 'company_profile'),
    path('ReturnProfile/', views.backtoProfile, name='return_to_profile'),
    path('removeSkill/<int:pk>/', views.seekerRemoveSkills, name='remove_skill'),
    path('removeWork/<int:pk>/',  views.seekerRemoveWork, name='remove_work'),
    path('EditJob/<int:pk>/', views.companyEditJob, name = 'company_edit_job'),
    path('Delete/<int:pk>/', views.companyDeletejob, name = 'company_delete_job'),
    path('Job/<int:pk>/', views.viewJob, name='viewJob'),
    path('Applications/<int:pk>', views.companyViewApplications, name= 'company_view_applications'),
    path('Reject/<int:pk>/<int:application_id>', views.companyRejectApplication, name= 'company_reject_application'),
    path('Accept/<int:pk>/<int:application_id>', views.companyAcceptApplication, name= 'company_accept_application'),
    path('Revoke/<int:pk>/<int:application_id>', views.companyRevokeAction, name= 'company_revoke_action'),
    path('deleteAccount/', views.deleteAccount, name='delete_account'),
    path('myApplications/', views.seekerViewApplications, name='seeker_view_applications'),
    path('deleteremove/<int:pk>/', views.seekerCancelRemoveApplication, name='seeker_canceldelete_applications'),
    path('viewCompany/<int:pk>/', views.seekerViewCompany, name='seeker_view_company'),
    path('viewSeeker/<int:pk>/', views.companyViewSeeker, name='company_view_seeker'),
    path('changePassword/', auth_views.PasswordChangeView.as_view(template_name ='base/user-change-password.html', form_class = UserCompanyPasswordChangeForm), name ='change_password'),
    path('PasswordChanged/', auth_views.PasswordChangeDoneView.as_view(template_name='base/user-change-password-done.html'), name='password_change_done'),
    #reset_password enter email
   path('reset_password/', 
   auth_views.PasswordResetView.as_view(template_name="base/password_reset.html", 
   form_class =UserPasswordResetForm), 
   name = "reset_password"),
   
   #reset_password sent message
   path('reset_password_sent/', 
   auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_sent.html"), 
   name = "password_reset_done"),

   #reset_password new password creation
   path('reset/<uidb64>/<token>/',
   auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_form.html",
   form_class = UserPasswordChangeForm), 
   name="password_reset_confirm"),

   #reset_password new password creation success
   path('reset_password/_complete', 
   auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_done.html"), 
   name="password_reset_complete"),
]