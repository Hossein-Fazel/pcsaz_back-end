from django.db import connection

def all_products():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM product;")
        colnames = [item[0] for item in cursor.description]
        result = cursor.fetchall()
    return [dict(zip(colnames, item)) for item in result]

def compatible_cpu_motherboard(cpu_id= None, motherboard_id= None):
    with connection.cursor() as coursor:
        if cpu_id:
            coursor.execute("SELECT motherboard_id from mc_socket_compatible_with cpu_id = %s", (cpu_id,))
            return coursor.fetchall()
        elif motherboard_id:
            coursor.execute("SELECT cpu_id from mc_socket_compatible_with motherboard_id = %s", (motherboard_id,))
            return coursor.fetchall()

def compatible_cooler_cpu(cpu_id= None, cooler_id= None):
    with connection.cursor() as coursor:
        if cpu_id:
            coursor.execute("SELECT cooler_id from cc_socket_compatible_with cpu_id = %s", (cpu_id,))
            return coursor.fetchall()
        elif cooler_id:
            coursor.execute("SELECT cpu_id from cc_socket_compatible_with cooler_id = %s", (cooler_id,))
            return coursor.fetchall()

def compatible_ram_motherboard(motherboard_id = None, ram_id= None):
    with connection.cursor() as coursor:
        if ram_id:
            coursor.execute("SELECT motherboard_id from rm_slot_compatible_with ram_id = %s", (ram_id,))
            return coursor.fetchall()
        elif motherboard_id:
            coursor.execute("SELECT ram_id from rm_slot_compatible_with motherboard_id = %s", (motherboard_id,))
            return coursor.fetchall()

def compatible_motherboard_gpu(motherboard_id= None, gpu_id= None):
    with connection.cursor() as coursor:
        if gpu_id:
            coursor.execute("SELECT motherboard_id from gm_slot_compatible_with gpu_id = %s", (gpu_id,))
            return coursor.fetchall()
        elif motherboard_id:
            coursor.execute("SELECT gpu_id from gm_slot_compatible_with motherboard_id = %s", (motherboard_id,))
            return coursor.fetchall()

def compatible_motherboard_ssd(motherboard_id= None, ssd_id= None):
    with connection.cursor() as coursor:
        if ssd_id:
            coursor.execute("SELECT motherboard_id from sm_slot_compatible_with ssd_id = %s", (ssd_id,))
            return coursor.fetchall()
        elif motherboard_id:
            coursor.execute("SELECT ssd_id from sm_slot_compatible_with motherboard_id = %s", (motherboard_id,))
            return coursor.fetchall()

def compatible_gpu_connector(gpu_id= None, connector= None):
    with connection.cursor() as coursor:
        if connector:
            coursor.execute("SELECT gpu_id from connector_compatible_with connector = %s", (connector,))
            return coursor.fetchall()
        elif gpu_id:
            coursor.execute("SELECT connector from connector_compatible_with gpu_id = %s", (gpu_id,))
            return coursor.fetchall()
