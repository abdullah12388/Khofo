import datetime

import bleach
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
# from paypal.standard.forms import PayPalPaymentsForm
from django.contrib.auth.decorators import login_required
from ..orders.models import Cart
from ..products.models import Product
from ..products.views import get_quantity
from ..user.models import BuyerUserDetails


# Create your views here.

def checkOut(request):
    if 'khufu_cart' not in request.session:
        if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
            HttpResponseRedirect('/ar/')
        else:
            HttpResponseRedirect('/en/')
    else:
        if request.user.is_authenticated:
            # [productObject, quantity, specs]
            cart_products = Cart.objects.filter(user=request.user)
            products_list = []
            products = []
            _available_quantity = []
            indexs = []
            for p in range(len(cart_products)):
                products_list += Product.objects.filter(id=cart_products[p].product_id)
            # print('products = ', products_list)
            for x in range(len(cart_products)):
                _avail_quan_temp = get_quantity(products_list[x].id)
                print('_avail_quan_temp = ', _avail_quan_temp)
                if _avail_quan_temp == -1:
                    _available_quantity.append(cart_products[x].max_quantity)
                else:
                    _available_quantity.append(_avail_quan_temp)
                print('_available_quantity = ', _available_quantity)
                if _available_quantity[x] >= cart_products[x].quantity:
                    products.append((products_list[x], cart_products[x].quantity, cart_products[x].specs,
                                     cart_products[x].max_quantity, cart_products[x].id), )
                else:
                    if int(_available_quantity[x]) == 0:
                        indexs.append(x)
                    cart_products[x].quantity = _available_quantity[x]
                    cart_products[x].save()
                    products.append((products_list[x], _available_quantity[x], cart_products[x].specs,
                                     cart_products[x].max_quantity, cart_products[x].id), )
                # print('indexs = ', indexs)
                print('products = ', products)
            context = {
                'product': products,
                'items': len(products),
            }
            _products_list = request.session['khufu_cart']['product']
            for i in indexs:
                _products_list[i][1] = 0
            _context = request.session['khufu_cart']
            _context.update({
                'product': _products_list,
            })
            request.session['khufu_cart'] = _context
        else:
            products = request.session['khufu_cart']['product']
            products_list = []
            for p in products:
                products_list += Product.objects.filter(id=p[0], is_trashed=False)
            for x in range(len(products)):
                products[x][0] = products_list[x]
            context = {
                'product': products,
                'items': len(products),
            }
        return render(request, 'checkOut.html', context)
    return render(request, 'checkOut.html', {'items': 0})

@login_required
def check_user_buyer(request):
    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
        if 'khufu_cart' not in request.session:
            HttpResponseRedirect('/ar/')
        else:
            if 'product' in request.session['khufu_cart']:
                try:
                    buyer = BuyerUserDetails.objects.get(user=request.user, is_trashed=False)
                    return HttpResponseRedirect('/ar/user/address/update/')
                except ObjectDoesNotExist as error:
                    print("Warning: ", error)
                    return HttpResponseRedirect('/ar/user/address/add/')
        return HttpResponseRedirect('/ar/order/')
    else:
        if 'khufu_cart' not in request.session:
            HttpResponseRedirect('/en/')
        else:
            if 'product' in request.session['khufu_cart']:
                try:
                    buyer = BuyerUserDetails.objects.get(user=request.user, is_trashed=False)
                    return HttpResponseRedirect('/en/user/address/update/')
                except ObjectDoesNotExist as error:
                    print("Warning: ", error)
                    return HttpResponseRedirect('/en/user/address/add/')
        return HttpResponseRedirect('/en/order/')

