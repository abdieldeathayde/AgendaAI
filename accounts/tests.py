from django.test import TestCase
from django.urls import reverse

from users.models import User
from .models import Appointment, Customer, Professional, Service


class CrudFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )
        self.appointment = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-20T10:00:00Z',
            end_time='2026-09-20T10:45:00Z',
            status='SC',
        )

    def test_customer_update_and_delete_work(self):
        response = self.client.post(
            reverse('customer_update', args=[self.customer.pk]),
            {'user': self.user.pk, 'name': 'João Atualizado', 'phone': '11888888888'},
        )
        self.assertEqual(response.status_code, 302)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'João Atualizado')

        response = self.client.post(reverse('customer_delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())

    def test_professional_update_and_delete_work(self):
        response = self.client.post(
            reverse('professional_update', args=[self.professional.pk]),
            {'user': self.user.pk, 'name': 'Maria Silva', 'specialty': 'Barba e cabelo', 'bio': 'Nova bio'},
        )
        self.assertEqual(response.status_code, 302)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.name, 'Maria Silva')

        response = self.client.post(reverse('professional_delete', args=[self.professional.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Professional.objects.filter(pk=self.professional.pk).exists())

    def test_service_update_and_delete_work(self):
        response = self.client.post(
            reverse('service_update', args=[self.service.pk]),
            {'professional': self.professional.pk, 'name': 'Corte premium', 'description': 'Atualizado', 'duration_minutes': 60, 'price': '90.00'},
        )
        self.assertEqual(response.status_code, 302)
        self.service.refresh_from_db()
        self.assertEqual(self.service.name, 'Corte premium')

        response = self.client.post(reverse('service_delete', args=[self.service.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Service.objects.filter(pk=self.service.pk).exists())

    def test_appointment_update_and_delete_work(self):
        response = self.client.post(
            reverse('appointment_update', args=[self.appointment.pk]),
            {
                'customer': self.customer.pk,
                'service': self.service.pk,
                'start_time': '2026-09-21T11:00:00',
                'end_time': '2026-09-21T11:45:00',
                'status': 'CF',
            },
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'CF')

        response = self.client.post(reverse('appointment_delete', args=[self.appointment.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Appointment.objects.filter(pk=self.appointment.pk).exists())


class AppointmentStatusFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )

        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-20T10:00:00Z',
            end_time='2026-09-20T10:45:00Z',
            status='SC',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-21T11:00:00Z',
            end_time='2026-09-21T11:45:00Z',
            status='CF',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-22T12:00:00Z',
            end_time='2026-09-22T12:45:00Z',
            status='CO',
        )

    def test_appointment_status_filter_works(self):
        response = self.client.get(reverse('appointments') + '?status=CF')

        self.assertEqual(response.status_code, 200)
        self.assertIn('appointments', response.context)
        self.assertEqual(len(response.context['appointments']), 1)
        self.assertEqual(response.context['appointments'][0].status, 'CF')
        self.assertContains(response, 'Confirmado')

    def test_appointment_filters_by_status_and_professional(self):
        second_user = User.objects.create_user(username='outro', password='123456', email='outro@example.com')
        professional_b = Professional.objects.create(
            user=second_user,
            name='José',
            specialty='Barba',
            bio='Especialista em barba',
        )
        service_b = Service.objects.create(
            professional=professional_b,
            name='Barba premium',
            description='Barba premium',
            duration_minutes=30,
            price='45.00',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=service_b,
            start_time='2026-09-25T15:00:00Z',
            end_time='2026-09-25T15:30:00Z',
            status='CF',
        )

        response = self.client.get(
            reverse('appointments') + f'?status=CF&professional={self.professional.pk}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['appointments']), 1)
        self.assertEqual(response.context['appointments'][0].service.professional, self.professional)

    def test_appointment_export_csv_works(self):
        response = self.client.get(reverse('appointments_export') + '?status=SC')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment; filename="agendamentos.csv"', response['Content-Disposition'])
        self.assertIn('Cliente,Serviço,Profissional,Data,Status,Preço', response.content.decode('utf-8'))
        self.assertIn('João', response.content.decode('utf-8'))


class ManagementPagesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-20T10:00:00Z',
            end_time='2026-09-20T10:45:00Z',
            status='CO',
        )

    def test_reports_page_loads(self):
        response = self.client.get(reverse('reports'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Relatórios')
        self.assertIn('revenue_by_status', response.context)

    def test_finance_page_loads(self):
        response = self.client.get(reverse('finance'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Financeiro')
        self.assertIn('monthly_revenue', response.context)


class DashboardPerformanceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-20T10:00:00Z',
            end_time='2026-09-20T10:45:00Z',
            status='CO',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-21T12:00:00Z',
            end_time='2026-09-21T12:45:00Z',
            status='SC',
        )

    def test_dashboard_exposes_performance_metrics(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('top_services', response.context)
        self.assertIn('top_professionals', response.context)
        self.assertEqual(response.context['top_services'][0]['name'], 'Corte clássico')
        self.assertEqual(response.context['top_professionals'][0]['name'], 'Maria')
        self.assertContains(response, 'Desempenho por serviço')
        self.assertContains(response, 'Profissionais em destaque')


class DashboardPeriodFilterTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )

        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-10T10:00:00Z',
            end_time='2026-09-10T10:45:00Z',
            status='CO',
        )
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2026-09-18T12:00:00Z',
            end_time='2026-09-18T12:45:00Z',
            status='CO',
        )

    def test_dashboard_supports_period_filter(self):
        response = self.client.get(reverse('dashboard') + '?period=7')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['period_filter'], '7')
        self.assertEqual(response.context['period_total_appointments'], 1)
        self.assertEqual(response.context['period_revenue'], 70.00)
        self.assertContains(response, 'Últimos 7 dias')


class DashboardTrendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='123456', email='admin@example.com')
        self.client.force_login(self.user)

        self.customer = Customer.objects.create(user=self.user, name='João', phone='11999999999')
        self.professional = Professional.objects.create(
            user=self.user,
            name='Maria',
            specialty='Corte e barba',
            bio='Especialista em cortes modernos',
        )
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte clássico',
            description='Corte premium',
            duration_minutes=45,
            price='70.00',
        )

        for index, day in enumerate([3, 5, 7], start=1):
            Appointment.objects.create(
                customer=self.customer,
                service=self.service,
                start_time=f'2026-09-{day}T10:00:00Z',
                end_time=f'2026-09-{day}T10:45:00Z',
                status='CO' if index % 2 else 'SC',
            )

    def test_dashboard_exposes_daily_trend(self):
        response = self.client.get(reverse('dashboard') + '?period=7')

        self.assertEqual(response.status_code, 200)
        self.assertIn('trend_data', response.context)
        self.assertTrue(len(response.context['trend_data']) >= 7)
        self.assertContains(response, 'Tendência diária')


class AppointmentBusinessRulesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rules', password='123456')
        self.customer = Customer.objects.create(user=self.user, name='Cliente Teste')
        self.professional = Professional.objects.create(user=self.user, name='Profissional Teste')
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte',
            duration_minutes=60,
            price='80.00',
        )

    def future_datetime(self, day=30, hour=10):
        return f'2099-01-{day:02d}T{hour:02d}:00:00Z'

    def test_appointment_uses_service_price_snapshot(self):
        appointment = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time=self.future_datetime(),
            end_time='2099-01-30T11:00:00Z',
        )
        self.assertEqual(str(appointment.price), '80.00')

    def test_rejects_wrong_duration(self):
        appointment = Appointment(
            customer=self.customer,
            service=self.service,
            start_time=self.future_datetime(),
            end_time='2099-01-30T10:30:00Z',
        )
        with self.assertRaises(Exception):
            appointment.full_clean()

    def test_rejects_overlapping_active_appointments(self):
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time=self.future_datetime(),
            end_time='2099-01-30T11:00:00Z',
        )
        conflict = Appointment(
            customer=self.customer,
            service=self.service,
            start_time='2099-01-30T10:30:00Z',
            end_time='2099-01-30T11:30:00Z',
        )
        with self.assertRaises(Exception):
            conflict.full_clean()

    def test_allows_overlap_when_existing_appointment_is_cancelled(self):
        Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time=self.future_datetime(),
            end_time='2099-01-30T11:00:00Z',
            status=Appointment.Status.CANCELLED,
        )
        appointment = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time='2099-01-30T10:30:00Z',
            end_time='2099-01-30T11:30:00Z',
        )
        self.assertIsNotNone(appointment.pk)


class NewFeaturesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin_test', password='password123', is_staff=True)
        self.client.force_login(self.user)
        self.customer = Customer.objects.create(user=self.user, name='Cliente Teste', phone='11999999999')
        self.professional = Professional.objects.create(user=self.user, name='Prof Teste', active=True)
        self.service = Service.objects.create(
            professional=self.professional,
            name='Corte',
            duration_minutes=30,
            price='50.00',
            active=True,
        )

    def test_appointment_status_update(self):
        from django.utils import timezone
        start = timezone.now() + timezone.timedelta(days=2)
        end = start + timezone.timedelta(minutes=30)
        appt = Appointment.objects.create(
            customer=self.customer,
            service=self.service,
            start_time=start,
            end_time=end,
            status=Appointment.Status.SCHEDULED,
        )
        # Update status to CF (Confirmado)
        response = self.client.get(reverse('appointment_status_update', args=[appt.pk, 'CF']))
        self.assertEqual(response.status_code, 302)
        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.Status.CONFIRMED)

    def test_availability_crud(self):
        from datetime import time
        from accounts.models import Availability
        # Create
        response = self.client.post(reverse('availability_create'), {
            'professional': self.professional.pk,
            'day_of_week': 0,
            'start_time': '09:00',
            'end_time': '18:00',
        })
        self.assertEqual(response.status_code, 302)
        av = Availability.objects.filter(professional=self.professional, day_of_week=0).first()
        self.assertIsNotNone(av)

        # List
        response = self.client.get(reverse('availabilities'))
        self.assertEqual(response.status_code, 200)

        # Delete
        response = self.client.post(reverse('availability_delete', args=[av.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Availability.objects.filter(pk=av.pk).exists())

    def test_available_slots_service_and_api(self):
        from datetime import date, time
        from accounts.models import Availability
        from accounts.services import get_available_slots

        target_date = date(2099, 1, 5)  # Monday (weekday = 0)
        Availability.objects.create(
            professional=self.professional,
            day_of_week=0,
            start_time=time(9, 0),
            end_time=time(11, 0),
        )

        slots = get_available_slots(self.professional, target_date, self.service)
        self.assertGreater(len(slots), 0)

        # Test API endpoint
        response = self.client.get(
            f"/api/professionals/{self.professional.pk}/available-slots/?date=2099-01-05&service={self.service.pk}"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["professional_id"], self.professional.pk)
        self.assertIn("slots", data)
        self.assertGreater(len(data["slots"]), 0)

    def test_swagger_and_schema_endpoints(self):
        schema_resp = self.client.get(reverse('schema'))
        self.assertEqual(schema_resp.status_code, 200)

        docs_resp = self.client.get(reverse('swagger-ui'))
        self.assertEqual(docs_resp.status_code, 200)

    def test_seed_data_command(self):
        from django.core.management import call_command
        call_command('seed_data')
        self.assertTrue(Professional.objects.count() >= 3)
        self.assertTrue(Service.objects.count() >= 8)
        self.assertTrue(Customer.objects.count() >= 6)
        self.assertTrue(Appointment.objects.count() >= 10)

