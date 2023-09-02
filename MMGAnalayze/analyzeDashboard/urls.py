from django.urls import path
from analyzeDashboard.views import *

urlpatterns = [
    path('<int:building_id>/', research_list, name='research_list'),
    path('detail/<int:research_id>/', research_detail, name='research_detail'),
    path('create_research/<int:building_id>/', create_research, name='create_research'),
    path('research/<int:research_id>/delete_file/<int:file_id>/', delete_file, name='delete_file'),
    path('research/<int:research_id>/download_file/<int:file_id>/', download_research_file, name='download_research_file'),
]