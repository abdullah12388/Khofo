# Python
import bleach
# Django
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView, ListView
from langdetect import detect
# Models
from ..support.forms import EmailForm
from .models import Product, ProductImage, Category, SubCategory, ProductOffer, SpecName, SpecValue, \
    SpecValueChangeable, Review
from ..orders.models import Order
from ..advertisement import views as ads_view


# Create your views here.

# Views
# -----------------------------------------------------------------------------------

# Index (Home)
class CategoriesListView(ListView):
    template_name = 'index.html'
    context_object_name = 'categories'

    def get_queryset(self):
        categories = Category.objects.filter(is_trashed=False)
        if categories.count() > 0:
            products = Product.objects.filter(category_id__in=categories.values_list('id'), is_trashed=False)
            if products.count() > 0:
                categories = categories.filter(id__in=products.values_list('category_id')).order_by('show_num')
                return categories
        return False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoriesListView, self).get_context_data()
        category_names = get_all_categories_names()
        current_advers2 = get_current_advertisment(self.request, 'home')
        context.update({
            'catNames': category_names,
            'currentAdvers': current_advers2,
            'pageName': 'home',
        })
        return context


# Page of specific category
class CategoryListView(ListView):
    template_name = 'category.html'
    context_object_name = 'subCategory'

    def get_queryset(self):
        sub_categories = SubCategory.objects.filter(category=self.kwargs['pk'], is_trashed=False)
        if sub_categories.count() > 0:
            products = Product.objects.filter(sub_category_id__in=sub_categories.values_list('id'), is_trashed=False)
            if products.count() > 0:
                sub_categories = sub_categories.filter(id__in=products.values_list('sub_category_id')).order_by(
                    'category')
                return sub_categories
        return False

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        categories = Category.objects.filter(pk=self.kwargs['pk'], is_trashed=False)
        sub_categories = SubCategory.objects.filter(category=self.kwargs['pk'], is_trashed=False)
        withOff = []
        for sub_category in sub_categories:
            if ProductOffer.objects.filter(sub_category=sub_category, is_trashed=False):
                withOff.append(sub_category)
                # print(withOff)
            else:
                print('Not Exists')
        if len(withOff) > 0:
            context.update({
                'offers': withOff,
            })
        if categories.exists():
            currentAdvers = ads_view.advert(
                request=self.request, pageName=categories[0].name)
            if categories[0].name in self.request.session:
                show_num = self.request.session[categories[0].name]['num']
            else:
                show_num = 0
            currentAdvers2 = ads_view.sortAds(list(currentAdvers), int(show_num))
            context.update({
                'cat': categories,
                'currentAdvers': currentAdvers2,
                'pageName': categories[0].name,
            })
        return context


# products of specific sub_category
class ProductsList(ListView):
    template_name = "sub-category.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.method == 'GET':
            item_count = 30
            products = get_product_with_paginator(request=self.request, sub_category_id=self.kwargs['spk'],
                                                  items_count=item_count, order_by_type='show_num')
            sort = self.request.GET.get('sort', None)
            if sort:
                sort = bleach.clean(sort.strip())
                if sort == 'n':
                    products = get_product_with_paginator(request=self.request, sub_category_id=self.kwargs['spk'],
                                                          items_count=item_count, order_by_type='-created_on')
                    return products
                elif sort == 'l':
                    products = get_product_with_paginator(request=self.request, sub_category_id=self.kwargs['spk'],
                                                          items_count=item_count, order_by_type='price')
                    return products
                elif sort == 'h':
                    products = get_product_with_paginator(request=self.request, sub_category_id=self.kwargs['spk'],
                                                          items_count=item_count, order_by_type='-price')
                    return products
            return products

    def get_context_data(self, **kwargs):
        context = super(ProductsList, self).get_context_data(**kwargs)
        offers = ProductOffer.objects.filter(
            sub_category_id=self.kwargs['spk'], is_trashed=False).filter(type=2).filter(showed_in=2)
        sub = SubCategory.objects.filter(id=self.kwargs['spk'], is_trashed=False)
        if offers.exists():
            context.update({'offers': offers, })
        if sub.exists():
            current_advers = ads_view.advert(request=self.request, pageName=sub[0].name)
            # print('current_advers = ', current_advers)
            if sub[0].name in self.request.session:
                show_num = self.request.session[sub[0].name]['num']
            else:
                show_num = 0
            currentAdvers2 = ads_view.sortAds(list(current_advers), int(show_num))
            context.update({
                'currentAdvers': currentAdvers2,
                'pageName': sub[0].name,
            })
        return context


