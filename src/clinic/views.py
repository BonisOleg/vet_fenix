from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_http_methods

from clinic.forms import ContactForm
from clinic.models import Advantage, Doctor, Service
from core.models import SiteSettings


def home(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'clinic/home.html',
        {
            'services': Service.objects.filter(is_active=True),
            'doctors': Doctor.objects.filter(is_active=True),
            'advantages': Advantage.objects.filter(is_active=True),
            'active_nav': 'home',
        },
    )


def services_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'clinic/services.html',
        {
            'services': Service.objects.filter(is_active=True),
            'active_nav': 'services',
        },
    )


def doctors_page(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        'clinic/doctors.html',
        {
            'doctors': Doctor.objects.filter(is_active=True),
            'active_nav': 'doctors',
        },
    )


@require_http_methods(['GET', 'POST'])
def contacts_page(request: HttpRequest) -> HttpResponse:
    site = SiteSettings.load()
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Дякуємо! Ми звʼяжемося з вами найближчим часом.')
        return redirect('clinic:contacts')
    return render(
        request,
        'clinic/contacts.html',
        {
            'form': form,
            'map_query': site.address,
            'active_nav': 'contacts',
        },
    )


@require_GET
def privacy_policy_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'clinic/privacy_policy.html')


@require_GET
def public_offer_page(request: HttpRequest) -> HttpResponse:
    return render(request, 'clinic/public_offer.html')


@require_GET
def service_detail_partial(request: HttpRequest, slug: str) -> HttpResponse:
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(
        request,
        'clinic/partials/service_detail.html',
        {'service': service},
    )
