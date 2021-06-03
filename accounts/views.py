from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, TeacherProfileForm, UserProfileForm
from .models import Student, Teacher
from .decorators import unauthenticated, allowed_user, admin_only
import ast


@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, "accounts/home.html")


@login_required(login_url='login')
@allowed_user(allowed_roles=['teacher'])
def teacherProfile(request):
    user = request.user
    teacher = request.user.teacher

    if request.method == 'POST':
        print(request.POST)
        if 'updateEngagement' in request.POST:
            print("Update Engagement")
            engagementForm = TeacherProfileForm(
                request.POST, instance=teacher)

            if engagementForm.is_valid():
                engagementForm.save()
                print(engagementForm.cleaned_data)
            else:
                print(engagementForm.errors)

        elif 'updateInformation' in request.POST:
            informationForm = UserProfileForm(
                request.POST, request.FILES, instance=user)
            engagementForm = TeacherProfileForm(
                request.POST, instance=teacher)

            if "phone_number" in request.POST:
                phone = request.POST.get("phone_number")
                if engagementForm.is_valid():
                    print("##############################")
                    print(engagementForm.cleaned_data)
                    engagementForm.save()
                else:
                    print(engagementForm.errors)
                    messages.error(
                        request, "Enter a valid phone number (e.g. 01711111111 or +8801711111111)")

            if informationForm.is_valid():
                informationForm.save()
                print(informationForm.cleaned_data)
            else:
                print(informationForm.errors)

    informationForm = UserProfileForm(instance=user)
    engagementForm = TeacherProfileForm(instance=teacher)
    context = {'informationForm': informationForm,
               'engagementForm': engagementForm}
    return render(request, "accounts/teacher_profile.html", context)


@allowed_user(allowed_roles=['admin', 'student', 'teacher'])
def viewRoutine(request):
    return render(request, "accounts/view_routine.html")


@unauthenticated
def register(request):

    form = CreateUserForm()
    context = {'form': form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            userEmail = form.cleaned_data.get('email')
            messages.success(
                request, 'Account was created for ' + userEmail)

            isStudent = form.cleaned_data.get('is_student')
            isTeacher = form.cleaned_data.get('is_teacher')
            if isStudent:
                Student.objects.create(user=user)
            elif isTeacher:
                Teacher.objects.create(user=user)
            return redirect('login')
        else:
            error_list = form.errors.as_json()
            error_list = ast.literal_eval(error_list)
            messages.info(request, error_list['password2'][0]['message'])
            return redirect('register')

    return render(request, "accounts/register.html", context)


@unauthenticated
def loginUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Email or Password is incorrect')
            return render(request, "accounts/login.html")
    context = {}
    return render(request, "accounts/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('login')
