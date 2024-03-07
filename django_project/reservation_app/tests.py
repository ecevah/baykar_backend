from django.test import TestCase
from django.urls import reverse
from reservation_app.models import IHA, Customers, Reservations
from django.contrib.auth.hashers import make_password
import json
from datetime import datetime

class IhaTestCase(TestCase):
    def setUp(self):
        # Örnek IHA oluşturma
        IHA.objects.create(brand="DJI", model="Phantom", weight=1.2, category="Hobby", price=1000)

    def test_create_iha(self):
        url = reverse('iha_create')
        data = {
            'brand': 'DJI',
            'model': 'Mavic',
            'weight': '0.5',
            'category': 'Professional',
            'price': '1500'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_get_ihas(self):
        url = reverse('get_ihas')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)  # Setup'ta oluşturulan IHA'nın kontrolü

    def test_get_specific_iha(self):
        url = reverse('get_specific_iha') + '?brand=DJI'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json()['data']) > 0)

    def test_delete_iha(self):
        iha = IHA.objects.get(brand="DJI")
        url = reverse('iha_delete', kwargs={'iha_id': iha.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

class CustomerTestCase(TestCase):
    def setUp(self):
        # Örnek müşteri oluşturma
        hashed_password = make_password('12345')
        Customers.objects.create(name="John", surname="Doe", username="johndoe", password=hashed_password)

    def test_create_customer(self):
        url = reverse('create_customer')
        data = {
            'name': 'Jane',
            'surname': 'Doe',
            'username': 'janedoe',
            'password': '54321'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_login_customer(self):
        url = reverse('login_customer')
        data = {
            'username': 'johndoe',
            'password': '12345'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

# Benzer şekilde Rezervasyonlar ve diğer işlemler için de test caseleri yazılabilir.

# Lütfen dikkat edin, bu test örnekleri temel senaryoları kapsamaktadır.
# Gerçek bir projede, daha kapsamlı ve detaylı test caseleri yazmanız gerekebilir.
