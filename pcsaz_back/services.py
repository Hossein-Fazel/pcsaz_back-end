from django.db import connection


def validate_referral_code(referral_code:str):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM client WHERE referral_code = %s", (referral_code,))
        if not cursor.fetchone():
            raise ValueError('The referral code does not exist')
