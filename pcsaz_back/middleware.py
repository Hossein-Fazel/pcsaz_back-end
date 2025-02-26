from pcsaz_back.settings import JWT_SECRET_KEY
from django.http import JsonResponse
from pcsaz_back.services import validate_referral_code
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
                data['phone']
                data['password']
            except:
                return JsonResponse({'error': 'Signup data is required!'}, status=400)
        
            rcode = data.get('referrer_code')
            if rcode:
                try:
                    validate_referral_code(rcode)
                except ValueError as e:
                    return JsonResponse({'error': e.__str__()}, status=400)

        return self.get_response(request)