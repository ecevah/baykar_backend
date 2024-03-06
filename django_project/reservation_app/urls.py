from django.urls import path
from . import views

urlpatterns = [

    path('ihas', views.get_ihas, name='get_ihas'),
    path('iha/create', views.create_iha, name='iha_create'),
    path('iha/find', views.get_specific_iha, name='get_specific_iha'),


    path('customers', views.get_customers, name='get_customers'),
    path('customer/create', views.create_customer, name='customer_create'),
    path('customer/find', views.get_specific_customer, name='get_specific_customer'),


    path('reservations', views.get_reservations, name='get_reservations'),
    path('reservation/create', views.create_reservation, name='reservation_create'),
    path('reservation/find', views.get_specific_reservation, name='get_specific_reservation'),
]
