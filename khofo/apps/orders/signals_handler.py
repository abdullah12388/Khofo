# from paypal.standard.models import ST_PP_COMPLETED
# from django.shortcuts import get_object_or_404
# from ..products.models import Product
# from .models import Cart, Order
# from ..user.models import BuyerUserDetails
# from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
# from django.dispatch import receiver
# from ..products import views as product_views
#
#
# @receiver(valid_ipn_received)
# def valid_payment_notification(sender, **kwargs):
#     ipn = sender
#     temp_list = ipn.custom.split(',')
#     print('request.user = ', temp_list[0])
#     if ipn.receiver_email != "sb-x8ysa626483@business.example.com":
#         print('not a valid payment')
#         return
#     if ipn.payment_status == 'Completed':
#         print('payment completed')
#         user_buyer = BuyerUserDetails.objects.get(user_id=temp_list[0])
#         print("user_buyer = ", user_buyer)
#         if Cart.objects.filter(user_id=temp_list[0]).exists():
#             print('money_type = ', temp_list[1])
#             cart_list = Cart.objects.filter(user_id=temp_list[0])
#             for x in range(len(cart_list)):
#                 product_obj = Product.objects.get(id=cart_list[x].product_id)
#                 order = Order.objects.create(
#                     user=user_buyer,
#                     category_id=product_obj.category.id,
#                     sub_category_id=product_obj.sub_category.id,
#                     money_type=int(temp_list[1]),
#                     product=product_obj,
#                     quantity=cart_list[x].quantity,
#                     status='ordered',
#                     provider_id=product_obj.provider.id,
#                     specification=cart_list[x].specs,
#                 )
#                 order.save()
#                 available_quantity = product_views.get_quantity(product_obj.id)
#                 if available_quantity:
#                     if available_quantity < 1:
#                         order.is_trashed = True
#             Cart.objects.filter(user_id=temp_list[0]).delete()
#
#
# @receiver(invalid_ipn_received)
# def invalid_payment_notification(sender, **kwargs):
#     print('in invalid signals')
#     ipn = sender
#     if ipn.receiver_email != "sb-x8ysa626483@business.example.com":
#         print('not a valid payment')
#         return
