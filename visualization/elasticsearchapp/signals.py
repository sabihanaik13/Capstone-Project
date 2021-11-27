from .models import Companies
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Companies)
def index_post(sender, instance, **kwargs):
    print(instance)
    instance.indexing()
