from datetime import datetime, timezone

import bleach
import pandas as pd
from django.contrib.auth import authenticate, logout, get_user_model, login as user_login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import AdvertisementAddForm
from .models import Advertisement, AdsManager
from ..products.models import Category, SubCategory


# Create your views here.


def advert(request, pageName):
    openDateTime = datetime.now(timezone.utc)
    currentAdvers = Advertisement.objects.filter(page__iexact=pageName, startDate__lte=openDateTime,
                                                 endDate__gte=openDateTime, is_trashed=False).order_by('show_num')
    return currentAdvers


def adNumToCookie(request):
    if request.GET:
        # print(request.GET.get('show_num'))
        cookieData = bleach.clean(request.GET.get('show_num'))
        arg_list = [arg.strip() for arg in cookieData.split(',')]
        # print('arg_list = ', arg_list)
        if not arg_list[0] in request.session:
            request.session[arg_list[0]] = {
                'num': arg_list[1],
            }
        else:
            _context = request.session[arg_list[0]]
            _context.update({
                'num': arg_list[1],
            })
            request.session[arg_list[0]] = _context
    return JsonResponse({'done': True})


def sortAds(adsList, show_num):
    return adsList[show_num:] + adsList[:show_num]


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
                                return HttpResponseRedirect('/ar/ads/adsManagement/')
                            else:
                                return HttpResponseRedirect(
                                    '/ar/ads/adsManagerlogin/?error=nau')  # error of type not authenticated
                            ########################################################
                        else:
                            return HttpResponseRedirect(
                                '/ar/ads/adsManagerlogin/?error=nam')  # error of type not ads Manager
                    else:
                        return HttpResponseRedirect('/ar/ads/adsManagerlogin/?error=ns')  # error of type not staff
                else:
                    return HttpResponseRedirect('/ar/ads/adsManagerlogin/?error=na')  # error of type not active
            else:
                return HttpResponseRedirect('/ar/ads/adsManagerlogin/?error=nf')  # error of type not Found
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
                                return HttpResponseRedirect('/en/ads/adsManagement/')
                            else:
                                return HttpResponseRedirect(
                                    '/en/ads/adsManagerlogin/?error=nau')  # error of type not authenticated
                            ########################################################
                        else:
                            return HttpResponseRedirect(
                                '/en/ads/adsManagerlogin/?error=nam')  # error of type not ads Manager
                    else:
                        return HttpResponseRedirect('/en/ads/adsManagerlogin/?error=ns')  # error of type not staff
                else:
                    return HttpResponseRedirect('/en/ads/adsManagerlogin/?error=na')  # error of type not active
            else:
                return HttpResponseRedirect('/en/ads/adsManagerlogin/?error=nf')  # error of type not Found
    return render(request, "account/adsManagerlogin.html", context)


@login_required
def ads_manager_logout(request):
    logout(request)
    if request.LANGUAGE_CODE == "ar" or request.LANGUAGE_CODE == 'ar-eg':
        return HttpResponseRedirect('/ar/ads/adsManagerlogin')
    else:
        return HttpResponseRedirect('/en/ads/adsManagerlogin')


