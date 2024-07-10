from django.core.cache import cache

from catalog.models import Category
from config.settings import CACHE_ENABLED


def get_categories_cache():
    if not CACHE_ENABLED:
        return list(Category.objects.all())

    key = 'category_list'
    categories = cache.get(key)
    if categories is not None:
        return categories
    categories = list(Category.objects.all())
    cache.set(key, categories)
    return categories