#
# def finalCart(request):
#     if 'khufu_cart' not in request.session:
#         if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
#             HttpResponseRedirect('/ar/')
#         else:
#             HttpResponseRedirect('/en/')
#     else:
#         if 'product' in request.session['khufu_cart']:
#             products = request.session['khufu_cart']['product']
#             products_list = []
#             for p in products:
#                 products_list += Product.objects.filter(id=p[0], is_trashed=False)
#             for x in range(len(products)):
#                 products[x][0] = products_list[x]
#             totalPrices = 0
#             product_names = []
#             product_quantity = []
#             for i in range(len(products)):
#                 totalPrices += int(products[i][0].price) * int(products[i][1])
#                 product_names.append(products[i][0].name)
#                 product_quantity.append(products[i][1])
#             host = request.get_host()
#             print('host = ', host)
#             print('country', request.session['site_info']['country_short'])
#             if request.session['site_info']['country_short'] == 'EG':
#                 money_type = 2
#             else:
#                 money_type = 1
#             paypal_dict = {
#                 'business': settings.PAYPAL_RECEIVER_EMAIL,
#                 'amount': totalPrices,
#                 'quantity': '{}'.format(product_quantity),
#                 'item_name': 'Order {}'.format(product_names),
#                 'invoice': '{},{},{}'.format(product_names, product_quantity, datetime.datetime.now()),
#                 'currency_code': 'USD',
#                 'notify_url': 'http://{}{}'.format(host, '/paypal/'),
#                 'return_url': 'http://{}{}'.format(host, '/order/cart/?s=done&del=deleted'),
#                 'cancel_url': 'http://{}{}'.format(host, '/order/cart/?s=canceled'),
#                 'custom': '{},{}'.format(request.user.id, money_type),
#             }
#             print('paypal_dict = ', paypal_dict)
#             form = PayPalPaymentsForm(initial=paypal_dict)
#             context = {
#                 'product': products,
#                 'form': form,
#                 'items': len(products),
#             }
#             if 'del' in request.GET:
#                 print('del in session')
#                 if request.GET['del'] == 'deleted':
#                     print('del == deleted')
#                     print(request.session['khufu_cart'])
#                     # del request.session['khufu_cart']
#                     request.session['khufu_cart'] = {
#                         'product': [],
#                         'items': 0,
#                     }
#             return render(request, 'finalCart.html', context)
#     return render(request, 'finalCart.html', {'items': 0})
#

