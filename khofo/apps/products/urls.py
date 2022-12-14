from django.conf.urls import url
from django.urls import path

from . import views

app_name = 'products'
urlpatterns = [
    path('category/<int:pk>/', views.CategoryListView.as_view(), name="category"),
    path('category/<int:pk>/subcategory/<int:spk>/products/', views.ProductsList.as_view(), name="sub_category"),
    path('category/<int:pk>/subcategoryrow/<int:spk>/products/', views.ProductsListRow.as_view(),
         name="sub_category_row"),
    path('product/<int:pk>/', views.ProductDetails.as_view(), name="product_details"),
    path('reviews/<int:pk>/', views.ProductReview.as_view(), name="product_review"),
    path('productSearch/', views.ProductSearchListView.as_view(), name="product_search_results"),
    # AJAX
    # ----------------------------------------------------------------------------------------------
    path('ajax/recentviewed/', views.show_recent, name='show_recent'),
    path('ajax/getsubcategoryid/', views.get_sub_category_id),
    path('ajax/check_filter/', views.check_filter),
    path('ajax/delete_selection/', views.delete_selection, name='delete_selection'),
    path('ajax/search/', views.product_search),

]
