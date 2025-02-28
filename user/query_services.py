from django.db import connection
from pcsaz_back import auth_services

def get_user(phone, password):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM client WHERE phone_number = %s AND password = %s", (phone, auth_services.hash_pass(password),))
        user = cursor.fetchone()
    return user


def insert_client(first_name, last_name, phone, password):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO client(first_name, last_name, phone_number, referral_code, password) VALUES (%s, %s, %s, %s, %s);",
                    (first_name, last_name, phone, f"{first_name[0]}{last_name[0]}_{phone}", auth_services.hash_pass(password),))


def insert_refer(referrer_code, phone):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM client WHERE referral_code = %s;", (referrer_code,))
        r_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM client WHERE phone_number = %s;", (phone,))
        u_id = cursor.fetchone()[0]

        cursor.execute("INSERT INTO refer(referee, referrer) VALUES(%s, %s);", (u_id, r_id,))


def common_user_data(uid):
    with connection.cursor() as cur:
        cur.execute("SELECT first_name, last_name, referral_code, wallet_balance, client_timestamp  FROM client WHERE id = %s", (uid,))
        colnames = [item[0] for item in cur.description]
        result = cur.fetchone()
        userdata = dict(zip(colnames, result))
    return userdata


def user_addresses(uid):
    with connection.cursor() as cur:
        cur.execute("SELECT province, remainder FROM address WHERE id = %s", (uid,))
        colnames = ["province", "remainder"]
        result = cur.fetchall()
    return [dict(zip(colnames, item)) for item in result]


def check_vip(uid):
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
            ''', (uid,)
        )
        return cursor.fetchone()


def number_of_referred(uid):
    query = '''
        SELECT COUNT(*) AS number
        FROM refer
        WHERE referrer = %s
    '''
    with connection.cursor() as cursor:
        cursor.execute(query, (uid,))
        result = cursor.fetchone()
    return result


def vip_ramainder_time(uid):
    with connection.cursor() as cur:
        query = '''
            SELECT CONCAT(
                TIMESTAMPDIFF(DAY, CURRENT_TIMESTAMP, Subscription_expiration_time), 'd ',
                LPAD(TIMESTAMPDIFF(HOUR, CURRENT_TIMESTAMP, Subscription_expiration_time) %% 24, 2, '0'), ':',
                LPAD(TIMESTAMPDIFF(MINUTE, CURRENT_TIMESTAMP, Subscription_expiration_time) %% 60, 2, '0')
            ) AS remTime
            FROM vip_client 
            WHERE id = %s 
            AND Subscription_expiration_time > CURRENT_TIMESTAMP;
        '''
        cur.execute(query, (uid,))
        return cur.fetchone()


def monthly_purchases(uid):
    with connection.cursor() as cursor:
        fetch_query = '''
            SELECT lsc.cart_number, lsc.locked_number
            FROM vip_client vip
            JOIN locked_shopping_cart lsc ON vip.id = lsc.id
            JOIN issued_for isu ON lsc.id = isu.id AND lsc.cart_number = isu.cart_number AND lsc.locked_number = isu.locked_number
            WHERE vip.id = %s 
            AND Subscription_expiration_time >= CURRENT_TIMESTAMP 
            AND isu.tracking_code IN (
                SELECT tns.tracking_code 
                FROM transaction tns
                WHERE transaction_status = 'Successful'
                    AND transaction_timestamp >= DATE_FORMAT(TIMESTAMPADD(MONTH,-1,CURRENT_TIMESTAMP), '%%Y-%%m-01 00:00:00')
            );
        '''
        cursor.execute(fetch_query, (uid,))
        return cursor.fetchall()


def carts_status(uid):
    with connection.cursor() as cur:
        query = '''
            SELECT cart_number, cart_status
            FROM shopping_cart
            WHERE id = %s
        '''
        cur.execute(query, (uid,))
        colnames = ['cart_number', 'cart_status']
        result = cur.fetchall()
        return [dict(zip(colnames, item)) for item in result]


def recent_purchases(uid):
    with connection.cursor() as cur:
        query = '''
            SELECT isu.cart_number, isu.locked_number
            FROM issued_for isu
            JOIN transaction trs ON isu.tracking_code = trs.tracking_code
            WHERE isu.id = %s AND trs.transaction_status = "Successful"
            ORDER BY trs.transaction_timestamp DESC
            LIMIT 5;
        '''
        cur.execute(query, (uid,))
        return cur.fetchall()

def products_of_purchase(uid, cart_number, locked_number):
    with connection.cursor() as cur:
        products_query = '''
            SELECT category, brand, model, adt.quantity
            FROM added_to adt
            JOIN product pdt ON adt.product_id = pdt.id
            WHERE adt.id = %s AND adt.cart_number = %s AND adt.locked_number = %s
        '''
        cur.execute(products_query, (uid, cart_number, locked_number,))
        res2 = cur.fetchall()
        colnames = ["category", "brand", "model", "quantity"]
        return [dict(zip(colnames, item)) for item in res2]


def conut_gift_codes(uid):
    with connection.cursor() as cur:
        query = '''
            WITH RECURSIVE Referrals AS (
                SELECT id AS referee
                FROM client
                WHERE id = %s
                UNION ALL

                SELECT r.referee
                FROM refer r JOIN Referrals rs ON r.referrer = rs.referee
            )
            SELECT COUNT(*) FROM Referrals;
        '''
        cur.execute(query, (uid,))
        return cur.fetchone()


def soonexp_discount_code(uid):
    with connection.cursor() as cur:
        query = '''
            SELECT pc.code, dc.expiration_date
            FROM private_code pc JOIN discount_code dc ON pc.code = dc.code
            WHERE pc.id = %s AND dc.expiration_date >= CURRENT_TIMESTAMP AND dc.expiration_date < CURRENT_TIMESTAMP + INTERVAL 7 DAY;
        '''
        cur.execute(query, (uid,))
        colnames = [item[0] for item in cur.description]
        result = cur.fetchall()
    return [dict(zip(colnames, item)) for item in result]


def calculate_cart_price(uid, cart_number, locked_number):
    with connection.cursor() as cur:
        price_query = '''
                CALL calculate_cart_price(%s, %s, %s, @total_purchase);
            '''
        cur.execute(price_query, (uid, cart_number, locked_number,))
        cur.execute("SELECT @total_purchase;")
        return cur.fetchone()


def insert_address(uid, province, remainder):
    with connection.cursor() as cursor:
        query='''
            INSERT INTO address(id, province, remainder) VALUES(%s, %s, %s);
        '''
        cursor.execute(query, (uid, province, remainder,))
