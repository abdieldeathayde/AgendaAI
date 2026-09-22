import csv
from decimal import Decimal
from io import StringIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    AppointmentForm,
    AvailabilityForm,
    CustomerForm,
    ProfessionalForm,
    ServiceForm,
)
from .models import Appointment, Availability, Customer, Professional, Service


# ---------------- Clientes ----------------

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'accounts/customers.html', {'customers': customers})


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f"Cliente '{customer.name}' cadastrado com sucesso!")
            return redirect('customers')
    else:
        form = CustomerForm()
    return render(request, 'accounts/customer_form.html', {'form': form, 'title': 'Novo cliente'})


@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente '{customer.name}' atualizado com sucesso!")
            return redirect('customers')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'accounts/customer_form.html', {'form': form, 'title': 'Editar cliente'})


@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        name = customer.name
        customer.delete()
        messages.info(request, f"Cliente '{name}' excluído.")
        return redirect('customers')
    return render(request, 'accounts/delete_confirm.html', {'object': customer, 'title': 'Excluir cliente', 'return_url': 'customers'})


# ---------------- Profissionais ----------------

@login_required
def professional_list(request):
    professionals = Professional.objects.prefetch_related('availabilities', 'services').all()
    return render(request, 'accounts/professionals.html', {'professionals': professionals})


@login_required
def professional_create(request):
    if request.method == 'POST':
        form = ProfessionalForm(request.POST)
        if form.is_valid():
            pro = form.save()
            messages.success(request, f"Profissional '{pro.name}' cadastrado com sucesso!")
            return redirect('professionals')
    else:
        form = ProfessionalForm()
    return render(request, 'accounts/professional_form.html', {'form': form, 'title': 'Novo profissional'})


@login_required
def professional_update(request, pk):
    professional = get_object_or_404(Professional, pk=pk)
    if request.method == 'POST':
        form = ProfessionalForm(request.POST, instance=professional)
        if form.is_valid():
            form.save()
            messages.success(request, f"Profissional '{professional.name}' atualizado com sucesso!")
            return redirect('professionals')
    else:
        form = ProfessionalForm(instance=professional)
    return render(request, 'accounts/professional_form.html', {'form': form, 'title': 'Editar profissional'})


@login_required
def professional_delete(request, pk):
    professional = get_object_or_404(Professional, pk=pk)
    if request.method == 'POST':
        name = professional.name
        professional.delete()
        messages.info(request, f"Profissional '{name}' excluído.")
        return redirect('professionals')
    return render(request, 'accounts/delete_confirm.html', {'object': professional, 'title': 'Excluir profissional', 'return_url': 'professionals'})


# ---------------- Serviços ----------------

@login_required
def service_list(request):
    services = list(Service.objects.select_related('professional').all())
    average_price = (
        sum((service.price for service in services), Decimal('0')) / Decimal(len(services))
        if services else Decimal('0')
    )
    return render(
        request,
        'accounts/services.html',
        {'services': services, 'average_price': average_price},
    )


