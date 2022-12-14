from django.contrib import admin
from django.utils.html import format_html

from . import models
from django.utils.translation import gettext_lazy as _

# Register your models here.
admin.site.register(models.ChatMessages)


@admin.register(models.Iloc)
class IlocAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'user',
                    'importer_country',
                    'importer_port',
                    'order_id',
                    'order_amount',
                    'shipping_amount',
                    'exproter_bank',
                    'exproter_account_number',
                    'exproter_bank_fees',
                    'importer_bank',
                    'iloc_number',
                    'iloc_amount',
                    'iloc_file',
                    'shipping_company', 
                    'arrival_date', 
                    'shipping_file',
                    'delivered_date',]

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
