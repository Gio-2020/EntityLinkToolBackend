from django.urls import path
from . import views
urlpatterns = [
    path('getTable', views.getTable),
    # path('getExcel', views.getExcel),
    path('getExcel', views.getExcel)
]