from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    VehicleViewSet, VehiclePurchaseViewSet, VehicleDetailViewSet,
    VehicleSaleViewSet, VehicleRegistrationViewSet
)

router = DefaultRouter()
router.register(r'vehicles', VehicleViewSet)
router.register(r'vehicle-purchases', VehiclePurchaseViewSet)
router.register(r'vehicle-details', VehicleDetailViewSet)
router.register(r'vehicle-sales', VehicleSaleViewSet)
router.register(r'vehicle-registrations', VehicleRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


# from django.urls import path
# from .views import VehicleListView, FilterOptionsView

# urlpatterns = [
#     path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
#     path('vehicles/filter-options/', FilterOptionsView.as_view(), name='filter-options'),
# ]