# products of specific sub_category with selection
class ProductsListRow(ListView):
    template_name = "sub-category-row.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.method == 'GET':
            products = products_filter(request=self.request,
                                       sub_category_id=self.kwargs['spk'])
            # playing(request=self.request, sub_category_id=self.kwargs['spk'])
            if not products == False:
                paginator = Paginator(products, 10)
                page = self.request.GET.get('page')
                products = paginator.get_page(page)
                # print('products = ', products)
                return products
        products = Product.objects.filter(sub_category_id__exact=self.kwargs['spk'], is_trashed=False).order_by('-id')
        paginator = Paginator(products, 10)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        return products

    def get_context_data(self, **kwargs):
        context = super(ProductsListRow, self).get_context_data(**kwargs)
        offers = ProductOffer.objects.filter(
            sub_category_id=self.kwargs['spk'], is_trashed=False).filter(type=2).filter(showed_in=2)
        sub = SubCategory.objects.filter(id=self.kwargs['spk'], is_trashed=False)
        products = Product.objects.filter(
            sub_category_id__exact=self.kwargs['spk'], is_trashed=False)
        if products.exists():
            mini = products.order_by('price').first()
            maxi = products.order_by('price').last()
            context.update({
                'min_price': mini.price,
                'max_price': maxi.price,
            })
        if offers.exists():
            context.update({'offers': offers, })
        spec_names = SpecName.objects.filter(sub_category_id=self.kwargs['spk'], is_trashed=False)
        if spec_names.exists():
            enabled_selection = []
            if 'selection' in self.request.session:
                enabled_selection = self.request.session['selection']
                self.request.session.pop('selection')
                # print("enabled_selection = ", enabled_selection)
            all_specs = {}
            all_specs_ar = {}
            for spec_name in spec_names:
                spec_values = SpecValue.objects.filter(
                    sub_category_id=self.kwargs['spk'], spec_name=spec_name, is_trashed=False).distinct('spec_value')
                # print('spec_values = ', spec_values)
                values = [spec_value for spec_value in spec_values]
                all_specs.update({
                    str(spec_name.spec_name): values,
                })
                all_specs_ar.update({
                    str(spec_name.spec_name_ar): values,
                })
            # print("all_specs = ", all_specs)
            # print("all_specs_ar = ", all_specs_ar)
            context.update({
                'spec_names': all_specs,
                'spec_names_ar': all_specs_ar,
                "enabled_selection": enabled_selection,
            })
        if sub.exists():
            current_advers = ads_view.advert(
                request=self.request, pageName=sub[0].name)
            if sub[0].name in self.request.session:
                show_num = self.request.session[sub[0].name]['num']
            else:
                show_num = 0
            currentAdvers2 = ads_view.sortAds(list(current_advers), int(show_num))
            context.update({
                'currentAdvers': currentAdvers2,
                'pageName': sub[0].name,
            })
        return context


################################

