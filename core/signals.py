from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import News, Tag


@receiver(m2m_changed, sender=News.tags.through)
def update_times_used(sender, instance, action, reverse, pk_set, **kwargs):
    if action in ["post_add", "post_remove"]:
        for tag in Tag.objects.filter(pk__in=pk_set):
            tag.times_used = tag.news_set.count()
            tag.save()
    elif action == "post_clear":
        for tag in Tag.objects.all():
            tag.times_used = tag.news_set.count()
            tag.save()
