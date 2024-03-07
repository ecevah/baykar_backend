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



# Render the documentation page.
def docs(request):
    return render(request, 'index.html')

"""
IHA Operations
"""
# IHA creation function. It receives the data received via the POST method and saves a new IHA.
@csrf_exempt
@require_http_methods(["POST"])
def create_iha(request):
    try:
        # Get IHA information from POST data
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        weight = request.POST.get('weight')
        category = request.POST.get('category')
        price = request.POST.get('price')
        image = request.FILES.get('image')  # Get the image that comes as a file

        # Make sure all fields are filled in
        if not brand or not model or not weight or not category or not price:
            raise ValueError("Tüm alanlar doldurulmalıdır.")

        # Create new IHA object and save to database
        iha = IHA(
            brand=brand,
            model=model,
            weight=weight,
            category=category,
            price=price
        )

        # If there is an image, save it
        if image:
            iha.image.save(image.name, image)

        iha.save()

        # Return successful response
        response_data = {
            'status': True,
            'message': 'IHA created successfully',
            'data': {
                'id': iha.id,
                'brand': iha.brand,
                'model': iha.model,
                'weight': iha.weight,
                'category': iha.category,
                'price': iha.price,
                'image_url': iha.image.url if iha.image else None,  # If there is an image, return its URL
            }
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        # Return error message in case of error
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to list all IHAs.
@require_http_methods(["GET"])
def get_ihas(request):
    try:
        ihas = IHA.objects.all()  # Get all IHA records
        iha_data = []

        # Add information for each IHA to a list
        for iha in ihas:
            iha_data.append({
                "id": iha.pk,
                "brand": iha.brand,
                "model": iha.model,
                "weight": iha.weight,
                "category": iha.category,
                "price": iha.price,
                'image_url': iha.image.url if iha.image else None  # Görsel varsa URL'ini ekle
            })
        
        # Return successful response
        response_data = {
            'status': True,
            'message': 'IHA successful response.',
            'data': iha_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        # Return error message in case of error
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to search for a specific IHA. It filters with query parameters.
@require_http_methods(["GET"])
def get_specific_iha(request):
    try:
        ihas_query = IHA.objects.all()

        # Get query parameters
        id = request.GET.get('id')
        brand = request.GET.get('brand')
        model = request.GET.get('model')
        weight = request.GET.get('weight')
        category = request.GET.get('category')
        price = request.GET.get('price')

        # Filtering operations
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

        # Add IHA information to a list via filtered results
        iha_data = [{
            "id": iha.pk,
            "brand": iha.brand,
            "model": iha.model,
            "weight": iha.weight,
            "category": iha.category,
            "price": iha.price,
            'image_url': iha.image.url if iha.image else None
        } for iha in ihas_query]

        # Return successful response
        response_data = {
            'status': True,
            'message': 'IHA find complated.',
            'data': iha_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        # Return error message in case of error
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to delete a specific IHA. Deletes a specific IHA record by IHA ID.
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_iha(request, iha_id):
    try:
        iha = IHA.objects.get(id=iha_id)  # Get specific IHA by ID
        iha.delete()  # IHA deleted 
        # Return successful response
        return JsonResponse({'status': True, 'message': f'IHA Deleted. ID={iha_id}'}, status=204)
    except IHA.DoesNotExist:
        # Return error message if IHA is not found
        return JsonResponse({'status': False, 'message': 'IHA bulunamadı.'}, status=404)
    except Exception as e:
        # Return error message in case of general error
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

# Function to update a specific IHA. Updates IHA information.
@csrf_exempt
@require_http_methods(["POST"])
def update_iha(request, iha_id):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Get JSON data from request body and parse it
        iha = IHA.objects.get(id=iha_id)  # Get the IHA to be updated by ID
        
        # Update IHA information based on received data
        iha.brand = data.get('brand', iha.brand)
        iha.model = data.get('model', iha.model)
        iha.weight = data.get('weight', iha.weight)
        iha.category = data.get('category', iha.category)
        iha.price = data.get('price', iha.price)
        iha.save()  # Save updated IHA
        
        # Return reply with updated IHA information
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
            'message': 'IHA updated.',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except IHA.DoesNotExist:
        # Return error message if IHA is not found
        return JsonResponse({'status': False, 'message': 'IHA bulunamadı.'}, status=404)
    except Exception as e:
        # Return error message in case of general error
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Customers Operations
"""
# Customer login function. It verifies the customer with the username and password and returns the JWT token.
@csrf_exempt
@require_http_methods(["POST"])
def login_customer(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')

        # Username and password are required fields
        if not username or not password:
            raise ValueError("Username and password required")

        try:
            customer = Customers.objects.get(username=username)  # Kullanıcı adına göre müşteriyi al
        except Customers.DoesNotExist:
            raise ValueError("Invalid username or password")

        # Check if your password is correct
        if not check_password(password, customer.password):
            raise ValueError("Invalid username or password")

        # JWT token create
        payload = {
            'user_id': customer.id,
            'username': customer.username,
            'exp': datetime.utcnow() + timedelta(days=1)  # Token validity period
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        # Return successful login reply
        response_data = {
            'status': True,
            'message': f'Login successful. Welcome {customer.name} :)',
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
        # Return error message in case of assignment
        error_data = {
            'status': False,
            'message': str(e)
        }
        return JsonResponse(error_data, status=400)

# New customer creation function. It receives the data received via the POST method and registers a new customer.
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
            raise ValueError("All fields must be filled")

        # Make sure your username is unique
        if Customers.objects.filter(username=username).exists():
            raise ValueError("Kullanıcı adı zaten var")

        # Hash the password
        hashed_password = make_password(password)
        new_customer = Customers.objects.create(
            name=name,
            surname=surname,
            username=username,
            password=hashed_password
        )

        # Return successful response
        response_data = {
            'status': True,
            'message': 'Customer created.',
            'data': {
                'id': new_customer.id,
                'name': new_customer.name,
                'surname': new_customer.surname,
                'username': new_customer.username,
            }
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        # Return error message in case of error
        error_data = {
            'status': False,
            'message': str(e)
        }
        return JsonResponse(error_data, status=400)

# Function to list all customers.
@require_http_methods(["GET"])
def get_customers(request):
    try:
        customers = Customers.objects.all()  # Get all customer records
        customer_data = []

        # Add information for each customer to a list
        for customer in customers:
            customer_data.append({
                "id": customer.pk,
                "name": customer.name,
                "surname": customer.surname,
                "username": customer.username,
            })

        response_data = {
            'status': True,
            'message': 'Find Complated.',
            'data': customer_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to search for a specific customer. It filters with query parameters.
@require_http_methods(["GET"])
def get_specific_customer(request):
    try:
        customers_query = Customers.objects.all()

        # Get query parameters
        customer_id = request.GET.get('id')
        name = request.GET.get('name')
        surname = request.GET.get('surname')
        username = request.GET.get('username')

        # Filtering operations
        if customer_id:
            customers_query = customers_query.filter(pk=customer_id)
        if name:
            customers_query = customers_query.filter(name=name)
        if surname:
            customers_query = customers_query.filter(surname=surname)
        if username:
            customers_query = customers_query.filter(username=username)

        # Add customer information to a list via filtered results
        customer_data = [{
            "id": customer.id,
            "name": customer.name,
            "surname": customer.surname,
            "username": customer.username
        } for customer in customers_query]

        response_data = {
            'status': True,
            'message': 'Müşteri bilgileri başarıyla alındı.',
            'data': customer_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to delete a specific customer. Deletes a specific customer record by customer ID.
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_customer(request, customer_id):
    try:
        customer = Customers.objects.get(id=customer_id)  # Get specific customer by ID
        customer.delete()  # Delete Customer
        return JsonResponse({'status': True, 'message': f'Customer deleted ID={customer_id}'}, status=204)
    except Customers.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Customer not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

# Function to update a specific customer. Updates customer information.
@csrf_exempt
@require_http_methods(["PUT"])
def update_customer(request, customer_id):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Get JSON data from request body and parse it
        customer = Customers.objects.get(id=customer_id)  # Get the customer to be updated by ID
        
        # Update customer information based on received data
        customer.name = data.get('name', customer.name)
        customer.surname = data.get('surname', customer.surname)
        customer.save()  
        
        # Return reply with updated customer information
        updated_data = {
            'id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'username': customer.username,
        }

        response_data = {
            'status': True,
            'message': 'Customer updated successfully',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except Customers.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Müşteri bulunamadı.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Rezervasyon İşlemleri
"""
# New reservation creation function. It receives the data received via the POST method and saves a new reservation.
@csrf_exempt
@require_http_methods(["POST"])
def create_reservation(request):
    try:
        data = json.loads(request.body.decode('utf-8'))  # Get JSON data from request body and parse it

        iha_id = data.get('iha_id')
        customer_id = data.get('customer_id')
        start_date_str = data.get('start_date')
        finish_date_str = data.get('finish_date')
        number = data.get('number')

        # Make sure the required fields are filled in
        if not all([iha_id, customer_id, start_date_str, finish_date_str]):
            raise ValueError("IHA ID, Müşteri ID, Başlangıç Tarihi ve Bitiş Tarihi gereklidir")

        # Retrieve IHA and customer records by ID
        iha = IHA.objects.get(pk=iha_id)
        customer = Customers.objects.get(pk=customer_id)

        # Convert dates received as string to datetime object
        start_datetime = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
        finish_datetime = datetime.strptime(finish_date_str, "%Y-%m-%dT%H:%M:%S")

        # Calculate booking duration (in hours) and total price
        reservation_duration_hours = (finish_datetime - start_datetime).total_seconds() / 3600
        total_price = reservation_duration_hours * iha.price * number

        # Create the new reservation record and save it in the database
        new_reservation = Reservations.objects.create(
            iha=iha,
            customer=customer,
            start_date=start_datetime,
            finish_date=finish_datetime,
            total_price=total_price,
            number=number
        )

        response_data = {
            'status': True,
            'message': 'Reservation created successfully',
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

# Function to list all reservations.
@require_http_methods(["GET"])
def get_reservations(request):
    try:
        reservations = Reservations.objects.select_related('iha', 'customer').all()  # Tüm rezervasyon kayıtlarını al
        reservation_data = []

        # Add information to a list for each reservation
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
            'message': 'Reservations find successful',
            'data': reservation_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to search for a specific reservation. It filters with query parameters.
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

        # Add booking information to a list via filtered results
        reservations_data = [{
            "reservation_id": reservation.id,
            "iha": {
                "brand": reservation.iha.brand,
                "model": reservation.iha.model,
                "category": reservation.iha.category,
                "price": reservation.iha.price,
                'image_url': reservation.iha.image.url if reservation.iha.image else None
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
            'message': 'Rezervasyon find succesfully.',
            'data': reservations_data
        }

        return JsonResponse(response_data, safe=False)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)

# Function to delete a specific reservation. Deletes a specific reservation record with its reservation ID.
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_reservation(request, reservation_id):
    try:
        reservation = Reservations.objects.get(id=reservation_id) 
        reservation.delete()
        return JsonResponse({'status': True, 'message': 'Reservation Deleted.'}, status=204)
    except Reservations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Reservation not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

# Function to update a specific reservation. Updates reservation information.
@csrf_exempt
@require_http_methods(["PUT"])
def update_reservation(request, reservation_id):
    try:
        data = json.loads(request.body.decode('utf-8')) 
        reservation = Reservations.objects.get(id=reservation_id)  
        
        # Update reservation information based on received data
        start_date_str = data.get('start_date')
        finish_date_str = data.get('finish_date')
        if start_date_str:
            reservation.start_date = datetime.strptime(start_date_str, "%Y-%m-%dT%H:%M:%S")
        if finish_date_str:
            reservation.finish_date = datetime.strptime(finish_date_str, "%Y-%m-%dT%H:%M:%S")

        if 'total_price' in data:
            reservation.total_price = data['total_price']

        reservation.clean()  # Perform model cleaning operations
        reservation.save()  # Save updated reservation
        
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
            'message': 'Reservation updated successfully',
            'data': updated_data
        }

        return JsonResponse(response_data, status=200)
    
    except Reservations.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'Rezervasyon bulunamadı.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'status': False, 'message': str(e.messages)}, status=400)
    except Exception as e:
        return JsonResponse({'status': False, 'message': str(e)}, status=400)

"""
Admin operations
"""
# Admin login function. The administrator verifies with his username and password and the JWT token is returned.
@csrf_exempt
@require_http_methods(["POST"])
def login_admin(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        username = json_data.get('username')
        password = json_data.get('password')

        if not username or not password:
            raise ValueError("Kullanıcı adı ve parola gereklidir")

        if password != 'admin' and username != 'admin':
            raise ValueError("Geçersiz kullanıcı adı veya parola")

        payload = {
            'message': 'Hoşgeldin Patron !',
            'exp': datetime.utcnow() + timedelta(days=1)  # Token geçerlilik süresi
        }
        token = jwt.encode(payload, settings.SECRET_KEY_ADMIN, algorithm='HS256')

        response_data = {
            'status': True,
            'message': f'Giriş Başarılı. Hoşgeldin Patron :)',
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

# Function used for validation. JWT checks whether the token is valid or not.
@require_http_methods(["GET"])
def get_verify(request):
    try:
        response_data = {
            'status': True,
            'message': 'Verification successful.',
        }

        return JsonResponse(response_data, safe=False, status=200)
    
    except Exception as e:
        error_data = {
            'status': False,
            'message': str(e)
        }

        return JsonResponse(error_data, status=400)
