# python
import subprocess
import sys
import bleach
import requests
# django
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
# models
from django.shortcuts import render
from ..products.models import Category, SubCategory
from ..support.models import SiteInfo
# forms
from .forms import EmailForm


# Create your views here.


# Contact Us
# --------------------------------------------------------------------
def contact_us(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            email_form = EmailForm(request.POST, request.FILES,
                                   initial={'name': request.user.username, 'email': request.user.email})
        else:
            email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            post = email_form.save(commit=False)
            post.name = bleach.clean(post.name.strip())
            post.email = bleach.clean(post.email.strip())
            post.message = bleach.clean(post.message.strip())
            post.save()
            title = 'Inquiry Message'
            html_content = '<span><h3>Name: {} </h3></span>' \
                           '<span><h3>Email: {} </h3></span>' \
                           '<span><h3>Message: {} </h3></span>'.format(post.name, post.email, post.message)

            try:
                email = EmailMultiAlternatives(title, to=[settings.RECEIVER_EMAIL])
                if post.document1:
                    email.attach(post.document1.name, post.document1.read())
                if post.document2:
                    email.attach(post.document2.name, post.document2.read())
                if post.document3:
                    email.attach(post.document3.name, post.document3.read())
                if post.document4:
                    email.attach(post.document4.name, post.document4.read())
                if post.document5:
                    email.attach(post.document5.name, post.document5.read())
                email.attach_alternative(html_content, "text/html")
                email.send()
            except BadHeaderError as error:
                print("error contact_us : ", error)
                return HttpResponse('Invalid Email found.')
        else:
            print("contact_us form is invalid")
    else:
        if request.user.is_authenticated:
            email_form = EmailForm(initial={
                'name': request.user.username,
                'email': request.user.email
            })
        else:
            email_form = EmailForm()
    return render(request, "contact_us.html", {'email_form': email_form})


def get_site_info(request):
    data = {'done': False, }
    try:
        if request.GET:
            ip = request.GET.get('ip', None)
            if ip:
                ip = bleach.clean(ip.strip())
                # print('ip from JS = ', ip)
            else:
                ip = requests.get('http://ip.42.pl/raw').text
            python_path = sys.executable
            script_path = str(settings.PYTHON_SCRIPTS_DIR) + "/location.py"
            result = subprocess.check_output([python_path, script_path] + [str(ip)])
            location_result = eval(str(result.decode('ascii')))
            # print("location result = ", location_result)
            all_data = SiteInfo.objects.all()
            # print("site_info = ", len(all_data))
            if len(all_data) > 0:
                site_info = all_data.first()
                request.session['site_info'] = {
                    'name': site_info.name,
                    'name_ar': site_info.name_ar,
                    'phone': site_info.phone,
                    'email': site_info.email,
                    'address': site_info.address,
                    'address_ar': site_info.address_ar,
                    'postal_code': site_info.postal_code,
                    'logo': site_info.logo.url,
                    'logo_2': site_info.logo_2.url,
                    'login_logo': site_info.login_logo.url,
                    'dollar_rate': site_info.dollar_rate,
                    'language': site_info.language,
                    'facebook': site_info.facebook,
                    'twitter': site_info.twitter,
                    'google': site_info.google,
                    'youtube': site_info.youtube,
                    'instagram': site_info.instagram,
                    'wuzzuf': site_info.wuzzuf,
                    'linkedin': site_info.linkedin,
                    'knicks_link': site_info.knicks_link,
                    'knicks_logo': site_info.knicks_logo.url,
                    'country_short': location_result['country_short'],
                    'country_long': location_result['country_long'],
                }
                # get the footer information
                get_footer_info(request)
                # print("site_info session = ", request.session['site_info'])
                change_site_language(location_result['country_short'])
                # print("LANGUAGE_CODE = ", request.LANGUAGE_CODE)
                data.update({
                    "done": True,
                    "site_info": request.session['site_info'],
                })
            else:
                print("Error : site_info table have no data")
        else:
            print("Error : This not a Get request")
    except Exception as error:
        print("Error : ", error)
    return JsonResponse(data)


def get_site_info2(request):
    data = {'done': False, }
    if request.GET:
        all_data = SiteInfo.objects.all()
        # print("site_info = ", len(all_data))
        if len(all_data) > 0:
            site_info = all_data.first()
            if 'site_info' in request.session:
                if 'country_short' and 'country_long' in request.session['site_info']:
                    country_short = request.session['site_info']['country_short']
                    country_long = request.session['site_info']['country_long']
                    request.session['site_info'] = {
                        'name': site_info.name,
                        'name_ar': site_info.name_ar,
                        'phone': site_info.phone,
                        'email': site_info.email,
                        'address': site_info.address,
                        'address_ar': site_info.address_ar,
                        'postal_code': site_info.postal_code,
                        'logo': site_info.logo.url,
                        'logo_2': site_info.logo_2.url,
                        'login_logo': site_info.login_logo.url,
                        'dollar_rate': site_info.dollar_rate,
                        'language': site_info.language,
                        'facebook': site_info.facebook,
                        'twitter': site_info.twitter,
                        'google': site_info.google,
                        'youtube': site_info.youtube,
                        'instagram': site_info.instagram,
                        'wuzzuf': site_info.wuzzuf,
                        'linkedin': site_info.linkedin,
                        'knicks_link': site_info.knicks_link,
                        'knicks_logo': site_info.knicks_logo.url,
                        'country_short': country_short,
                        'country_long': country_long,
                    }
                    get_footer_info(request)
                    # print("site_info session = ", request.session['site_info'])
                    change_site_language(country_short)
                    data.update({
                        "done": True,
                        "site_info": request.session['site_info']
                    })
        else:
            print("Error : site_info table have no data")
    else:
        print("Error : This not a Get request")
    return JsonResponse(data)


def get_footer_info(request):
    categories = Category.objects.filter(is_trashed=False)
    if len(categories) > 0:
        category_list = []
        for category in categories:
            sub_category_list = []
            sub_categories = SubCategory.objects.filter(category=category, is_trashed=False)
            if sub_categories.exists():
                for sub_cat in sub_categories:
                    sub_category_list.append({
                        'id': sub_cat.id,
                        'name': sub_cat.name,
                        'name_ar': sub_cat.name_ar,
                    })
                category_list.append({
                    'category': [category.id, category.name],
                    'category_ar': [category.id, category.name_ar],
                    'sub_categories': sub_category_list
                })
        request.session['footer_info'] = category_list
        # print("category_list = ", request.session['footer_info'])


def change_site_language(country_short):
    country_list = ['OM', 'YE', 'SA', 'AE', 'QA', 'BH', 'KW', 'JO', 'LB', 'IQ', 'SY', 'EG', 'LY', 'TN',
                    'DZ', 'MA', 'MR', 'SO', 'SD', 'KM']
    if country_short in country_list:
        settings.LANGUAGE_CODE = "ar-eg"
    else:
        settings.LANGUAGE_CODE = "en-us"
