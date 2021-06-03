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
    form1 = UserProfileForm(instance=user)
    form2 = TeacherProfileForm(instance=teacher)

    if request.method == 'POST':
        form1 = UserProfileForm(request.POST, request.FILES, instance=user)
        form2 = TeacherProfileForm(
            request.POST, request.FILES, instance=teacher)

        if form1.is_valid():
            form1.save()
        else:
            print(form1.errors)

        if form2.is_valid():
            form2.save()
        else:
            print(form2.errors)
    context = {'form1': form1, 'form2': form2}
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
