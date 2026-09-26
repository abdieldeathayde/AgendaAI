from django.shortcuts import redirect
from django.urls import path

from .views import dashboard, finance, reports

urlpatterns = [
    path('', lambda request: redirect('register'), name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reports/', reports, name='reports'),
    path('finance/', finance, name='finance'),
]
