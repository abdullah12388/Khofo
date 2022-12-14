"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
# Views
from apps.products import views as product_view
from apps.advertisement import views as ads_view
from apps.user import views as clint_views
from apps.support import views as support_view

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    #################################################################################

]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', product_view.CategoriesListView.as_view(), name="home"),
    # path('paypal/', include('paypal.standard.ipn.urls')),
    path('home/', product_view.CategoriesListView.as_view(), name="home"),
    path('user/', include('apps.user.urls')),
    path('productHome/', include('apps.products.urls')),
    path('order/', include('apps.orders.urls')),
    path('shipping/', include('apps.shippings.urls')),
    path('ads/', include('apps.advertisement.urls')),
    path('logout/', clint_views.client_logout, name="logout"),
    path('chaining/', include('smart_selects.urls')),
    # path('adsManagement/', ads_view.AdsManagement, name="AdsManagement"),
    path('support/', include('apps.support.urls')),
     path('export/', include('apps.export.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

handler400 = 'apps.user.views.handler400'
handler403 = 'apps.user.views.handler403'
handler404 = 'apps.user.views.handler404'
handler500 = 'apps.user.views.handler500'

# Change Admin Site
# admin.site.site_header = "Khufu Admin"
# admin.site.site_title = "Khufu Admin Portal"
# admin.site.index_title = "Welcome to Khufu Portal"
