# python
import bleach
import random
import string
# Django
from django.contrib.auth import authenticate, logout, get_user_model, login as user_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, CreateView
from django.contrib import messages
from django.core.mail import EmailMessage, BadHeaderError
from django.utils.translation import gettext_lazy as _
# Models
from ..products.models import Product, ShowRecent
from ..orders.models import Cart, Order
from ..user.models import BuyerUserDetails
# Forms
from .forms import UpdateUserForm, AddressUserForm

User = get_user_model()


# Client SignUp
def signup(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Check if field not empty
        if email and username and password:
            email = bleach.clean(email.strip())
            username = bleach.clean(username.strip())
            password_strip = bleach.clean(password.strip())
            password = bleach.clean(password)
            # Check if the password_field has a extra white spaces (trim)
            if len(password) == len(password_strip):
                if 8 <= len(password_strip) < 30:
                    if 6 < len(email) < 60:
                        if 4 < len(username) < 30:
                            user_mail_found = User.objects.filter(email=email).exists()
                            user_name_found = User.objects.filter(username=username).exists()
                            if user_mail_found:
                                messages.warning(request, _("This email is already exists."))
                            if user_name_found:  # error of type existing username
                                messages.warning(request, _("This email is already exists."))
                            else:
                                user_save = User()
                                user_save.email = email
                                user_save.username = username
                                user_save.password = make_password(password_strip)
                                user_save.save()
                                user_login(request, user_save)
                                if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
                                    return HttpResponseRedirect('/ar/')
                                else:
                                    return HttpResponseRedirect('/en/')
                        else:
                            messages.warning(request, _("Username must be between 4 and 30 characters."))
                            print("Username must be between 4 and 30 characters.")
                    else:
                        messages.warning(request, _("Email must be between 8 and 60 characters."))
                        print("Email must be between 8 and 60 characters.")
                else:
                    messages.warning(request, _("password must be between 8 and 30 characters."))
                    print("password must be between 8 and 30 characters.")
            else:
                messages.warning(request, _("Password must not contain extra white spaces."))
                print("Password must not contain extra white spaces.")
        else:
            messages.warning(request, _("email or username or password is empty."))
            print("email or username or password is empty.")
    else:
        print("This is not a POST request.")
    return render(request, "account/login.html", context=context)


# Client Login
def login(request):
    context = {}
    if request.method == 'POST':
        valuenext = request.POST.get('next', '')
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            username = bleach.clean(username.strip())
            password = bleach.clean(password.strip())
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active and not user.is_staff:
                    user_login(request, user)
                    #######################################################
                    fill_session_cart(request)
                    ########################################################
                    if valuenext is not '':
                        return redirect(valuenext)
                    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
                        return HttpResponseRedirect('/ar/')
                    else:
                        return HttpResponseRedirect('/en/')
                else:
                    messages.warning(request, _('this account is not active'))
            else:
                messages.warning(request, _("Username or Password not valid"))
        else:
            messages.warning(request, _('username and password can not be empty'))
    return render(request, "account/login.html", context)


@login_required
def client_logout(request):
    # add_cart_for_registered(request)
    add_show_recent_for_registered(request)
    logout(request)
    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
        return HttpResponseRedirect('/ar/')
    else:
        return HttpResponseRedirect('/en/')


@login_required
def profile(request):
    context = {}
    try:
        buyer = BuyerUserDetails.objects.get(user=request.user, is_trashed=False)
        # print(buyer)
        context = {
            'buyer_address': buyer,
        }
    except ObjectDoesNotExist as error:
        print("error in profile = ", error)
    return render(request, "account/customer_profile.html", context=context)


# Client change password
def change_password(request):
    if request.method == 'POST':
        _new_pass = request.POST.get('new_pass')
        _confirm_pass = request.POST.get('confirm_pass')
        if _new_pass and _confirm_pass:
            _new_pass_strip = bleach.clean(_new_pass.strip())
            _confirm_pass_strip = bleach.clean(_confirm_pass.strip())
            _new_pass = bleach.clean(_new_pass)
            _confirm_pass = bleach.clean(_confirm_pass)
            if len(_new_pass_strip) == len(_new_pass) and len(_confirm_pass_strip) == len(_confirm_pass):
                _user_id = request.user.id
                user = get_object_or_404(User, pk=_user_id)
                if _new_pass_strip == _confirm_pass_strip:
                    user.password = make_password(_new_pass_strip)
                    user.save()
                    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
                        return HttpResponseRedirect('/ar/user/login/')
                    else:
                        return HttpResponseRedirect('/en/user/login/')
                else:
                    messages.warning(request, _("The confirm password is not match the new Password."))
                    print("The confirm password is not match the new Password.")
            else:
                messages.warning(request, _("Password must not contain extra white spaces."))
                print("Password must not contain extra white spaces.")
        else:
            print("Error : old_password or new_password is empty")
            messages.warning(request, _("old password or new password is empty"))
    return render(request, 'account/change_password.html', {})


def forget_password(request):
    data = {"done": False}
    if request.method == 'GET':
        _user_email = request.GET.get('email')
        if _user_email:
            if _user_email == _user_email.strip():
                _user_email = bleach.clean(_user_email.strip())
                # print("_user_email = ", _user_email)
                _user_with_email = User.objects.filter(email=_user_email)
                if _user_with_email.exists():
                    _user_with_email = _user_with_email.first()
                    _random_pass = random_password()
                    _host = request.get_host()
                    _title = 'KHOFU Online Store Reset Password'
                    _link = 'http://' + _host + '/user/login/'
                    _message = 'use your new password "' + _random_pass + '" to login.\nyou can change your password after loging in.\nto login follow the link below:\n' + _link
                    try:
                        _email = EmailMessage(_title, _message, to=[_user_email])
                        _email.send()
                        _user_with_email.password = make_password(_random_pass)
                        _user_with_email.save()
                        data.update({
                            'done': True,
                            'alert': True
                        })
                    except BadHeaderError as error:
                        print("Error : ", error)
                else:
                    messages.warning(request, _("This email not belong to any account"))
            else:
                messages.warning(request, _("Password must not contain extra white spaces."))
        else:
            messages.warning(request, _('Email can not be empty'))
    return JsonResponse(data)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/update_account.html'
    model = User
    form_class = UpdateUserForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, **kwargs):
        return get_object_or_404(User, pk=self.request.user.id)


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'account/update_address.html'
    model = BuyerUserDetails
    form_class = AddressUserForm
    success_url = reverse_lazy('user:profile')

    def get_object(self, **kwargs):
        return get_object_or_404(BuyerUserDetails, user=self.request.user)


