from django.shortcuts import render
from django.forms import modelform_factory
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_only, allowed_user
from accounts.models import User, Teacher, Engagement
from accounts.forms import TeacherProfileForm, UserProfileForm


@login_required(login_url='login')
@admin_only
def home(request):
    return render(request, "core/home.html")


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
                engagement = Engagement.objects.filter(
                    teacher=teacher, time_table__in=engagementForm.cleaned_data['time_table'])
                for i in range(len(engagement)):
                    engagement[i].status = 'ENG'
                    engagement[i].save()

                print(engagementForm.cleaned_data)
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


@allowed_user(allowed_roles=['admin', 'student', 'teacher'])
def viewRoutine(request):
    return render(request, "core/view_routine.html")
