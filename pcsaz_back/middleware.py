from pcsaz_back.settings import JWT_SECRET_KEY
from django.db import connection
from django.http import JsonResponse
import jwt
import json

class JWTAuthentication:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path in ['/user/login/', '/user/signup/']:
            return self.get_response(request)

        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            return JsonResponse({'error': "Jwt is required!"}, status=401)

        try:
            payload = jwt.decode(token, JWT_SECRET_KEY , algorithms=['HS256'])
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


class signup_checkdata:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/user/signup/':
            try:
                data = json.loads(request.body)
                data['first_name']
                data['last_name']
                phone = data['phone']
                password = data['password']
            except:
                return JsonResponse({'error': 'Signup data is required!'}, status=400)
            
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM client WHERE phone_number = %s LIMIT 1;", [phone])
                if cursor.fetchone():
                    return JsonResponse({'error': 'The phone number is already registered'}, status=409)
                
                referrer_code = data.get('referrer_code')
                if referrer_code:
                    cursor.execute("SELECT * FROM client WHERE referral_code = %s", [referrer_code])
                    if not cursor.fetchone():
                        return JsonResponse({'error': 'The referral code does not exist'}, status=400)
        
        return self.get_response(request)