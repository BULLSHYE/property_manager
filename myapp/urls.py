from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LandlordViewSet, PropertyViewSet, RoomViewSet, TenantViewSet, ElectricityViewSet, PaymentViewSet, property_monthly_details

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Property Management API",  # Change this title to match your project name
        default_version='v1',
        description="API documentation for Property Management System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourdomain.com"),  # Update the contact email
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # This makes the API public
)

# Registering the API ViewSets with the DefaultRouter
router = DefaultRouter()
router.register(r'landlords', LandlordViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'tenants', TenantViewSet)
router.register(r'meter-readings', ElectricityViewSet)
router.register(r'payments', PaymentViewSet)

# Defining URL Patterns
urlpatterns = [
    path('api/', include(router.urls)),  # This will include all registered ViewSets
    path('api/property-details/<int:property_id>/<int:month>/', property_monthly_details, name="property-monthly-details"),
    
    # Swagger UI for API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI path
]
