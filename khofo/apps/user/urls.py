from django.urls import path
from . import views


app_name = 'user'
urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('profile/', views.profile, name="profile"),
    path('profile/account/',  views.UserUpdateView.as_view(), name="update_user"),
    path('profile/address/',  views.AddressUpdateView.as_view(), name="update_address"),
    path('address/add/',  views.CreateAddressView.as_view(), name="add_address"),
    path('address/update/',  views.UpdateAddressView.as_view(), name="add_address"),
    path('profile/account/changePassword/',  views.change_password, name="change_password"),
    path('forget-password/',  views.forget_password, name="forget_password"),
    path('orders/',  views.UserOrdersListView.as_view(), name="user_orders"),
]
