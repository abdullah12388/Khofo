from django.conf import settings
from django.db import models
from smart_selects.db_fields import ChainedForeignKey
from django.utils.translation import gettext_lazy as _

from ..delegates.models import Delegate
from ..products.models import Product, Category, SubCategory
from ..providers.models import Provider
from ..shippings.models import Shipping
from ..user.models import BuyerUserDetails, Country


# Create your models here.


class Order(models.Model):
    ORDERED = 'ordered'
    PROCESSING = 'processing'
    PREPARED = 'prepared'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    STATUS_CHOICES = [
        (ORDERED, _("ordered")),
        (PROCESSING, _("processing")),
        (PREPARED, _("prepared")),
        (ACCEPTED, _("accepted")),
        (REJECTED, _("rejected")),
        (SHIPPED, _("shipped")),
        (DELIVERED, _("delivered")),
    ]
    DOLLAR = 1
    EG_POUND = 2
    MONEY_CHOICES = [
        (DOLLAR, "$ US dollar"),
        (EG_POUND, "EG pound"),
    ]
    user = models.ForeignKey(to=BuyerUserDetails, on_delete=models.CASCADE, verbose_name=_('user'))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_('category'))
    sub_category = ChainedForeignKey(SubCategory, chained_field="category", chained_model_field="category",
                                     show_all=False, verbose_name=_('sub_category'))
    delegate = models.ForeignKey(to=Delegate, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('delegate'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField( verbose_name=_('quantity'))
    money_type = models.PositiveSmallIntegerField(choices=MONEY_CHOICES, default=DOLLAR, verbose_name=_('money_type'))
    status = models.CharField(choices=STATUS_CHOICES, max_length=200, verbose_name=_('status'))
    delegate_report = models.TextField(blank=True, null=True, verbose_name=_('delegate_report'))
    shipping_report = models.TextField(blank=True, null=True, verbose_name=_('shipping_report'))
    provider = models.ForeignKey(to=Provider, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('provider'))
    shipping = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('shipping'))
    specification = models.TextField(null=True, blank=True, verbose_name=_('specification'))
    invoice_id = models.CharField(max_length=200,verbose_name='invoice')
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                                    related_name="Order_modified_by", verbose_name=_('modified_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))
    is_reviewed = models.BooleanField(default=False, verbose_name=_('is_reviewed'))
    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return str(self.user)


class History(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    date = models.DateTimeField(auto_now=True, verbose_name=_('date'))
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, verbose_name=_('order'))

    class Meta:
        verbose_name = _("History")
        verbose_name_plural = _("Histories")

    def __str__(self):
        return str(self.user)


class Cart(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    add_date = models.DateTimeField(auto_now=True, verbose_name=_('add_date'))
    specs = models.TextField(blank=True, null=True, verbose_name=_('specs'))
    max_quantity = models.PositiveIntegerField(verbose_name=_('max_quantity'))
    is_trashed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Cart")
        verbose_name_plural = _("Carts")

    def __str__(self):
        return str(self.quantity)


# class SpecCart(models.Model):
#     cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE, verbose_name=_('cart'))
#     spec_name = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('spec_name'))
#     spec_value = models.PositiveIntegerField(verbose_name=_('spec_value'))
#     is_trashed = models.BooleanField(default=False)
#
#     class Meta:
#         verbose_name = _("SpecCart")
#         verbose_name_plural = _("SpecCarts")
#
#     def __str__(self):
#         return self.spec_name
#


# class Iloc(models.Model):
#     user = models.ForeignKey(to=BuyerUserDetails, on_delete=models.CASCADE, verbose_name=_('user'))
#     user_address = models.CharField(max_length=500, verbose_name=_('user_address'))
#     user_country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name="Iloc_user_country", verbose_name=_('user_country'))
#     user_region = models.CharField(max_length=500, verbose_name=_('user_region'))
#     user_city = models.CharField(max_length=500, verbose_name=_('user_city'))
#     user_zip_code = models.CharField(max_length=50,verbose_name=_('user_zip_code'))
#     user_mobile = models.CharField(max_length=50,  verbose_name=_('user_mobile'))
#     importer_country = models.ForeignKey(to=Country, on_delete=models.CASCADE, related_name="Iloc_importer_country", verbose_name=_('importer_country'))
#     importer_port = models.CharField(max_length=500, verbose_name=_('importer_port'))
#     order_id = models.CharField(max_length=200,verbose_name='order_id')
#     order_amount = models.PositiveIntegerField( verbose_name=_('order_amount'))
#     shipping_amount = models.PositiveIntegerField( verbose_name=_('shipping_amount'))
#     exproter_bank = models.CharField(max_length=500, verbose_name=_('exproter_bank'))
#     exproter_account_number = models.CharField(max_length=200, verbose_name=_('exproter_account_number'))
#     exproter_bank_fees = models.PositiveIntegerField(verbose_name=_('exproter_bank_fees'))
#     importer_bank = models.CharField(max_length=500, verbose_name=_('importer_bank'))
#     iloc_number = models.CharField(max_length=200,verbose_name='iloc_number')
#     iloc_amount = models.PositiveIntegerField( verbose_name=_('iloc_amount'))
#     iloc_file = models.FileField(upload_to='iloc/', verbose_name=_('iloc_file'))
#     shipping_company = models.ForeignKey(to=Shipping, on_delete=models.CASCADE, verbose_name=_('shipping_company'))
#     arrival_date = models.DateField(verbose_name=_('arrival_date'))
#     shipping_file = models.FileField(upload_to='iloc_shipping/', verbose_name=_('shipping_file'))
#     class Meta:
#         verbose_name = _("Iloc")
#         verbose_name_plural = _("Ilocs")

#     def __str__(self):
#         return str(self.user)
