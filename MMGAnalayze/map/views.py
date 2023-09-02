import folium
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from analyzeDashboard.models import *
import json
from django.conf import settings
import os

#
# from map.forms import PointForm
#
#
# class MapView(View):
#
#     def get(self, request):
#         user = request.user
#         if user.is_authenticated:
#             form = PointForm()
#             context = {
#                 'form': form
#             }
#             return render(request, 'map/map.html', context=context)
#         else:
#             return redirect('userLogin')
#
#
# class SetPointView(View):
#
#     def post(self, request):
#         user = request.user
#         data = {'url': None}
#
#         return JsonResponse(data)
#
#
#
class MapPageMax(View):
    def get(self, request):
        return render(request, 'map/map_max.html')


class SiberianFederalOkrug(View):
    def get(self, request):
        media_path = os.path.join(settings.MEDIA_ROOT, 'map', 'sib_fed_okrug.json')
        with open(media_path, encoding='utf-8') as file:
            data = json.load(file)

        # Получите список всех регионов из JSON-файла
        regions = [item[1] for item in data]

        # Создайте словарь для хранения статусов регионов
        region_status_dict = {}

        # Проверьте для каждого региона, есть ли в нем строения с красным или желтым статусом
        for region in regions:
            buildings_in_region = Building.objects.filter(id_region=region['properties']['id'])
            red_building_exists = buildings_in_region.filter(status='red').exists()
            yellow_building_exists = buildings_in_region.filter(status='yellow').exists()

            if red_building_exists:
                region_status_dict[region['properties']['id']] = 'red'
            elif yellow_building_exists:
                region_status_dict[region['properties']['id']] = 'yellow'
            else:
                region_status_dict[region['properties']['id']] = 'lightgray'

        context = {
            'region_status_dict': json.dumps(region_status_dict),  # Преобразуйте словарь в строку JSON
        }

        return render(request, 'map/siberian_federal_okrug.html', context)
