from django.db import Error
from django.http import JsonResponse
from user import query_services
from pcsaz_back import auth_services
import json


def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            phone = data['phone']
            password = data['password']
        except:
            return JsonResponse({'error': 'Login data is missing or is not enough'}, status=400)

        user = query_services.get_user(phone, password)

        if not user:
            return JsonResponse({'error': 'The phone number or password is incorrect'}, status=401)
        
        token = auth_services.generate_jwt(user[0])
        return JsonResponse({'jwt' : token, 'message' : 'Login was successful'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def signup(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        firstname = data['first_name']
        lastname = data['last_name']
        phone = data['phone']
        referrer_code = data.get('referrer_code')
        password = data['password']
        
        try:
            query_services.insert_client(firstname, lastname, phone, password)
        except Error as e:
            return JsonResponse({'error' : e.__str__()[8:len(e.__str__())-2]}, status= 409)

        if referrer_code:
            query_services.insert_refer(referrer_code, phone)

        user = query_services.get_user(phone, password)
        
        token = auth_services.generate_jwt(user[0])

        return JsonResponse({'message' : 'Signup was successful', 'jwt' : token}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_personal(request):
    if request.method == 'GET':
        user_id = request.data

        personal_data = query_services.common_user_data(user_id)
        address = query_services.user_addresses(user_id)
        if address:
            personal_data['adresses'] = address

        result = query_services.check_vip(user_id)
        personal_data['is_vip'] = bool(result[0]) if result else False

        # get number of referred
        result = query_services.number_of_referred(user_id)
        personal_data['count_of_referred'] = result[0] if result else 0
        
        return JsonResponse(personal_data, status=200)        

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_vip_detail(request):
    if request.method == 'GET':
        vip_detail = {}
        user_id = request.data
        
        rtime = query_services.vip_ramainder_time(user_id)
        vip_detail['Time_remaining'] = {
            "days" : rtime[0],
            "hours" : int(rtime[1]),
            "minutes" : int(rtime[2]),
        }


        carts = query_services.monthly_purchases(user_id)
        total_bonus = 0
        for cart_number, locked_number in carts:
            result = query_services.calculate_cart_price(user_id, cart_number, locked_number)
            if result:
                total_bonus += result[0] * 0.15

        vip_detail['bonus'] = total_bonus
        
        return JsonResponse(vip_detail, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_discount_detail(request):
    if request.method == 'GET':
        discount_detail = {}
        user_id = request.data

        result = query_services.conut_gift_codes(user_id)
        discount_detail['Gift_codes'] = result[0] if result else 0

        discount_detail['discount_codes'] = query_services.soonexp_discount_code(user_id)

        return JsonResponse(discount_detail, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def get_carts_detail(request):
    if request.method == 'GET':
        carts_detail = {}
        user_id = request.data
        
        carts_detail['carts_status'] = query_services.carts_status(user_id)

        recent_shopps = []

        result = query_services.recent_purchases(user_id)

        for cart_number, locked_number, ttime, tcode, ltime  in result:
            products = query_services.products_of_purchase(user_id, cart_number, locked_number)

            res2 = query_services.calculate_cart_price(user_id, cart_number, locked_number)
            recent_shopps.append(
                {
                    "tracking_code" : tcode,
                    "cart_number" : cart_number,
                    "locked_number" : locked_number,
                    "products" : products,
                    "total_price" : res2[0],
                    "locked_timestamp" : ltime,
                    "transaction_timestamp" : ttime
                }
            )
        carts_detail['recent_shops'] = recent_shopps
        return JsonResponse(carts_detail, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


def add_address(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = request.data
        addresses = data["adresses"]

        for address in addresses:
            try:
                query_services.insert_address(user_id, address["province"], address["remainder"])
            except Error as e:
                return JsonResponse({'message' : e.__str__()[8:len(e.__str__())-2]}, status=409)

        return JsonResponse({'message' : 'Addresses added successfully'}, status=200)

    return JsonResponse({'error': 'Invalid request method'}, status=405)