# get a specific product details
class ProductDetails(DetailView):
    template_name = 'product.html'
    context_object_name = 'product'

    def get_queryset(self):
        # print("Product = ", Product.objects.filter(pk=self.kwargs['pk']))
        return Product.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetails, self).get_context_data(**kwargs)
        #################################################################################################
        # get specifications of the product
        spec_values = SpecValue.objects.filter(product_id=self.kwargs['pk'], is_trashed=False)
        if spec_values.exists():
            context.update({"spec_values": spec_values})
        #################################################################################################
        # recent views
        visit_product(self.request, self.kwargs['pk'])
        #################################################################################################
        product_images = ProductImage.objects.filter(product_id=self.kwargs['pk'], is_trashed=False)
        discount = ProductOffer.objects.filter(product_id=self.kwargs['pk'], is_trashed=False)
        spec_values_list = get_changable_specifications(self.request, self.kwargs['pk'])
        # print('spec_values_list = ', spec_values_list[0])
        context.update({
            'imgs': product_images,
            'discount': discount.first(),
            'spec_values_list': spec_values_list,
        })
        #################################################################################################
        # get quantity
        available_quantity = get_quantity(self.kwargs['pk'])
        # print('available_quantity = ', available_quantity)
        context.update({
            "available_quantity": int(available_quantity),
        })
        #################################################################################################
        # E-mail Form if a user has an inquiry about this product
        if self.request.user.is_authenticated:
            email_form = EmailForm(initial={
                'name': self.request.user.username,
                'email': self.request.user.email
            })
        else:
            email_form = EmailForm()
        context.update({'email_form': email_form})
        #################################################################################################
        return context

    # Send the user inquiry question
    def post(self, request, **kwargs):
        if request.user.is_authenticated:
            email_form = EmailForm(request.POST, request.FILES,
                                   initial={'name': request.user.username, 'email': request.user.email})
        else:
            email_form = EmailForm(request.POST, request.FILES)
        if email_form.is_valid():
            post = email_form.save(commit=False)
            post.save()
            product_name = bleach.clean(request.POST.get('productId', None))
            product_id = bleach.clean(request.POST.get('productName', None))
            title = 'Product Inquiry Message'
            html_content = '<span><h3>Product Id: {} </h3></span>' \
                           '<span><h3>Product Name: {} </h3></span>' \
                           '<span><h3>Name: {} </h3> </span>' \
                           '<span><h3>Email: {} </h2> </span>' \
                           '<span><h3>Message:  {} </h3></span>'.format(product_name, product_id, post.name,
                                                                        post.email, post.message)
            try:
                email = EmailMultiAlternatives(title, to=[settings.RECEIVER_EMAIL])
                email.attach_alternative(html_content, "text/html")
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid Email found.')

        # do something with your data
        return HttpResponseRedirect(request.path)


# get the products that match the search
class ProductSearchListView(ListView):
    template_name = "product_search_results.html"
    context_object_name = "products"

    def get_queryset(self):
        if self.request.method == 'GET':
            posted_data = self.request.GET.get('search_input')
            if posted_data:
                search_input = bleach.clean(posted_data.strip())
                if len(search_input) >= 3:
                    items_count = 30
                    lang = detect(search_input)
                    if lang == 'ar' or lang == 'fa':
                        products = Product.objects.filter(name_ar__icontains=search_input, is_trashed=False)
                        if products.exists():
                            paginator = Paginator(products, items_count)
                            page = self.request.GET.get('page')
                            products = paginator.get_page(page)
                            return products
                    else:
                        products = Product.objects.filter(name__icontains=search_input, is_trashed=False)
                        if products.exists():
                            paginator = Paginator(products, items_count)
                            page = self.request.GET.get('page')
                            products = paginator.get_page(page)
                            return products
        return None


