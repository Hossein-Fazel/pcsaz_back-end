from django.db import Error
from django.http import JsonResponse
from sazgaryab import query_services
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

def find_compatibles(request):
    if request.method == "POST":
        try:
            products = json.loads(request.body)['products']
        except:
            return JsonResponse({"error" : 'No products have been entered'}, status=400)
        
        cc_products = []
        
        for item in products:
            if item["category"] == "RAM Stick":
                prs = list(item[0] for item in query_services.compatible_ram_motherboard(ram_id= item["id"]))
                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))
            

            elif item["category"] == "Motherboard":
                prs = list(item[0] for item in query_services.compatible_ram_motherboard(motherboard_id= item["id"]))
                prs.extend(item[0] for item in query_services.compatible_cpu_motherboard(motherboard_id= item["id"]))
                prs.extend(item[0] for item in query_services.compatible_motherboard_gpu(motherboard_id= item["id"]))
                prs.extend(item[0] for item in query_services.compatible_motherboard_ssd(motherboard_id= item["id"]))

                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))
            

            elif item["category"] == "CPU":
                prs = list(item[0] for item in query_services.compatible_cooler_cpu(cpu_id= item["id"]))
                prs.extend(item[0] for item in query_services.compatible_cpu_motherboard(cpu_id= item["id"]))

                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))
            

            elif item["category"] == "Cooler":
                prs = list(item[0] for item in query_services.compatible_cooler_cpu(cooler_id= item["id"]))
                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))

            elif item["category"] == "GPU":
                prs = list(item[0] for item in query_services.compatible_motherboard_gpu(gpu_id= item["id"]))
                prs.extend(item[0] for item in query_services.compatible_gpu_connector(ssd_id= item["id"]))

                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))
            
            elif item["category"] == "Power Supply":
                prs = list(item[0] for item in query_services.compatible_gpu_connector(connector_id= item["id"]))
                if len(cc_products) == 0:
                    cc_products = list(prs)
                else:
                    cc_products = list(find_intersect(cc_products, prs))
        
        pr_detail = []
        for id in cc_products:
            pr_detail.append(query_services.about_product(id))
        
        return JsonResponse({"products": pr_detail, "message" : "compatible products find"}, status=200)