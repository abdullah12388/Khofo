from django.urls import path, include
from . import views

app_name = 'export'

urlpatterns = [
    path('user/<int:pk>/', views.UserExportDetailView.as_view(), name='UserExportDetailView'),
    path('delegate/<int:pk>/', views.DelegateExportDetailView.as_view(), name='DelegateExportDetailView'),
    path('send-message/', views.send_message, name='send_message'),
]
