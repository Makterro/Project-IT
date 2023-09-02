from django.urls import path

from dashboard.views import *

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('list/region/<int:region_number>/', RegionListMeasurementView.as_view(), name='region_for_measurement'),
    path('measurement/<int:measurement_id>/', MeasurementDetailView.as_view(), name='measurement_detail'),
    path('sensor/<int:sensor_id>/', SensorDetailView.as_view(), name='sensor_detail'),
    path('building/region/<int:region_number>/', BuldingsListView.as_view(), name='buildings_in_region'),
    path('building/<int:building_id>/', BuildingDetailView.as_view(), name='building_detail'),
    path('critical_buildings/', CriticalBuildingsView.as_view(), name='critical_buildings'),
    path('building/edit/<int:building_id>', building_edit, name='building_edit'),

    path('sensor/region/<int:region_number>/', SensortView.as_view(), name='region_for_sensor'),

    # path('generate_report/<int:sensor_reading_id>/', generate_measurement_report, name='generate_measurement_report'),
    path('generate_report/<int:building_id>/', generate_building_report, name='generate_building_report'),
]


