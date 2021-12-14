import redis
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Image
from django.conf import settings


redis_connector = redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)


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


def get_total_views(image):
    return redis_connector.incr(f"image:{image.id}:views")
