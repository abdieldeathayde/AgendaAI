from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from django.conf import settings


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customer_profile")
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name


class Professional(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="professional_profile")
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Service(models.Model):
    professional = models.ForeignKey(Professional, related_name="services", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)

    def clean(self):
        errors = {}
        if self.duration_minutes <= 0:
            errors["duration_minutes"] = "A duração deve ser maior que zero."
        if self.price is not None and self.price < 0:
            errors["price"] = "O preço não pode ser negativo."
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.name


class Availability(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Segunda-feira"
        TUESDAY = 1, "Terça-feira"
        WEDNESDAY = 2, "Quarta-feira"
        THURSDAY = 3, "Quinta-feira"
        FRIDAY = 4, "Sexta-feira"
        SATURDAY = 5, "Sábado"
        SUNDAY = 6, "Domingo"

    professional = models.ForeignKey(Professional, related_name="availabilities", on_delete=models.CASCADE)
    day_of_week = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("professional", "day_of_week"), name="unique_professional_weekday")
        ]
        ordering = ["day_of_week", "start_time"]

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("O horário inicial deve ser anterior ao horário final.")

    def __str__(self):
        return f"{self.professional.name} - {self.get_day_of_week_display()}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        SCHEDULED = "SC", "Agendado"
        CONFIRMED = "CF", "Confirmado"
        CANCELLED = "CA", "Cancelado"
        COMPLETED = "CO", "Concluído"

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="appointments")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="appointments")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.SCHEDULED)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]
        indexes = [
            models.Index(fields=("start_time", "status")),
            models.Index(fields=("customer", "start_time")),
        ]

    def clean(self):
        errors = {}

        if not self.service_id:
            errors["service"] = "Selecione um serviço."
        if not self.start_time or not self.end_time:
            errors["start_time"] = "Informe início e fim do agendamento."
        elif self.start_time >= self.end_time:
            errors["end_time"] = "O horário final deve ser posterior ao inicial."

        if errors:
            raise ValidationError(errors)

        duration = self.end_time - self.start_time
        expected = timedelta(minutes=self.service.duration_minutes)
        if duration != expected:
            errors["end_time"] = (
                f"O serviço '{self.service.name}' dura {self.service.duration_minutes} minutos."
            )

        professional = self.service.professional
        if not self.service.active:
            errors["service"] = "Não é possível agendar um serviço inativo."
        if not professional.active:
            errors["service"] = "Não é possível agendar com um profissional inativo."

        weekday = timezone.localtime(self.start_time).weekday()
        start_local = timezone.localtime(self.start_time).time()
        end_local = timezone.localtime(self.end_time).time()
        availabilities = Availability.objects.filter(professional=professional, day_of_week=weekday)
        if availabilities.exists() and not availabilities.filter(start_time__lte=start_local, end_time__gte=end_local).exists():
            errors["start_time"] = "O profissional não está disponível nesse horário."

        if self.status in {self.Status.SCHEDULED, self.Status.CONFIRMED}:
            conflicts = Appointment.objects.filter(
                service__professional=professional,
                status__in=[self.Status.SCHEDULED, self.Status.CONFIRMED],
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exclude(pk=self.pk)
            if conflicts.exists():
                errors["start_time"] = "O profissional já possui um agendamento nesse período."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.price is None and self.service_id:
            self.price = self.service.price
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def professional(self):
        return self.service.professional

    def __str__(self):
        return f"{self.customer.name} - {self.service.name} - {self.start_time:%d/%m/%Y %H:%M}"
