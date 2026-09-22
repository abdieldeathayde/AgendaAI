from datetime import date, datetime, time, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import (
    Appointment,
    Availability,
    Customer,
    Professional,
    Service,
)
from users.models import User


PROFESSIONALS = [
    {
        "username": "lucas.barber",
        "name": "Lucas Martins",
        "email": "lucas.demo@agendaai.local",
        "phone": "(47) 99111-1001",
        "specialty": "Barbearia e visagismo masculino",
        "bio": "Especialista em degradê, barba e visagismo facial.",
        "services": [
            ("Corte Fade", "Corte moderno com acabamento na navalha.", 45, "55.00"),
            ("Barba Premium", "Barba com toalha quente e finalização.", 30, "40.00"),
            ("Combo Corte + Barba", "Corte completo mais barba premium.", 75, "90.00"),
        ],
    },
    {
        "username": "amanda.silva",
        "name": "Amanda Silva",
        "email": "amanda.demo@agendaai.local",
        "phone": "(47) 99222-2002",
        "specialty": "Cabelos, colorimetria e tratamentos",
        "bio": "Especialista em cortes femininos, coloração e tratamentos capilares.",
        "services": [
            ("Corte Feminino + Escova", "Corte personalizado com escova.", 60, "120.00"),
            ("Hidratação Profunda", "Tratamento intensivo para recuperação dos fios.", 45, "95.00"),
            ("Coloração Global", "Coloração completa com avaliação.", 90, "180.00"),
        ],
    },
    {
        "username": "rodrigo.visagista",
        "name": "Rodrigo Oliveira",
        "email": "rodrigo.demo@agendaai.local",
        "phone": "(47) 99333-3003",
        "specialty": "Visagismo e design de barba",
        "bio": "Consultoria de imagem e desenho de barba personalizado.",
        "services": [
            ("Consultoria de Visagismo", "Análise de formato de rosto e estilo.", 60, "90.00"),
            ("Design de Barba", "Alinhamento, desenho e pigmentação opcional.", 40, "50.00"),
            ("Corte Executivo", "Corte clássico com acabamento premium.", 45, "70.00"),
        ],
    },
    {
        "username": "juliana.estetica",
        "name": "Juliana Costa",
        "email": "juliana.demo@agendaai.local",
        "phone": "(47) 99444-4004",
        "specialty": "Estética facial e corporal",
        "bio": "Atendimento de estética facial com foco em bem-estar e cuidados da pele.",
        "services": [
            ("Limpeza de Pele", "Higienização e cuidados faciais.", 60, "110.00"),
            ("Design de Sobrancelhas", "Modelagem e acabamento.", 30, "45.00"),
            ("Massagem Relaxante", "Sessão de relaxamento corporal.", 60, "100.00"),
        ],
    },
    {
        "username": "marcos.terapeuta",
        "name": "Marcos Almeida",
        "email": "marcos.demo@agendaai.local",
        "phone": "(47) 99555-5005",
        "specialty": "Massoterapia e bem-estar",
        "bio": "Atendimento focado em relaxamento e bem-estar.",
        "services": [
            ("Massagem Relaxante", "Sessão de 60 minutos.", 60, "100.00"),
            ("Massagem Desportiva", "Atendimento para recuperação muscular.", 60, "130.00"),
            ("Drenagem Corporal", "Sessão de drenagem e bem-estar.", 50, "115.00"),
        ],
    },
]

CUSTOMERS = [
    ("carlos.silva", "Carlos Silva", "carlos.demo@agendaai.local", "(47) 99101-0101"),
    ("beatriz.souza", "Beatriz Souza", "beatriz.demo@agendaai.local", "(47) 99202-0202"),
    ("fernando.lima", "Fernando Lima", "fernando.demo@agendaai.local", "(47) 99303-0303"),
    ("mariana.alves", "Mariana Alves", "mariana.demo@agendaai.local", "(47) 99404-0404"),
    ("juliana.rocha", "Juliana Rocha", "juliana.rocha.demo@agendaai.local", "(47) 99505-0505"),
    ("gabriel.mendes", "Gabriel Mendes", "gabriel.demo@agendaai.local", "(47) 99606-0606"),
    ("ana.costa", "Ana Costa", "ana.demo@agendaai.local", "(47) 99707-0707"),
    ("pedro.santos", "Pedro Santos", "pedro.demo@agendaai.local", "(47) 99808-0808"),
    ("camila.nunes", "Camila Nunes", "camila.demo@agendaai.local", "(47) 99909-0909"),
    ("rafael.moura", "Rafael Moura", "rafael.demo@agendaai.local", "(47) 99010-1010"),
    ("larissa.fernandes", "Larissa Fernandes", "larissa.demo@agendaai.local", "(47) 99111-1111"),
    ("thiago.pereira", "Thiago Pereira", "thiago.demo@agendaai.local", "(47) 99212-1212"),
]


