from datetime import datetime, time, timedelta
from django.utils import timezone

from accounts.models import Appointment, Availability, Service


def get_available_slots(professional, target_date, service):
    """
    Calcula os intervalos de horários livres para um profissional em uma data específica
    considerando o serviço desejado e os agendamentos já confirmados/agendados.
    """
    weekday = target_date.weekday()
    availabilities = Availability.objects.filter(professional=professional, day_of_week=weekday)
    if not availabilities.exists():
        return []

    # Agendamentos conflitantes no dia
    existing_appointments = list(
        Appointment.objects.filter(
            service__professional=professional,
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED],
            start_time__date=target_date,
        ).order_by("start_time")
    )

    slots = []
    duration = timedelta(minutes=service.duration_minutes)
    now = timezone.now()

    for availability in availabilities:
        current_dt = timezone.make_aware(datetime.combine(target_date, availability.start_time))
        end_dt = timezone.make_aware(datetime.combine(target_date, availability.end_time))

        while current_dt + duration <= end_dt:
            slot_start = current_dt
            slot_end = current_dt + duration

            # Não permite agendar horários que já passaram
            if slot_start < now:
                current_dt += timedelta(minutes=15)
                continue

            # Checar sobreposição com agendamentos já existentes
            has_conflict = any(
                appt.start_time < slot_end and appt.end_time > slot_start
                for appt in existing_appointments
            )

            if not has_conflict:
                slots.append({
                    "start": slot_start.strftime("%H:%M"),
                    "end": slot_end.strftime("%H:%M"),
                    "start_datetime": slot_start.strftime("%Y-%m-%dT%H:%M"),
                    "end_datetime": slot_end.strftime("%Y-%m-%dT%H:%M"),
                })

            current_dt += timedelta(minutes=15)

    return slots

