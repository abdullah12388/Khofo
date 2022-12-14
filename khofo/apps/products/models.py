# Django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File
# Python
import os
from io import BytesIO
from PIL import Image
# Models
from smart_selects.db_fields import ChainedForeignKey
from ..delegates.models import Delegate
from ..providers.models import Provider
from ..shippings.models import ShippingCondition


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name_ar'))
    show_num = models.PositiveIntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return str(self.name) + ' - ' + str(self.name_ar)


class SubCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name_ar'))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_('category'))
    delegate = models.ForeignKey(to=Delegate, on_delete=models.CASCADE, verbose_name=_('delegate'))
    show_num = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("SubCategory")
        verbose_name_plural = _("SubCategories")

    def __str__(self):
        return str(self.name) + ' - ' + str(self.name_ar)


class Product(models.Model):
    name = models.CharField(max_length=500, verbose_name=_('name'))
    name_ar = models.CharField(max_length=200, verbose_name=_('name_ar'))
    price = models.FloatField(verbose_name=_('price'))
    provider_price = models.FloatField(verbose_name=_('provider_price'))
    brand_name = models.CharField(max_length=500, verbose_name=_('brand_name'))
    brand_name_ar = models.CharField(max_length=200, verbose_name=_('brand_name_ar'))
    model_number = models.CharField(max_length=500, verbose_name=_('model_number'))
    short_description = models.CharField(max_length=500, verbose_name=_('short_description'))
    short_description_ar = models.CharField(max_length=500, verbose_name=_('short_description_ar'))
    main_img = models.ImageField(upload_to='images/', verbose_name=_('main_img'))
    stars = models.FloatField(verbose_name=_('stars'))
    long_desc_img = models.ImageField(upload_to='images/', verbose_name=_('long_desc_img'))
    provider = models.ForeignKey(to=Provider, on_delete=models.CASCADE, verbose_name=_('provider'))
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_('category'))
    sub_category = ChainedForeignKey(SubCategory, chained_field="category", chained_model_field="category",
                                     show_all=False, verbose_name=_('sub_category'))
    process_time = models.FloatField()
    max_quantity = models.IntegerField()
    delay_count = models.IntegerField()
    weight = models.FloatField()
    volume = models.FloatField()
    additional_shipping_cost = models.FloatField(verbose_name=_('additional_shipping_cost'))
    shipping_condition = models.ForeignKey(to=ShippingCondition, on_delete=models.CASCADE, blank=True, null=True,
                                           verbose_name=_('shipping_condition'))
    show_num = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return str(self.name) + ' - ' + str(self.name_ar)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Product, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        compress(self.main_img)


class ProductImage(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    image = models.ImageField(upload_to='images/', verbose_name=_('image'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("ProductImage")
        verbose_name_plural = _("ProductImages")

    def __str__(self):
        return str(self.product)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(ProductImage, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        compress(self.image)


class Review(models.Model):
    review = models.CharField(max_length=500, verbose_name=_('review'), null=True, blank=True)
    stars = models.FloatField(verbose_name=_('stars'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")

    def __str__(self):
        return str(self.product)


class ProductOffer(models.Model):
    BEST = 1
    HIGHVALUE = 2
    ADBANNER = 1
    SLIDER = 2
    TYPE_CHOICES = [
        (BEST, 'best'),
        (HIGHVALUE, 'highValue'),
    ]
    SHOWED_IN_CHOICES = [
        (SLIDER, 'slider'),
        (ADBANNER, 'adbanner'),
    ]
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name=_('category'))
    sub_category = ChainedForeignKey(SubCategory, chained_field="category", chained_model_field="category",
                                     show_all=False, verbose_name=_('sub_category'))
    product = ChainedForeignKey(Product, chained_field="sub_category", chained_model_field="sub_category",
                                show_all=False, verbose_name=_('product'))
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('image'))
    discount = models.FloatField(verbose_name=_('discount'))
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, blank=True, null=True, verbose_name=_('type'))
    showed_in = models.PositiveIntegerField(choices=SHOWED_IN_CHOICES, blank=True, null=True,
                                            verbose_name=_('showed_in'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("ProductOffer")
        verbose_name_plural = _("ProductOffers")

    def __str__(self):
        return str(self.product)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(ProductOffer, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        resize_img(self.image)


class SpecName(models.Model):
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE, verbose_name=_('sub_category'))
    spec_name = models.CharField(max_length=100, verbose_name=_('spec_name'))
    spec_name_ar = models.CharField(max_length=100, verbose_name=_('spec_name_ar'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("SpecName")
        verbose_name_plural = _("SpecNames")

    def __str__(self):
        return str(self.spec_name) + ' - ' + str(self.spec_name_ar)


class SpecValue(models.Model):
    sub_category = models.ForeignKey(to=SubCategory, on_delete=models.CASCADE, verbose_name=_('sub_category'))
    spec_name = ChainedForeignKey(SpecName, chained_field="sub_category", chained_model_field="sub_category",
                                  show_all=False, verbose_name=_('spec_name'))
    product = ChainedForeignKey(Product, chained_field="sub_category", chained_model_field="sub_category",
                                show_all=False, verbose_name=_('product'))
    spec_value = models.CharField(max_length=200, verbose_name=_('spec_value'))
    spec_value_ar = models.CharField(max_length=200, verbose_name=_('spec_value_ar'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("SpecValue")
        verbose_name_plural = _("SpecValues")

    def __str__(self):
        return str(self.spec_value) + ' & ' + str(self.product)


class ShowRecent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('user'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("ShowRecent")
        verbose_name_plural = _("ShowRecents")

    def __str__(self):
        return self.user.username


class SpecNameChangeable(models.Model):
    spec_name = models.CharField(max_length=100, verbose_name=_('spec_name'))
    spec_name_ar = models.CharField(max_length=100, verbose_name=_('spec_name_ar'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("SpecNameChangeable")
        verbose_name_plural = _("SpecNameChangeables")

    def __str__(self):
        return str(self.spec_name) + ' - ' + str(self.spec_name_ar)


class SpecValueChangeable(models.Model):
    spec_name = models.ForeignKey(to=SpecNameChangeable, on_delete=models.CASCADE, verbose_name=_('spec_name'))
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name=_('product'))
    spec_value = models.CharField(max_length=200, verbose_name=_('spec_value'))
    spec_value_ar = models.CharField(max_length=200, verbose_name=_('spec_value_ar'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    modified_on = models.DateTimeField(auto_now=True, verbose_name=_('modified_on'))
    is_trashed = models.BooleanField(default=False, verbose_name=_('is_trashed'))

    class Meta:
        verbose_name = _("SpecValueChangeable")
        verbose_name_plural = _("SpecValueChangeables")

    def __str__(self):
        return str(self.product) + ' & ' + str(self.spec_name) + ' & ' + str(self.spec_value)


def resize_img(image1):
    image = Image.open(image1.path)
    size = os.path.getsize(image1.path) / 1048576
    if size >= 1:
        image.save(image1.path, quality=20, optimize=True)
    elif size >= .75:
        image.save(image1.path, quality=50, optimize=True)
    elif size >= .5:
        image.save(image1.path, quality=70, optimize=True)


def compress(image):
    im = Image.open(image.path).convert('RGB')
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.thumbnail((600, 600), Image.ANTIALIAS)
    im.save(im_io, format='JPEG')
    # create a django-friendly Files object
    im.save(image.path)