# A specific User evaluate a specific Product he bought before
class ProductReview(LoginRequiredMixin, DetailView):
    template_name = 'product_review.html'
    context_object_name = 'product'
    redirect_field_name = 'next'

    def get_queryset(self):
        #################################################################################################
        # recent views
        visit_product(self.request, self.kwargs['pk'])
        #################################################################################################
        return Product.objects.filter(pk=self.kwargs['pk'], is_trashed=False)

    def post(self, request, **kwargs):
        if request.POST:
            total_star = 0
            total_users = 0
            star_num = request.POST['h_star']
            review = request.POST['review']
            if star_num and review:
                star_num = bleach.clean(star_num.strip())
                review = bleach.clean(review.strip())
                # print(star_num, review, request.user.id)
                Review.objects.create(user_id=request.user.id, product_id=self.kwargs['pk'], stars=star_num,
                                      review=review)
                rev_table = Review.objects.filter(product_id=self.kwargs['pk'])
                for rt in rev_table:
                    total_star += float(rt.stars)
                    total_users += float(1)
                avr_star = float(total_star) / float(total_users)
                # print(total_users, total_star, avr_star)
                Product.objects.filter(id=self.kwargs['pk']).update(stars=avr_star)
                return HttpResponseRedirect('/en/?rev=d')
            else:
                messages.warning(request, _("please choose the stars and leave a comment"))
                print("please choose the stars and leave a comment")


#======================================================================================================================

# AJAX
# -------------------------------------------------------------------------------
def check_filter(request):
    done = False
    data = {'done': done, }
    if request.GET:
        spec_name = request.GET.get('spec_name', None)
        spec_value = request.GET.get('spec_value', None)
        sub_category_id = request.GET.get('sub_category_id', None)
        lang_code = request.GET.get('lang_code', None)
        # print(spec_name, ' && ', spec_value, ' && ', sub_category_id, ' && ', lang_code)
        if spec_name and spec_value and sub_category_id and lang_code:
            spec_name_cleaned = bleach.clean(spec_name)
            spec_value_cleaned = bleach.clean(spec_value)
            sub_category_id_cleaned = bleach.clean(sub_category_id)
            lang_code_cleaned = bleach.clean(lang_code)
            # fill the selection session with what customer select
            if not 'selection' in request.session:
                request.session['selection'] = [{
                    "spec_name": spec_name_cleaned,
                    "spec_value": spec_value_cleaned,
                }]
            else:
                selection = request.session['selection']
                selection.append({
                    "spec_name": spec_name_cleaned,
                    "spec_value": spec_value_cleaned,
                })
                request.session['selection'] = selection
                # print(request.session['selection'])
            selection = request.session['selection']
            if lang_code_cleaned == 'ar':
                spec_name = SpecName.objects.get(spec_name_ar__exact=selection[0]['spec_name'],
                                                 sub_category=sub_category_id_cleaned, is_trashed=False)
                spec_values = SpecValue.objects.filter(spec_name=spec_name,
                                                       spec_value_ar__iexact=selection[0]['spec_value'],
                                                       sub_category=sub_category_id_cleaned, is_trashed=False)
                # print('spec_values = ', spec_values)
                if spec_values.exists():
                    product_ids = [spec.product_id for spec in spec_values]
                    # print("ids = ", product_ids)
                    spec_values = SpecValue.objects.filter(product_id__in=product_ids,
                                                           sub_category_id=sub_category_id_cleaned, is_trashed=False
                                                           ).order_by('id')
                    # print("spec_values_new = ", spec_values)
                    if spec_values.exists():
                        for index in range(1, len(selection)):
                            # print("spec_obj = ", selection[index]['spec_value'])
                            spec_name = SpecName.objects.get(spec_name_ar__exact=selection[index]['spec_name'],
                                                             sub_category=sub_category_id_cleaned, is_trashed=False)
                            spec_values = spec_values.filter(spec_name=spec_name,
                                                             spec_value_ar__iexact=selection[index]['spec_value'],
                                                             sub_category=sub_category_id_cleaned, is_trashed=False)
                        if spec_values.exists():
                            # print("spec_values_new 02 = ", spec_values)
                            product_ids = [spec.product_id for spec in spec_values]
                            # print("ids = ", product_ids)
                            spec_values_new = SpecValue.objects.filter(product_id__in=product_ids,
                                                                       sub_category_id=sub_category_id_cleaned,
                                                                       is_trashed=False).order_by('id')
                            spec_values_values = [spec.spec_value_ar for spec in spec_values_new]
                            # print('spec_values_values = ', spec_values_values)
                            done = True
                            data.update({
                                'done': done,
                                'spec_values_values': spec_values_values,
                            })
            else:
                selection = request.session['selection']
                spec_name = SpecName.objects.get(spec_name__exact=selection[0]['spec_name'],
                                                 sub_category=sub_category_id_cleaned, is_trashed=False)
                spec_values = SpecValue.objects.filter(spec_name=spec_name,
                                                       spec_value__iexact=selection[0]['spec_value'],
                                                       sub_category=sub_category_id_cleaned, is_trashed=False)

                # print('spec_values = ', spec_values)
                if spec_values.exists():
                    product_ids = [spec.product_id for spec in spec_values]
                    # print("ids = ", product_ids)
                    spec_values = SpecValue.objects.filter(product_id__in=product_ids,
                                                           sub_category_id=sub_category_id_cleaned,
                                                           is_trashed=False).order_by('id')
                    # print("spec_values_new = ", spec_values)
                    if spec_values.exists():
                        for index in range(1, len(selection)):
                            # print("spec_obj = ", selection[index]['spec_value'])
                            spec_name = SpecName.objects.get(spec_name__exact=selection[index]['spec_name'],
                                                             sub_category=sub_category_id_cleaned, is_trashed=False)
                            spec_values = spec_values.filter(spec_name=spec_name,
                                                             spec_value__iexact=selection[index]['spec_value'],
                                                             sub_category=sub_category_id_cleaned, is_trashed=False)
                        if spec_values.exists():
                            # print("spec_values_new 02 = ", spec_values)
                            product_ids = [spec.product_id for spec in spec_values]
                            # print("ids = ", product_ids)
                            spec_values_new = SpecValue.objects.filter(product_id__in=product_ids,
                                                                       sub_category_id=sub_category_id_cleaned,
                                                                       is_trashed=False).order_by('id')
                            spec_values_values = [spec.spec_value for spec in spec_values_new]
                            # print('spec_values_values = ', spec_values_values)
                            done = True
                            data.update({
                                'done': done,
                                'spec_values_values': spec_values_values,
                            })
    return JsonResponse(data)


