from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User_ = get_user_model()


class Provider(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    working_field = models.CharField(max_length=500, verbose_name=_('working_field'))
    phone = models.CharField(max_length=100, verbose_name=_('phone'))
    website = models.URLField(max_length=1000, verbose_name=_('website'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))

    class Meta:
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=Provider)
def enable_is_delegate(sender, instance=None, created=False, **kwargs):
    if created:
        user = User_.objects.get(id=instance.user.id)
        user.is_provider = True
        user.save()
