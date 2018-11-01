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
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

handler404 = TemplateView.as_view(template_name='index.html')

from .views import HealthCheckView

urlpatterns = [
    path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/doc/', include('django.contrib.admindocs.urls')), # django admindocs
    path('admin/', admin.site.urls), # admin site
    path('admin', RedirectView.as_view(url='admin/', permanent=False)), # admin site
    path('api/v1/', include('lcd.urls')),
    path('health/', HealthCheckView.as_view()),
    path('collection/<coll>', TemplateView.as_view(template_name='index.html')),
    path('', TemplateView.as_view(template_name='index.html')),
]
