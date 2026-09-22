from django.urls import path

from .views import dashboard, finance, reports

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('reports/', reports, name='reports'),
    path('finance/', finance, name='finance'),
]
