from django.urls import path
from .views import APIView


urlpatterns = [
    path('submitData/', APIView.as_view({'post': 'post'}), name='submitData'),
]