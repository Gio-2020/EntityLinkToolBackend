from django.contrib import admin
from .models import KB, TrainingSet, TrainingRecord
# Register your models here.
admin.site.register(KB)
admin.site.register(TrainingSet)
admin.site.register(TrainingRecord)