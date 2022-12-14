from django.urls import path, include
from . import views

app_name = 'orders'
urlpatterns = [
    path('', views.checkOut, name="checkOut"),
    path('check_user_buyer/', views.check_user_buyer, name="check_user_buyer"),
    # path('cart/', views.finalCart, name="finalCart"),
    # AJAX
    # ----------------------------------------------------------------------------------------------
    path('ajax/addCookie/', views.addCookie, name="addCookie"),
    path('ajax/updateCookie/', views.updateCookie, name="updateCookie"),
    path('ajax/deleteProduct/', views.deleteCookieProduct, name="deleteProduct"),
    # path('paypal/', include('paypal.standard.ipn.urls')),
    # path('success/', views.success, name='success'),
    # path('fail/', views.fail, name='fail'),
]
