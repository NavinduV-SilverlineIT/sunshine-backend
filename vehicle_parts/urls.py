from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiclePartsViewSet

router = DefaultRouter()
router.register(r'vehicle-parts', VehiclePartsViewSet, basename='vehicle-parts')

urlpatterns = [
    path('', include(router.urls)),
]