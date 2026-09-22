from rest_framework import serializers

from .models import Appointment, Availability, Customer, Professional, Service


class AvailabilitySerializer(serializers.ModelSerializer):
    weekday_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    professional_name = serializers.CharField(source='professional.name', read_only=True)

    class Meta:
        model = Availability
        fields = ('id', 'professional', 'professional_name', 'day_of_week', 'weekday_display', 'start_time', 'end_time')


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'user', 'name', 'phone')


class ProfessionalSerializer(serializers.ModelSerializer):
    availabilities = AvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Professional
        fields = ('id', 'user', 'name', 'specialty', 'bio', 'active', 'availabilities')


class ServiceSerializer(serializers.ModelSerializer):
    professional_name = serializers.CharField(source='professional.name', read_only=True)

    class Meta:
        model = Service
        fields = ('id', 'professional', 'professional_name', 'name', 'description', 'duration_minutes', 'price', 'active')


class AppointmentSerializer(serializers.ModelSerializer):
    professional = serializers.IntegerField(source='service.professional_id', read_only=True)
    professional_name = serializers.CharField(source='service.professional.name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Appointment
        fields = (
            'id', 'customer', 'customer_name', 'service', 'service_name',
            'professional', 'professional_name', 'start_time', 'end_time',
            'status', 'price', 'notes', 'created_at', 'updated_at',
        )
        read_only_fields = ('price', 'created_at', 'updated_at', 'professional', 'professional_name', 'service_name', 'customer_name')

    def validate(self, attrs):
        from django.utils import timezone

        start_time = attrs.get("start_time", getattr(self.instance, "start_time", None))
        status = attrs.get("status", getattr(self.instance, "status", Appointment.Status.SCHEDULED))
        if self.instance is None and start_time and status in {Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED}:
            if start_time < timezone.now():
                raise serializers.ValidationError({"start_time": "Não é possível criar um agendamento ativo no passado."})

        if self.instance is not None:
            instance = Appointment(
                pk=self.instance.pk,
                customer=attrs.get("customer", self.instance.customer),
                service=attrs.get("service", self.instance.service),
                start_time=attrs.get("start_time", self.instance.start_time),
                end_time=attrs.get("end_time", self.instance.end_time),
                status=attrs.get("status", self.instance.status),
                price=self.instance.price,
                notes=attrs.get("notes", self.instance.notes),
            )
        else:
            instance = Appointment(**attrs)
        instance.full_clean()
        return attrs
