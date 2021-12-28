from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import ImageCreateForm
from .models import Image

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
        form = ImageCreateForm(initial={"user": request.user})
    return render(request, "images/image/create.html", {"form": form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(
        request, "images/image/detail.html", {"section": "images", "image": image}
    )
