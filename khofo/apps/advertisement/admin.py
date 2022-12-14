from django.contrib import admin
from django.utils.translation import gettext_lazy as _
# Register your models here.
from django.utils.html import format_html

from . import models


@admin.register(models.Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'advertiserName', 'advertiserEmail', 'advertiserPhone', 'image', 'page', 'startDate', 'endDate',
        'duration', 'interval', 'advertiseManager', 'manage_buttons')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.AdsManager)
class AdsManagerAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'address', 'profile_picture', 'phone', 'ssn_id', 'birth_date', 'gender', 'manage_buttons')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
