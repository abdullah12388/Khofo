from django.conf import settings
from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _

from ..delegates.models import Delegate
from ..products.models import Product, Category, SubCategory
from ..providers.models import Provider
from ..shippings.models import Shipping
from ..user.models import BuyerUserDetails, Country
from ..delegates.models import Delegate


# Create your models here.


class Iloc(models.Model):
    user = models.ForeignKey(to=BuyerUserDetails, on_delete=models.CASCADE, verbose_name=_('user'))
    user_address = models.CharField(max_length=500, verbose_name=_('user_address'))
    user_country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name="Iloc_user_country",
                                     verbose_name=_('user_country'))
    user_region = models.CharField(max_length=500, verbose_name=_('user_region'))
    user_city = models.CharField(max_length=500, verbose_name=_('user_city'))
    user_zip_code = models.CharField(max_length=50, verbose_name=_('user_zip_code'))
    user_mobile = models.CharField(max_length=50, verbose_name=_('user_mobile'))
    importer_country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name="Iloc_importer_country",
                                         verbose_name=_('importer_country'))
    importer_port = models.CharField(max_length=500, verbose_name=_('importer_port'))
    order_id = models.CharField(max_length=200, verbose_name='order_id')
    order_amount = models.PositiveIntegerField(verbose_name=_('order_amount'))
    shipping_amount = models.PositiveIntegerField(verbose_name=_('shipping_amount'))
    exproter_bank = models.CharField(max_length=500, verbose_name=_('exproter_bank'))
    exproter_account_number = models.CharField(max_length=200, verbose_name=_('exproter_account_number'))
    exproter_bank_fees = models.PositiveIntegerField(verbose_name=_('exproter_bank_fees'))
    importer_bank = models.CharField(max_length=500, verbose_name=_('importer_bank'))
    iloc_number = models.CharField(max_length=200, verbose_name='iloc_number')
    iloc_amount = models.PositiveIntegerField(verbose_name=_('iloc_amount'))
    iloc_file = models.FileField(upload_to='iloc/', verbose_name=_('iloc_file'))
    shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, verbose_name=_('shipping_company'))
    arrival_date = models.DateField(verbose_name=_('arrival_date'))
    shipping_file = models.FileField(upload_to='iloc_shipping/', verbose_name=_('shipping_file'))
    delivered_date = models.DateField(verbose_name=_('delivered_date'))

    class Meta:
        verbose_name = _("Iloc")
        verbose_name_plural = _("Ilocs")

    def __str__(self):
        return str(self.user)


class ChatMessages(models.Model):
    STUFF_ = "stuff"
    CLIENT = "client"
    SENDER_CHOICES = [
        (STUFF_, "stuff"),
        (CLIENT, "client"),
    ]
    message = models.CharField(max_length=500, verbose_name=_('message'))
    stuff = models.ForeignKey(to=Delegate, on_delete=models.CASCADE, verbose_name=_('stuff'))
    buyer = models.ForeignKey(to=BuyerUserDetails, on_delete=models.CASCADE, verbose_name=_('buyer'))
    sender = models.CharField(choices=SENDER_CHOICES, default=STUFF_, max_length=100, verbose_name=_('sender'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    def __str__(self):
        return str(self.sender)
