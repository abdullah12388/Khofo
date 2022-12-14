from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from PIL import Image
import os

User_ = get_user_model()


class Delegate(models.Model):
    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = [
        (MALE, "male"),
        (FEMALE, "female"),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    profile_picture = models.ImageField(upload_to='images/', verbose_name=_('profile_picture'))
    phone = models.CharField(max_length=100, verbose_name=_('phone'))
    ssn_id = models.CharField(max_length=500, verbose_name=_('ssnid'))
    birth_date = models.DateField(verbose_name=_('birth_date'))
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, verbose_name=_('gender'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))

    class Meta:
        verbose_name = _("Delegate")
        verbose_name_plural = _("Delegates")

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super(Delegate, self).save(force_insert=False, force_update=False, using=None,update_fields=None)
        resize_img(self.profile_picture)

@receiver(post_save, sender=Delegate)
def enable_is_delegate(sender, instance=None, created=False, **kwargs):
    if created:
        user = User_.objects.get(id=instance.user.id)
        user.is_delegate = True
        user.save()

def resize_img(image1):
    image = Image.open(image1.path)
    size = os.path.getsize(image1.path) / 1048576
    if size >= 1:
        image.save(image1.path, quality=20, optimize=True)
    elif size >= .75:
        image.save(image1.path, quality=50, optimize=True)
    elif size >= .5:
        image.save(image1.path, quality=70, optimize=True)