@login_required(login_url='/ads/adsManagerlogin/')
def AdsManagement(request):
    if request.user.is_authenticated:
        # print('in auth if')
        if request.method == 'POST':
            form = AdvertisementAddForm(request.POST, request.FILES)
            if form.is_valid():
                ads_man = form.save(commit=False)
                # ads_man.advertiseManager_id = 1
                # ads_man.save()
                sd2 = form.cleaned_data['startDate']
                ed2 = form.cleaned_data['endDate']
                filter_page2 = form.cleaned_data['page']
                new_add_duration = form.cleaned_data['duration']
                # print(sd2, ed2, filter_page2, new_add_duration)
                avail_list2 = []
                day_duration2 = 0
                date_range2 = pd.date_range(sd2, ed2)
                for single_date2 in date_range2:
                    dt2 = single_date2.strftime("%Y-%m-%d")
                    if Advertisement.objects.filter(startDate__lte=dt2, is_trashed=False).filter(endDate__gte=dt2).filter(
                            page__iexact=filter_page2).exists():
                        day_ads_list2 = Advertisement.objects.filter(startDate__lte=dt2, is_trashed=False).filter(
                            endDate__gte=dt2).filter(page__iexact=filter_page2)
                        for dal2 in day_ads_list2:
                            day_duration2 += int(dal2.duration)
                        # print(day_duration)
                        avail_list2.append([day_duration2, dt2], )
                        day_duration2 = 0
                for d2 in avail_list2:
                    if (int(d2[0]+new_add_duration)) > 600:
                        # print(int(d2[0]+new_add_duration))
                        return HttpResponseRedirect('/en/ads/adsManagement/?error=f')
                ads_man.advertiseManager_id = request.session['ads_manager_user_id']
                ads_man.save()
                return HttpResponseRedirect('/en/ads/adsManagement/?success=t')
            else:
                print('form not valid = ', form.errors)
        # print('req = ', request.GET)
        if request.GET:
            if not request.GET.get('error', None) == 'f':
                if request.GET.get('start_date', None):
                    if request.GET.get('end_date', None):
                        if request.GET.get('duration', None):
                            if request.GET.get('page', None):
                                done = True
                                sd = bleach.clean(request.GET.get('start_date', None))
                                ed = bleach.clean(request.GET.get('end_date', None))
                                du = bleach.clean(request.GET.get('duration', None))
                                # print('duration = ', du)
                                filter_page = ''
                                page_sel = bleach.clean(request.GET.get('page', None))
                                if request.GET.get('category', None) and request.GET.get('sub_category', None):
                                    cat_sel = bleach.clean(request.GET.get('category', None))
                                    sub_cat_sel = bleach.clean(request.GET.get('sub_category', None))
                                elif request.GET.get('category', None) and not request.GET.get('sub_category', None):
                                    cat_sel = bleach.clean(request.GET.get('category', None))
                                    sub_cat_sel = None
                                else:
                                    cat_sel = None
                                    sub_cat_sel = None
                                if page_sel == 'home':
                                    filter_page = 'home'
                                elif page_sel == 'c' and cat_sel is not None:
                                    filter_page = Category.objects.get(id=cat_sel).name
                                elif page_sel == 'sc' and cat_sel is not None and sub_cat_sel is not None:
                                    filter_page = SubCategory.objects.get(id=sub_cat_sel).name
                                else:
                                    print('error in page name')
                                # print(filter_page)
                                avail_list = []
                                lables = []
                                defaultData = []
                                day_duration = 0
                                date_range = pd.date_range(sd, ed)
                                for single_date in date_range:
                                    dt = single_date.strftime("%Y-%m-%d")
                                    if Advertisement.objects.filter(startDate__lte=dt, is_trashed=False).filter(endDate__gte=dt).filter(
                                            page__iexact=filter_page).exists():
                                        day_ads_list = Advertisement.objects.filter(startDate__lte=dt, is_trashed=False).filter(
                                            endDate__gte=dt).filter(page__iexact=filter_page)
                                        for dal in day_ads_list:
                                            day_duration += int(dal.duration)
                                        # print(day_duration)
                                        avail_list.append([day_duration, dt], )
                                        day_duration = 0
                                    else:
                                        avail_list.append([0, dt], )
                                    # print(single_date.strftime("%Y-%m-%d"))
                                # print(avail_list)
                                for al in avail_list:
                                    defaultData.append(al[0]+int(du))
                                    lables.append(al[1])
                                for al2 in defaultData:
                                    if int(al2) > 600:
                                        done = False
                                # print('lables = ', lables)
                                # print('defaultData = ', defaultData)
                                data = {
                                    'done': done,
                                    'defaultData': defaultData,
                                    'lables': lables,
                                }
                                return JsonResponse(data)
                                # return render(request, "adsManagement.html", context)
                            else:
                                print('page = none')
                        else:
                            print('duration = none')
                    else:
                        print('end date = none')
                else:
                    print('start date = none')
            else:
                print('Error[f] no place for this ad')
        else:
            print('No GET request')
    else:
        print('not user')
    return render(request, "advertisement/adsManagement.html", {'form': AdvertisementAddForm})


def GetAllCategories(request):
    if request.GET:
        cat_list = list(Category.objects.all().values('id', 'name'))
        data = {
            'done': True,
            'catList': cat_list,
        }
        return JsonResponse(data)


def GetAllSubCategories(request):
    if request.GET:
        cat_id = bleach.clean(request.GET.get('cat_id'))
        sub_cat_list = list(SubCategory.objects.filter(category_id=cat_id).values('id', 'name'))
        data = {
            'done': True,
            'subCatList': sub_cat_list,
        }
        return JsonResponse(data)

# class AddAdvertisements(CreateView):
#     model = Advertisement
#     form_class = AdvertisementAddForm
#     success_url = reverse_lazy('AdsManagement')
#     fields = ['advertiserName',
#               'advertiserEmail',
#               'advertiserPhone',
#               'image',
#               'page',
#               'startDate',
#               'endDate',
#               'duration',
#               'interval',
#               'advertiseManager',]
#     def form_valid(self, form):
#         ads_manager_id = AdsManager.objects.get(user_id=self.request.user)
#         form.instance.advertiseManager = ads_manager_id
#         return super().form_valid(form)
