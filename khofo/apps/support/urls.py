from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [
    path('contactus/', views.contact_us, name="contact_us"),
    path('ajax/get_site_info/', views.get_site_info),
    path('ajax/get_site_info2/', views.get_site_info2),
    path('ajax/get_footer_info/', views.get_footer_info, name='get_categories'),
]
