from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Profile, Contact


def authenticate_user(request, form):
    user = authenticate(request, username=form["username"], password=form["password"])
    return user


def add_user(form):
    new_user = form.save(commit=False)
    new_user.set_password(form.cleaned_data["password"])
    new_user.save()
    Profile.objects.create(user=new_user)
    return new_user


def follow_or_unfollow(user_id, from_user, action):
    status = "success"
    if user_id and action:
        try:
            to_user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=from_user, user_to=to_user)
            else:
                Contact.objects.filter(user_from=from_user, user_to=to_user).delete()
        except User.DoesNotExist:
            status = "fail"
    else:
        status = "fail"
    return status
