from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'shipping'
urlpatterns = [
    path('choose-shipping/', views.choose_shipping, name="choose_shipping"),
    path('request-order/', views.request_order, name="request_order"),
    path('sendapi/', views.send_api, name="send_api"),
    path('ajax/shipping-details/', views.shipping_details, name="shipping_details"),
]
