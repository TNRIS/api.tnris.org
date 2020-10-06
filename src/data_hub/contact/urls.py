"""contact URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from rest_framework.schemas import get_schema_view

from .viewsets import (
    SubmitFormViewSet,
    ZipPolicyViewSet,
    ImagePolicyViewSet,
    FilePolicyViewSet,
    SurveyTemplateViewSet
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'submit/?', SubmitFormViewSet, basename="SubmitForm")
router.register(r'policy/zip-upload', ZipPolicyViewSet, basename="ZipPolicy")
router.register(r'policy/image-upload', ImagePolicyViewSet, basename="ImagePolicy")
router.register(r'policy/file-upload', FilePolicyViewSet, basename="FilePolicy")
router.register(r'survey', SurveyTemplateViewSet, basename="Survey")

schema_view = get_swagger_view(title='Contact API')

urlpatterns = [
    path('', include(router.urls)),
]
