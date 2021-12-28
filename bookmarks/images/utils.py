from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Image


def get_images_of_current_paginator(page):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    return images
