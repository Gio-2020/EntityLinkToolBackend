from django.db import models

# Create your models here.
# todo: adding indexes
class KnowledgeBaseStatistic(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    knowledge_base_name = models.CharField(verbose_name = '知识库名称', unique = True, max_length = 255)
    num_entity = models.IntegerField(verbose_name = '知识库实体数量', default = 0)
    similar_entity_statistic = models.JSONField(verbose_name = '相似实体统计', default = list)
    num_entity_attribute_statistic = models.JSONField(verbose_name = '实体描述字段数量统计', default = list)

class KnowledgeBaseData(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    alias = models.JSONField(default = list, verbose_name='别名')
    subject_id = models.CharField(max_length = 255, verbose_name = 'id')
    subject = models.CharField(verbose_name = '名称', max_length = 255)
    type = models.JSONField(default = list, verbose_name = '类型')
    data = models.JSONField(default = list, verbose_name = '数据')
    knowledge_base = models.ForeignKey(KnowledgeBaseStatistic, on_delete = models.CASCADE, verbose_name = '所属知识库名称', to_field = 'knowledge_base_name')

    class Meta:
        indexes = [
            models.Index(fields=['subject_id', 'subject']),
        ]

class DatasetStatistic(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    dataset_name = models.CharField(verbose_name = '数据集名称', unique = True, max_length = 255)
    knowledge_base_name = models.ForeignKey(KnowledgeBaseStatistic, on_delete = models.CASCADE, verbose_name = '链接知识库名称', to_field = 'knowledge_base_name')

    training_set_num = models.IntegerField(verbose_name = '训练集样本数量', default = 0)
    training_set_pos_num = models.IntegerField(verbose_name = '训练集正样本数量', default = 0)
    training_set_neg_num = models.IntegerField(verbose_name = '训练集负样本数量', default = 0)
    
    dev_set_num = models.IntegerField(verbose_name = '验证集样本数量', default = 0)
    dev_set_pos_num = models.IntegerField(verbose_name = '验证集正样本数量', default = 0)
    dev_set_neg_num = models.IntegerField(verbose_name = '验证集负样本数量', default = 0)
    
    test_set_num = models.IntegerField(verbose_name = '测试集样本数量', default = 0)
    test_set_pos_num = models.IntegerField(verbose_name = '测试集正样本数量', default = 0)
    test_set_neg_num = models.IntegerField(verbose_name = '测试集负样本数量', default = 0)

    text_length_statistic = models.JSONField(verbose_name = '文本长度统计', default = list)
    entity_num_statistic = models.JSONField(verbose_name = '实体数量统计', default = list)


class DatasetData(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    segment_id = models.CharField(max_length = 255, verbose_name = '段序号') # train.json中的text_id, 用于判断两条记录是否出自同一文本
    text = models.CharField(max_length = 255, verbose_name = '原始文本')
    entity = models.CharField(max_length = 255, verbose_name = '抽取出的实体')
    # subject = models.CharField(max_length = 100, verbose_name = '知识库中对应实体名称', default = None) # 知识库没有对应则为空
    subject_id = models.CharField(max_length = 255, verbose_name = '知识库中对应实体id')
    offset = models.CharField(max_length = 255,verbose_name = '偏移量')
    # entity_description = models.JSONField(default = list, verbose_name = '实体描述') # 知识库没有对应则为空
    # training_set_name = models.CharField(max_length = 100, verbose_name = '所属训练集名称', default = '')
    dataset_name = models.ForeignKey(DatasetStatistic, on_delete = models.CASCADE, to_field = 'dataset_name')
    pos_label = models.BooleanField(verbose_name = '正例标记') # True表示正例，False表示负例
    class_label = models.CharField(verbose_name = '所属类别', max_length = 255) # train, dev or test

class OriginDatasetData(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    segment_id = models.CharField(max_length = 255, verbose_name = '段序号') # train.json中的text_id, 用于判断两条记录是否出自同一文本
    text = models.CharField(max_length = 255, verbose_name = '原始文本')
    entity = models.CharField(max_length = 255, verbose_name = '抽取出的实体')
    # subject = models.CharField(max_length = 100, verbose_name = '知识库中对应实体名称', default = None) # 知识库没有对应则为空
    subject_id = models.CharField(max_length = 255, verbose_name = '知识库中对应实体id')
    offset = models.CharField(max_length = 255,verbose_name = '偏移量')
    # entity_description = models.JSONField(default = list, verbose_name = '实体描述') # 知识库没有对应则为空
    # training_set_name = models.CharField(max_length = 100, verbose_name = '所属训练集名称', default = '')
    dataset_name = models.ForeignKey(DatasetStatistic, on_delete = models.CASCADE, to_field = 'dataset_name')

class TrainingRecord(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    knowleage_base = models.CharField(max_length = 255, verbose_name = '知识库名称')
    dataset = models.CharField(max_length = 255, verbose_name = '数据集名称')
    dataset_partition = models.JSONField(default = list, verbose_name = '数据集划分')
    model = models.CharField(max_length = 255, verbose_name = '模型')
    hyperparameters = models.JSONField(default = list, verbose_name = '超参数')
    result = models.JSONField(default = list, verbose_name = '训练结果')
    training_record_name = models.CharField(max_length = 255, unique = True, verbose_name = '训练模型名称')

# 用于主动学习的标注数据
class AnnotatedData(models.Model):
    auto_increment_id = models.AutoField(primary_key = True, verbose_name = '自增id')
    model_name = models.CharField(max_length = 255, verbose_name = '训练模型名称')
    segment_id = models.CharField(max_length = 255, verbose_name = '段序号') # train.json中的text_id, 用于判断两条记录是否出自同一文本
    text = models.CharField(max_length = 255, verbose_name = '原始文本')
    entity_to_annotate = models.CharField(max_length = 255, verbose_name = '原始文本中待标注的实体')
    subject = models.CharField(verbose_name = '链接到的知识库实体', max_length = 255)
    subject_id = models.CharField(max_length = 255, verbose_name = '知识库实体id')