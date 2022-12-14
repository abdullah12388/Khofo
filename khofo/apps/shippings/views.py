# django
from datetime import datetime, timedelta, date
import bleach
import requests
import random
import json
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
# models
from ..orders.models import Cart, Order
from ..shippings.models import Express, ShippingTime
from ..products.models import Product, ProductOffer
from ..support.models import SiteInfo
from ..user.models import BuyerUserDetails, Country
from ..products import views as product_views


@login_required
def choose_shipping(request):
    if 'khufu_cart' not in request.session:
        return HttpResponseRedirect('/')
    else:
        if 'product' in request.session['khufu_cart']:
            products = request.session['khufu_cart']['product']
            products_list = []
            for product in products:
                products_list += Product.objects.filter(id=product[0], is_trashed=False)
            for index in range(len(products)):
                products[index][0] = products_list[index]

            context = {
                'product': products,
                # 'form': form,
                'items': len(products),
            }
            # if 'del' in request.GET:
            #     print('del in session')
            #     if request.GET['del'] == 'deleted':
            #         print('del == deleted')
            #         print(request.session['khufu_cart'])
            #         # del request.session['khufu_cart']
            #         request.session['khufu_cart'] = {
            #             'product': [],
            #             'items': 0,
            #         }
            return render(request, 'account/shipping.html', context)
    return render(request, 'account/shipping.html', {'items': 0})


# Ajax
# -------------------------------------------------------------------------------------------------------------------

