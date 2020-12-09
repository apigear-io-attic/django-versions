from django.db import models
import reversion
# Create your models here.

from django.db.models.signals import post_save
from actstream import action


@reversion.register()
class Document(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=200)
    content = models.TextField()

    def __str__(self) -> str:
        return self.name


def was_saved_handler(sender, instance, created, **kwargs):
    action.send(instance, verb='was saved')


post_save.connect(was_saved_handler, sender=Document)
