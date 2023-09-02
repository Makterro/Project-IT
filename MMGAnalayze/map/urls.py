from django.urls import path

from map.views import *

urlpatterns = [
    #path('', MapView.as_view(), name='map'),
    path('map_max/', MapPageMax.as_view(), name='map_max'),
    path('sib_fed_okrug/', SiberianFederalOkrug.as_view(), name='sib_fed_okrug'),
]