class CreateAddressView(LoginRequiredMixin, CreateView):
    template_name = 'account/add_address_book.html'
    form_class = AddressUserForm
    success_url = reverse_lazy('shipping:choose_shipping')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    template_name = 'account/add_address_book.html'
    model = BuyerUserDetails
    form_class = AddressUserForm
    success_url = reverse_lazy('shipping:choose_shipping')

    def get_object(self, **kwargs):
        return get_object_or_404(BuyerUserDetails, user=self.request.user)


class UserOrdersListView(LoginRequiredMixin, ListView):
    template_name = 'account/user_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        try:
            buyer = BuyerUserDetails.objects.get(user=self.request.user, is_trashed=False)
            return Order.objects.filter(user=buyer, is_trashed=False).values()
        except ObjectDoesNotExist as error:
            print("Error :  ", error)
        return None


###########################################################################

# fill the cart_session with products when the user login
def fill_session_cart(request):
    ################## Registered User #####################
    if request.user.is_authenticated:
        # print('in user auth if')
        if 'khufu_cart' in request.session:
            if 'product' in request.session['khufu_cart']:
                # print('khufu is exists')
                products = request.session['khufu_cart']['product']
                if len(request.session['khufu_cart']['product']) > 0:
                    # print('there is/are product/s in the cookie')
                    for product in products:
                        # print('product_ID = ', product[0])
                        # print('product_Quan = ', product[1])
                        product_instance = Product.objects.filter(id=product[0], is_trashed=False)
                        if product_instance.exists():
                            product_instance = product_instance.first()
                            # if Cart.objects.filter(user=request.user, product=product_instance, is_trashed=False).exists():
                            #     old_instance = Cart.objects.get(user=request.user, product=product_instance, is_trashed=False)
                            #     old_instance.quantity += int(product[1])
                            #     old_instance.specs = product[2]
                            #     old_instance.save()
                            # else:
                            cart = Cart.objects.create(user=request.user, product=product_instance,
                                                       quantity=product[1], specs=product[2], max_quantity=product[3],
                                                       is_trashed=False)
                            cart.save()
                    user_cart = Cart.objects.filter(user=request.user, is_trashed=False)
                    product_list = []
                    for i in range(len(user_cart)):
                        product_list.append(
                            [user_cart[i].product.id, user_cart[i].quantity, user_cart[i].specs,
                             user_cart[i].max_quantity])
                    # print(product_list)
                    context = {
                        'product': product_list,
                        'items': len(product_list),
                    }
                    # print(context)
                    request.session['khufu_cart'] = context
                else:
                    print('there is no product in the cookie')
        else:
            user_cart = Cart.objects.filter(user=request.user, is_trashed=False)
            if user_cart.exists():
                product_list = []
                for i in user_cart:
                    product_list.append([i.product.id, i.quantity, i.specs, i.max_quantity])
                print(product_list)
                context = {
                    'product': product_list,
                    'items': len(product_list),
                }
                request.session['khufu_cart'] = context
        get_show_recent_from_database(request)
    else:
        return HttpResponseRedirect('/ar/user/login/?error=nau')  # error of type not authenticated


