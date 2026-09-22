from datetime import datetime

from django.db.models import Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Appointment, Availability, Customer, Professional, Service
from .serializers import (
    AppointmentSerializer,
    AvailabilitySerializer,
    CustomerSerializer,
    ProfessionalSerializer,
    ServiceSerializer,
)
from .services import get_available_slots


class AvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = AvailabilitySerializer

    def get_queryset(self):
        queryset = Availability.objects.select_related('professional').order_by('day_of_week', 'start_time')
        professional = self.request.query_params.get('professional')
        if professional:
            queryset = queryset.filter(professional_id=professional)
        return queryset


class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        queryset = Customer.objects.select_related('user').order_by('name')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(phone__icontains=search))
        return queryset


class ProfessionalViewSet(viewsets.ModelViewSet):
    serializer_class = ProfessionalSerializer

    def get_queryset(self):
        queryset = Professional.objects.select_related('user').prefetch_related('availabilities').order_by('name')
        active = self.request.query_params.get('active')
        if active in {'true', 'false'}:
            queryset = queryset.filter(active=active == 'true')
        return queryset

    @action(detail=True, methods=['get'], url_path='available-slots', permission_classes=[permissions.AllowAny])
    def available_slots(self, request, pk=None):
        professional = self.get_object()
        date_str = request.query_params.get('date')
        service_id = request.query_params.get('service')

        if not date_str:
            target_date = timezone.localdate()
        else:
            try:
                target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return Response({"error": "Formato de data inválido. Utilize AAAA-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if not service_id:
            service = professional.services.filter(active=True).first()
            if not service:
                return Response({"error": "Nenhum serviço ativo encontrado para este profissional."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                service = professional.services.get(pk=service_id, active=True)
            except Service.DoesNotExist:
                return Response({"error": "Serviço não encontrado ou inativo."}, status=status.HTTP_404_NOT_FOUND)

        slots = get_available_slots(professional, target_date, service)
        return Response({
            "professional_id": professional.id,
            "professional_name": professional.name,
            "service_id": service.id,
            "service_name": service.name,
            "duration_minutes": service.duration_minutes,
            "date": target_date.strftime("%Y-%m-%d"),
            "slots": slots,
        })


class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.select_related('professional').order_by('name')
        professional = self.request.query_params.get('professional')
        active = self.request.query_params.get('active')
        if professional:
            queryset = queryset.filter(professional_id=professional)
        if active in {'true', 'false'}:
            queryset = queryset.filter(active=active == 'true')
        return queryset


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        queryset = Appointment.objects.select_related('customer', 'service', 'service__professional').all()
        status = self.request.query_params.get('status')
        professional = self.request.query_params.get('professional')
        customer = self.request.query_params.get('customer')
        date = self.request.query_params.get('date')
        if status:
            queryset = queryset.filter(status=status)
        if professional:
            queryset = queryset.filter(service__professional_id=professional)
        if customer:
            queryset = queryset.filter(customer_id=customer)
        if date:
            queryset = queryset.filter(start_time__date=date)
        return queryset
