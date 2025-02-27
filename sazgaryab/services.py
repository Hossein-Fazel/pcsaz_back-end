from django.db import connection

def all_products():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM product;")
        colnames = [item[0] for item in cursor.description]
        result = cursor.fetchall()
    return [dict(zip(colnames, item)) for item in result]