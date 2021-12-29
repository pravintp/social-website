from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .utils import authenticate_user, add_user

# Create your views here.


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate_user(request, form)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Authenticated successfully")
                return HttpResponse("Disabled account")
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = add_user(user_form)
            return render(request, "account/register_done.html", {"new_user": new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, "account/register.html", {"user_form": user_form})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST, files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile")

        return render(
            request,
            "account/edit.html",
            {"user_form": user_form, "profile_form": profile_form},
        )

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def user_list(request):
    return render(
        request,
        "account/user/list.html",
        {"section": "people", "users": User.objects.filter(is_active=True)},
    )


@login_required
def user_detail(request, username):
    return render(
        request,
        "account/user/detail.html",
        {
            "section": "people",
            "user": get_object_or_404(User, username=username, is_active=True),
        },
    )