def show_recent(request):
    done = False
    data = {
        'done': done,
    }
    if request.GET:
        recent_list = []
        if 'visited' in request.session:
            if 'ids' in request.session['visited']:
                ids_list = request.session['visited']['ids']
                ##############################################
                recent_list = list(Product.objects.filter(
                    pk__in=ids_list, is_trashed=False).values('id', 'name', 'name_ar', 'price', 'main_img'))
                # print('recent_list with values = ', Product.objects.filter(pk__in=ids_list, is_trashed=False).values('id', 'name', 'price', 'main_img'))
                # print(sorted(recent_list, key=lambda i: i['id']))
                # sorting recent_list['id'] using ids_list
                recent_list.sort(key=lambda t: ids_list.index(t['id']))
                # print('ids_list = ', ids_list)
                # print('values_list = ', recent_list.values('id'))
                # print('new recent list = ', recent_list)
                ##############################################
                if recent_list:
                    # convert price
                    if 'site_info' in request.session:
                        if 'country_short' in request.session['site_info']:
                            if not request.session['site_info']['country_short'] == "EG":
                                if 'dollar_rate' in request.session['site_info']:
                                    dollar_rate = request.session['site_info']['dollar_rate']
                                    new_recent_list = []
                                    for product in recent_list:
                                        new_price = float(product['price']) / float(dollar_rate)
                                        new_recent_list.append({
                                            'id': product['id'],
                                            'name': product['name'],
                                            'name_ar': product['name_ar'],
                                            'price': float("{0:.2f}".format(new_price)),
                                            'main_img': product['main_img'],
                                        })
                                    recent_list = new_recent_list
                                    # print("new_recent_list = ", recent_list)
                    done = True  # get spacific columns of list records
                    data.update({
                        'done': done,
                        'products': recent_list,
                    })
                    return JsonResponse(data)
            return JsonResponse(data)
        return JsonResponse(data)
    return JsonResponse(data)


