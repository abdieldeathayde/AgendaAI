from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render
from django.utils import timezone

from accounts.models import Appointment, Customer, Professional, Service


@login_required
def dashboard(request):
    today = timezone.localdate()
    now = timezone.now()
    period_filter = request.GET.get("period", "30")

    try:
        period_days = max(1, min(int(period_filter), 365))
    except (TypeError, ValueError):
        period_days = 30

    period_start = today - timedelta(days=period_days - 1)
    period_appointments = Appointment.objects.filter(start_time__date__gte=period_start)

    revenue_expression = Sum("price")
    period_total_appointments = period_appointments.count()
    period_revenue = period_appointments.filter(status=Appointment.Status.COMPLETED).aggregate(
        total=revenue_expression
    )["total"] or 0

    total_customers = Customer.objects.count()
    total_professionals = Professional.objects.filter(active=True).count()
    total_services = Service.objects.filter(active=True).count()
    total_appointments = Appointment.objects.count()

    recent_appointments = Appointment.objects.select_related(
        "customer", "service", "service__professional"
    ).order_by("-start_time")[:5]

    status_counts = dict(
        Appointment.objects.values("status").annotate(total=Count("id")).values_list("status", "total")
    )
    confirmed_appointments = status_counts.get(Appointment.Status.CONFIRMED, 0)
    completed_appointments = status_counts.get(Appointment.Status.COMPLETED, 0)
    scheduled_appointments = status_counts.get(Appointment.Status.SCHEDULED, 0)

    revenue = Appointment.objects.filter(status=Appointment.Status.COMPLETED).aggregate(
        total=Sum("price")
    )["total"] or 0

    today_queryset = Appointment.objects.filter(start_time__date=today)
    today_appointments = today_queryset.count()
    today_revenue = today_queryset.filter(status=Appointment.Status.COMPLETED).aggregate(
        total=Sum("price")
    )["total"] or 0

    upcoming_appointments = Appointment.objects.filter(
        start_time__gte=now,
        status__in=[Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED],
    ).select_related("customer", "service", "service__professional").order_by("start_time")[:5]

    top_services = list(
        Appointment.objects.values("service__name")
        .annotate(total_appointments=Count("id"))
        .order_by("-total_appointments", "service__name")[:3]
    )
    for item in top_services:
        item["name"] = item.pop("service__name")

    top_professionals = list(
        Appointment.objects.values("service__professional__name")
        .annotate(total_appointments=Count("id"))
        .order_by("-total_appointments", "service__professional__name")[:3]
    )
    for item in top_professionals:
        item["name"] = item.pop("service__professional__name")

    trend_data = []
    for offset in range(period_days):
        current_date = period_start + timedelta(days=offset)
        daily = Appointment.objects.filter(start_time__date=current_date)
        trend_data.append({
            "date": current_date.strftime("%d/%m"),
            "appointments": daily.count(),
            "revenue": daily.filter(status=Appointment.Status.COMPLETED).aggregate(total=Sum("price"))["total"] or 0,
        })

    return render(request, "users/dashboard.html", {
        "title": "Dashboard",
        "user": request.user,
        "total_customers": total_customers,
        "total_professionals": total_professionals,
        "total_services": total_services,
        "total_appointments": total_appointments,
        "confirmed_appointments": confirmed_appointments,
        "completed_appointments": completed_appointments,
        "scheduled_appointments": scheduled_appointments,
        "revenue": revenue,
        "today_appointments": today_appointments,
        "today_revenue": today_revenue,
        "upcoming_appointments": upcoming_appointments,
        "recent_appointments": recent_appointments,
        "top_services": top_services,
        "top_professionals": top_professionals,
        "period_filter": str(period_days),
        "period_days": period_days,
        "period_start": period_start,
        "period_total_appointments": period_total_appointments,
        "period_revenue": period_revenue,
        "trend_data": trend_data,
    })


@login_required
def reports(request):
    statuses = []
    for status_value, status_label in Appointment.Status.choices:
        count = Appointment.objects.filter(status=status_value).count()
        statuses.append({"label": status_label, "value": count, "code": status_value})

    professionals = (
        Appointment.objects.values("service__professional__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    services = (
        Appointment.objects.values("service__name")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    return render(request, "users/reports.html", {
        "title": "Relatórios",
        "revenue_by_status": statuses,
        "top_professionals": professionals,
        "top_services": services,
    })


@login_required
def finance(request):
    today = timezone.localdate()
    monthly_revenue = []

    for offset in range(6):
        month_index = today.year * 12 + (today.month - 1) - offset
        target_year, target_month = divmod(month_index, 12)
        month_start = date(target_year, target_month + 1, 1)
        next_month = date(target_year + 1, 1, 1) if target_month == 11 else date(target_year, target_month + 2, 1)
        month_end = next_month - timedelta(days=1)

        month_total = Appointment.objects.filter(
            status=Appointment.Status.COMPLETED,
            start_time__date__gte=month_start,
            start_time__date__lte=month_end,
        ).aggregate(total=Sum("price"))["total"] or 0

        monthly_revenue.append({"label": month_start.strftime("%b/%Y"), "value": month_total})

    monthly_revenue.reverse()

    upcoming_revenue = Appointment.objects.filter(
        status=Appointment.Status.CONFIRMED,
        start_time__gte=timezone.now(),
    ).aggregate(total=Sum("price"))["total"] or 0

    return render(request, "users/finance.html", {
        "title": "Financeiro",
        "monthly_revenue": monthly_revenue,
        "upcoming_revenue": upcoming_revenue,
    })
