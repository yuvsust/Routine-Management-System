from django.shortcuts import render, redirect
from django.forms import modelform_factory, formset_factory, modelformset_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_only, allowed_user
from accounts.models import User, Teacher, TeacherEngagement
from accounts.forms import TeacherProfileForm, UserProfileForm
from .models import Course, Room, Class
from .forms import CourseRegisterForm, RoomRegisterForm


@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, "core/admin_dashboard.html")


@login_required(login_url='login')
@allowed_user(allowed_roles=['teacher'])
def teacherProfile(request):
    user = request.user
    teacher = request.user.teacher
    informationForm, engagementForm = None, None

    if request.method == 'POST':
        print(request.POST)
        if 'uploadEngagement' in request.POST:
            print("Upload Engagement")

            PartialEngagementForm = modelform_factory(
                Teacher, form=TeacherProfileForm, fields=("time_table",)
            )
            engagementForm = PartialEngagementForm(
                request.POST, instance=teacher)

            if engagementForm.is_valid():
                form = engagementForm.save()
                # Mark engaged in the database
                engagement = TeacherEngagement.objects.filter(
                    teacher=teacher, time_table__in=engagementForm.cleaned_data['time_table'])
                for i in range(len(engagement)):
                    engagement[i].status = 'ENG'
                    engagement[i].save()
            else:
                print(engagementForm.errors)

        elif 'updateInformation' in request.POST:
            informationForm = UserProfileForm(
                request.POST, request.FILES, instance=user)

            if "phone_number" in request.POST:
                PartialEngagementForm = modelform_factory(
                    Teacher, form=TeacherProfileForm, fields=("phone_number",)
                )
                engagementForm = PartialEngagementForm(
                    request.POST, instance=teacher)
                if engagementForm.is_valid():
                    engagementForm.save()
                else:
                    messages.error(
                        request, "Enter a valid phone number (e.g. 01711111111 or +8801711111111)")

            if informationForm.is_valid():
                informationForm.save()
            else:
                informationForm = informationForm

    if not informationForm:
        informationForm = UserProfileForm(instance=user)
    engagementForm = TeacherProfileForm(instance=teacher)
    context = {'informationForm': informationForm,
               'engagementForm': engagementForm}

    return render(request, "core/teacher_profile.html", context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin', 'student', 'teacher'])
def viewRoutine(request):
    return render(request, "core/admin_dashboard.html")


@login_required(login_url='login')
@admin_only
def createRoutine(request):
    ClassFormSet = modelformset_factory(
        Class, exclude=('status',), max_num=320, extra=2)
    formset = ClassFormSet()
    teachers = Teacher.objects.all()
    courses = Course.objects.all()
    rooms = Room.objects.all()
    classes11 = Class.objects.classesOfSemester("11")
    classes12 = Class.objects.classesOfSemester("12")
    classes21 = Class.objects.classesOfSemester("21")
    classes22 = Class.objects.classesOfSemester("22")
    classes31 = Class.objects.classesOfSemester("31")
    classes32 = Class.objects.classesOfSemester("32")
    classes41 = Class.objects.classesOfSemester("41")
    classes42 = Class.objects.classesOfSemester("42")

    if request.method == "POST":
        classForm = ClassFormSet(request.POST)
        if classForm.is_valid():
            classForm.save()
            return redirect('create_routine')
    context = {'teachers': teachers,
               'courses': courses,
               'rooms': rooms,
               'classes11': classes11,
               'classes12': classes12,
               'classes21': classes21,
               'classes22': classes22,
               'classes31': classes31,
               'classes32': classes32,
               'classes41': classes41,
               'classes42': classes42,
               'formset': formset}
    return render(request, "core/create_routine.html", context)


@login_required(login_url='login')
@admin_only
def registerCourse(request):
    form = CourseRegisterForm

    if request.method == 'POST':
        form = CourseRegisterForm(request.POST)
        if form.is_valid():
            course = form.save()
            course_code = form.cleaned_data.get('course_code')
            messages.success(
                request, "New Course ( " + course_code + " ) is registered !!", extra_tags='success')
            redirect('course_register')

    context = {'form': form}
    return render(request, "core/course_register.html", context)


@login_required(login_url='login')
@admin_only
def registerRoom(request):
    form = RoomRegisterForm

    if request.method == 'POST':
        form = RoomRegisterForm(request.POST)
        if form.is_valid():
            room = form.save()
            room_id = form.cleaned_data.get('room_id')
            messages.success(
                request, "New Room ( " + room_id + " ) is registered !!", extra_tags='success')
            redirect('room_register')

    context = {'form': form}
    return render(request, "core/room_register.html", context)