# AJAX
# ----------------------------------------------------------------------------------------------
def updateCookie(request):
    if request.GET:
        if 'khufu_cart' in request.session:
            if 'product' in request.session['khufu_cart']:
                products = request.session['khufu_cart']['product']
                product_list = []
                avail_quan_in_cart = 0
                # print(products)
                prod_index = bleach.clean(request.GET.get('index', None))
                # print('prod_index = ', prod_index)
                prod_id = products[int(prod_index)][0]
                # print('prod_id = ', prod_id)
                prod_max_quan = products[int(prod_index)][3]
                # print('prod_max_quan = ', prod_max_quan)
                avail_quan = get_quantity(int(prod_id))
                if int(avail_quan) == -1:
                    avail_quan = int(prod_max_quan)
                # print('avail_quan = ', avail_quan)
                for i in range(len(products)):
                    if int(prod_id) == int(products[i][0]):
                        avail_quan_in_cart += int(bleach.clean(request.GET.get('cart[' + str(i) + ']', None)))
                    # print('avail_quan_in_cart = ', avail_quan_in_cart)
                    # print('quantity = ', bleach.clean(request.GET.get('cart[' + str(i) + ']', None)))
                if int(avail_quan) >= int(avail_quan_in_cart):
                    avail_remain = int(avail_quan) - int(avail_quan_in_cart)
                    # print('avail_remain = ', avail_remain)
                    for i in range(len(products)):
                        product_list.append(
                            [products[i][0], bleach.clean(request.GET.get('cart[' + str(i) + ']', None)), products[i][2],
                             products[i][3]])
                else:
                    return JsonResponse({'done':True})
                context = request.session['khufu_cart']
                context.update({
                    'product': product_list,
                })
                request.session['khufu_cart'] = context
                ############# Registered User #####################
                if request.user.is_authenticated:
                    if bleach.clean(request.GET.get('operator', None)) == 'plus':
                        # print(bleach.clean(request.GET.get('operator', None)))
                        pro_index = bleach.clean(request.GET.get('index', None))
                        # print('pro_index = ', pro_index)
                        for i in range(len(products)):
                            # print('i = ', i)
                            if i == int(pro_index):
                                # print(pro_index)
                                product_instance = Product.objects.get(id=products[i][0], is_trashed=False)
                                # print(product_instance)
                                if Cart.objects.filter(user=request.user, product=product_instance,
                                                       is_trashed=False).exists():
                                    old_instance = Cart.objects.filter(user=request.user, product=product_instance,
                                                                    quantity=products[i][1], specs=products[i][2],
                                                                    is_trashed=False).first()
                                    # print('old_instance = ', old_instance)
                                    if old_instance.quantity < old_instance.max_quantity:
                                        old_instance.quantity += 1
                                        old_instance.specs = products[i][2]
                                        old_instance.save()
                                else:
                                    print('no product in the cart with this id')
                            else:
                                print('i != pro_index')
                    elif bleach.clean(request.GET.get('operator', None)) == 'negative':
                        # print(bleach.clean(request.GET.get('operator', None)))
                        pro_index = bleach.clean(request.GET.get('index', None))
                        # print(pro_index)
                        for i in range(len(products)):
                            # print(i)
                            if i == int(pro_index):
                                # print(pro_index)
                                product_instance = Product.objects.get(id=products[i][0], is_trashed=False)
                                # print(product_instance)
                                if Cart.objects.filter(user=request.user, product=product_instance,
                                                       is_trashed=False).exists():
                                    old_instance = Cart.objects.filter(user=request.user, product=product_instance,
                                                                    is_trashed=False).first()
                                    old_instance.quantity -= 1
                                    old_instance.specs = products[i][2]
                                    old_instance.save()
                                else:
                                    print('no product in the cart with this id')
                            else:
                                print('i != pro_index')
                    elif bleach.clean(request.GET.get('operator', None)) == 'type':
                        # print(bleach.clean(request.GET.get('operator', None)))
                        pro_index = bleach.clean(request.GET.get('index', None))
                        # print(pro_index)
                        for i in range(len(products)):
                            # print(i)
                            if i == int(pro_index):
                                # print(pro_index)
                                product_instance = Product.objects.get(id=products[i][0], is_trashed=False)
                                # print(product_instance)
                                if Cart.objects.filter(user=request.user, product=product_instance,
                                                       is_trashed=False).exists():
                                    old_instance = Cart.objects.get(user=request.user, product=product_instance,
                                                                    quantity=products[i][1], specs=products[i][2],
                                                                    is_trashed=False)
                                    if old_instance.quantity < old_instance.max_quantity:
                                        old_instance.quantity = bleach.clean(
                                            request.GET.get('cart[' + str(i) + ']', None))
                                        old_instance.specs = products[i][2]
                                        old_instance.save()
                                else:
                                    print('no product in the cart with this id')
                            else:
                                print('i != pro_index')
                    else:
                        print('no operators')
                else:
                    print('not user')
            ###################################################
    return HttpResponseRedirect('/order/')


