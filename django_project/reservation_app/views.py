from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from reservation_app.models import IHA, Customers, Reservations
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def create_iha(request):
    try:
        data = request.body.decode('utf-8')
        json_data = json.loads(data)

        brand = json_data.get('brand')
        model = json_data.get('model')
        weight = json_data.get('weight')
        category = json_data.get('category')
        price = json_data.get('price')

        if not brand or not model or not weight or not category or not price:
            raise ValueError("All fields are required")

        new_iha = IHA.objects.create(
            brand=brand,
            model=model,
            weight=weight,
            category=category,
            price=price
        )

        response_data = {
            'status': True,
            'message': 'IHA creation successful.',
            'data': {
                'id': new_iha.id,
                'brand': new_iha.brand,
                'model': new_iha.model,
                'weight': new_iha.weight,
                'category': new_iha.category,
                'price': new_iha.price
            }
        }

        return JsonResponse(response_data, safe=False, status=200)

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

        new_customer = Customers.objects.create(
            name=name,
            surname=surname,
            username=username,
            password=password
        )

        response_data = {
            'status': True,
            'message': 'Customer creation successful.',
            'data': {
                'id': new_customer.id,
                'name': new_customer.name,
                'surname': new_customer.surname,
                'username': new_customer.username,
                'password': new_customer.password
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

        if not iha_id or not customer_id or not start_date_str or not finish_date_str:
            raise ValueError("IHA ID, Customer ID, Start Date, and Finish Date are required")

        iha = IHA.objects.get(pk=iha_id)

        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        finish_date = datetime.datetime.strptime(finish_date_str, "%Y-%m-%d").date()
        reservation_duration = (finish_date - start_date).days
        total_price = reservation_duration * 24 * iha.price

        new_reservation = Reservations.objects.create(
            iha=iha,
            customer=customer_id,
            start_date=start_date,
            finish_date=finish_date,
            total_price=total_price
        )

        response_data = {
            'status': True,
            'message': 'Reservation creation successful.',
            'data': {
                'id': new_reservation.id,
                'iha_id': new_reservation.iha.id,
                'customer_id': new_reservation.customer.id,
                'start_date': str(new_reservation.start_date),
                'finish_date': str(new_reservation.finish_date),
                'total_price': new_reservation.total_price
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
