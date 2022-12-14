from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models


# Register your models here.

@admin.register(models.ShippingTime)
class ShippingTimeAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'country', 'shipping_company', 'shipping_type', 'days', 'created_by', 'created_on', 'modified_on',
    'is_trashed', 'manage_buttons')
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


@admin.register(models.Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'phone', 'website', 'created_by', 'created_on', 'modified_on',
                    'is_trashed', 'manage_buttons')
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


@admin.register(models.ShippingCondition)
class ShippingConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_ar', 'price', 'created_by', 'created_on', 'modified_on', 'is_trashed',
                    'manage_buttons')
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


@admin.register(models.Express)
class ExpressAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost',
                    'price_average', 'transport_time', 'shipping_condition', 'created_by', 'created_on', 'modified_on',
                    'is_trashed', 'manage_buttons')
    list_editable = ('price_average',)
    readonly_fields = ['created_by', 'price_average', ]
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        average = float((((obj.slice_max - obj.slice_min) * obj.rate) + obj.initial_cost))
        result = average / (2 * (((obj.slice_max - obj.slice_min) / 2) + obj.slice_min))
        obj.price_average = float("{0:.2f}".format(result))
        obj.save()

    def get_queryset(self, request):
        query_set = super(ExpressAdmin, self).get_queryset(request)
        return query_set.order_by('price_average')

    def get_list_filter(self, request):
        return ['country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost', 'transport_time',
                'shipping_condition', 'created_on', 'modified_on', 'is_trashed', ]

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.AirFreight)
class AirFreightAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost',
                    'transport_time', 'shipping_condition', 'created_by', 'created_on', 'modified_on', 'is_trashed',
                    'manage_buttons')
    readonly_fields = ['created_by', 'price_average', ]
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def get_list_filter(self, request):
        return ['country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost', 'transport_time',
                'price_average', 'shipping_condition', 'created_on', 'modified_on', 'is_trashed', ]

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SeaFreight)
class SeaFreightAdmin(admin.ModelAdmin):
    list_display = ('id', 'country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost',
                    'transport_time', 'price_average', 'shipping_condition', 'created_by', 'created_on', 'modified_on',
                    'is_trashed', 'manage_buttons')
    readonly_fields = ['created_by', 'price_average', ]
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def get_list_filter(self, request):
        return ['country', 'slice_min', 'slice_max', 'shipping_company', 'rate', 'initial_cost', 'transport_time',
                'shipping_condition', 'created_on', 'modified_on', 'is_trashed', ]

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
