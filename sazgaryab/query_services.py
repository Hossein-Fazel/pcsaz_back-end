from django.db import connection

def compatible_cpu_motherboard(cpu_id= None, motherboard_id= None):
    with connection.cursor() as cursor:
        if cpu_id:
            cursor.execute("SELECT motherboard_id from mc_socket_compatible_with WHERE cpu_id = %s", (cpu_id,))
            return cursor.fetchall()
        elif motherboard_id:
            cursor.execute("SELECT cpu_id from mc_socket_compatible_with WHERE motherboard_id = %s", (motherboard_id,))
            return cursor.fetchall()

def compatible_cooler_cpu(cpu_id= None, cooler_id= None):
    with connection.cursor() as cursor:
        if cpu_id:
            cursor.execute("SELECT cooler_id from cc_socket_compatible_with WHERE cpu_id = %s;", (cpu_id,))
            return cursor.fetchall()
        elif cooler_id:
            cursor.execute("SELECT cpu_id from cc_socket_compatible_with WHERE cooler_id = %s", (cooler_id,))
            return cursor.fetchall()

def compatible_ram_motherboard(motherboard_id = None, ram_id= None):
    with connection.cursor() as cursor:
        if ram_id:
            cursor.execute("SELECT motherboard_id from rm_slot_compatible_with WHERE ram_id = %s", (ram_id,))
            return cursor.fetchall()
        elif motherboard_id:
            cursor.execute("SELECT ram_id from rm_slot_compatible_with WHERE motherboard_id = %s", (motherboard_id,))
            return cursor.fetchall()

def compatible_motherboard_gpu(motherboard_id= None, gpu_id= None):
    with connection.cursor() as cursor:
        if gpu_id:
            cursor.execute("SELECT motherboard_id from gm_slot_compatible_with WHERE gpu_id = %s", (gpu_id,))
            return cursor.fetchall()
        elif motherboard_id:
            cursor.execute("SELECT gpu_id from gm_slot_compatible_with WHERE motherboard_id = %s", (motherboard_id,))
            return cursor.fetchall()

def compatible_motherboard_ssd(motherboard_id= None, ssd_id= None):
    with connection.cursor() as cursor:
        if ssd_id:
            cursor.execute("SELECT motherboard_id from sm_slot_compatible_with WHERE ssd_id = %s", (ssd_id,))
            return cursor.fetchall()
        elif motherboard_id:
            cursor.execute("SELECT ssd_id from sm_slot_compatible_with WHERE motherboard_id = %s", (motherboard_id,))
            return cursor.fetchall()

def compatible_gpu_connector(gpu_id= None, connector_id= None):
    with connection.cursor() as cursor:
        if connector_id:
            cursor.execute("SELECT gpu_id from connector_compatible_with WHERE power_id = %s", (connector_id,))
            return cursor.fetchall()
        elif gpu_id:
            cursor.execute("SELECT power_id from connector_compatible_with WHERE gpu_id = %s", (gpu_id,))
            return cursor.fetchall()

def about_product(pid="ALL"):
    with connection.cursor() as cursor:
        query = "SELECT * FROM product" + (" WHERE id = %s" * (pid != "ALL"))
        params = (int(pid),) if pid != "ALL" else ()
        cursor.execute(query, params)
        colnames = [item[0] for item in cursor.description]
        result = cursor.fetchall()

        return dict(zip(colnames, result[0])) if pid != "ALL" else [dict(zip(colnames, item)) for item in result]