from django.db import connection
from django.http import JsonResponse
import json
import jwt

SECRET_KEY = 'hosseinFazeljwt'

def login(request):
    if request.method == 'POST':
        
        try:
            data = json.loads(request.body)
            phone = data.get('phone')
        except:
            return JsonResponse({'error': 'Phone number is required!'}, status=400)

        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM client WHERE phone_number = %s", [phone])
            user = cursor.fetchone()

        if not user:
            return JsonResponse({'error': 'Invalid phone number!'}, status=401)
        
        is_vip = False
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT CASE
                    WHEN EXISTS (
                        SELECT 1 FROM vip_client
                        WHERE id = %s AND Subscription_expiration_time > CURRENT_TIMESTAMP
                    ) THEN 1
                    ELSE 0
                END AS is_vip;
                ''', [user[0]]
            )
            result = cursor.fetchone()
            is_vip = bool(result[0]) if result else False

        payload = {
            'user_id': user[0],
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return JsonResponse({'jwt' : token, 'message' : 'Login was successful'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)