# Calculate shipping price Algorithm
@login_required
def shipping_details(request):
    context = {
        'done': False,
    }
    if request.GET and request.user.is_authenticated:
        print("request.GET = ", request.GET)
        products_count = request.GET.get('products_count', None)
        if products_count:
            products_count = int(bleach.clean(products_count))
            if products_count > 0:
                express = []
                air_freight = []
                sea_freight = []
                for index in range(products_count):
                    id = request.GET.get('id[' + str(index) + ']', None)
                    name = request.GET.get('name[' + str(index) + ']', None)
                    quantity = request.GET.get('quantity[' + str(index) + ']', None)
                    weight = request.GET.get('weight[' + str(index) + ']', None)
                    size = request.GET.get('size[' + str(index) + ']', None)
                    shipping_type = request.GET.get('shipping_type[' + str(index) + ']', None)
                    if id and name and quantity and weight and size and shipping_type:
                        id = int(bleach.clean(id))
                        name = str(bleach.clean(name))
                        quantity = int(bleach.clean(quantity))
                        weight = float(bleach.clean(weight))
                        size = float(bleach.clean(size))
                        shipping_type = str(bleach.clean(shipping_type))
                        print("id = ", id, " // quantity = ", quantity, " // weight = ", weight,
                              " // size = ", size, " //shipping_type = ", shipping_type)
                        product_dict = {
                            'id': id,
                            'name': name,
                            'quantity': quantity,
                            'weight': weight,
                            'size': size,
                            'shipping_type': shipping_type,
                        }
                        if shipping_type == 'express':
                            express_length = len(express)
                            express = lowest_weight(express_length, product_dict, weight, express)
                        elif shipping_type == 'air_freight':
                            air_freight_length = len(air_freight)
                            air_freight = lowest_weight(air_freight_length, product_dict, weight, air_freight)
                        elif shipping_type == 'sea_freight':
                            sea_freight_length = len(sea_freight)
                            sea_freight = lowest_weight(sea_freight_length, product_dict, weight, sea_freight)
                print('express = ', express)
                print('air_freight = ', air_freight)
                print('sea_freight = ', sea_freight)
                if len(express) > 0:
                    express_company_list = Express.objects.all().distinct('shipping_company').values_list(
                        'shipping_company', flat=True)
                    if len(express_company_list) > 0:
                        start_weight = express[0]['weight']
                        end_weight = sum([ex['weight'] * ex['quantity'] for ex in express])
                        express_obj = Express.objects.filter(slice_max__gte=start_weight, slice_min__lte=end_weight,
                                                             is_trashed=False)
                        print("express_obj = ", express_obj.order_by('price_average').values_list('shipping_company',
                                                                                                  flat=True).distinct())
                        print("express_company_list = ", express_company_list)
                        express_obj = express_obj.order_by('price_average')
                        print("express_obj = ", express_obj)
                        price_list = []
                        shipping_company_list = []
                        for company in express_company_list:
                            express_object = express_obj.filter(shipping_company_id=company)
                            print("express_obja = ", express_object)
                            express_package = get_express_package(express_object, express)
                            print('express_package__ = ', express_package)
                            if len(express_package) > 0:
                                price = 0
                                for exp_pack in express_package:
                                    print('exp_pack = ', exp_pack[-1]['price'])
                                    price += exp_pack[-1]['price']
                                print("price = ", price)
                                price_list.append(price)
                                shipping_company_list.append(company)

                        print("price_list = ", price_list)
                        print("shipping_company_list = ", shipping_company_list)
                        if len(price_list) > 0:
                            smallest_price = min(price_list)
                            shipping_company_id = shipping_company_list[price_list.index(smallest_price)]
                            buyer = BuyerUserDetails.objects.filter(user_id=request.user.id)
                            if buyer.exists():
                                country = buyer.first().country.id
                                print("country = ", country)
                                shipping_time = ShippingTime.objects.filter(country_id=country, shipping_type='express',
                                                                            shipping_company_id=shipping_company_id)
                                if shipping_time.exists():
                                    shipping_time = shipping_time.first()
                                    days = shipping_time.days
                                    now = datetime.now().strftime('%d-%m-%Y')
                                    after = date.today() + timedelta(days=days)
                                    print('shipping_time = ', shipping_time.days)
                                    print("now = ", now)
                                    print("after = ", after.strftime('%B %d, %Y'))
                                    ###############USER ADDRESS##################
                                    _address = buyer.first().address
                                    _country = Country.objects.get(pk=buyer.first().country.id).name
                                    _region = buyer.first().region
                                    _city = buyer.first().city
                                    _zip_code = buyer.first().zip_code
                                    _user_email = buyer.first().user.email
                                    print(_address, _country, _region, _city, _zip_code)
                                    #############################################
                                    ###############SITE INFO##################
                                    site_info = SiteInfo.objects.all()
                                    _site_address = site_info.first().address
                                    _email = site_info.first().email
                                    _phone = site_info.first().phone
                                    _name = site_info.first().name
                                    print(_site_address, _email, _phone, _name, _user_email)
                                    #############################################
                                    context.update({
                                        'done': True,
                                        'express': {
                                            'price': float("{0:.2f}".format(smallest_price)),
                                            'afterDate': after.strftime('%B %d, %Y'),
                                            'shipping_company_id': shipping_company_id,
                                            'type': 'express',
                                        },
                                        'air': {
                                            'price': 20.0,
                                            'afterDate': after.strftime('%B %d, %Y'),
                                            'shipping_company_id': shipping_company_id,
                                            'type': 'air',
                                        },
                                        'sea': {
                                            'price': 30.0,
                                            'afterDate': after.strftime('%B %d, %Y'),
                                            'shipping_company_id': shipping_company_id,
                                            'type': 'sea',
                                        },
                                        'user_address': {
                                            'address': _address,
                                            'country': _country[0:3].upper(),
                                            'region': _region,
                                            'city': _city,
                                            'zip_code': _zip_code,
                                        },
                                        'user_email': _user_email,
                                        'site_info': {
                                            'site_address': _site_address,
                                            'email': _email,
                                            'phone': _phone,
                                            'name': _name,
                                        }
                                    })
                                else:
                                    print("There's no shipping time data in the table")
                            else:
                                print("this user has no address book")
                    else:
                        print("Express table is empty")
    return JsonResponse(context)


