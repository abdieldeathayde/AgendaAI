from django.contrib import admin

from .models import Appointment, Availability, Customer, Professional, Service


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'user')
    search_fields = ('name', 'phone', 'user__username')


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'user')
    search_fields = ('name', 'specialty', 'user__username')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'professional', 'price', 'duration_minutes')
    list_filter = ('professional',)


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('professional', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('professional', 'day_of_week')


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('customer', 'service', 'start_time', 'status')
    list_filter = ('status', 'service__professional')
    search_fields = ('customer__name', 'service__name')
