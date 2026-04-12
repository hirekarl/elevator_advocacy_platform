from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Building
from .tasks import fetch_building_news

@receiver(post_save, sender=Building)
def trigger_news_search(sender, instance, created, **kwargs):
    """
    (Deprecated) Moved trigger to views.py to prevent searches for 
    invalid buildings or incomplete geocoding.
    """
    pass
