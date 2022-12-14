# Python
from io import BytesIO
from PIL import Image
# Django
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class Mail(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('user'))
    email = models.EmailField(verbose_name=_('email'), max_length=60)
    message = models.CharField(max_length=20000, verbose_name=_('message'))
    document1 = models.FileField(upload_to='emails/', null=True, blank=True, verbose_name=_('document1'))
    document2 = models.FileField(upload_to='emails/', null=True, blank=True, verbose_name=_('document2'))
    document3 = models.FileField(upload_to='emails/', null=True, blank=True, verbose_name=_('document3'))
    document4 = models.FileField(upload_to='emails/', null=True, blank=True, verbose_name=_('document4'))
    document5 = models.FileField(upload_to='emails/', null=True, blank=True, verbose_name=_('document5'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))

    class Meta:
        verbose_name = _("Mail")
        verbose_name_plural = _("Mails")

    def __str__(self):
        return self.email


class SiteInfo(models.Model):
    ENGLISH = 'english'
    ARABIC = 'arabic'
    LANGUAGE_CHOICES = [
        (ENGLISH, 'english'),
        (ARABIC, 'arabic'),
    ]
    name = models.CharField(max_length=100, verbose_name=_('name'))
    name_ar = models.CharField(max_length=100, verbose_name=_('name_ar'))
    phone = models.CharField(max_length=100, verbose_name=_('phone'))
    email = models.CharField(max_length=100, verbose_name=_('email'))
    address = models.CharField(max_length=200, verbose_name=_('address'))
    address_ar = models.CharField(max_length=200, verbose_name=_('address_ar'))
    postal_code = models.CharField(max_length=100, verbose_name=_('postal_code'))
    logo = models.ImageField(upload_to='site/', verbose_name=_('logo'))
    logo_2 = models.ImageField(upload_to='site/', verbose_name=_('logo_2'))
    login_logo = models.ImageField(upload_to='site/', verbose_name=_('login_logo'))
    facebook = models.URLField(max_length=500, verbose_name=_('facebook'))
    twitter = models.URLField(max_length=500, verbose_name=_('twitter'))
    google = models.URLField(max_length=500, verbose_name=_('google'))
    youtube = models.URLField(max_length=500, verbose_name=_('youtube'))
    wuzzuf = models.URLField(max_length=500, verbose_name=_('wuzzuf'))
    linkedin = models.URLField(max_length=500, verbose_name=_('linkedin'))
    instagram = models.URLField(max_length=500, verbose_name=_('instagram'))
    knicks_link = models.URLField(max_length=500, verbose_name=_('knicks_link'))
    knicks_logo = models.ImageField(upload_to='site/', verbose_name=_('knicks_logo'))
    dollar_rate = models.FloatField(verbose_name=_('dollar_rate'))
    language = models.CharField(choices=LANGUAGE_CHOICES, default=ENGLISH, max_length=100, verbose_name=_('language'))

    class Meta:
        verbose_name = _("SiteInfo")
        verbose_name_plural = _("SiteInfo")

    def __str__(self):
        return self.name


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(SiteInfo, self).save(force_insert=False, force_update=False, using=None, update_fields=None)
        compress(self.logo)
        compress(self.logo_2)
        compress(self.login_logo)
        compress(self.knicks_logo)


class Music(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('music'))
    music = models.FileField(upload_to='music/', null=True, blank=True, verbose_name=_('music'))
    created_on = models.DateTimeField(auto_now_add=True, verbose_name=_('created_on'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_('created_by'))

    class Meta:
        verbose_name = _("Music")
        verbose_name_plural = _("Musics")

    def __str__(self):
        return self.name


def compress(image):
    im = Image.open(image.path).convert('RGB')
    # create a BytesIO object
    im_io = BytesIO()
    # save image to BytesIO object
    im.thumbnail((600, 600), Image.ANTIALIAS)
    im.save(im_io, format='JPEG')
    # create a django-friendly Files object
    im.save(image.path)