# Generate random password to be send to user to his e-mail if he forgot his password
def random_password(stringLength=10):
    password_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(password_characters) for i in range(stringLength))


# add recent_view products of specific user from session to his account in the database
def add_show_recent_for_registered(request):
    if 'visited' in request.session:
        # print(request.session['visited'])
        if 'ids' in request.session['visited']:
            product_ids = request.session['visited']['ids']
            # print('product_ids = ', product_ids)
            ShowRecent.objects.filter(user=request.user).delete()
            products = Product.objects.filter(id__in=product_ids, is_trashed=False)
            for product in products:
                ShowRecent.objects.create(
                    user=request.user,
                    product=product,
                )
                # print('product = ', Product.objects.get(id=product_ids[product]))
    else:
        print("There's no any visited in session")


# retrieve recent_view products of specific user from database
def get_show_recent_from_database(request):
    if ShowRecent.objects.filter(user=request.user, is_trashed=False).exists():
        if 'visited' in request.session:
            if 'ids' in request.session['visited']:
                cookie_ids = request.session['visited']['ids']
                # catch all the product_ids that stored in the session and compare with the product_ids that exist
                # in the database
                for id in cookie_ids:
                    show_recent = ShowRecent.objects.filter(user=request.user, product_id=id)
                    # if the product_ids in the session and the database were the same, it will delete that exists in
                    # the database in create a new one to considerate the arrangement of products that were first seen
                    if show_recent.exists():
                        show_recent.delete()
                        ShowRecent.objects.create(user=request.user, product_id=id)
                    else:
                        ShowRecent.objects.create(user=request.user, product_id=id)
        # then it will retrieve all the recent_view products and append it to the session
        showRecentObjs = ShowRecent.objects.filter(user=request.user).order_by('created_on')
        ids_list = [showRecentObj.product_id for showRecentObj in showRecentObjs]
        # print('ids_list = ', ids_list)
        # then he
        if 'visited' in request.session:
            context = request.session['visited']
            # print('contextBefore = ', context)
            context.update({
                'ids': ids_list,
            })
            # print('contextAfter = ', context)
            request.session['visited'] = context
            # print('request.session = ', request.session['visited'])
        else:
            request.session['visited'] = {
                'ids': ids_list,
            }


