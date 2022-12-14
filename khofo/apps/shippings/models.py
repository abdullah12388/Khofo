# django
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# models
from ..user.models import Country

User_ = get_user_model()


# Create your models here.


class Shipping(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    address = models.CharField(max_length=500, verbose_name=_('address'))
    phone = models.CharField(max_length=100, verbose_name=_('phone'))
    website = models.URLField(max_length=1000, verbose_name=_('website'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_by',
                                   verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Shipping")
        verbose_name_plural = _("Shippings")

    def __str__(self):
        return self.user.username


class ShippingCondition(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name_ar'))
    price = models.FloatField(verbose_name=_('price'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Shipping Condition")
        verbose_name_plural = _("Shipping Conditions")

    def __str__(self):
        return str(self.name)


class ShippingTime(models.Model):
    EXPRESS = 'express'
    AIR_FREIGHT = 'air freight'
    SEA_FREIGHT = 'sea freight'
    SHIPPING_TYPE_CHOICES = [
        (EXPRESS, 'express'),
        (AIR_FREIGHT, 'air freight'),
        (SEA_FREIGHT, 'sea freight'),
    ]
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name=_('Country'))
    shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE)
    shipping_type = models.CharField(choices=SHIPPING_TYPE_CHOICES, default=EXPRESS, max_length=100)
    days = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Shipping Time")
        verbose_name_plural = _("Shipping Times")

    def __str__(self):
        return str(self.days)


class Express(models.Model):
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name=_('country'))
    slice_min = models.FloatField(verbose_name=_('slice_min'))
    slice_max = models.FloatField(verbose_name=_('slice_max'))
    shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, verbose_name=_('shipping_company'))
    rate = models.FloatField(verbose_name=_('rate'))
    initial_cost = models.FloatField(verbose_name=_('initial_cost'))
    price_average = models.FloatField(max_length=4, verbose_name=_('price_average'))
    transport_time = models.FloatField(verbose_name=_('transport_time'))
    shipping_condition = models.ForeignKey(to=ShippingCondition, on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name=_('shipping_condition'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Express")
        verbose_name_plural = _("Express")

    def __str__(self):
        return str("price: " + str(self.price_average)) + str("//slice_min: " + str(self.slice_min)) \
               + str("//slice_max: " + str(self.slice_max))


class AirFreight(models.Model):
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name=_('country'))
    slice_min = models.FloatField(verbose_name=_('slice_min'))
    slice_max = models.FloatField(verbose_name=_('slice_max'))
    shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, verbose_name=_('shipping_company'))
    rate = models.FloatField(verbose_name=_('rate'))
    initial_cost = models.FloatField(verbose_name=_('initial_cost'))
    price_average = models.FloatField(verbose_name=_('price_average'))
    transport_time = models.FloatField(verbose_name=_('transport_time'))
    shipping_condition = models.ForeignKey(to=ShippingCondition, on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name=_('shipping_condition'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Air Freight")
        verbose_name_plural = _("Air Freights")

    def __str__(self):
        return str(self.shipping_company)


class SeaFreight(models.Model):
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE, verbose_name=_('country'))
    slice_min = models.FloatField(verbose_name=_('slice_min'))
    slice_max = models.FloatField(verbose_name=_('slice_max'))
    shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, verbose_name=_('shipping_company'))
    rate = models.FloatField(verbose_name=_('rate'))
    initial_cost = models.FloatField(verbose_name=_('initial_cost'))
    price_average = models.FloatField(verbose_name=_('price_average'))
    transport_time = models.FloatField(verbose_name=_('transport_time'))
    shipping_condition = models.ForeignKey(to=ShippingCondition, on_delete=models.CASCADE, null=True, blank=True,
                                           verbose_name=_('shipping_condition'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Sea Freight")
        verbose_name_plural = _("Sea Freights")

    def __str__(self):
        return str(self.shipping_company)


@receiver(post_save, sender=Shipping)
def enable_is_shipping(sender, instance=None, created=False, **kwargs):
    if created:
        user = User_.objects.get(id=instance.user.id)
        user.is_shipping = True
        user.save()
