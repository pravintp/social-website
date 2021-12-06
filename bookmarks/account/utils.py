from django.contrib.auth import authenticate


def authenticate_user(request, form):
    user = authenticate(request, username=form["username"], password=form["password"])
    return user
