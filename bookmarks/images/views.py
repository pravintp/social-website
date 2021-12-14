from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from django.contrib.auth.models import User

from .forms import ImageCreateForm
from .utils import get_images_of_current_paginator
from .models import Image
from actions.utils import create_action

# Create your views here.


@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            image = form.save()
            create_action(request.user, "bookmarked image", image)
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


@ajax_required
@login_required
@require_POST
def image_like_view(request):
    image_id = request.POST.get("id")
    action = request.POST.get("action")
    if image_id and action:
        image = Image.objects.get(id=image_id)
        if action == "like":
            image.like(request.user)
            create_action(request.user, "likes", image)
        else:
            image.unlike(request.user)
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})


@login_required
def image_list(request):
    page = request.GET.get("page")
    images = get_images_of_current_paginator(page)
    if request.is_ajax():
        return render(
            request,
            "images/image/list_ajax.html",
            {"section": "images", "images": images},
        )
    return render(
        request, "images/image/list.html", {"section": "images", "images": images}
    )
