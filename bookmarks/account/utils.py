from django.contrib.auth import authenticate

from .models import Profile


def authenticate_user(request, form):
    user = authenticate(request, username=form["username"], password=form["password"])
    return user


def add_user(form):
    new_user = form.save(commit=False)
    new_user.set_password(form.cleaned_data["password"])
    new_user.save()
    Profile.objects.create(user=new_user)
    return new_user
