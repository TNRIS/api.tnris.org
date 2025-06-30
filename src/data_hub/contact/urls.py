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
    CcpSubmitFormViewSet,
    CcpOrderFormViewSet,
    CcpOrderSubmitViewSet,
    CcpOrderStatusViewSet,
    CcpOrderCleanupViewSet,
    CcpInitiateRetentionCleanupViewSet,
    CcpGenOtpViewSet,
    FiservSubmitFormViewSet,
    FiservGenOtpViewSet,
    FiservOrderStatusViewSet,
    FiservInitiateRetentionCleanupViewSet,
    FiservOrderCleanupViewSet,
    FiservOrderSubmitViewSet,
    FiservOrderFormViewSet,
    FiservRedirectUrlViewSet,
    ZipPolicyViewSet,
    ImagePolicyViewSet,
    FilePolicyViewSet,
    SubmitSurveyViewSet,
    SurveyTemplateViewSet,
    DataHubOrdersViewSet,
    SubmitCampaignSubscriptionViewSet
)

router = routers.DefaultRouter(trailing_slash=False)

#v1 urls CCP
router.register(r'submit/?', CcpSubmitFormViewSet, basename="SubmitForm")
router.register(r'order/otp/?', CcpGenOtpViewSet, basename="OrderOtp")
router.register(r'order/status/?', CcpOrderStatusViewSet, basename="OrderStatus")
router.register(r'order/retentionCleanup/?', CcpInitiateRetentionCleanupViewSet, basename="InitiateRetentionCleanup")
router.register(r'order/cleanup/?', CcpOrderCleanupViewSet, basename="OrderCleanup")
router.register(r'order/?', CcpOrderFormViewSet, basename="OrderForm")
router.register(r'order/submit/?', CcpOrderSubmitViewSet, basename="PaymentForm")
#v2 urls FiServ
router.register(r'v2/submit/?', FiservSubmitFormViewSet, basename="SubmitForm")
router.register(r'v2/order/otp/?', FiservGenOtpViewSet, basename="OrderOtp")
router.register(r'v2/order/status/?', FiservOrderStatusViewSet, basename="OrderStatus")
router.register(r'v2/order/retentionCleanup/?', FiservInitiateRetentionCleanupViewSet, basename="InitiateRetentionCleanup")
router.register(r'v2/order/cleanup/?', FiservOrderCleanupViewSet, basename="OrderCleanup")
router.register(r'v2/order/submit/?', FiservOrderSubmitViewSet, basename="PaymentForm")
router.register(r'v2/order/?', FiservOrderFormViewSet, basename="OrderForm")
router.register(r'v2/order/redirect/?', FiservRedirectUrlViewSet, basename="RedirectUrl")

router.register(r'policy/zip-upload', ZipPolicyViewSet, basename="ZipPolicy")
router.register(r'policy/image-upload', ImagePolicyViewSet, basename="ImagePolicy")
router.register(r'policy/file-upload', FilePolicyViewSet, basename="FilePolicy")
router.register(r'survey', SurveyTemplateViewSet, basename="Survey")
router.register(r'survey/submit/?', SubmitSurveyViewSet, basename="SubmitSurvey")
router.register(r'orders', DataHubOrdersViewSet, basename="Orders")
router.register(r'campaignsubscription', SubmitCampaignSubscriptionViewSet, basename="SubmitCampaignSubscription")

schema_view = get_swagger_view(title='Contact API')

urlpatterns = [
    path('', include(router.urls)),
]
