from django.urls import path, include
from .views import index, CalculateDataAPIView, GetCorrelationAPIView

urlpatterns = [
    path('', index, name='index'),
    path('calculate/', CalculateDataAPIView.as_view(), name='calculate'),
    path('correlation', GetCorrelationAPIView.as_view(), name='correlation'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    ]
