from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ImageCreateForm

# Create your views here.


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            image = form.save()
            messages.success(request, "Image added successfully")
            return redirect(image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET, initial={"user": request.user})
    return render(request, "images/image/create.html", {"form": form})
