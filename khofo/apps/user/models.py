# Django
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_delegate = models.BooleanField(default=False)
    is_shipping = models.BooleanField(default=False)
    is_provider = models.BooleanField(default=False)
    is_ads_manager = models.BooleanField(default=False)


class Country(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('name'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")

    def __str__(self):
        return self.name


class BuyerUserDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name=_('country'))
    region = models.CharField(max_length=500, verbose_name=_('region'))
    city = models.CharField(max_length=500, verbose_name=_('city'))
    zip_code = models.CharField(max_length=50,verbose_name=_('zip_code'))
    mobile = models.CharField(max_length=50,  verbose_name=_('mobile'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("BuyerUserDetails")
        verbose_name_plural = _("BuyerUserDetails")

    def __str__(self):
        return self.user.username

    # def save(self, force_insert=False, force_update=False, using=None,update_fields=None):
    #     super(BuyerUserDetails, self).save(force_insert=False, force_update=False, using=None,update_fields=None)
    #     resize_img(self.profile_pic)
