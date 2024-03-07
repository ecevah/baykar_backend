from django.urls import path
from . import views
from django.urls import path, include

"""
untokenizer
http://127.0.0.1:8000 => Documents Page
http://127.0.0.1:8000/login => Login Api Url
http://127.0.0.1:8000/register => Register Api Url


/api/ == Customer Middleware
http://127.0.0.1:8000/api/ihas => All IHA List
http://127.0.0.1:8000/api/iha/find => Specific search with all features in iha table.
http://127.0.0.1:8000/api/customers => All Customer List
http://127.0.0.1:8000 => Documents Page

/v1/ == Admin Middleware


http://127.0.0.1:8000 => Documents Page
http://127.0.0.1:8000 => Documents Page
http://127.0.0.1:8000 => Documents Page
http://127.0.0.1:8000 => Documents Page
"""


urlpatterns = [
    path('', views.docs, name='documents'),

    path('api/ihas', views.get_ihas, name='get_ihas'),
    path('api/iha/find', views.get_specific_iha, name='get_specific_iha'),
    path('v1/iha/create', views.create_iha, name='iha_create'),
    path('v1/iha/delete/<int:iha_id>', views.delete_iha, name='iha_delete'),
    path('v1/iha/update/<int:iha_id>', views.update_iha, name='iha_update'),


    path('login', views.login_customer, name='login_customer'),
    path('register', views.create_customer, name='create_customer'),
    path('v1/customers', views.get_customers, name='get_customers'),
    path('api/customer/find', views.get_specific_customer, name='get_specific_customer'),
    path('api/delete/<int:customer_id>', views.delete_customer, name='delete_customer'),
    path('api/update/<int:customer_id>', views.update_customer, name='update_customer'),


    path('api/reservations', views.get_reservations, name='get_reservations'),
    path('api/reservation/create', views.create_reservation, name='reservation_create'),
    path('api/reservation/find', views.get_specific_reservation, name='get_specific_reservation'),
    path('v1/delete/<int:reservation_id>', views.delete_reservation, name='delete_reservation'),
    path('v1/update/<int:reservation_id>', views.update_reservation, name='update_reservation'),



]
