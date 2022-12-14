import math
import os

from django import template
from django.conf import settings
from django.shortcuts import get_object_or_404

from ..models import ProductOffer, Product, SubCategory, Category

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(0, number)


@register.filter()
def to_int(value):
    return int(value)


@register.filter
def ceil(value):
    try:
        return math.ceil(value)
    except (ValueError, ZeroDivisionError):
        return None


@register.filter()
def get_products(scid, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    return ProductOffer.objects.filter(sub_category=scid, is_trashed=False).filter(type=arg_list[0]).filter(
        showed_in=arg_list[1])


@register.filter()
def get_products_cat(catid, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    return ProductOffer.objects.filter(category=catid, is_trashed=False).filter(type=arg_list[0]).filter(
        showed_in=arg_list[1])


@register.filter()
def typeOf(fileUrl):
    allExtOfVideo = [
        '.webm',
        '.mkv',
        '.flv',
        '.vob',
        '.ogv',
        '.ogg',
        '.drc',
        '.gifv',
        '.mng',
        '.avi',
        '.MTS',
        '.M2TS',
        '.TS',
        '.mov',
        '.qt',
        '.wmv',
        '.yuv',
        '.rm',
        '.rmvb',
        '.asf ',
        '.amv',
        '.mp4',
        '.m4p',
        '.m4v',
        '.mpg',
        '.mp2',
        '.mpeg',
        '.mpe',
        '.mpv',
        '.mpg',
        '.mpeg',
        '.m2v',
        '.m4v',
        '.svi',
        '.3gp',
        '.3g2',
        '.mxf',
        '.roq',
        '.nsv',
        '.flv',
        '.f4v',
        '.f4p',
        '.f4a',
        '.f4b',
    ]
    allExtOfImage = [
        '.jpe',
        '.jpg',
        '.jpeg',
        '.gif',
        '.png',
        '.bmp',
        '.ico',
        '.svg',
        '.svgz',
        '.tif',
        '.tiff',
        '.ai',
        '.drw',
        '.pct',
        '.psp',
        '.xcf',
        '.psd',
        '.raw',
    ]
    ext = os.path.splitext(fileUrl)[1]
    if ext.lower() in allExtOfVideo:
        return 'video'
    elif ext.lower() in allExtOfImage:
        return 'image'
    else:
        return False


@register.filter()
def get_context_list(spec_name, context):
    return context[str(spec_name)]


@register.filter()
def get_products_count(scid):
    return Product.objects.filter(sub_category=scid, is_trashed=False).count()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter()
def price_discount(price, discount):
    price_discount = int(price) * float(int(discount) / 100)
    new_price = int(price) - price_discount
    return new_price


@register.simple_tag
def check_selection(enabled_List, spec_name, spec_value):
    # spec_name = str(args[0])
    # spec_value = str(args[1])
    spec_obj = {
        'spec_name': str(spec_name),
        'spec_value': str(spec_value),
    }
    # print("spec_obj = ", spec_obj)
    if spec_obj in enabled_List:
        return True
    return False


@register.filter()
def convert_money(price, dollar_rate):
    if price and dollar_rate:
        new_price = float(price) / float(dollar_rate)
        return float("{0:.2f}".format(new_price))
    return False


@register.filter()
def is_arabic(country_short):
    country_list = ['OM', 'YE', 'SA', 'AE', 'QA', 'BH', 'KW', 'JO', 'LB', 'IQ', 'SY', 'EG', 'LY', 'TN', 'DZ', 'MA',
                    'MR', 'SO', 'SD', 'KM']
    # print("country_short = ", country_short)
    # print("country_short in country_list = ", country_short in country_list)
    return country_short in country_list


@register.filter()
def get_cat_name(catid):
    return Category.objects.get(id=catid).name


@register.filter()
def get_sub_cat_name(subcatid):
    return SubCategory.objects.get(id=subcatid).name


@register.filter()
def change_lang(lang):
    settings.LANGUAGE_CODE = str(lang)
    # print(settings.LANGUAGE_CODE)
    return True


@register.filter()
def total_ads_duration(ads_list):
    total_duration = 0
    for ad in ads_list:
        total_duration = total_duration + int(ad.duration)
    return total_duration


@register.filter()
def subtrac(n1, n2):
    return int(n1 - n2)


@register.filter()
def get_product_img(proid):
    product = get_object_or_404(Product, pk=int(proid))
    return product.main_img


@register.filter()
def get_product_name(proid):
    product = get_object_or_404(Product, pk=int(proid))
    return product.name


@register.filter()
def get_product_name_ar(proid):
    product = get_object_or_404(Product, pk=int(proid))
    return product.name_ar


@register.filter()
def get_product_short_desc(proid):
    product = get_object_or_404(Product, pk=int(proid))
    return product.short_description

# @register.filter()
# def get_public_ip(ip):
#     ip = get('https://api.ipify.org').text
#     return ip
