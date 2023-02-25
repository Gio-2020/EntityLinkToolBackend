from django.contrib import admin
from .models import KnowledgeBaseData, KnowledgeBaseStatistic, DatasetData, DatasetStatistic, OriginDatasetData, TrainingRecord, AnnotatedData
# Register your models here.
admin.site.register(KnowledgeBaseData)
admin.site.register(KnowledgeBaseStatistic)
admin.site.register(DatasetData)
admin.site.register(DatasetStatistic)
admin.site.register(OriginDatasetData)
admin.site.register(AnnotatedData)
admin.site.register(TrainingRecord)