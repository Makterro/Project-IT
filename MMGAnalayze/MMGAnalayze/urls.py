from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from mainPage.views import *
from django.urls import path, include

from dashboard.views import DashboardView
from mainPage.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view(), name='mainPage'),
    path('feedback/', FeedBackPage.as_view(), name='feedback'),
    path('dashboard/', include('dashboard.urls')),
    path('analyze/', include('analyzeDashboard.urls')),
    path('proba_map/', MapPage.as_view(), name='proba_mapPage'),
    path('map/', include('map.urls')),
    path('auth/', include('auth.urls')),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
