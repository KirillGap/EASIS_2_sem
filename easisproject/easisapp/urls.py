from django.contrib import admin
from django.urls import path

from .views import upload_file, analyse_file, tree_view

urlpatterns = [
    path('upload/', upload_file, name='upload'),
    path('analys/<str:file_name>/', analyse_file, name='analys'),
    path('tree/<str:file_name>/<str:sentence>/', tree_view, name='tree')
]