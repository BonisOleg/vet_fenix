from django.urls import path

from clinic import views

app_name = 'clinic'

urlpatterns = [
    path('', views.home, name='home'),
    path('poslugy/', views.services_page, name='services'),
    path('poslugy/<slug:slug>/', views.service_detail_partial, name='service_detail'),
    path('likari/', views.doctors_page, name='doctors'),
    path('kontakty/', views.contacts_page, name='contacts'),
    path('polityka-konfidentsijnosti/', views.privacy_policy_page, name='privacy_policy'),
    path('dogovir-publichnoi-oferty/', views.public_offer_page, name='public_offer'),
]
