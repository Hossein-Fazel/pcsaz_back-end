from django.db import connection
from django.http import JsonResponse
import json
import jwt
from pprint import pprint

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
        
        payload = {
            'user_id': user[0]
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return JsonResponse({'jwt' : token, 'message' : 'Login was successful'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_personal(request):
    if request.method == 'GET':
        try:
            payload = validate_jwt(request)
        except ValueError as e:
            js = json.loads(e.__str__())
            return JsonResponse({"error" : js['error']}, status=js['status'])

        # get user common data
        with connection.cursor() as cur:
            cur.execute("SELECT first_name, last_name, referral_code, wallet_balance, client_timestamp  FROM client WHERE id = %s", [payload['user_id']])
            colnames = [item[0] for item in cur.description]
            result = cur.fetchone()
            userdata = dict(zip(colnames, result))

        # get user addresses
        with connection.cursor() as cur:
            cur.execute("SELECT province, remainder FROM address WHERE id = %s", [payload['user_id']])
            colnames = ["province", "remainder"]
            result = cur.fetchall()
            if result:
                userdata['adresses'] = [dict(zip(colnames, item)) for item in result]
        
        # check is vip or not
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
                ''', [payload['user_id']]
            )
            result = cursor.fetchone()
            userdata['is_vip'] = bool(result[0]) if result else False

        # get number of referred
        query = '''
            SELECT COUNT(*) AS number
            FROM refer
            WHERE referrer = %s
        '''
        with connection.cursor() as cursor:
            cursor.execute(query, [payload['user_id']])
            result = cursor.fetchone()
            userdata['count of referred'] = result[0]
        
        return JsonResponse(userdata, status=200)        

    return JsonResponse({'error': 'Invalid request method'}, status=405)