@login_required
def service_create(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            svc = form.save()
            messages.success(request, f"Serviço '{svc.name}' cadastrado com sucesso!")
            return redirect('services')
    else:
        form = ServiceForm()
    return render(request, 'accounts/service_form.html', {'form': form, 'title': 'Novo serviço'})


@login_required
def service_update(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, f"Serviço '{service.name}' atualizado com sucesso!")
            return redirect('services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'accounts/service_form.html', {'form': form, 'title': 'Editar serviço'})


@login_required
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        name = service.name
        service.delete()
        messages.info(request, f"Serviço '{name}' excluído.")
        return redirect('services')
    return render(request, 'accounts/delete_confirm.html', {'object': service, 'title': 'Excluir serviço', 'return_url': 'services'})


# ---------------- Disponibilidade / Horários ----------------

@login_required
def availability_list(request):
    selected_pro = request.GET.get('professional')
    professionals = Professional.objects.all()
    availabilities = Availability.objects.select_related('professional').order_by('professional__name', 'day_of_week')

    if selected_pro:
        availabilities = availabilities.filter(professional_id=selected_pro)

    return render(
        request,
        'accounts/availabilities.html',
        {
            'availabilities': availabilities,
            'professionals': professionals,
            'selected_pro': selected_pro,
        },
    )


@login_required
def availability_create(request):
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            av = form.save()
            messages.success(request, f"Disponibilidade ({av.get_day_of_week_display()}) adicionada para {av.professional.name}!")
            return redirect('availabilities')
    else:
        initial = {}
        if pro_id := request.GET.get('professional'):
            initial['professional'] = pro_id
        form = AvailabilityForm(initial=initial)

    return render(request, 'accounts/availability_form.html', {'form': form, 'title': 'Configurar horário de atendimento'})


@login_required
def availability_delete(request, pk):
    availability = get_object_or_404(Availability, pk=pk)
    if request.method == 'POST':
        desc = f"{availability.professional.name} ({availability.get_day_of_week_display()})"
        availability.delete()
        messages.info(request, f"Horário de {desc} removido.")
        return redirect('availabilities')
    return render(request, 'accounts/delete_confirm.html', {'object': availability, 'title': 'Excluir horário', 'return_url': 'availabilities'})


# ---------------- Agendamentos ----------------

@login_required
def appointment_list(request):
    selected_status = request.GET.get('status')
    selected_professional = request.GET.get('professional')
    professionals = Professional.objects.all()

    appointments_qs = Appointment.objects.select_related('customer', 'service', 'service__professional').all()

    # Cálculo correto dos agendamentos de hoje
    today = timezone.localdate()
    today_count = Appointment.objects.filter(start_time__date=today).count()
    total_count = Appointment.objects.count()

    if selected_status:
        appointments_qs = appointments_qs.filter(status=selected_status)

    if selected_professional:
        appointments_qs = appointments_qs.filter(service__professional_id=selected_professional)

    return render(
        request,
        'accounts/appointments.html',
        {
            'appointments': appointments_qs,
            'total_count': total_count,
            'today_count': today_count,
            'selected_status': selected_status,
            'selected_professional': selected_professional,
            'professionals': professionals,
        },
    )


@login_required
def appointment_status_update(request, pk, new_status):
    appointment = get_object_or_404(Appointment, pk=pk)
    valid_statuses = dict(Appointment.Status.choices)

    if new_status in valid_statuses:
        appointment.status = new_status
        appointment.save(update_fields=['status'])
        messages.success(
            request,
            f"Agendamento de {appointment.customer.name} atualizado para '{valid_statuses[new_status]}'."
        )
    else:
        messages.error(request, "Status informado é inválido.")

    next_url = request.GET.get('next') or 'appointments'
    return redirect(next_url)


@login_required
def appointments_export(request):
    selected_status = request.GET.get('status')
    selected_professional = request.GET.get('professional')

    appointments = Appointment.objects.select_related('customer', 'service', 'service__professional').all()
    if selected_status:
        appointments = appointments.filter(status=selected_status)
    if selected_professional:
        appointments = appointments.filter(service__professional_id=selected_professional)

    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(['Cliente', 'Serviço', 'Profissional', 'Data', 'Status', 'Preço'])

    for appointment in appointments:
        writer.writerow([
            appointment.customer.name,
            appointment.service.name,
            appointment.service.professional.name,
            appointment.start_time.strftime('%d/%m/%Y %H:%M'),
            appointment.get_status_display(),
            str(appointment.price if appointment.price is not None else appointment.service.price),
        ])

    response = HttpResponse(buffer.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="agendamentos.csv"'
    return response


import json

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f"Agendamento para {appointment.customer.name} criado com sucesso!")
            return redirect('appointments')
    else:
        form = AppointmentForm()

    service_durations = {str(s.id): s.duration_minutes for s in Service.objects.filter(active=True)}
    return render(request, 'accounts/appointment_form.html', {
        'form': form,
        'title': 'Novo agendamento',
        'service_durations_json': json.dumps(service_durations),
    })


@login_required
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f"Agendamento #{appointment.pk} atualizado com sucesso!")
            return redirect('appointments')
    else:
        form = AppointmentForm(instance=appointment)

    service_durations = {str(s.id): s.duration_minutes for s in Service.objects.filter(active=True)}
    return render(request, 'accounts/appointment_form.html', {
        'form': form,
        'title': 'Editar agendamento',
        'service_durations_json': json.dumps(service_durations),
    })


@login_required
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        pk_val = appointment.pk
        appointment.delete()
        messages.info(request, f"Agendamento #{pk_val} excluído com sucesso.")
        return redirect('appointments')
    return render(request, 'accounts/delete_confirm.html', {'object': appointment, 'title': 'Excluir agendamento', 'return_url': 'appointments'})
