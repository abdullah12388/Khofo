# Django
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.datetime_safe import datetime
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
# Outer Packages
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
# Models
from . import models
from ..providers.models import Provider
from ..shippings.models import Shipping
from ..products.models import Product
from django.core.mail import EmailMessage

User = get_user_model()


# Register your models here.


class OrderFunctions:
    def get_filtered_orders(self, request, orders):
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
        # print('filters = ', filters)
        return orders.filter(**filters)

    def send_reviews(self, request, order):
        title = 'Khofu Product Review'
        buyer_user = models.BuyerUserDetails.objects.get(id=order.user_id).user_id
        link = request.META['HTTP_HOST'] + '/productHome/reviews/' + str(order.product.id)
        message = 'Please, visit the link down to review our product:\n ' + link
        user_email = User.objects.get(id=buyer_user).email
        email = EmailMessage(title, message, to=[user_email])
        email.send()
        # print(buyer_user, message, user_email, email)
        return True


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_per_page = 7

    def save_model(self, request, obj, form, change):
        if change:
            obj.modified_by = request.user
            models.History.objects.create(user=request.user, date=datetime.now(), order=obj)
            if obj.status == 'delivered':
                orederFunctions = OrderFunctions()
                # all_orders = models.Order.objects.filter(user_id=obj.user_id, product_id=obj.product_id, status=obj.status , is_reviewed=False)
                done = orederFunctions.send_reviews(request, obj)
                if done:
                    obj.is_reviewed = True
        obj.save()

    # Change_list ( Column )
    def get_list_display(self, request):
        list_display = [
            'id', 'user', 'product', 'shipping', 'provider', 'invoice_id', 'status', 'is_reviewed', 'quantity',
            'price_column',
            'provider_price_column', 'money_type', 'category', 'sub_category', 'delegate', 'modified_on', 'modified_by',
            'manage_buttons']
        if request.user.is_delegate or request.user.is_superuser:
            return list_display
        elif request.user.is_provider:
            list_display.pop(4)  # remove provider column
            list_display.pop(6)  # remove price column
            list_display.insert(7, 'final_provider_price_column')  # add final_price column
            return list_display
        elif request.user.is_shipping:
            list_display.pop(3)  # remove SHIPPING column
            list_display.pop(7)  # remove provider_price column
            list_display.insert(7, 'final_price_column')  # add final_price column
            return list_display
        return []

    # Change_list ( filter model query )
    def get_queryset(self, request):
        query_set = super(OrderAdmin, self).get_queryset(request)
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                return query_set.filter(provider=provider)
            except ObjectDoesNotExist:
                return query_set
        elif request.user.is_shipping:
            try:
                shipping = Shipping.objects.get(user=request.user)
                return query_set.filter(shipping=shipping)
            except ObjectDoesNotExist:
                return query_set
        else:
            return query_set

    # Change_list ( filter FK dropdown values )
    def get_list_filter(self, request):
        filter_list = ['user', 'category', 'sub_category', 'delegate', 'product', 'provider', 'shipping', 'status',
                       'quantity', 'money_type', 'invoice_id', ('created_on', DateRangeFilter)]
        # return filter_list
        if request.user.is_delegate or request.user.is_superuser:
            return filter_list
        elif request.user.is_shipping:
            filter_list.pop(6)
            return filter_list
        elif request.user.is_provider:
            filter_list.pop(5)
            return filter_list
        else:
            return []

    # Change_list ( price_column )
    def price_column(self, obj):
        return obj.product.price

    # Change_list ( provider_price_column )
    def provider_price_column(self, obj):
        return obj.product.provider_price

    # Change_list ( final_price_column )
    def final_price_column(self, obj):
        final_price = obj.quantity * obj.product.price
        # self.final_price_list.append(final_price)
        return final_price

    # Change_list ( final_provider_price_column )
    def final_provider_price_column(self, obj):
        final_price = obj.quantity * obj.product.provider_price
        return final_price

    # Change_list ( manage_buttons [delete, update] )
    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    # just a callable function
    def get_total_provider_price(self, request):
        orederFunctions = OrderFunctions()
        all_orders = models.Order.objects.all()
        all_orders = orederFunctions.get_filtered_orders(request, all_orders)
        total_provider_price = 0
        for order in all_orders:
            product = Product.objects.get(pk=order.product.id)
            total_provider_price += product.provider_price * order.quantity
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                orders = models.Order.objects.filter(provider=provider)
                orders = orederFunctions.get_filtered_orders(request, orders)
                total_provider_price = 0
                for order in orders:
                    product = Product.objects.get(pk=order.product.id)
                    total_provider_price += product.provider_price * order.quantity
                return total_provider_price
            except ObjectDoesNotExist:
                return total_provider_price
        return total_provider_price

    # just a callable function
    def get_total_price(self, request):
        orederFunctions = OrderFunctions()
        orders = models.Order.objects.all()
        orders = orederFunctions.get_filtered_orders(request, orders)
        total_price = 0
        for order in orders:
            product = Product.objects.get(pk=order.product.id)
            total_price += product.price * order.quantity
        return total_price

    # just a callable function
    def get_total_quantity(self, request):
        orederFunctions = OrderFunctions()
        all_orders = models.Order.objects.all()
        all_orders = orederFunctions.get_filtered_orders(request, all_orders)
        total_quantity = all_orders.aggregate(tot=Sum('quantity'))['tot']
        if request.user.is_provider:
            try:
                provider = Provider.objects.get(user=request.user)
                orders = models.Order.objects.filter(provider=provider)
                orders = orederFunctions.get_filtered_orders(request, orders)
                quantity = 0
                for order in orders:
                    quantity += order.quantity
                return quantity
            except ObjectDoesNotExist:
                return HttpResponse("This's not a Provider")
        return total_quantity

    # changelist_view
    def changelist_view(self, request, extra_context=None, ):
        total_price = self.get_total_price(request=request)
        total_provider_price = self.get_total_provider_price(request=request)
        total_quantity = self.get_total_quantity(request=request)
        my_context = {}
        if request.user.is_superuser or request.user.is_delegate:
            my_context = {
                'total_quantity': total_quantity,
                'total_price': total_price,
                'total_provider_price': total_provider_price,
            }
        elif request.user.is_provider:
            my_context.update({
                'total_provider_price': total_provider_price,
                'total_quantity': total_quantity,
            })
        return super(OrderAdmin, self).changelist_view(request, extra_context=my_context)

    # Change_Form ( read_only fields )
    def get_readonly_fields(self, request, obj=None):
        read_only = ['user', 'product', 'quantity', 'status', 'delegate_report', 'shipping_report', 'provider',
                     'shipping', 'modified_by', 'is_trashed']
        if request.user.is_superuser:
            return ['modified_by']
        elif request.user.is_delegate:
            read_only.pop(3)
            read_only.pop(3)
            return read_only
        elif request.user.is_shipping:
            read_only.pop(3)
            read_only.pop(4)
            return read_only
        elif request.user.is_provider:
            read_only.pop(3)
            return read_only

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True
    price_column.short_description = _('price')
    provider_price_column.short_description = _('provider price')
    final_price_column.short_description = _('final price')
    final_provider_price_column.short_description = _('final provider price')


@admin.register(models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'order']

    def get_list_filter(self, request):
        filtered_list = ['user', ('date', DateRangeFilter), 'order__id']
        return filtered_list


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'add_date']

    def manage_buttons(self, obj):
        return format_html('<a href="{}/change/">{}</a>'' -'
                           ' ''<a href="{}/delete/">{}</a>'.
                           format(obj.id, _('update'), obj.id, _('delete')))

    manage_buttons.short_description = _('Manage')
    manage_buttons.allow_tags = True

