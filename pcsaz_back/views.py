import jwt

SECRET_KEY = 'hosseinFazeljwt'

def validate_jwt(request):
    token = request.META.get('HTTP_AUTHORIZATION')
    if not token:
        raise ValueError('{"error": "Jwt is required!", "status": 400}')

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        raise ValueError('{"error": "Invalid jwt!", "status":401}')
