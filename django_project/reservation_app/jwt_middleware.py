import jwt
from django.http import JsonResponse
from django.conf import settings

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        token = request.headers.get('Authorization', None)
      
        if request.path.startswith('/vi/'):
            secret_keys = [settings.SECRET_KEY_ADMIN]

        elif request.path.startswith('/api/'):
            secret_keys = [settings.SECRET_KEY_ADMIN, settings.SECRET_KEY]
        else:
            return self.get_response(request)

        for secret_key in secret_keys:
            try:
                payload = jwt.decode(token, secret_key, algorithms=['HS256'])
                request.user_id = payload['user_id']
                break  
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Token expired'}, status=401)
            except jwt.InvalidTokenError:
                continue
        else:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        response = self.get_response(request)
        return response
