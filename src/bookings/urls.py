from django.urls import path

from bookings import views

app_name = 'bookings'

urlpatterns = [
    path('', views.booking_page, name='booking'),
    path('submit/', views.booking_submit, name='booking_submit'),
    path('callback/', views.callback_submit, name='callback_submit'),
]
