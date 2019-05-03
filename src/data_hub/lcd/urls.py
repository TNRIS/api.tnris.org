"""lcd URL Configuration

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
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view
from .viewsets import CollectionViewSet, ResourceViewSet, AreaViewSet
from .views import resource_update_progress
import lore
import msd


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'collections/?', CollectionViewSet, base_name="Collections")
router.register(r'resources/?', ResourceViewSet, base_name="Resources")
router.register(r'areas/?', AreaViewSet, base_name="Areas")

schema_view = get_swagger_view(title='TNRIS Data API')

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', schema_view, name='api_schema'),
    path('data_hub-auth/?', include('rest_framework.urls', namespace='lcd_rest_framework')),
    path('resource-update-progress/', resource_update_progress, name='resource-update-progress'),
    path('historical/', include('lore.urls')),
    path('map/', include('msd.urls'))
]
