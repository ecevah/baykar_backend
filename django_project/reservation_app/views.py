from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.conf import settings
from django.shortcuts import render
import json
from datetime import datetime, timedelta
import jwt
from reservation_app.models import IHA, Customers, Reservations



def docs(request):
    return render(request, 'index.html')

"""
IHA
"""
@csrf_exempt
@require_http_methods(["POST"])
def create_iha(request):
    try:
        # JSON verisi artık request.POST üzerinden alınıyor
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        weight = request.POST.get('weight')
        category = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Dosya, request.FILES içinden alınıyor

        if not brand or not model or not weight or not category or not price:
            raise ValueError("All fields are required")

        iha = IHA(
            brand=brand,
            model=model,
            weight=weight,
            category=category,
            price=price
        )

        if image:
            iha.image.save(image.name, image)

        iha.save()

        response_data = {
            'status': True,
            'message': 'IHA creation successful.',
            'data': {
                'id': iha.id,
                'brand': iha.brand,
                'model': iha.model,
                'weight': iha.weight,
                'category': iha.category,
                'price': iha.price,
                'image_url': iha.image.url if iha.image else None,
            }
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_ihas(request):
    try:
        ihas = IHA.objects.all()
        iha_data = []

        for iha in ihas:
            iha_data.append({
                "brand": iha.brand,
                "model": iha.model,
                "weight": iha.weight,
                "category": iha.category,
                "price": iha.price
            })
        
        response_data = {
            'status': True,
            'message': 'Find successful.',
            'data': iha_data
        }

        return JsonResponse(response_data, safe= False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_specific_iha(request):
    try:
        ihas_query = IHA.objects.all()

        id = request.GET.get('id')
        brand = request.GET.get('brand')
        model = request.GET.get('model')
        weight = request.GET.get('weight')
        category = request.GET.get('category')
        price = request.GET.get('price')

        if id:
            ihas_query = ihas_query.filter(pk=id)
        if brand:
            ihas_query = ihas_query.filter(brand=brand)
        if model:
            ihas_query = ihas_query.filter(model=model)
        if weight:
            ihas_query = ihas_query.filter(weight=weight)
        if category:
            ihas_query = ihas_query.filter(category=category)
        if price:
            ihas_query = ihas_query.filter(price=price)

        iha_data = [{
            "id": iha.pk,
            "brand": iha.brand,
            "model": iha.model,
            "weight": iha.weight,
            "category": iha.category,
            "price": iha.price
        } for iha in ihas_query]

        response_data = {
            'status': True,
            'message': 'IHA information retrieved successfully.',
            'data': iha_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_iha(request, iha_id):
    try:
        iha = IHA.objects.get(id=iha_id)
        iha.delete()
        return JsonResponse({'status': True, 'message': f'IHA Deleted. ID={iha_id}'}, status=204)
    except IHA.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'IHA not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def update_iha(request, iha_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        iha = IHA.objects.get(id=iha_id)
        
        iha.brand = data.get('brand', iha.brand)
        iha.model = data.get('model', iha.model)
        iha.weight = data.get('weight', iha.weight)
        iha.category = data.get('category', iha.category)
        iha.price = data.get('price', iha.price)
        iha.save()
        
        updated_data = {
            'id': iha.id,
            'brand': iha.brand,
            'model': iha.model,
            'weight': iha.weight,
            'category': iha.category,
            'price': iha.price
        }

        response_data = {
            'status': True,
            'message': 'IHA updated successfully.',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except IHA.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'IHA not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Customer
"""
@csrf_exempt
@require_http_methods(["POST"])
def login_customer(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')

        if not username or not password:
            raise ValueError("Username and password are required")

        try:
            customer = Customers.objects.get(username=username)
        except Customers.DoesNotExist:
            raise ValueError("Invalid username or password")

        if not check_password(password, customer.password):
            raise ValueError("Invalid username or password")

        payload = {
            'user_id': customer.id,
            'username': customer.username,
            'exp': datetime.utcnow() + timedelta(days=1) 
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        response_data = {
            'status': True,
            'message': f'Login Succesful. Welcome {customer.name} :)',
            'data': {
                'id': customer.pk,
                'name': customer.name,
                'surname': customer.surname,
                'username': customer.username
            },
            'token': token
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }
        return JsonResponse(error_data, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create_customer(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        name = json_data.get('name')
        surname = json_data.get('surname')
        username = json_data.get('username')
        password = json_data.get('password')

        if not name or not surname or not username or not password:
            raise ValueError("All fields are required")

        if Customers.objects.filter(username=username).exists():
            raise ValueError("Username already exists")

        hashed_password = make_password(password)
        new_customer = Customers.objects.create(
            name=name,
            surname=surname,
            username=username,
            password=hashed_password
        )

        response_data = {
            'status': True,
            'message': 'Customer creation successful.',
            'data': {
                'id': new_customer.id,
                'name': new_customer.name,
                'surname': new_customer.surname,
                'username': new_customer.username,
            }
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }
        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_customers(request):
    try:
        customers = Customers.objects.all()
        customer_data = []

        for customer in customers:
            customer_data.append({
                "id": customer.pk,
                "name": customer.name,
                "surname": customer.surname,
                "username": customer.username,
            })

        response_data = {
            'status': True,
            'message': 'Find successful.',
            'data': customer_data
        }

        return JsonResponse(response_data, safe= False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_specific_customer(request):
    try:
        customers_query = Customers.objects.all()

        customer_id = request.GET.get('id')
        name = request.GET.get('name')
        surname = request.GET.get('surname')
        username = request.GET.get('username')

        if customer_id:
            customers_query = customers_query.filter(pk=customer_id)
        if name:
            customers_query = customers_query.filter(name=name)
        if surname:
            customers_query = customers_query.filter(surname=surname)
        if username:
            customers_query = customers_query.filter(username=username)

        customer_data = [{
            "id": customer.id,
            "name": customer.name,
            "surname": customer.surname,
            "username": customer.username
        } for customer in customers_query]

        response_data = {
            'status': True,
            'message': 'Customers retrieved successfully.',
            'data': customer_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_customer(request, customer_id):
    try:
        customer = Customers.objects.get(id=customer_id)
        customer.delete()
        return JsonResponse({'status': True, 'message': f'Customer Deleted. ID={customer_id}'}, status=204)
    except Customers.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Customer not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_customer(request, customer_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        customer = Customers.objects.get(id=customer_id)
        
        customer.name = data.get('name', customer.name)
        customer.surname = data.get('surname', customer.surname)
        customer.save()
        
        updated_data = {
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'username': customer.username,
        }

        response_data = {
            'status': True,
            'message': 'Customer updated successfully.',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except Customers.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Customer not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Reservation
"""
@csrf_exempt
@require_http_methods(["POST"])
def create_reservation(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        iha_id = json_data.get('iha_id')
        customer_id = json_data.get('customer_id')
        start_date_str = json_data.get('start_date')
        finish_date_str = json_data.get('finish_date')
        number = json_data.get('number')

        if not iha_id or not customer_id or not start_date_str or not finish_date_str:
            raise ValueError("IHA ID, Customer ID, Start Date, and Finish Date are required")

        iha = IHA.objects.get(pk=iha_id)
        customer = Customers.objects.get(pk=customer_id) 

        start_datetime = datetime.datetime.fromisoformat(start_date_str)
        finish_datetime = datetime.datetime.fromisoformat(finish_date_str)

        reservation_duration_hours = (finish_datetime - start_datetime).total_seconds() / 3600
        total_price = reservation_duration_hours * iha.price * number

        new_reservation = Reservations.objects.create(
            iha=iha,
            customer=customer, 
            start_date=start_datetime,
            finish_date=finish_datetime,
            total_price=total_price,
            number= number
        )

        response_data = {
            'status': True,
            'message': 'Reservation creation successful.',
            'data': {
                'id': new_reservation.id,
                'iha_id': new_reservation.iha.id,
                'customer_id': new_reservation.customer.id,
                'start_date': new_reservation.start_date.isoformat(),
                'finish_date': new_reservation.finish_date.isoformat(),
                'total_price': new_reservation.total_price,
                'number': new_reservation.number
            }
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_reservations(request):
    try:
        reservations = Reservations.objects.select_related('iha', 'customer').all()
        reservation_data = []

        for reservation in reservations:
            reservation_data.append({
                "iha_id": reservation.iha.id,
                "customer_id": reservation.customer.id,
                "start_date": str(reservation.start_date),
                "finish_date": str(reservation.finish_date),
                "total_price": reservation.total_price
            })

        response_data = {
            'status': True,
            'message': 'Find successful.',
            'data': reservation_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@require_http_methods(["GET"])
def get_specific_reservation(request):
    try:
        reservations_query = Reservations.objects.select_related('iha', 'customer')

        reservation_id = request.GET.get('reservation_id')
        start_date_from = request.GET.get('start_date_from')
        start_date_to = request.GET.get('start_date_to')
        iha_brand = request.GET.get('iha_brand')
        iha_model = request.GET.get('iha_model')
        customer_name = request.GET.get('customer_name')
        customer_surname = request.GET.get('customer_surname')
        customer_username = request.GET.get('customer_username')

        if reservation_id:
            reservations_query = reservations_query.filter(pk=reservation_id)
        if start_date_from:
            reservations_query = reservations_query.filter(start_date__gte=start_date_from)
        if start_date_to:
            reservations_query = reservations_query.filter(start_date__lte=start_date_to)
        if iha_brand:
            reservations_query = reservations_query.filter(iha__brand=iha_brand)
        if iha_model:
            reservations_query = reservations_query.filter(iha__model=iha_model)
        if customer_name:
            reservations_query = reservations_query.filter(customer__name=customer_name)
        if customer_surname:
            reservations_query = reservations_query.filter(customer__surname=customer_surname)
        if customer_username:
            reservations_query = reservations_query.filter(customer__username=customer_username)

        reservations_data = [{
            "reservation_id": reservation.id,
            "iha": {
                "brand": reservation.iha.brand,
                "model": reservation.iha.model,
                "category": reservation.iha.category,
                "price": reservation.iha.price
            },
            "customer": {
                "name": reservation.customer.name,
                "surname": reservation.customer.surname,
                "username": reservation.customer.username,
            },
            "start_date": reservation.start_date.isoformat(),
            "finish_date": reservation.finish_date.isoformat(),
            "total_price": reservation.total_price,
        } for reservation in reservations_query]

        response_data = {
            'status': True,
            'message': 'Reservations retrieved successfully.',
            'data': reservations_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

@csrf_exempt
@require_http_methods(["Delete"])
def delete_reservation(request, reservation_id):
    try:
        reservation = Reservations.objects.get(id=reservation_id)
        reservation.delete()
        return JsonResponse({'status': True, 'message': f'Reservation Deleted. ID={reservation_id}'}, status=204)
    except Reservations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Reservation not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["PUT"])
def update_reservation(request, reservation_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        reservation = Reservations.objects.get(id=reservation_id)
        
        start_date_str = data.get('start_date')
        finish_date_str = data.get('finish_date')
        if start_date_str:
            reservation.start_date = datetime.datetime.fromisoformat(start_date_str)
        if finish_date_str:
            reservation.finish_date = datetime.datetime.fromisoformat(finish_date_str)

        if 'total_price' in data:
            reservation.total_price = data['total_price']

        reservation.clean()
        reservation.save()
        
        updated_data = {
            'id': reservation.id,
            'iha_id': reservation.iha.id,
            'customer_id': reservation.customer.id,
            'start_date': reservation.start_date.isoformat(),
            'finish_date': reservation.finish_date.isoformat(),
            'total_price': reservation.total_price,
        }

        response_data = {
            'status': True,
            'message': 'Reservation updated successfully.',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except Reservations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Reservation not found.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'status': False, 'message': str(e.messages)}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Admin Login
"""

@csrf_exempt
@require_http_methods(["POST"])
def login_admin(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')

        if not username or not password:
            raise ValueError("Username and password are required")

        if password != 'admin' and username != 'admin':
            raise ValueError("Invalid username or password")

        payload = {
            'message': 'Welcome Boss !',
            'exp': datetime.utcnow() + timedelta(days=1) 
        }
        token = jwt.encode(payload, settings.SECRET_KEY_ADMIN, algorithm='HS256')

        response_data = {
            'status': True,
            'message': f'Login Succesful. Welcome Boss :)',
            'data': {
                'name': 'Ahmet',
                'surname': 'Ecevit',
                'username': 'eecevah'
            },
            'token': token
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }
        return JsonResponse(error_data, status=400)