"""
def shipping_details(request):
    context = {
        'done': False,
    }
    if request.GET and request.user.is_authenticated:
        # print("request.GET = ", request.GET)
        products_count = request.GET.get('products_count', None)
        if products_count:
            products_count = int(bleach.clean(products_count))
            if products_count > 0:
                express = []
                air_freight = []
                sea_freight = []
                ############################################
                slice_price = 0
                min_w = 0
                max_w = 0
                Acc_weight = 0
                shipping_packages = ''
                Remaining_weight = 0
                cost = 0
                f = False
                cart_list = []
                slices_list = []
                package_list = []
                Remaining_list = []
                total_cost = 0
                ############################################
                for index in range(products_count):
                    id = request.GET.get('id[' + str(index) + ']', None)
                    name = request.GET.get('name[' + str(index) + ']', None)
                    quantity = request.GET.get('quantity[' + str(index) + ']', None)
                    weight = request.GET.get('weight[' + str(index) + ']', None)
                    size = request.GET.get('size[' + str(index) + ']', None)
                    shipping_type = request.GET.get('shipping_type[' + str(index) + ']', None)
                    if id and name and quantity and weight and size and shipping_type:
                        id = int(bleach.clean(id))
                        name = str(bleach.clean(name))
                        quantity = int(bleach.clean(quantity))
                        weight = float(bleach.clean(weight))
                        size = float(bleach.clean(size))
                        shipping_type = str(bleach.clean(shipping_type))
                        # print("id = ", id, " // quantity = ", quantity, " // weight = ", weight,
                        #       " // size = ", size, " //shipping_type = ", shipping_type)
                        product_dict = {
                            'id': id,
                            'name': name,
                            'quantity': quantity,
                            'weight': weight,
                            'size': size,
                            'shipping_type': shipping_type,
                        }
                        if shipping_type == 'express':
                            express_length = len(express)
                            express = lowest_weight(express_length, product_dict, weight, express)
                        elif shipping_type == 'air_freight':
                            air_freight_length = len(air_freight)
                            air_freight = lowest_weight(air_freight_length, product_dict, weight, air_freight)
                        elif shipping_type == 'sea_freight':
                            sea_freight_length = len(sea_freight)
                            sea_freight = lowest_weight(sea_freight_length, product_dict, weight, sea_freight)
                # print('express = ', express)
                # print('air_freight = ', air_freight)
                # print('sea_freight = ', sea_freight)
                if len(express) > 0:
                    express_company_list = Express.objects.all().distinct('shipping_company').values_list(
                        'shipping_company', flat=True)
                    start_weight = express[0]['weight']
                    end_weight = sum([ex['weight'] * ex['quantity'] for ex in express])
                    express_obj = Express.objects.filter(slice_max__gte=start_weight, slice_min__lte=end_weight,
                                                         is_trashed=False)
                    # print("express_obj = ", express_obj.order_by('price_average').values_list('shipping_company', flat=True).distinct())
                    # print("express_company_list = ", express_company_list)
                    express_obj = express_obj.order_by('price_average')
                    # print("express_obj = ", express_obj)
                ###################################################################
                    for eo in express_obj:
                        slices_list.append({'slice_min': eo.slice_min,'slice_max': eo.slice_max,'price_average': eo.price_average},)
                    cart_list = express
                    # print('cart list = ', cart_list)
                    # print('slices_list = ', slices_list)
                    for s in slices_list:
                        min_w = s['slice_min']
                        max_w = s['slice_max']
                        slice_price = s['price_average']
                        if cart_list is None:
                            break
                        for rl in Remaining_list:
                            if rl['quantity'] != 0:
                                cart_list.append(rl)
                            else:
                                Remaining_list = []
                        while True:
                            Remaining_weight = 0
                            f = False
                            for item2 in cart_list:
                                if item2['weight'] <= max_w and item2['quantity'] != 0:
                                    f = True
                                    break
                            if f is False:
                                break
                            for item in range(len(cart_list)):  # cart loop
                                if cart_list[item]['weight'] > max_w:
                                    break
                                if cart_list[item]['quantity'] != 0:
                                    for q in range(cart_list[item]['quantity']):  # product loop
                                        Acc_weight += cart_list[item]['weight']
                                        if Acc_weight > max_w:
                                            Acc_weight -= cart_list[item]['weight']
                                            break
                                        else:
                                            package_list.append({'name': cart_list[item]['name'], 'quantity': 1,
                                                                 'weight': cart_list[item]['weight']}, )
                                            cart_list[item]['quantity'] -= 1
                            for item3 in range(len(Remaining_list)):  # Remaining loop
                                if Remaining_list[item3]['weight'] > max_w:
                                    break
                                if Remaining_list[item3]['quantity'] != 0:
                                    Acc_weight += Remaining_list[item3]['weight']
                                    if Acc_weight > max_w:
                                        Acc_weight -= Remaining_list[item3]['weight']
                                        break
                                    else:
                                        package_list.append({'name': Remaining_list[item3]['name'], 'quantity': 1,
                                                             'weight': Remaining_list[item3]['weight']}, )
                                        Remaining_list[item3]['quantity'] -= 1
                            if Acc_weight < min_w:
                                for pl in package_list:
                                    Remaining_list.append(pl)
                            else:
                                for p in range(len(package_list)):
                                    shipping_packages += package_list[p]['name'] + '+'
                                cost = int(Acc_weight) * int(slice_price)
                                total_cost += int(cost)
                                shipping_packages += ' , weight = ' + str(Acc_weight) + ' , cost = ' + str(cost) + '\n'
                            package_list = []
                            Acc_weight = 0
                            for item5 in cart_list:
                                if item5['quantity'] == 0:
                                    cart_list.remove(item5)
                            ####################################################################
                            # print('shipping packages = ', shipping_packages)
                            # print('total cost = ', total_cost)
    return JsonResponse(context)
"""