# def add_cart_for_registered(request):
#     if 'khufu_cart' in request.session:
#         if 'product' in request.session['khufu_cart']:
#             print(request.session['khufu_cart'])
#             _products = request.session['khufu_cart']['product']
#             print('products = ', _products)
#             Cart.objects.filter(user=request.user).delete()
#             for product in _products:
#                 product_obj = Product.objects.filter(id=product[0], is_trashed=False)
#                 Cart.objects.create(
#                     user=request.user,
#                     product=product_obj,
#                     quantity=product[1],
#                     specs=product[2],
#                     max_quantity=product[3]
#                 )
                # print('product = ', Product.objects.get(id=product_ids[x]))

###########################################################################

# Customizing error views
# --------------------------------------------------------------


# HTTP Error  Handler
def handler400(request, exception):
    return render(request, 'error_views/400.html', status=400)


def handler403(request, exception):
    return render(request, 'error_views/403.html', status=403)


def handler404(request, exception):
    return render(request, 'error_views/404.html', status=404)


def handler500(request):
    return render(request, 'error_views/500.html', status=500)


################################################################################################################

# Hashed functions

"""
def signup(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user_save = user_form.save()
            user_save.set_password(user_save.password)
            user_save.save()
            user_login(request, user_save)
            # set all CLIENT data into session
            request.session['user_id'] = user_save.pk
            request.session['username'] = user_save.username
            request.session['email'] = user_save.email
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/user/signup/?error=ue')# error of type user exists
    else:
        user_form = UserForm()
        context = {
            'user_form': user_form,
        }
    return render(request, "account/signup.html", context=context)
"""

"""
def adsManagerLogin(request):
    context = {}
    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
        if request.method == 'POST':
            username = bleach.clean(request.POST.get('username'))
            password = bleach.clean(request.POST.get('password'))
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    if user.is_staff:
                        if user.is_ads_manager:
                            user_login(request, user)
                            ########################################################
                            ################## Registered User #####################
                            if request.user.is_authenticated:
                                request.session['ads_manager_user_id'] = AdsManager.objects.get(user_id=user.pk).id
                                return HttpResponseRedirect('/ar/adsManagement/')
                            else:
                                return HttpResponseRedirect(
                                    '/ar/user/adsManagerlogin/?error=nau')  # error of type not authenticated
                            ########################################################
                        else:
                            return HttpResponseRedirect(
                                '/ar/user/adsManagerlogin/?error=nam')  # error of type not ads Manager
                    else:
                        return HttpResponseRedirect('/ar/user/adsManagerlogin/?error=ns')  # error of type not staff
                else:
                    return HttpResponseRedirect('/ar/user/adsManagerlogin/?error=na')  # error of type not active
            else:
                return HttpResponseRedirect('/ar/user/adsManagerlogin/?error=nf')  # error of type not Found
    else:
        if request.method == 'POST':
            username = bleach.clean(request.POST.get('username'))
            password = bleach.clean(request.POST.get('password'))
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    if user.is_staff:
                        if user.is_ads_manager:
                            user_login(request, user)
                            ########################################################
                            ################## Registered User #####################
                            if request.user.is_authenticated:
                                request.session['ads_manager_user_id'] = AdsManager.objects.get(user_id=user.pk).id
                                return HttpResponseRedirect('/en/adsManagement/')
                            else:
                                return HttpResponseRedirect(
                                    '/en/user/adsManagerlogin/?error=nau')  # error of type not authenticated
                            ########################################################
                        else:
                            return HttpResponseRedirect(
                                '/en/user/adsManagerlogin/?error=nam')  # error of type not ads Manager
                    else:
                        return HttpResponseRedirect('/en/user/adsManagerlogin/?error=ns')  # error of type not staff
                else:
                    return HttpResponseRedirect('/en/user/adsManagerlogin/?error=na')  # error of type not active
            else:
                return HttpResponseRedirect('/en/user/adsManagerlogin/?error=nf')  # error of type not Found
    return render(request, "account/adsManagerlogin.html", context)
"""

#################################################################################################################
