from datetime import timedelta

from django import forms

from .models import Appointment, Availability, Customer, Professional, Service


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuário',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu usuário'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha'})
    )


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['user', 'name', 'phone']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: João da Silva'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(11) 99999-9999'}),
        }


class ProfessionalForm(forms.ModelForm):
    class Meta:
        model = Professional
        fields = ['user', 'name', 'specialty', 'bio', 'active']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Maria Santos'}),
            'specialty': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Corte e barba'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva a formação, experiência e especialidades do profissional.'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['professional', 'name', 'description', 'duration_minutes', 'price', 'active']
        widgets = {
            'professional': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex.: Corte clássico'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Descreva os detalhes do serviço e benefícios oferecidos.'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '45'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': 0, 'placeholder': '79.90'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['professional', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'professional': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }


class AppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['end_time'].required = False
        self.fields['end_time'].help_text = "Calculado automaticamente se deixado em branco com base na duração do serviço."

    def clean(self):
        cleaned_data = super().clean()
        service = cleaned_data.get("service")
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        status = cleaned_data.get("status")

        if service and start_time and not end_time:
            end_time = start_time + timedelta(minutes=service.duration_minutes)
            cleaned_data["end_time"] = end_time

        if self.instance.pk is None and start_time and status in {Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED}:
            from django.utils import timezone
            if start_time < timezone.now():
                self.add_error("start_time", "Não é possível criar um agendamento ativo no passado.")
        return cleaned_data

    class Meta:
        model = Appointment
        fields = ['customer', 'service', 'start_time', 'end_time', 'status', 'notes']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'service': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observações do atendimento'}),
        }