def send_api(request):
    context = {
        'done': False
    }
    if request.GET:
        order_id = random.randrange(999999999)
        # print('request.LANGUAGE_CODE = ', request.LANGUAGE_CODE)
        # print('country_short = ', request.session['site_info']['country_short'])
        if request.session['site_info']['country_short'] == 'EG':
            if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == "ar-eg":
                language = 'ar_EG'
            else:
                language = 'en_US'
            currency = 'EGP'
            merchant_id = 'TESTKHOFU_EGP'
            url = 'https://banquemisr.gateway.mastercard.com/api/rest/version/54/merchant/TESTKHOFU_EGP/session'
            data = {
                'apiOperation': "CREATE_CHECKOUT_SESSION",
                'interaction': {
                    'operation': "PURCHASE",
                },
                'order': {
                    'id': order_id,
                    'currency': "EGP"
                }
            }
            user = 'Merchant.TESTKHOFU_EGP'
            password = '50484e0dd923993588a9098834f32bd4'
        else:
            if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == "ar-eg":
                language = 'ar_EG'
            else:
                language = 'en_US'
            currency = 'USD'
            merchant_id = 'TESTKHOFU'
            url = 'https://banquemisr.gateway.mastercard.com/api/rest/version/54/merchant/TESTKHOFU/session'
            data = {
                'apiOperation': 'CREATE_CHECKOUT_SESSION',
                'interaction': {
                    'operation': 'PURCHASE',
                },
                'order': {
                    'id': order_id,
                    'currency': 'USD'
                }
            }
            user = 'Merchant.TESTKHOFU'
            password = '18efdc814b3dfa86fa141b92a79ec896'
        # print('order_id = ', order_id)
        # print('merchant_id = ', merchant_id)
        # print('currency = ', currency)
        # print('language = ', language)
        # print('url = ', url)
        # print('data = ', json.dumps(data))
        # print('user = ', user)
        # print('password = ', password)
        resp = requests.post(url, data=json.dumps(data), auth=(user, password))
        # print('post api = ', resp)
        # print('post api status_code = ', resp.status_code)
        if resp.status_code == 201:
            # print('post api = ', resp.status_code)
            # print('response = ', resp.json())
            context.update({
                'done': True,
                'res': resp.json(),
                'merchant': merchant_id,
                'currency': currency,
                'locale': language,
                'order_id': order_id,
            })
        return JsonResponse(context)

