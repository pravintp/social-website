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
    redis_connector.zincrby("image_ranking", 1, image.id)
    return redis_connector.incr(f"image:{image.id}:views")


def get_most_viewed():
    image_ranking = redis_connector.zrange("image_ranking", 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    return most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
