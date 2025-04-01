from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandlordViewSet, PropertyViewSet, RoomViewSet, TenantViewSet, ElectricityViewSet, PaymentViewSet, property_monthly_details

router = DefaultRouter()
router.register(r'landlords', LandlordViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'meter-readings', ElectricityViewSet)
router.register(r'payments', PaymentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/property-details/<int:property_id>/<int:month>/', property_monthly_details, name="property-monthly-details"),
]
