from django.contrib.auth import authenticate

from .models import Profile
from actions.models import Action
from actions.utils import create_action


def authenticate_user(request, form):
    user = authenticate(request, username=form["username"], password=form["password"])
    return user


def add_user(form):
    new_user = form.save(commit=False)
    new_user.set_password(form.cleaned_data["password"])
    new_user.save()
    Profile.objects.create(user=new_user)
    create_action(new_user, "has created an account")
    return new_user


def get_actions(user):
    actions = Action.objects.exclude(user=user)
    following_ids = user.following.values_list("id", flat=True)
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.prefetch_related("target")[:10]
    return actions
