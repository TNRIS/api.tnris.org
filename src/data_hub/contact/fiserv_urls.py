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

from .viewsets import (
    FiservSubmitFormViewSet,
    FiservGenOtpViewSet,
    FiservOrderStatusViewSet,
    FiservInitiateRetentionCleanupViewSet,
    FiservOrderCleanupViewSet,
    FiservOrderSubmitViewSet,
    FiservOrderFormViewSet,
    FiservRedirectUrlViewSet,
)

router = routers.DefaultRouter(trailing_slash=False)

#v2 urls FiServ
router.register(r'submit/?', FiservSubmitFormViewSet, basename="FiservSubmitForm")
router.register(r'order/otp/?', FiservGenOtpViewSet, basename="FiservOrderOtp")
router.register(r'order/status/?', FiservOrderStatusViewSet, basename="FiservOrderStatus")
router.register(r'order/retentionCleanup/?', FiservInitiateRetentionCleanupViewSet, basename="FiservInitiateRetentionCleanup")
router.register(r'order/cleanup/?', FiservOrderCleanupViewSet, basename="FiservOrderCleanup")
router.register(r'order/submit/?', FiservOrderSubmitViewSet, basename="FiservPaymentForm")
router.register(r'order/?', FiservOrderFormViewSet, basename="FiservOrderForm")
router.register(r'order/redirect/?', FiservRedirectUrlViewSet, basename="FiservRedirectUrl")

schema_view = get_swagger_view(title='Contact Fiserv API')

urlpatterns = [
    path('', include(router.urls)),
]
