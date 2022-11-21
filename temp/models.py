from django.db import models

# Create your models here.

class KB(models.Model):
    alias = models.JSONField(default = list, verbose_name='别名')
    subject_id = models.CharField(primary_key = True, max_length = 20, verbose_name = 'id')
    subject = models.CharField(verbose_name = '名称', max_length = 100)
    type = models.JSONField(default = list, verbose_name = '类型')
    data = models.JSONField(default = list, verbose_name = '数据')

class TrainingSet(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    segment_id = models.CharField(max_length = 20, verbose_name = '段序号') # train.json中的text_id, 用于判断两条记录是否出自同一文本
    text = models.CharField(max_length = 100, verbose_name = '原始文本')
    entity = models.CharField(max_length = 100, verbose_name = '抽取出的实体')
    subject = models.CharField(max_length = 100, verbose_name = '知识库中对应实体名称', default = None) # 知识库没有对应则为空
    entity_description = models.JSONField(default = list, verbose_name = '实体描述') # 知识库没有对应则为空
    # entity_kb = models.ForeignKey(KB, on_delete = models.CASCADE)