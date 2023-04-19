from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path('submitData/', PassViewSet.as_view({'get': 'get_email', 'post': 'post'})),
    path('submitData/<int:pk>', PassViewSet.as_view({'get': 'get_one', 'patch': 'change'})),
]
