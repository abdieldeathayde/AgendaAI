from django.urls import path

from .crud_views import (
    appointment_create,
    appointment_delete,
    appointment_list,
    appointment_status_update,
    appointment_update,
    appointments_export,
    availability_create,
    availability_delete,
    availability_list,
    customer_create,
    customer_delete,
    customer_list,
    customer_update,
    professional_create,
    professional_delete,
    professional_list,
    professional_update,
    service_create,
    service_delete,
    service_list,
    service_update,
)
from .views import login_view, logout_view

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('customers/', customer_list, name='customers'),
    path('customers/new/', customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', customer_update, name='customer_update'),
    path('customers/<int:pk>/delete/', customer_delete, name='customer_delete'),

    path('professionals/', professional_list, name='professionals'),
    path('professionals/new/', professional_create, name='professional_create'),
    path('professionals/<int:pk>/edit/', professional_update, name='professional_update'),
    path('professionals/<int:pk>/delete/', professional_delete, name='professional_delete'),

    path('availabilities/', availability_list, name='availabilities'),
    path('availabilities/new/', availability_create, name='availability_create'),
    path('availabilities/<int:pk>/delete/', availability_delete, name='availability_delete'),

    path('services/', service_list, name='services'),
    path('services/new/', service_create, name='service_create'),
    path('services/<int:pk>/edit/', service_update, name='service_update'),
    path('services/<int:pk>/delete/', service_delete, name='service_delete'),

    path('appointments/', appointment_list, name='appointments'),
    path('appointments/export/', appointments_export, name='appointments_export'),
    path('appointments/new/', appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/edit/', appointment_update, name='appointment_update'),
    path('appointments/<int:pk>/delete/', appointment_delete, name='appointment_delete'),
    path('appointments/<int:pk>/status/<str:new_status>/', appointment_status_update, name='appointment_status_update'),
]