# Save Order from Cart after Payment Success
def request_order(request):
    context = {
        'done': False
    }
    if request.GET:
        scid = request.GET.get('scid')
        invoice = request.GET.get('invoice')
        if scid and invoice:
            scid = bleach.clean(scid.strip())
            invoice = bleach.clean(invoice.strip())
            # print("scid = ", scid)
            # print("invoice = ", invoice)
            if 'site_info' in request.session:
                if 'country_short' in request.session['site_info']:
                    if request.session['site_info']['country_short'] == 'EG':
                        money_type = 2
                    else:
                        money_type = 1
                    user_buyer = BuyerUserDetails.objects.filter(user_id=request.user.id)
                    if user_buyer.exists():
                        user_buyer = user_buyer.first()
                        # print("user = ", request.user.id)
                        # print("user_buyer = ", user_buyer)
                        cart_list = Cart.objects.filter(user_id=request.user.id)
                        if cart_list.exists():
                            # print('cart_list = ', cart_list)
                            for cart in cart_list:
                                if cart.quantity > 0:
                                    product_obj = Product.objects.filter(id=cart.product_id, is_trashed=False)
                                    if product_obj.exists():
                                        product_obj = product_obj.first()
                                        # print('product_obj = ', product_obj)
                                        order = Order.objects.create(
                                            user=user_buyer,
                                            category_id=product_obj.category.id,
                                            sub_category_id=product_obj.sub_category.id,
                                            delegate_id=product_obj.sub_category.delegate.id,
                                            money_type=money_type,
                                            product=product_obj,
                                            quantity=cart.quantity,
                                            status='ordered',
                                            provider_id=product_obj.provider.id,
                                            shipping_id=scid,
                                            specification=cart.specs,
                                            invoice_id=invoice,
                                        )
                                        # print('order = ', order)
                                        order.save()
                                        available_quantity = product_views.get_quantity(product_obj.id)
                                        if not available_quantity is -1:
                                            # print('in available_quantity')
                                            if available_quantity < 1:
                                                product_obj.is_trashed = True
                                                product_obj.save()
                                                product_offers = ProductOffer.objects.filter(product=product_obj)
                                                if product_offers.exists():
                                                    for product_offer in product_offers:
                                                        product_offer.is_trashed = True
                                                        product_offer.save()
                                                # Cart.objects.filter(product_id=product_obj.id).update(is_trashed=True)
                                        # print('product_obj = ', product_obj.is_trashed)
                            Cart.objects.filter(user_id=request.user.id).delete()
                        if 'del' in request.GET:
                            print('del in session')
                            if request.GET['del'] == 'deleted':
                                print('del == deleted')
                                print(request.session['khufu_cart'])
                                del request.session['khufu_cart']
                                request.session['khufu_cart'] = {
                                    'product': [],
                                    'items': 0,
                                }
                        context = {
                            'done': True
                        }
                    else:
                        print("this user has no buyer details")
                else:
                    print("country_short not in request.session['site_info']")
            else:
                print("site_info not in request.session")
        print("scid or invoice is empty")
    return JsonResponse(context)


# Outer Functions
# -----------------------------------------------------------------------------------------------------------------------

# Outer Function

def lowest_weight(length, product_dict, weight, shipping_type):
    if length == 0:
        shipping_type.append(product_dict)
    elif length > 0:
        if weight < shipping_type[length - 1]['weight']:
            if length == 1:
                shipping_type.insert(0, product_dict)
            else:
                for j in range((length - 2), -1, -1):
                    if weight < shipping_type[j]['weight']:
                        if j == 0:
                            shipping_type.insert(j, product_dict)
                            break
                        continue
                    else:
                        shipping_type.insert((j + 1), product_dict)
                        break
        else:
            shipping_type.append(product_dict)
    return shipping_type


