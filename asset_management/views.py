import json

from django.core import serializers
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from asset_management.models import Workshop, Productionline, Asset, AssetService, JtopoDevices, JtopoFilePath


@require_http_methods(["GET"])
def add_workshop(request):
    response = {}
    try:
        workshop_id = request.GET.get('workshop_id')
        workshop_name = request.GET.get('workshop_name')
        workshop_shortened = request.GET.get('workshop_shortened')
        workshop_productionline_number = request.GET.get('workshop_productionline_number')

        workshop = Workshop(id=workshop_id, name=workshop_name, shortened=workshop_shortened, productionline_number=workshop_productionline_number)
        workshop.save()
        response['respMsg'] = 'success'
        response['respCode'] = '000000'
    except Exception as e:
        response['respMsg'] = str(e)
        response['respCode'] = '999999'
    return JsonResponse(response)


# @require_http_methods(["GET"])
# def show_books(request):
#     response = {}
#     try:
#         books = Book.objects.filter()
#         response['list'] = json.loads(serializers.serialize("json", books))
#         response['respMsg'] = 'success'
#         response['respCode'] = '000000'
#     except Exception as e:
#         response['respMsg'] = str(e)
#         response['respCode'] = '999999'
#     return JsonResponse(response)

