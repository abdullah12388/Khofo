from django.urls import path

from . import views

app_name = 'ads'
urlpatterns = [
    path('ads_manager_logout/', views.ads_manager_logout, name="ads_manager_logout"),
    path('adsManagement/', views.AdsManagement, name="AdsManagement"),
    path('adNumToCookie/', views.adNumToCookie, name="adNumToCookie"),
    path('adsManagerlogin/', views.adsManagerLogin, name="adsManagerlogin"),
    path('GetAllCategories/', views.GetAllCategories, name='get_all_categories'),
    path('GetAllSubCategories/', views.GetAllSubCategories, name='get_all_sub_categories'),
]
