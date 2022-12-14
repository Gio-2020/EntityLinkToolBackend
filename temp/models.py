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
    training_set_name = models.CharField(max_length = 100, verbose_name = '所属训练集名称', default = '')
    # entity_kb = models.ForeignKey(KB, on_delete = models.CASCADE)

class TrainingRecord(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    knowleage_base = models.CharField(max_length = 20, verbose_name = '知识库名称')
    dataset = models.CharField(max_length = 20, verbose_name = '数据集名称')
    dataset_partition = models.JSONField(default = list, verbose_name = '数据集划分')
    model = models.CharField(max_length = 20, verbose_name = '模型')
    hyperparameters = models.JSONField(default = list, verbose_name = '超参数')
    result = models.JSONField(default = list, verbose_name = '训练结果')