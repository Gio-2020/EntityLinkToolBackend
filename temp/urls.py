from django.urls import path
from . import views
urlpatterns = [
    path('getTable', views.getTable),
    # path('getExcel', views.getExcel),
    path('getExcel', views.getExcel),
    path('saveSingleTrainingData', views.saveSingleTrainingData),
    path('saveTrainingSet', views.saveTrainingSet),
    path('reviceSingleTrainingData', views.reviceSingleTrainingData),
    path('deleteSingleTrainingData', views.deleteSingleTrainingData),
    path('searchKnowledgeBaseByName', views.searchKnowledgeBaseByName)
]