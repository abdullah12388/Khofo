# Django
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

# models
from . import models


# Register your models here.


@admin.register(models.SiteInfo)
class SiteInfoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'phone', 'email', 'address', 'postal_code', 'dollar_rate', 'language', 'manage_buttons')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'music', 'created_on', 'created_by', 'manage_buttons')
    readonly_fields = ['created_by', ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


admin.site.register(models.Mail)
