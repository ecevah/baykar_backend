from django.urls import path
from . import views
from . import rest_views
from django.urls import path

"""
untokenizer
http://127.0.0.1:8000 => Documents Page
http://127.0.0.1:8000/login => Login Api Url
http://127.0.0.1:8000/register => Register Api Url


/api/ == Customer Middleware
http://127.0.0.1:8000/api/ihas => All IHA List
http://127.0.0.1:8000/api/iha/find => Specific search with all features in iha table.
http://127.0.0.1:8000/api/customers => All Customer List
http://127.0.0.1:8000/api/customers/find => Specific search with all features in iha table.
http://127.0.0.1:8000/api/customers/delete/<id> => ID of customer to delete
http://127.0.0.1:8000/api/customers/update/<id> => ID of customer to update
http://127.0.0.1:8000/api/reservations => All Reservations List
http://127.0.0.1:8000/api/reservation/create => Create reservation
http://127.0.0.1:8000/api/reservations/find => Specific search with all features in iha table.
http://127.0.0.1:8000/api/reservations/delete/<id> => ID of reservation to delete
http://127.0.0.1:8000/api/reservations/update/<id> => ID of reservation to update


http://127.0.0.1:8000/api/verify => Check Token



/v1/ == Admin Middleware

"""


urlpatterns = [

    #REST FRAMEWORK
    path('iha', rest_views.IHAListCreateView.as_view(), name='iha-list-create'),
    path('iha/<int:pk>', rest_views.IHARetrieveUpdateDestroyView.as_view(), name='iha-detail'),

    path('customers', rest_views.CustomerListCreateView.as_view(), name='customer-list-create'),
    path('customers/<int:pk>', rest_views.CustomerRetrieveUpdateDestroyView.as_view(), name='customer-detail'),

    path('reservations', rest_views.ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>', rest_views.ReservationRetrieveUpdateDestroyView.as_view(), name='reservation-detail'),

    path('register', rest_views.CustomerRegisterView.as_view(), name='customer-register'),
    path('login', rest_views.CustomerLoginView.as_view(), name='customer-login'),
    path('customer/list', rest_views.CustomerListView.as_view(), name='customer-list'),
    path('reservation/create', rest_views.CreateReservationView.as_view(), name='create-reservation'),


    #Django REST API
    path('', views.docs, name='documents'),

    path('api/verify', views.get_verify, name='get_verify'),

    path('api/ihas', views.get_ihas, name='get_ihas'),
    path('api/iha/find', views.get_specific_iha, name='get_specific_iha'),
    path('v1/iha/create', views.create_iha, name='iha_create'),
    path('v1/iha/delete/<int:iha_id>', views.delete_iha, name='iha_delete'),
    path('v1/iha/update/<int:iha_id>', views.update_iha, name='iha_update'),


    path('login', views.login_customer, name='login_customer'),
    path('register', views.create_customer, name='create_customer'),
    path('v1/customers', views.get_customers, name='get_customers'),
    path('api/customer/find', views.get_specific_customer, name='get_specific_customer'),
    path('api/customer/delete/<int:customer_id>', views.delete_customer, name='delete_customer'),
    path('api/customer/update/<int:customer_id>', views.update_customer, name='update_customer'),


    path('api/reservations', views.get_reservations, name='get_reservations'),
    path('api/reservation/create', views.create_reservation, name='reservation_create'),
    path('api/reservation/find', views.get_specific_reservation, name='get_specific_reservation'),
    path('api/reservation/delete/<int:reservation_id>', views.delete_reservation, name='delete_reservation'),
    path('v1/reservation/update/<int:reservation_id>', views.update_reservation, name='update_reservation'),
]
