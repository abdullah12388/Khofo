from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from . import models

# Register your models here.


@admin.register(models.Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'working_field', 'phone', 'website', 'manage_buttons')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))
    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
