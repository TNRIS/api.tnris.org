from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('get_monthly_stats/', views.get_monthly_stats)
]