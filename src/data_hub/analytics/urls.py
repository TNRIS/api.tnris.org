from django.urls import path, include
from rest_framework import routers
from . import views

urlpatterns = [
    path('get_monthly_stats/', views.get_monthly_stats)
    # path('hello/', views.hello_world),
    # path('get_monthly_stats_old/', views.get_monthly_stats_old)
]