def delete_selection(request):
    if request.GET:
        if 'selection' in request.session:
            request.session.pop('selection')
            print("deleted")
        else:
            print("selection not found")
    else:
        print("Error")
    return JsonResponse({"done": True})


def get_sub_category_id(request):
    done = False
    data = {
        'done': done,
    }
    if request.GET:
        name = bleach.clean(request.GET.get('name', None))
        try:
            sub_category = SubCategory.objects.get(name=name, is_trashed=False)
            done = True
            spec_names = SpecName.objects.filter(sub_category=sub_category, is_trashed=False)
            products = Product.objects.filter(sub_category=sub_category, is_trashed=False)
            spec_names_list = list(spec_names.values('id', 'spec_name'))
            products_list = list(products.values('id', 'name'))
            data.update({
                'done': done,
                'spec_names_list': spec_names_list,
                'products_list': products_list,
            })
        except ObjectDoesNotExist:
            done = False

    return JsonResponse(data)


def product_search(request):
    context = {
        'done': False
    }
    if request.GET:
        input = bleach.clean(request.GET.get("searchInput"))
        if input:
            # print("detect = ", langdetect.detect(input))
            language = detect(input)
            if language == 'ar' or language == 'fa':
                products = Product.objects.filter(name_ar__icontains=input, is_trashed=False)
                if products.exists():
                    _in = ' في '
                    product_list = []
                    for product in products:
                        # print("products = ", product)
                        product_list.append({
                            'product_id': product.id,
                            'product_name': product.name_ar,
                            'product_category': product.category.name_ar,
                            'product_sub_category': product.sub_category.name_ar,
                            'in': _in,
                            'lang': 'ar'
                        })
                        # print("productList = ", product_list)
                        context.update({
                            'done': True,
                            'productList': product_list
                        })
            else:
                products = Product.objects.filter(name__icontains=input, is_trashed=False)
                if products.exists():
                    _in = ' in '
                    product_list = []
                    for product in products:
                        # print("products = ", product)
                        product_list.append({
                            'product_id': product.id,
                            'product_name': product.name,
                            'product_category': product.category.name,
                            'product_sub_category': product.sub_category.name,
                            'in': _in,
                            'lang': 'en',
                        })
                        # print("productList = ", product_list)
                        context.update({
                            'done': True,
                            'productList': product_list
                        })
    return JsonResponse(context)

#=======================================================================================================================

# Outer Functions
# -----------------------------------------------------------------------------
# get the specifications of a specific product
def get_changable_specifications(request, product_id):
    spec_names = SpecValueChangeable.objects.filter(product_id=product_id, is_trashed=False)
    if spec_names.exists():
        spec_values_list = []
        spec_names = spec_names.distinct('spec_name')
        spec_names_ids = [spec.spec_name.id for spec in spec_names]
        for spec_name in spec_names_ids:
            spec_values = SpecValueChangeable.objects.filter(spec_name_id=spec_name, product_id=product_id,
                                                             is_trashed=False)
            if spec_values.exists():
                spec_values_list.append(spec_values)
        return spec_values_list
    return False


