from django.db import Error
from django.http import JsonResponse
from sazgaryab import query_services
from pprint import pprint
import json
def get_all_products(request):
    if request.method == 'GET':
        try:
            products = query_services.about_product()
        except Error as e:
            return JsonResponse({'error' : e.__str__()[8:len(e.__str__())-2]}, status=500)
        
        return JsonResponse({'products' : products}, status=200)
    return JsonResponse({"error" : 'Invalid request method'}, status=405)

def find_intersect(base, new):
    sbase = set(base)
    common_ids = []
    for id in new:
        osize = len(sbase)
        sbase.add(id)
        if len(sbase) == osize:
            common_ids.append(id)

    return common_ids


def compact_products(old:dict, new:dict):
    for key, value in new.items():
        old_value = old.get(key , -1)
        if old_value == -1:
            old.update({key : value})
        else:
            old.update({key : find_intersect(old_value, value)})

def find_compatibles(request):
    if request.method == "POST":
        try:
            products = json.loads(request.body)['products']
        except:
            return JsonResponse({"error" : 'No products have been entered'}, status=400)
        
        cc_products = {}
        at_first = True
        
        for item in products:
            if item["category"] == "RAM Stick":
                prs = {"Motherboard" : list(item[0] for item in query_services.compatible_ram_motherboard(ram_id= item["id"]))}
                if len(cc_products) == 0 and at_first:
                    cc_products.update(prs)
                    at_first = False
                else:
                    compact_products(cc_products, prs)
            

            elif item["category"] == "Motherboard":
                prs = {"RAM Stick" : list(item[0] for item in query_services.compatible_ram_motherboard(motherboard_id= item["id"]))}
                prs.update({"CPU" : list(item[0] for item in query_services.compatible_cpu_motherboard(motherboard_id= item["id"]))})
                prs.update({"GPU" : list(item[0] for item in query_services.compatible_motherboard_gpu(motherboard_id= item["id"]))})
                prs.update({"SSD" : list(item[0] for item in query_services.compatible_motherboard_ssd(motherboard_id= item["id"]))})

                # pprint(prs)

                if len(cc_products) == 0 and at_first:
                    cc_products.update(prs)
                    # pprint(cc_products)
                    at_first = False
                else:
                    compact_products(cc_products, prs)
            

            elif item["category"] == "CPU":
                prs = {"Cooler" : list(item[0] for item in query_services.compatible_cooler_cpu(cpu_id= item["id"]))}
                prs.update({"Motherboard" : list(item[0] for item in query_services.compatible_cpu_motherboard(cpu_id= item["id"]))})

                if len(cc_products) == 0 and at_first:
                    cc_products.update(prs)
                    at_first = False
                else:
                    compact_products(cc_products, prs)
            

            elif item["category"] == "Cooler":
                prs = {"CPU" : list(item[0] for item in query_services.compatible_cooler_cpu(cooler_id= item["id"]))}
                if len(cc_products) == 0 and at_first:
                    cc_products.update(prs)
                    at_first = False
                else:
                    compact_products(cc_products, prs)

            elif item["category"] == "GPU":
                prs = {"Motherboard" : list(item[0] for item in query_services.compatible_motherboard_gpu(gpu_id= item["id"]))}
                prs.update({"Power Supply" : list(item[0] for item in query_services.compatible_gpu_connector(ssd_id= item["id"]))})

                if len(cc_products) == 0 and at_first:
                    cc_products.update(prs)
                    at_first = False
                else:
                    compact_products(cc_products, prs)
            
            elif item["category"] == "Power Supply":
                prs = {"GPU" : list(item[0] for item in query_services.compatible_gpu_connector(connector_id= item["id"]))}
                pprint(prs)
                if len(cc_products) == 0 and at_first:
                    cc_products = prs
                    at_first = False
                else:
                    compact_products(cc_products, prs)

        pr_detail = []
        # pprint(cc_products)
        for _ , value in cc_products.items():
            for pid in value:
                pr_detail.append(query_services.about_product(pid))

        return JsonResponse({"products": pr_detail, "message" : "compatible products find"}, status=200)