class Command(BaseCommand):
    help = "Cria uma base completa e fictícia para demonstração do AgendaAI."

    @staticmethod
    def _availability_slots(professional, day, service):
        slots = []
        duration = timedelta(minutes=service.duration_minutes)
        for availability in Availability.objects.filter(
            professional=professional,
            day_of_week=day.weekday(),
        ).order_by("start_time"):
            start_dt = timezone.make_aware(datetime.combine(day, availability.start_time))
            end_dt = timezone.make_aware(datetime.combine(day, availability.end_time))
            cursor = start_dt
            while cursor + duration <= end_dt:
                slots.append(cursor)
                cursor += timedelta(minutes=30)
        return slots

    @staticmethod
    def _has_conflict(professional, start_time, end_time, exclude_id=None):
        return Appointment.objects.filter(
            service__professional=professional,
            status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED],
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exclude(pk=exclude_id or -1).exists()

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Apaga os dados de demonstração antes de recriá-los.",
        )
        parser.add_argument(
            "--password",
            default="Demo@12345",
            help="Senha dos usuários de demonstração.",
        )
        parser.add_argument(
            "--admin-password",
            default="Admin@12345",
            help="Senha do usuário administrador.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        password = options["password"]
        admin_password = options["admin_password"]

        if options["reset"]:
            Appointment.objects.all().delete()
            Availability.objects.all().delete()
            Service.objects.all().delete()
            Professional.objects.all().delete()
            Customer.objects.all().delete()
            User.objects.filter(username__startswith="demo.").delete()
            User.objects.filter(username__in=[
                "lucas.barber", "amanda.silva", "rodrigo.visagista",
                "juliana.estetica", "marcos.terapeuta", "agenda.admin",
            ]).delete()
            self.stdout.write(self.style.WARNING("Dados de demonstração anteriores removidos."))

        admin = self._user(
            "agenda.admin",
            "Administrador",
            "AgendaAI",
            "admin@agendaai.local",
            admin_password,
            is_staff=True,
            is_superuser=True,
            is_customer=False,
        )

        professionals = []
        services = []

        for data in PROFESSIONALS:
            user = self._user(
                data["username"],
                *data["name"].split(maxsplit=1),
                data["email"],
                password,
                is_customer=False,
                is_professional=True,
                phone=data["phone"],
            )
            professional, _ = Professional.objects.update_or_create(
                user=user,
                defaults={
                    "name": data["name"],
                    "specialty": data["specialty"],
                    "bio": data["bio"],
                    "active": True,
                },
            )
            professionals.append(professional)

            for weekday in range(5):
                Availability.objects.update_or_create(
                    professional=professional,
                    day_of_week=weekday,
                    defaults={"start_time": time(9, 0), "end_time": time(18, 0)},
                )
            Availability.objects.update_or_create(
                professional=professional,
                day_of_week=5,
                defaults={"start_time": time(9, 0), "end_time": time(13, 0)},
            )

            for name, description, duration, price in data["services"]:
                service, _ = Service.objects.update_or_create(
                    professional=professional,
                    name=name,
                    defaults={
                        "description": description,
                        "duration_minutes": duration,
                        "price": Decimal(price),
                        "active": True,
                    },
                )
                services.append(service)

        customers = []
        for username, name, email, phone in CUSTOMERS:
            first, *rest = name.split()
            user = self._user(
                username,
                first,
                " ".join(rest) or "Demo",
                email,
                password,
                is_customer=True,
                is_professional=False,
                phone=phone,
            )
            customer, _ = Customer.objects.update_or_create(
                user=user,
                defaults={"name": name, "phone": phone},
            )
            customers.append(customer)

        # Recria os agendamentos para que a base seja sempre previsível.
        Appointment.objects.all().delete()

        now = timezone.localtime(timezone.now())
        today = now.date()

        # Histórico: 6 semanas de atendimentos concluídos/cancelados.
        historical_created = 0
        for days_ago in range(1, 43):
            day = today - timedelta(days=days_ago)
            if day.weekday() == 6:
                continue

            for pro_index, professional in enumerate(professionals):
                if (days_ago + pro_index) % 2:
                    continue

                pro_services = list(
                    Service.objects.filter(professional=professional, active=True)
                )
                if not pro_services:
                    continue

                service = pro_services[(days_ago + pro_index) % len(pro_services)]
                customer = customers[(days_ago * 2 + pro_index) % len(customers)]
                slot_candidates = self._availability_slots(professional, day, service)
                if not slot_candidates:
                    continue

                chosen_start = None
                for candidate in slot_candidates:
                    if not self._has_conflict(professional, candidate, candidate + timedelta(minutes=service.duration_minutes)):
                        chosen_start = candidate
                        break

                if chosen_start is None:
                    continue

                end = chosen_start + timedelta(minutes=service.duration_minutes)
                status = (
                    Appointment.Status.CANCELLED
                    if days_ago % 13 == 0
                    else Appointment.Status.COMPLETED
                )

                Appointment.objects.create(
                    customer=customer,
                    service=service,
                    start_time=chosen_start,
                    end_time=end,
                    status=status,
                    price=service.price,
                    notes="Dado fictício criado automaticamente para demonstração.",
                )
                historical_created += 1

        # Hoje: mistura de concluídos, confirmados e agendados.
        today_services = [s for s in services if s.professional_id in {p.id for p in professionals}]
        for index, service in enumerate(today_services[:4]):
            slot_candidates = self._availability_slots(service.professional, today, service)
            chosen_start = None
            for candidate in slot_candidates:
                if not self._has_conflict(service.professional, candidate, candidate + timedelta(minutes=service.duration_minutes)):
                    chosen_start = candidate
                    break
            if chosen_start is None:
                continue

            end = chosen_start + timedelta(minutes=service.duration_minutes)
            Appointment.objects.create(
                customer=customers[index],
                service=service,
                start_time=chosen_start,
                end_time=end,
                status=[
                    Appointment.Status.COMPLETED,
                    Appointment.Status.CONFIRMED,
                    Appointment.Status.SCHEDULED,
                    Appointment.Status.CANCELLED,
                ][index],
                price=service.price,
                notes="Atendimento de demonstração do dia.",
            )

        # Agenda futura: 14 dias úteis, com até 2 horários por profissional/dia.
        future_created = 0
        for days_ahead in range(1, 15):
            day = today + timedelta(days=days_ahead)
            if day.weekday() == 6:
                continue

            for pro_index, professional in enumerate(professionals):
                pro_services = list(
                    Service.objects.filter(professional=professional, active=True)
                )
                if not pro_services:
                    continue

                for slot_index in range(2):
                    service = pro_services[(days_ahead + slot_index) % len(pro_services)]
                    customer = customers[
                        (days_ahead * 3 + pro_index + slot_index) % len(customers)
                    ]
                    slot_candidates = self._availability_slots(professional, day, service)
                    chosen_start = None
                    for candidate in slot_candidates:
                        if not self._has_conflict(professional, candidate, candidate + timedelta(minutes=service.duration_minutes)):
                            chosen_start = candidate
                            break
                    if chosen_start is None:
                        continue

                    end = chosen_start + timedelta(minutes=service.duration_minutes)
                    Appointment.objects.create(
                        customer=customer,
                        service=service,
                        start_time=chosen_start,
                        end_time=end,
                        status=(
                            Appointment.Status.CONFIRMED
                            if (days_ahead + pro_index) % 3 == 0
                            else Appointment.Status.SCHEDULED
                        ),
                        price=service.price,
                        notes="Agendamento futuro fictício para demonstração.",
                    )
                    future_created += 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("AgendaAI populado com dados fictícios."))
        self.stdout.write(f"Administrador: agenda.admin / {admin_password}")
        self.stdout.write(f"Profissionais: {len(professionals)}")
        self.stdout.write(f"Serviços: {len(services)}")
        self.stdout.write(f"Clientes: {len(customers)}")
        self.stdout.write(
            f"Agendamentos: {Appointment.objects.count()} "
            f"(histórico={historical_created}, futuros={future_created})"
        )
        self.stdout.write(
            self.style.NOTICE(
                "Usuários de demonstração usam a senha informada em --password."
            )
        )

    @staticmethod
    def _user(
        username,
        first_name,
        last_name,
        email,
        password,
        **extra,
    ):
        defaults = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            **extra,
        }
        user, _ = User.objects.get_or_create(username=username, defaults=defaults)

        changed = False
        for key, value in defaults.items():
            if getattr(user, key) != value:
                setattr(user, key, value)
                changed = True
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
