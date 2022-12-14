# Django
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.urls import path
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
# Outer Packages
from rangefilter.filter import DateRangeFilter
# Models
from .render import Render
from . import models
from ..providers.models import Provider
from ..orders.models import Order

User = get_user_model()


class ProductFunctions:
    def get_filtered_products(self, request, products):
        filters = {}
        # print("request.GET = ", request.GET)
        for x in request.GET:
            sort = request.GET.get('o', None)
            page = request.GET.get('p', None)
            all = request.GET.get('all', None)
            # print("request.GET.get('o', None) = ", type(sort))
            if not sort and not page and not all:
                if not sort == '' and not page == '' and not all == '':
                    # print("index = ", x, " *** value = ", request.GET[x])
                    filters.update({
                        x: request.GET[x],
                    })
        products = products.filter(**filters)
        return products


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_per_page = 7

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    # Change_list ( Column )
    def get_list_display(self, request):
        list_display = [
            'id', 'name', 'brand_name', 'model_number', 'stars', 'provider', 'category', 'sub_category', 'price',
            'provider_price', 'process_time', 'max_quantity', 'delay_count', 'show_num', 'created_on', 'created_by', 'is_trashed',
            'manage_buttons']
        if request.user.is_delegate or request.user.is_superuser:
            list_display.insert(8, 'ordered_quantity_btn')
            return list_display
        elif request.user.is_provider:
            list_display.pop(5)  # remove provider column
            list_display.pop(7)  # remove price column
            list_display.insert(8, 'ordered_quantity_btn')  # add quantity column
            return list_display
        return []

    # Change_list ( filter model query )
    def get_queryset(self, request):
        query_set = super(ProductAdmin, self).get_queryset(request)
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                return query_set.filter(provider=provider)
            except ObjectDoesNotExist:
                return query_set
        else:
            return query_set

    # Change_list ( filter FK dropdown values )
    def get_list_filter(self, request):
        filter_list = ['name', 'price', 'brand_name', 'model_number', 'stars', 'provider', 'category', 'sub_category',
                       'show_num', 'process_time', 'max_quantity', 'delay_count', 'is_trashed', ('created_on', DateRangeFilter)]
        if request.user.is_delegate or request.user.is_superuser:
            return filter_list
        elif request.user.is_provider:
            filter_list.pop(5)
            return filter_list
        else:
            return []

    # Change_List ( Quantity Column )
    def ordered_quantity_btn(self, obj):
        orders = Order.objects.filter(product=obj)
        quantity = 0
        for order in orders:
            quantity += order.quantity
        return quantity

    # just a callable function
    def get_total_price(self, request):
        total_price = models.Product.objects.all().aggregate(tot=Sum('price'))['tot']
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                total_price = models.Product.objects.filter(provider=provider).aggregate(tot=Sum('price'))[
                    'tot']
                return total_price
            except ObjectDoesNotExist:
                return total_price
        return total_price

    # just a callable function
    def get_total_provider_price(self, request):
        total_provider_price = models.Product.objects.all().aggregate(tot=Sum('provider_price'))['tot']
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                total_provider_price = \
                    models.Product.objects.filter(provider=provider).aggregate(tot=Sum('provider_price'))[
                        'tot']

                return total_provider_price
            except ObjectDoesNotExist:
                return total_provider_price
        return total_provider_price

    # just a callable function
    def get_total_quantity(self, request):
        product_functions = ProductFunctions()
        all_products = models.Product.objects.all()
        products = product_functions.get_filtered_products(request=request, products=all_products)
        product_ids = [prod.id for prod in products]
        orders = Order.objects.filter(product_id__in=product_ids)
        total_quantity = orders.aggregate(tot=Sum('quantity'))['tot']
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                orders = orders.filter(provider=provider)
                total_quantity = orders.aggregate(tot=Sum('quantity'))['tot']
                return total_quantity
            except ObjectDoesNotExist:
                return HttpResponse("This's not a Provider")
        return total_quantity

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('print/', self.print_table),
        ]
        return my_urls + urls

    def print_table(self, request):
        product_functions = ProductFunctions()
        all_products = models.Product.objects.all()
        products = product_functions.get_filtered_products(request=request, products=all_products)
        today = timezone.now()
        params = {
            'today': today,
            'request': request,
        }
        if products:
            params.update({'products': products, })
        return Render.render('pdf.html', params)

    # changelist_view
    def changelist_view(self, request, extra_context=None, ):
        request.session['filter_dic'] = request.GET
        total_price = self.get_total_price(request=request)
        total_quantity = self.get_total_quantity(request=request)
        total_provider_price = self.get_total_provider_price(request=request)
        my_context = {}
        if request.user.is_superuser or request.user.is_delegate:
            my_context = {
                'total_quantity': total_quantity,
                'total_price': total_price,
                'total_provider_price': total_provider_price,
            }
        elif request.user.is_provider:
            my_context.update({
                'total_quantity': total_quantity,
                'total_provider_price': total_provider_price,
            })
        return super(ProductAdmin, self).changelist_view(request, extra_context=my_context)

    # Change_List ( Update - Delete ) Buttons
    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    # Change_Form ( read_only fields )
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ['name', 'price', 'provider_price', 'brand_name', 'model_number', 'short_description',
                           'main_img', 'stars',
                           'advantages', 'provider', 'category', 'sub_category', 'is_trashed', 'created_by']
        if not request.user.is_superuser and not request.user.is_delegate:
            return readonly_fields
        else:
            return ['created_by']

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
    ordered_quantity_btn.short_description = _('total_orders')


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_ar', 'show_num', 'created_by', 'created_on', 'is_trashed', 'manage_buttons')
    readonly_fields = ['created_by']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    # Change_list ( filter model query )
    def get_queryset(self, request):
        query_set = super(CategoryAdmin, self).get_queryset(request)
        return query_set.order_by('show_num')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'name_ar', 'category', 'show_num', 'created_by', 'created_on', 'is_trashed', 'manage_buttons')
    readonly_fields = ['created_by']
    list_per_page = 6

    def get_list_filter(self, request):
        return ['category']

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    # Change_list ( filter model query )
    def get_queryset(self, request):
        query_set = super(SubCategoryAdmin, self).get_queryset(request)
        return query_set.order_by('category')

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'stars', 'review', 'created_on', 'is_trashed', 'manage_buttons')
    list_per_page = 5

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'created_by', 'created_on', 'is_trashed', 'manage_buttons')
    readonly_fields = ['created_by']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.ProductOffer)
class ProductOffersAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'product', 'category', 'sub_category', 'type', 'showed_in', 'discount', 'created_by', 'is_trashed',
        'manage_buttons')
    readonly_fields = ['created_by']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SpecName)
class SpecNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'spec_name', 'sub_category', 'created_by', 'created_on', 'is_trashed', 'manage_buttons']
    readonly_fields = ['created_by']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SpecValue)
class SpecValueAdmin(admin.ModelAdmin):
    list_display = ['id', 'spec_value', 'spec_name', 'sub_category', 'product', 'created_by', 'created_on',
                    'is_trashed', 'manage_buttons']
    readonly_fields = ['created_by']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SpecNameChangeable)
class SpecNameChangableSpecNameAdmin(admin.ModelAdmin):
    list_display = ['id', 'spec_name', 'created_by', 'created_on', 'is_trashed', 'manage_buttons']
    readonly_fields = ['created_by']
    list_editable = ['is_trashed']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


@admin.register(models.SpecValueChangeable)
class SpecValueChangableAdmin(admin.ModelAdmin):
    list_display = ['id', 'spec_value', 'spec_name', 'product', 'created_by', 'created_on', 'is_trashed',
                    'manage_buttons']
    readonly_fields = ['created_by']
    list_editable = ['is_trashed']
    list_per_page = 5

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True


admin.site.register(models.ShowRecent)

# @admin.register(models.ProductColor)
# class ProductColorAdmin(admin.ModelAdmin):
#     list_display = ['id', 'color', 'product', 'created_on', 'created_by', 'is_trashed']
#     list_per_page = 5
#     readonly_fields  = ['created_by']
#     def save_model(self, request, obj, form, change):
#         obj.created_by = request.user
#         obj.save()

#     def manage_buttons(self, obj):
#         return format_html('<a href="{}/change/">{}</a>'' -'
#                            ' ''<a href="{}/delete/">{}</a>'.
#                            format(obj.id, _('update'), obj.id, _('delete')))


#     manage_buttons.short_description = _('Manage')
#     manage_buttons.allow_tags = True
