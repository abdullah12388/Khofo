from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from PIL import Image
import os

User_ = get_user_model()


# Create your models here.

class AdsManager(models.Model):
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
    ssn_id = models.CharField(max_length=500, verbose_name=_('ssn_id'))
    birth_date = models.DateField(verbose_name=_('birth_date'))
    gender = models.PositiveSmallIntegerField(choices=GENDER_CHOICES, verbose_name=_('gender'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))

    class Meta:
        verbose_name = _("AdsManager")
        verbose_name_plural = _("AdsManagers")

    def __str__(self):
        return self.user.username

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super(AdsManager, self).save(force_insert=False, force_update=False, using=None,update_fields=None)
        resize_img(self.profile_picture)

class Advertisement(models.Model):
    Duration_CHOICES = [
        (15, '15s'),
        (30, '30s'),
        (45, '45s'),
        (60, '60s'),
        (75, '75s'),
        (90, '90s'),
        (105, '105s'),
        (120, '120s'),
        # (150, '2.5m'),
        # (180, '3m'),
    ]
    Interval_CHOICES = [
        (5, '5m'),
        (10, '10m'),
    ]

    advertiserName = models.CharField(max_length=500, verbose_name=_('advertiser_name'))
    advertiserEmail = models.EmailField(max_length=254, verbose_name=_('advertiser_email'))
    advertiserPhone = models.CharField(max_length=500, verbose_name=_('advertiser_phone'))
    image = models.FileField(upload_to='images/', verbose_name=_('image'))
    page = models.CharField(max_length=500, verbose_name=_('page'))
    startDate = models.DateField(verbose_name=_('start_date'))
    endDate = models.DateField(verbose_name=_('end_date'))
    show_num = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('show_num'))
    duration = models.PositiveIntegerField(choices=Duration_CHOICES, blank=True, null=True, verbose_name=_('duration'))
    interval = models.PositiveIntegerField(choices=Interval_CHOICES, blank=True, null=True, verbose_name=_('interval'))
    nextShowTime = models.DateField(blank=True, null=True, verbose_name=_('next_show-time'))
    advertiseManager = models.ForeignKey(to=AdsManager, on_delete=models.CASCADE, verbose_name=_('advertise_manager'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Advertisement")
        verbose_name_plural = _("Advertisements")

    def __str__(self):
        return self.advertiserName

    def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
        super(Advertisement, self).save(force_insert=False, force_update=False, using=None,update_fields=None)
        resize_img(self.image)


@receiver(post_save, sender=AdsManager)
def enable_is_delegate(sender, instance=None, created=False, **kwargs):
    if created:
        user = User_.objects.get(id=instance.user.id)
        user.is_ads_manager = True
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