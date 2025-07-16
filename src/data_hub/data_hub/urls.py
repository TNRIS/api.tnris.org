"""data_hub URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import (
    handler400,
    handler403,
    handler404,
    handler500
)
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from .views import HealthCheckView
handler400 = 'data_hub.views.bad_request'
handler403 = 'data_hub.views.permission_denied'
handler404 = 'data_hub.views.page_not_found'
handler500 = 'data_hub.views.server_error'

from data_hub.sitemap import StaticSitemap, CollectionSitemap
from django.contrib.sitemaps.views import sitemap

from rest_framework.authtoken.views import obtain_auth_token

sitemaps = {
 'pages': StaticSitemap,
 'collections': CollectionSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/doc/', include('django.contrib.admindocs.urls')), # django admindocs
    path('admin/lcd/xlargesupplemental/', RedirectView.as_view(url='add/', permanent=False)), # no list view for xlarge supplemental model
    path('admin/lcd/xlargesupplemental/<int:id>/change/', RedirectView.as_view(url='/admin/lcd/xlargesupplemental/add/', permanent=False)), # no change view for xlarge supplemental model
    path('admin/', admin.site.urls), # admin site
    path('admin', RedirectView.as_view(url='admin/', permanent=False)), # admin site
    path('api/v1/', include('lcd.urls')),
    path('api/v2/contact/', include('contact.fiserv_urls')),
    path('health/', HealthCheckView.as_view()),
    path('api/v1/token/', obtain_auth_token, name="auth_token"),
    path('analytics/', include('analytics.urls')),
    path('', RedirectView.as_view(url='admin/', permanent=False)), # redirect home to admin
]
