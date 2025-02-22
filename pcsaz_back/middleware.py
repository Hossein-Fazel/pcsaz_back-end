# myapp/middleware.py
from django.http import JsonResponse
import jwt
from pprint import pprint

SECRET_KEY = 'hosseinFazeljwt'

class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/user/login/']:
            return self.get_response(request)

        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'error': "Jwt is required!"}, status=401)

        try:
            payload = jwt.decode(token, SECRET_KEY , algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=401)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        try:
            request.META['Content-Type'] = "application/json"
            request.data = payload['user_id']
        except:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        return self.get_response(request)