# Selection of the products
def products_filter(request, sub_category_id):
    mini = request.GET.get('min', None)
    maxi = request.GET.get('max', None)
    start = 0
    if len(request.GET) > 0:
        # print("teha GET ===== ", request.GET)
        for i in range(0, len(request.GET)):
            if request.GET.get('spec[' + str(i) + ']', None):
                start = i
                break

    if request.GET.get('spec_length', None):
        length = int(request.GET.get('spec_length'))
        spec_length = length - start
        spec_values_list = []
        spec_names_list = []
        # print('GET = ', request.GET)
        try:
            # print("mini = ", mini)
            # print("max = ", maxi)
            if request.LANGUAGE_CODE == 'ar' or request.LANGUAGE_CODE == 'ar-eg':
                for i in range(start, length):
                    spec_name_get = request.GET.get('spec[' + str(i) + ']', None)
                    # print("i = ", i)
                    # print("spec_name_get = ", spec_name_get)
                    spec_name = SpecName.objects.get(spec_name_ar=spec_name_get,
                                                     sub_category_id=sub_category_id, is_trashed=False)
                    # print('spec = ', spec_name)
                    for j in range(0, len(request.GET)):
                        spec_value_get = request.GET.get(
                            '' + str(spec_name_get) + '[' + str(j) + ']', None)
                        if spec_value_get:
                            spec_names_list.append(spec_name.id)
                            # print('values ' + str(j) + ' = ', spec_value)
                            spec_values_list.append(spec_value_get)
                # print("spec_values_list = ", spec_values_list)
                # print("spec_names_list = ", spec_names_list)
                if spec_values_list and spec_names_list:
                    spec_values_objects = SpecValue.objects
                    # The idea is to get the spec_value of a specification then get its products then get its spec_valuesObject
                    # and filter the new specifications upon the previous spec_valuesObject
                    for spec_value in spec_values_list:
                        spec_values_objects = spec_values_objects.filter(spec_value_ar__iexact=spec_value)
                        product_ids = [spec.product_id for spec in spec_values_objects]
                        spec_values_objects = SpecValue.objects.filter(product_id__in=product_ids,
                                                                       is_trashed=False).order_by('id')
                    # print("spec_values_objects = ", spec_values_objects)
                    if spec_values_objects.exists():
                        # print("spec_values_new 02 = ", spec_values)
                        product_ids = [spec.product_id for spec in spec_values_objects]
                        # print("ids = ", product_ids)
                        products = Product.objects.filter(id__in=product_ids, is_trashed=False).order_by('id')
                        # print('product = ', products)
                        if mini and maxi:
                            products = products.filter(price__range=(mini, maxi))
                        # print('product price = ', products)
                        return products
            else:
                for i in range(start, length):
                    spec_name_get = request.GET.get('spec[' + str(i) + ']', None)
                    # print("i = ", i)
                    # print("spec_name_get = ", spec_name_get)
                    spec_name = SpecName.objects.get(
                        spec_name=spec_name_get, sub_category_id=sub_category_id, is_trashed=False)
                    # print('spec = ', spec_name)
                    for j in range(0, len(request.GET)):
                        spec_value_get = request.GET.get(
                            '' + str(spec_name_get) + '[' + str(j) + ']', None)
                        if spec_value_get:
                            spec_names_list.append(spec_name.id)
                            # print('values ' + str(j) + ' = ', spec_value)
                            spec_values_list.append(spec_value_get)
                # print("spec_values_list = ", spec_values_list)
                # print("spec_names_list = ", spec_names_list)
                if spec_values_list and spec_names_list:
                    spec_values_objects = SpecValue.objects
                    # The idea is to get the spec_value of a specification then get its products then get its spec_valuesObject
                    # and filter the new specifications upon the previous spec_valuesObject
                    for spec_value in spec_values_list:
                        spec_values_objects = spec_values_objects.filter(spec_value__iexact=spec_value)
                        product_ids = [spec.product_id for spec in spec_values_objects]
                        spec_values_objects = SpecValue.objects.filter(product_id__in=product_ids,
                                                                       is_trashed=False).order_by('id')
                    # print("spec_values_objects = ", spec_values_objects)
                    if spec_values_objects.exists():
                        # print("spec_values_new 02 = ", spec_values)
                        product_ids = [spec.product_id for spec in spec_values_objects]
                        # print("ids = ", product_ids)
                        products = Product.objects.filter(id__in=product_ids, is_trashed=False).order_by('id')
                        # print('product = ', products)
                        if mini and maxi:
                            products = products.filter(price__range=(mini, maxi))
                        # print('product price = ', products)
                        return products
        except ObjectDoesNotExist as e:
            print("Error filter = ", e)
            return False

        if mini and maxi:
            products = Product.objects.filter(price__range=(mini, maxi), sub_category_id=sub_category_id,
                                              is_trashed=False)
            # print('mini & max = ', products)
            return products
        elif mini and not maxi:
            products = Product.objects.filter(price__gt=str(int(mini) - 1), sub_category_id=sub_category_id,
                                              is_trashed=False)
            # print('mini = ', products)
            return products
        elif maxi and not mini:
            products = Product.objects.filter(price__lt=str(int(maxi) + 1), sub_category_id=sub_category_id,
                                              is_trashed=False)
            # print('max = ', products)
            return products
    return False


