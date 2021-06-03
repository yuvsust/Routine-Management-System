from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import static
from .views import home, loginUser, logoutUser, register, viewRoutine, teacherProfile
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name="home"),
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('register/', register, name="register"),
    path('view-routine/', viewRoutine, name="view_routine"),
    path('profile/', teacherProfile, name="teacher_profile"),


    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="accounts/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),
]


'''
1 - Submit Email Form                       =>  PasswordResetView.as_view()
1 - Email sent success message              =>  PasswordChangeDoneView.as_view()
1 - Link to password reset form in email    =>  PasswordResetConfirmView.as_view()
1 - Password successfully changed message   =>  PasswordResetCompleteView.as_view()
'''
