from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import (
    AppointmentViewSet,
    AvailabilityViewSet,
    CustomerViewSet,
    ProfessionalViewSet,
    ServiceViewSet,
)

router = DefaultRouter()
router.register('customers', CustomerViewSet, basename='api-customers')
router.register('professionals', ProfessionalViewSet, basename='api-professionals')
router.register('services', ServiceViewSet, basename='api-services')
router.register('appointments', AppointmentViewSet, basename='api-appointments')
router.register('availabilities', AvailabilityViewSet, basename='api-availabilities')

urlpatterns = [
    path('', include(router.urls)),
]