# Outer Function
def get_express_package(express_obj, express):
    express_package = []
    RTNP_Max = []
    for exp_obj in express_obj:
        print("exp_obj = ", exp_obj)
        print("express = ", express)
        RTNP = []
        for product in express:
            print('product = ', product)
            weight = product['weight']
            quantity = product['quantity']
            mini = exp_obj.slice_min
            maxi = exp_obj.slice_max
            rate = exp_obj.rate
            initial = exp_obj.initial_cost
            if len(RTNP) < 1:
                print("len(RTNP) < 1")
                total_weight = weight * quantity
                if total_weight > mini:
                    if weight <= maxi:
                        fitQ = 0
                        Q = 1
                        while Q <= quantity:
                            weight_Q = weight * Q
                            if weight_Q > maxi:
                                if fitQ > 0:
                                    print("weight_Q > max && fitQ > 0 ", fitQ)
                                    price = ((((fitQ * weight) - mini) * 2) * rate) + initial
                                    express_package.append([
                                        {
                                            'id': product['id'],
                                            'name': product['name'],
                                            'quantity': fitQ,
                                            'slice_min': mini,
                                            'slice_max': maxi,
                                        }, {'price': price, }
                                    ])
                                    print('express_package = ', express_package)
                                    # Edit the product Quantity of the Cart
                                    express[express.index(product)]['quantity'] = int(
                                        (express[express.index(product)]['quantity']) - fitQ)
                                    quantity = (quantity - Q) + 1
                                    Q = 0
                                    print("weight_Q > max && fitQ > 0 && not Q == quantity", quantity)
                                    print("product = ", product)
                                else:
                                    print("weight_Q > max && not fitQ > 0 ", fitQ)
                                    if Q == quantity:
                                        print(" not fitQ > 0 && Q == quantity", Q)
                                        RTNP.append({
                                            'quantity': 1,
                                            'id': product['id'],
                                            'name': product['name'],
                                            'weight': product['weight'],
                                        })
                                        break
                                    else:
                                        print("weight_Q > max && not fitQ > 0 && not Q == quantity", Q)
                                        if Q > 1:
                                            RTNP.append({
                                                'quantity': (Q - 1),
                                                'id': product['id'],
                                                'name': product['name'],
                                                'weight': product['weight'],
                                            })
                                        quantity = (quantity - Q) + 1
                                        Q = 0
                            elif weight_Q >= mini:
                                if Q == quantity:
                                    print("weight_Q >= mini && Q == quantity", Q)
                                    price = (((weight_Q - mini) * 2) * rate) + initial
                                    express_package.append([
                                        {
                                            'quantity': quantity,
                                            'id': product['id'],
                                            'name': product['name'],
                                            'slice_min': mini,
                                            'slice_max': maxi,
                                        },
                                        {'price': price, }
                                    ])
                                    # Edit the product Quantity of the Cart
                                    express[express.index(product)]['quantity'] = int(
                                        (express[express.index(product)]['quantity']) - quantity)
                                    print('express_package = ', express_package)
                                    print("product = ", product)
                                else:
                                    fitQ = Q
                                    print("weight_Q >= mini && not Q == quantity", fitQ)
                            elif weight_Q < mini:
                                print("weight_Q < mini", Q)
                                if Q == quantity:
                                    print("weight_Q < mini && Q == quantity", Q)
                                    RTNP.append({
                                        'quantity': Q,
                                        'id': product['id'],
                                        'name': product['name'],
                                        'weight': product['weight'],
                                    })
                            Q += 1
                        print("RTNP = ", RTNP)
                    else:
                        RTNP_Max.append({
                            'quantity': quantity,
                            'id': product['id'],
                            'name': product['name'],
                        })
                        print("len(RTNP) < 1 /// RTNP_Max = ", RTNP_Max)
                else:
                    RTNP.append({
                        'quantity': quantity,
                        'id': product['id'],
                        'name': product['name'],
                        'weight': product['weight'],
                    })
            else:
                print("RTNP > 1")
                print("RTNP = ", RTNP)
                if weight <= maxi:
                    break_rtnp = False
                    quantity_1 = product['quantity']
                    for rtnp in RTNP:
                        weight_2 = rtnp['weight']
                        quantity_2 = rtnp['quantity']
                        total_weight = (weight_2 * quantity_2) + (quantity_1 * product['weight'])
                        print("total_weight = ", total_weight)
                        if total_weight > mini:
                            break_Q2 = False
                            Q2 = 1
                            print("rtnp = ", rtnp)
                            while Q2 <= quantity_2:
                                weight_Q2 = weight_2 * Q2
                                print("first loop quantity_2 = ", quantity_2)
                                print("Q2 = ", Q2)
                                print("weight_Q2 = ", weight_Q2)
                                #####################
                                weight_1 = product['weight']
                                fitQ1 = 0
                                Q1 = 1
                                while Q1 <= quantity_1:
                                    print("first loop quantity_1 = ", quantity_1)
                                    print("first loop quantity_1 --> quantity_2 = ", quantity_2)
                                    print("Q2 = ", Q2)
                                    print("Q1 = ", Q1)
                                    weight_Q1 = weight_1 * Q1
                                    sum_weight = weight_Q2 + weight_Q1
                                    print("sum_weight = ", sum_weight)
                                    if sum_weight > maxi:
                                        if fitQ1 > 0:
                                            print("sum_weight > maxi /// fitQ1 > 0")
                                            price = (((weight_Q2 + weight_Q1) * 2) * rate) + initial
                                            express_package.append([
                                                {'id': product['id'], 'name': product['name'],
                                                 'quantity': fitQ1, 'slice_min': mini,
                                                 'slice_max': maxi},
                                                {'id': rtnp['id'], 'name': rtnp['name'], 'quantity': Q2,
                                                 'slice_min': mini,
                                                 'slice_max': maxi},
                                                {'price': price, },
                                            ])
                                            # Edit the product Quantity of the Cart
                                            express[express.index(product)]['quantity'] = int(
                                                (express[express.index(product)]['quantity']) - fitQ1)
                                            express_q2 = next((product for product in express
                                                               if product['id'] == rtnp['id']), None)
                                            express_q2['quantity'] = express_q2['quantity'] - Q2
                                            print("express_q2 = ", express_q2)
                                            print('express_package = ', express_package)
                                            RTNP[RTNP.index(rtnp)]['quantity'] = quantity_2 - Q2
                                            quantity_1 = (quantity_1 - Q1) + 1
                                            Q1 = 0

                                            if Q2 == quantity_2:
                                                break_Q2 = True
                                                break
                                            else:
                                                quantity_2 = quantity_2 - Q2
                                                Q2 = 1
                                            print("quantity_2 = ", quantity_2)
                                            print("quantity_1 = ", quantity_1)
                                            print("RTNP[RTNP.index(rtnp)]['quantity'] = ",
                                                  RTNP[RTNP.index(rtnp)]['quantity'])
                                            print("product = ", product)
                                        else:
                                            if Q1 == quantity_1 and int(RTNP.index(rtnp) + 1) < len(RTNP):
                                                print("sum_weight > maxi /// not fitQ1 > 0 ///"
                                                      " Q1 == quantity_1 and RTNP.index(rtnp) < len(RTNP)")
                                                break_Q2 = True
                                                break
                                            elif Q1 == quantity_1 and int(RTNP.index(rtnp) + 1) == len(
                                                    RTNP):
                                                print("sum_weight > maxi /// not fitQ1 > 0 ///"
                                                      " Q1 == quantity_1 and RTNP.index(rtnp) == len(RTNP)")
                                                break_Q2 = True
                                                break_rtnp = True
                                                break
                                            else:
                                                if Q1 > 1:
                                                    if int(RTNP.index(rtnp) + 1) == len(RTNP):
                                                        print("sum_weight > maxi /// not fitQ1 > 0 ///"
                                                              " Q1 > 1 and RTNP.index(rtnp) == len(RTNP)")
                                                        RTNP.append({
                                                            'quantity': Q1 - 1,
                                                            'id': product['id'],
                                                            'name': product['name'],
                                                            'weight': product['weight'],
                                                        })
                                                        break_Q2 = True
                                                        break_rtnp = True
                                                    else:
                                                        print("sum_weight > maxi /// not fitQ1 > 0 /// "
                                                              "Q1 >1 and not RTNP.index(rtnp) == len(RTNP)")
                                                        break_Q2 = True
                                    elif sum_weight >= mini:
                                        if Q1 == quantity_1 and Q2 == quantity_2:
                                            print("sum_weight >= mini /// Q1 == quantity_1 and Q2 == quantity_2 ")
                                            price = ((((weight_Q2 + weight_Q1) - mini) * 2) * rate) + initial
                                            express_package.append([
                                                {'id': product['id'], 'name': product['name'],
                                                 'quantity': Q1, 'slice_min': mini,
                                                 'slice_max': maxi},
                                                {'id': rtnp['id'], 'name': rtnp['name'], 'quantity': Q2,
                                                 'slice_min': mini,
                                                 'slice_max': maxi},
                                                {'price': price},
                                            ])
                                            # Edit the product Quantity of the Cart
                                            express[express.index(product)]['quantity'] = int(
                                                (express[express.index(product)]['quantity']) - Q1)
                                            express_q2 = next((product for product in express
                                                               if product['id'] == rtnp['id']), None)
                                            express_q2['quantity'] = express_q2['quantity'] - Q2
                                            print("express_q2 = ", express_q2)
                                            print('express_package = ', express_package)
                                            RTNP[RTNP.index(rtnp)]['quantity'] = RTNP[RTNP.index(rtnp)][
                                                                                     'quantity'] - Q2
                                            quantity_1 = 0
                                            print("quantity_1 = ", quantity_1)
                                            print("RTNP[RTNP.index(rtnp)]['quantity'] = ",
                                                  RTNP[RTNP.index(rtnp)]['quantity'])
                                            print("product = ", product)

                                            break_Q2 = True
                                            break_rtnp = True
                                            break
                                        else:
                                            print("sum_weight >= mini /// not Q1 == quantity_1 ")
                                            fitQ1 = Q1
                                    elif sum_weight < mini:
                                        print("sum_weight < mini")
                                        print("quantity_1 = ", quantity_1, " // Q1 = ", Q1)
                                        print("quantity_2 = ", quantity_2, "// Q2 = ", Q2)
                                        if Q1 == quantity_1:
                                            print("sum_weight < mini  ///  Q1 == quantity_1")
                                            if Q2 == quantity_2 and int(RTNP.index(rtnp) + 1) == len(RTNP):
                                                print("sum_weight < mini ///Q1 == quantity_1 ///  "
                                                      "Q2 == quantity_2 and RTNP.index(rtnp) == len(RTNP)")
                                                break_Q2 = True
                                                break_rtnp = True
                                    Q1 += 1
                                    print("end of quantity1 LOOP")
                                Q2 += 1
                                if break_Q2:
                                    break
                            if break_rtnp:
                                break
                        else:
                            print("total_weight > mini")

                    if quantity_1 > 0:
                        print('RTNP finished and the quantity of the product did not finish, quantity > 0')
                        print('express = ', express)
                        print('express_package = ', express_package)
                        print('RTNP = ', RTNP)
                        print('quantity = ', quantity_1)
                        fitQ = 0
                        Q = 1
                        while Q <= quantity_1:
                            weight_Q = weight * Q
                            print("weight_Q = ", weight_Q)
                            if weight_Q > maxi:
                                if fitQ > 0:
                                    print("weight_Q > max && fitQ > 0 ", fitQ)
                                    price = ((((fitQ * weight) - mini) * 2) * rate) + initial
                                    express_package.append([
                                        {
                                            'id': product['id'],
                                            'name': product['name'],
                                            'quantity': fitQ,
                                            'slice_min': mini,
                                            'slice_max': maxi,
                                        },
                                        {'price': price, }
                                    ])
                                    print('express_package = ', express_package)
                                    # Edit the product Quantity of the Cart
                                    express[express.index(product)]['quantity'] = int(
                                        (express[express.index(product)]['quantity']) - fitQ)
                                    quantity_1 = (quantity_1 - Q) + 1
                                    Q = 0
                                    print("weight_Q > max && fitQ > 0 && not Q == quantity", quantity_1)
                                    print("product = ", product)
                                    print("express_package = ", express_package)
                                else:
                                    print("weight_Q > max && not fitQ > 0 ", fitQ)
                                    if Q == quantity_1:
                                        print(" not fitQ > 0 && Q == quantity", Q)
                                        RTNP.append({
                                            'quantity': 1,
                                            'id': product['id'],
                                            'name': product['name'],
                                            'weight': product['weight'],
                                        })
                                        print("RTNP = ", RTNP)
                                        break
                                    else:
                                        print("weight_Q > max && not fitQ > 0 && not Q == quantity", Q)
                                        if Q > 1:
                                            RTNP.append({
                                                'quantity': (Q - 1),
                                                'id': product['id'],
                                                'name': product['name'],
                                                'weight': product['weight'],
                                            })
                                            print("RTNP = ", RTNP)
                                        quantity_1 = (quantity_1 - Q) + 1
                                        Q = 0
                            elif weight_Q >= mini:
                                if Q == quantity_1:
                                    print("weight_Q >= mini && Q == quantity", Q)
                                    price = (((weight_Q - mini) * 2) * rate) + initial
                                    express_package.append([
                                        {
                                            'quantity': quantity_1,
                                            'id': product['id'],
                                            'name': product['name'],
                                            'slice_min': mini,
                                            'slice_max': maxi,
                                        },
                                        {'price': price, }
                                    ])
                                    # Edit the product Quantity of the Cart
                                    express[express.index(product)]['quantity'] = int(
                                        (express[express.index(product)]['quantity']) - quantity_1)
                                    print('express_package = ', express_package)
                                    print("product = ", product)
                                else:
                                    fitQ = Q
                                    print("weight_Q >= mini && not Q == quantity", fitQ)
                            elif weight_Q < mini:
                                print("weight_Q < mini", Q)
                                if Q == quantity_1:
                                    print("weight_Q < mini && Q == quantity", Q)
                                    RTNP.append({
                                        'quantity': Q,
                                        'id': product['id'],
                                        'name': product['name'],
                                        'weight': product['weight'],
                                    })
                                    print("RTNP = ", RTNP)
                            Q += 1

                        print("end of last loop")
                    print("Last RTNP = ", RTNP)
                else:
                    RTNP_Max.append({
                        'quantity': quantity,
                        'id': product['id'],
                    })

    return express_package
