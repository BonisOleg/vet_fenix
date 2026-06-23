from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from bookings.forms import AppointmentForm, CallbackLeadForm
from clinic.models import Doctor, Service


def _prefill_form(request: HttpRequest, form: AppointmentForm) -> AppointmentForm:
    service_slug = request.GET.get('service')
    doctor_slug = request.GET.get('doctor')
    initial = {}
    if service_slug:
        try:
            initial['service'] = Service.objects.get(slug=service_slug, is_active=True).pk
        except Service.DoesNotExist:
            pass
    if doctor_slug:
        try:
            initial['doctor'] = Doctor.objects.get(slug=doctor_slug, is_active=True).pk
        except Doctor.DoesNotExist:
            pass
    if initial and not form.is_bound:
        return AppointmentForm(initial=initial)
    return form


@require_http_methods(['GET'])
def booking_page(request: HttpRequest) -> HttpResponse:
    form = _prefill_form(request, AppointmentForm())
    return render(
        request,
        'bookings/booking.html',
        {'form': form, 'active_nav': 'booking'},
    )


@require_http_methods(['POST'])
def booking_submit(request: HttpRequest) -> HttpResponse:
    form = AppointmentForm(request.POST)
    if form.is_valid():
        appointment = form.save(commit=False)
        appointment.source_page = 'booking'
        appointment.save()
        return render(
            request,
            'bookings/partials/success.html',
            {'appointment': appointment},
        )
    return render(
        request,
        'bookings/partials/form.html',
        {'form': form},
        status=422,
    )


@require_http_methods(['POST'])
def callback_submit(request: HttpRequest) -> HttpResponse:
    form = CallbackLeadForm(request.POST)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.source_page = request.path[:64]
        lead.save()
        return render(
            request,
            'bookings/partials/callback_success.html',
            {'lead': lead},
        )
    return render(
        request,
        'bookings/partials/callback_form.html',
        {'form': form},
        status=422,
    )
