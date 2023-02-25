from django.urls import path
from . import views
urlpatterns = [
    path('getTable', views.getTable),
    path('getExcel', views.getExcel),
    path('saveSingleTrainingData', views.saveSingleTrainingData),
    path('saveTrainingSet', views.saveTrainingSet),
    path('reviceSingleTrainingData', views.reviceSingleTrainingData),
    path('deleteSingleTrainingData', views.deleteSingleTrainingData),
    path('searchKnowledgeBaseByName', views.searchKnowledgeBaseByName),
    path('getTrainingSet', views.getTrainingSet),
    # path('testAddTable', views.testAddTable)
    

    path('getDataset', views.getDataset),
    path('deleteDataset', views.deleteDataset),

    path('dataSetPartition', views.dataSetPartition),
    path('getTrainingSetting', views.getTrainingSetting),
    path('searchKnowledgeBaseByAlias', views.searchKnowledgeBaseByAlias),
    path('getAnnotationData', views.getAnnotationData),
    path('dataAnnotation', views.dataAnnotation),

    path('getKnowledgeBaseDetails', views.getKnowledgeBaseDetails),
    path('getAllKnowledgeBases', views.getAllKnowledgeBases),
    path('addNegativeSample', views.addNegativeSample),
    path('getDatasetDetails', views.getDatasetDetails)
]