# get the current advertisment
def get_current_advertisment(request, page_name):
    current_advers = ads_view.advert(request=request, pageName=page_name)
    if page_name in request.session:
        show_num = request.session['home']['num']
    else:
        show_num = 0
    # print('current_advers = ', current_advers[0].show_num)
    current_advers2 = ads_view.sortAds(list(current_advers), int(show_num))
    # print('current_advers2 = ', current_advers2[0].show_num)
    return current_advers2


# get all categories names
def get_all_categories_names():
    all_categories = Category.objects.filter(is_trashed=False)
    category_names = []
    for category in all_categories:
        if ProductOffer.objects.filter(category=category, is_trashed=False).exists():
            category_names.append(category)
            # print(catNames)
    return category_names


# Pagination of products
def get_product_with_paginator(request, sub_category_id, items_count, order_by_type):
    products = Product.objects.filter(sub_category_id__exact=sub_category_id, is_trashed=False).order_by(
        str(order_by_type))
    paginator = Paginator(products, items_count)
    page = request.GET.get('page', None)
    products = paginator.get_page(page)
    return products


# Add specific product to visited session
def visit_product(request, product_id):
    # hold list of ids [pk, pk, ]
    if 'visited' in request.session:
        if 'ids' in request.session['visited']:
            ids_list = request.session['visited']['ids']
            # print('visited = ', str(ids_list))
            for item in ids_list:
                # print(item)
                if item == product_id:
                    # print(ids_list)
                    ids_list.remove(item)
                    # print(ids_list)
            if len(ids_list) >= 30:
                ids_list.pop(0)
            ids_list.append(product_id)
            context1 = request.session['visited']
            # print('context1 = ', context1)
            context1.update({
                'ids': ids_list,
            })
            # print('context1 = ', context1)
            request.session['visited'] = context1
            # print(self.request.session['visited'])
    else:
        request.session['visited'] = {  # create cookie named visited
            'ids': [product_id],  # create list named ids = [pk, ]
        }


# get available quantity of a specific product
def get_quantity(pk):
    product_ = Product.objects.filter(pk=pk).first()
    orders = Order.objects.filter(product=product_)
    # print("orders = ", orders)
    total_quantity = orders.aggregate(tot=Sum('quantity'))['tot']
    if total_quantity:
        if int(product_.max_quantity * product_.delay_count) == total_quantity:
            return 0
        # print("total_quantity = ", total_quantity)
        quantity_range = float(total_quantity / product_.max_quantity)
        # print("quantity_range = ", quantity_range)
        delay_count = 1
        for count in range(1, product_.delay_count + 1):
            if 0 < quantity_range < count:
                delay_count = count
                break
        # print("delay_count = ", delay_count)
        available_quantity = (delay_count * product_.max_quantity) - total_quantity
        # print("available_quantity = ", int(available_quantity))
        return int(available_quantity)
    else:
        return -1

#===================================================================================================================
