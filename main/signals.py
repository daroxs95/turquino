from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import caches

@receiver(post_save)
def clean_cache_on_db_change(sender, **kwargs):
    caches['main_cache'].clear()
    print("cache reseted")
