from django.urls import path
from . import views

urlpatterns = [
    path('ihas', views.get_ihas, name='get_ihas'),
    path('customers', views.get_customers, name='get_customers'),
    path('reservations', views.get_reservations, name='get_reservations'),
    path('iha/create', views.create_iha, name='iha_create'),
    path('customer/create', views.create_customer, name='customer_create'),
    path('reservation/create', views.create_reservation, name='reservation_create'),
]