def deleteCookieProduct(request):
    if request.GET:
        if 'khufu_cart' in request.session and request.GET['deleted'] == 'true':
            products = request.session['khufu_cart']['product']
            ###################################################
            ############# Registered User #####################
            if request.user.is_authenticated:
                print('proid = ', bleach.clean(request.GET.get('proid')))
                product_instance = Product.objects.get(id=bleach.clean(request.GET.get('proid')))
                product_quantity = bleach.clean(request.GET.get('quantity'))
                cart_id = bleach.clean(request.GET.get('cartid'))
                if Cart.objects.filter(id=cart_id, user=request.user, product=product_instance,
                                       quantity=product_quantity, is_trashed=False).exists():
                    Cart.objects.get(id=cart_id, user=request.user, product=product_instance, quantity=product_quantity,
                                     is_trashed=False).delete()
                    user_cart = Cart.objects.filter(user=request.user, is_trashed=False)
                    product_list = []
                    for i in user_cart:
                        product_list.append([i.product.id, i.quantity, i.specs, i.max_quantity, i.id])
                    # print(product_list)
                    context = {
                        'product': product_list,
                        'items': len(product_list),
                    }
                    # print(context)
                    request.session['khufu_cart'] = context
                else:
                    print('no product with this id')
            ###################################################
            else:
                # print('products = ', products)
                # print('proid = ', bleach.clean(request.GET.get('proid')))
                # print('cartid = ', bleach.clean(request.GET.get('cartid')))
                # for p in range(len(products)):
                #     print('p = ', products[p])
                #     if products[p][0] == bleach.clean(request.GET.get('proid')) and products[p][1] == bleach.clean(request.GET.get('quantity')):
                #         print('p1 = ', products[p])
                products.pop(int(bleach.clean(request.GET.get('cartid'))))
                        # products.remove(
                        #     [bleach.clean(request.GET.get('proid')), bleach.clean(request.GET.get('quantity')),
                        #      products[p][2], products[p][3]])
                context = request.session['khufu_cart']
                context.update({
                    'product': products,
                    'items': len(products),
                })
                request.session['khufu_cart'] = context
            return JsonResponse({'url': '/order/', })
    return HttpResponseRedirect('/order/')


def addCookie(request):
    if request.GET:
        pid = bleach.clean(request.GET['productid'])
        quantity = bleach.clean(request.GET['quantity'])
        product_specs = bleach.clean(request.GET['product_specs'])
        max_quantity = bleach.clean(request.GET['max_quantity'])
        avail_quan_in_cart = 0
        if int(quantity) > int(max_quantity):
            return JsonResponse({'done': True,'remain': False})
        # print(pid)
        # print(quantity)
        # print(max_quantity)
        # print(product_specs)
        if 'khufu_cart' not in request.session:
            request.session['khufu_cart'] = {
                'product': [(pid, quantity, product_specs, max_quantity), ],
                'items': 1,
            }
        else:
            context = request.session['khufu_cart']
            product_list = context['product']
            avail_quan = get_quantity(pid)
            if int(avail_quan) == -1:
                avail_quan = int(max_quantity)
            # print('avail_quan = ', avail_quan)
            for prod in product_list:
                if int(prod[0]) == int(pid):
                    # print('product already in cart')
                    avail_quan_in_cart += int(prod[1])
                    # print('avail_quan_in_cart = ', avail_quan_in_cart)
            if int(avail_quan) > int(avail_quan_in_cart):
                avail_remain = int(avail_quan) - int(avail_quan_in_cart)
                # print('avail_quan = ', avail_quan)
                # print('avail_quan_in_cart = ', avail_quan_in_cart)
                # print('avail_remain = ', avail_remain)
                if int(avail_remain) > int(quantity):
                    product_list.append((pid, int(quantity), product_specs, max_quantity))
                else:
                    product_list.append((pid, int(avail_remain), product_specs, max_quantity))
                # print('product_list = ', product_list)
            else:
                # print('go to cart')
                return JsonResponse({'done': False,'remain': True})
            context.update({
                'product': product_list,
                'items': len(product_list),
            })
            request.session['khufu_cart'] = context
            # print(request.session['khufu_cart'])
        ############# Registered User #####################
        if request.user.is_authenticated:
            product_instance = Product.objects.get(id=pid, is_trashed=False)
            cart = Cart.objects.create(user=request.user, product=product_instance, quantity=quantity,
                                       specs=product_specs, max_quantity=max_quantity, is_trashed=False)
            cart.save()
        ###################################################
        return HttpResponseRedirect('/productHome/product/' + pid)
