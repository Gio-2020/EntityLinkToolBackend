from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse, FileResponse
from io import BytesIO
from django.forms import model_to_dict
# from .models import KB, TrainingSet, TrainingRecord
from .models import KnowledgeBaseData, KnowledgeBaseStatistic, DatasetData, DatasetStatistic, OriginDatasetData, TrainingRecord, AnnotatedData
import xlsxwriter
import json, os, pathlib, xlrd
import pandas as pd
from django.db.models import Max, Min
import random
import traceback
# Create your views here.

# 测试接口
# def getTable(request):
#     try:
#         requestData = json.loads(request.body.decode('utf-8'))
#         segment_id = requestData['segment_id']
#         print(segment_id)
#         test = TrainingSet.objects.filter(segment_id = segment_id)
#     except:
#         test = TrainingSet.objects.filter(segment_id = '20000')
#     # sample = {'text': test[0].text, 'auto_increment_id': }
#     data = []
#     # sample.text = test[0].text
#     # sample.segment_id = test[0].segment_id
#     # print(test[0].text)
#     for i in test:
#         temp = {'text': i.text, 'auto_increment_id': i.auto_increment_id,
#         'segment_id': i.segment_id, 'entity': i.entity, 
#         'entity_kb': i.entity_kb.subject, 'entity_property': i.entity_kb.data
#         }
#         data.append(temp)
#     the_response = {'errorCode': 200,'data': data}
#     return JsonResponse(the_response)

# excel下载接口
def getExcel(request):
    file_name = 'download.xlsx'
    dest_filename = './static/result.xlsx'
    if pathlib.Path(dest_filename).exists():
        excel = open(dest_filename,"rb")
        response = FileResponse(excel)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
    wb = xlsxwriter.Workbook(dest_filename)
    ws = wb.add_worksheet('trainingset')
    row_num = 0
    # 表头
    columns = ['auto_increment_id', 'segment_id', 'text', 'entity',
                'subject_id', 'offset']
    for col_num in range(len(columns)):
    	#表头写入
        ws.write(row_num, col_num, columns[col_num])
        #从数据库获取指定字段的数据
    rows = OriginDatasetData.objects.values_list('auto_increment_id',
    'segment_id','text', 'entity', 'subject_id', 'offset')
    for row in rows:
        if row_num > 1000:
            break
        row_num += 1
        #此时row是元组形式，需转换成列表的形式
        row = list(row)
        # print(row)
        for col_num in range(len(row)):
            # ws.write(row_num, col_num, row[col_num])
            # pairs = ''
            # temp = KB.objects.get(subject_id = row[4])
            # data = temp.data
            # for i in data:
            #     pairs += i['predicate']
            #     pairs += ':'
            #     pairs += i['object']
            #     pairs += '|'
            ws.write(row_num, 0, row[0])
            ws.write(row_num, 1, row[1])
            ws.write(row_num, 2, row[2])
            ws.write(row_num, 3, row[3])
            ws.write(row_num, 4, row[4])
            ws.write(row_num, 5, row[5])
            # ws.write(row_num, 5, temp.data)

    wb.close()
    # 数据库的数据写入excel表格之后，需要在浏览器以附件的形式下载，所以可以用二进制的形式进行读取
    excel = open(dest_filename,"rb")
    # FileResponse 该类可以将文件下载到浏览器
    response = FileResponse(excel)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

# def send(request):
#     test = KB.objects.filter(subject_id = '200000')
#     data = list(map(lambda x: model_to_dict(x, exclude=["avatr"]), test))
#     # print(data)

#     x_io = BytesIO()
#     work_book = xlsxwriter.Workbook(x_io)
#     work_sheet = work_book.add_worksheet("excel-1")
    
#     # data = [{"a":1, "b": 2}, {"a":22, "b":11}, {"a":54, "b":99}]
#     # print(data[0].keys)
#     keys = data[0].keys()

#     # keys = dict(data[0].keys())

#     # keys.sort()
#     row, col = 0, 0
#     # 写头
#     for k in keys:
#         # 意思是：在row行，col列，写了一个k
#         work_sheet.write(row, col, k)
#         col += 1
#     # 写内容
#     row, col = 1, 0
#     for temp in data:
#         for k in keys:
#             work_sheet.write(row, col, temp[k])
#             col += 1
#         row += 1
#         col = 0

#     work_book.close()
#     res = HttpResponse()
#     res["Content-Type"] = "application/octet-stream"
#     res["Content-Disposition"] = 'filename="userinfos.xlsx"'
#     res.write(x_io.getvalue())
#     print(res)
#     return res


def getTable(request):
    data = []
    try:
        # requestData = json.loads(request.body.decode('utf-8'))
        # knowledge_base_name = requestData['knowledgeBaseName']
        paper_file = request.FILES.get('trainingset')
        df = pd.read_excel(paper_file)
    except:
        return JsonResponse({'errorCode': 400,'data': None, 'message': 'file not found'})
    
    try:
        knowledge_base_name = request.POST.get('knowledgeBaseName')
        # requestData = json.loads(request.body.decode('utf-8'))
        # knowledge_base_name = requestData['knowledgeBaseName']
        print(knowledge_base_name, flush = True)
        kb = KnowledgeBaseData.objects.filter(knowledge_base = knowledge_base_name).values_list('subject_id', 'data')
        
    except:
        return JsonResponse({'errorCode': 400,'data': None, 'message': 'missing_knowledge_base'})
    # print(type(paper_file))
    # df = pd.read_excel(paper_file)
    num_row, num_col = df.shape
    print(num_row, num_col)
    for row in range(num_row):
        temp = {'self_defining_id': str(df.iloc[row][0]), 
                'segment_id': str(df.iloc[row][1]),
                'text': df.iloc[row][2], 
                'entity': df.iloc[row][3],
                'subject_id': str(df.iloc[row][4]),
                'offset': str(df.iloc[row][5]),
                'data': None}
        if temp['subject_id'] != 'NIL':
            # kb_single_data是一个tuple,第0个元素是subject_id,第二个元素是data
            kb_single_data = kb.get(subject_id = temp['subject_id'])
            # print(kb_single_data)
            temp['data'] = kb_single_data[1]
        data.append(temp)
    the_response = {'errorCode': 200, 'message': 'success', 'data': data}
    return JsonResponse(the_response)

def saveSingleTrainingData(request):
    pass


def saveTrainingSet(request):
    # try:
        requestData = json.loads(request.body.decode('utf-8'))
        trainingData = requestData['trainingData']
        trainingSetName = requestData['trainingSetName']
        knowledge_base_name = requestData['knowledgeBaseName']
        try:
            kb = KnowledgeBaseStatistic.objects.get(knowledge_base_name = knowledge_base_name)
        except:
            return JsonResponse({'error_code': 301, 'message': 'kb not found'})
        try:
            new_dataset = DatasetStatistic.objects.create(dataset_name = trainingSetName, knowledge_base_name = kb)
        except:
            return JsonResponse({'error_code': 300, 'message': 'duplicate dataset name'})
        # print(type(trainingData))
        min_index = -1
        max_index = -1
        for single in trainingData:
            # print(type(single))
            temp = OriginDatasetData.objects.create(segment_id = single['segment_id'],
            text = single['text'], entity = single['entity'], offset = single['offset'],
            subject_id = single['subject_id'], dataset_name = new_dataset)
            if trainingData.index(single) == 0:
                min_index = temp.auto_increment_id
            if trainingData.index(single) == len(trainingData) - 1:
                max_index = temp.auto_increment_id            
            # break
        return JsonResponse({'error_code': 200, 'message': 'success',
        'data': {'min': min_index, 'max': max_index}})
    # except:
    #     return JsonResponse({'error_code': 400, 'message': 'failure'})

def reviceSingleTrainingData(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        singleTrainingData = requestData['singleTrainingData']
        temp = OriginDatasetData.objects.get(auto_increment_id = singleTrainingData['auto_increment_id'])
        temp.segment_id = singleTrainingData['segment_id']
        temp.text = singleTrainingData['text']
        temp.entity = singleTrainingData['entity']
        temp.subject_id = singleTrainingData['subject_id']
        temp.offset = singleTrainingData['offset']
        # temp.entity_description = singleTrainingData['data']
        temp.save()
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'failure'})

def deleteSingleTrainingData(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        # trainingSetName = requestData['trainingSetName']
        auto_increment_id = requestData['auto_increment_id']
        obj = OriginDatasetData.objects.get(auto_increment_id = auto_increment_id)
        obj.delete()
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'failure'})

def searchKnowledgeBaseByName(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        entityName = requestData['entityName']
        knowledge_base_name = requestData['knowledgeBaseName']
        print(entityName, knowledge_base_name, flush = True)
        kb = KnowledgeBaseStatistic.objects.get(knowledge_base_name = knowledge_base_name)
        obj = KnowledgeBaseData.objects.filter(subject = entityName).values('subject', 'subject_id', 'knowledge_base')
        print(len(obj), flush = True)
        data = []
        for i in obj:
            print(i['knowledge_base'], type(i['knowledge_base']), flush = True)
            if i['knowledge_base'] != knowledge_base_name:
                continue
            print(i, flush = True)
            entity = KnowledgeBaseData.objects.filter(subject_id = i['subject_id']).get(knowledge_base = kb)
            # temp = {'alias': single.alias, 'subject': single.subject,
            # 'type': single.type, 'data': single.data}
            temp = {'alias': entity.alias, 'subject': entity.subject,
            'type': entity.type, 'data': entity.data}
            data.append(temp)
        return JsonResponse({'error_code': 200, 'message': 'success',
            'data': data})
    except:
         return JsonResponse({'error_code': 400, 'message': 'failure'})
       
# def testAddTable(request):
#     # requestData = json.loads(request.body.decode('utf-8'))
#     # trainingData = requestData['trainingData']
#     # trainingSetName = requestData['trainingSetName']
#     con = pymysql.connect(host='localhost', user='root',
#                       passwd='123456', database='mytest')
#     cur = con.cursor()
#     # cur.execute("use mytest;")
#     sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,  
#          SEX CHAR(1),
#          INCOME FLOAT )"""
#     cur.execute(sql)
#     con.close()

#     return JsonResponse({'error_code': 200, 'message': 'success'})

# 接收一个数据集名称，返回它的记录,包括负例
def getTrainingSet(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        trainingSetName = requestData['trainingSetName']
        trainingSet = DatasetData.objects.filter(dataset_name = trainingSetName)
        # print(type(trainingSetName))
        data = []
        for i in trainingSet:
            temp = {}
            temp['segment_id'] = i.segment_id
            temp['text'] = i.text
            temp['entity'] = i.entity
            temp['subject_id'] = i.subject_id
            temp['offset'] = i.offset
            temp['pos_label'] = i.pos_label
            data.append(temp) 
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
         return JsonResponse({'error_code': 400, 'message': traceback.format_exc()})

# 数据集划分
def dataSetPartition(request):
    requestData = json.loads(request.body.decode('utf-8'))
    trainingRecordName = requestData['trainingRecordName']
    dataSetName = requestData['dataSetName']
    trainingSetPartition = requestData['trainingSetPartition']
    validationSetPartition = requestData['validationSetPartition']
    testSetPartition = requestData['testSetPartition']
    dataset_partition = [{'train': trainingSetPartition}, {'dev': validationSetPartition}, 
                         {'test': testSetPartition}]
    dataset_statistic = DatasetStatistic.objects.get(dataset_name = dataSetName)
    dataset = DatasetData.objects.filter(dataset_name = dataSetName)
    max_auto_increment_id = dataset.aggregate(Max('auto_increment_id'))
    min_auto_increment_id = dataset.aggregate(Min('auto_increment_id'))
    print(min_auto_increment_id['auto_increment_id__min'], max_auto_increment_id['auto_increment_id__max'])
    index_list = list(range(min_auto_increment_id['auto_increment_id__min'], max_auto_increment_id['auto_increment_id__max'] + 1))
    print(index_list, flush = True)
    index_list = random.sample(index_list, len(index_list))
    print(index_list, flush = True)
    total_size = len(index_list)
    num_train = int(total_size * trainingSetPartition)
    num_dev = int(total_size * validationSetPartition)
    num_test = total_size - num_train - num_dev
    dataset_statistic.training_set_num = num_train
    dataset_statistic.dev_set_num = num_dev
    dataset_statistic.test_set_num = num_test
    dataset_statistic.training_set_neg_num = 0
    dataset_statistic.training_set_pos_num = 0
    dataset_statistic.dev_set_neg_num = 0
    dataset_statistic.dev_set_pos_num = 0
    dataset_statistic.test_set_neg_num = 0
    dataset_statistic.test_set_pos_num = 0
    entity_num_statistic = {'train': 0, 'dev': 0, 'test': 0}
    for index, item in enumerate(index_list):
        single_sample = DatasetData.objects.get(pk = item)
        if index <= num_train - 1:
            single_sample.class_label = 'train'
            single_sample.save()
            entity_num_statistic['train'] += 1
            if single_sample.pos_label == True:
                dataset_statistic.training_set_pos_num += 1
            else:
                dataset_statistic.training_set_neg_num += 1
            continue
        if index > num_train - 1 and index <= num_train + num_dev -1:
            single_sample.class_label = 'dev'
            single_sample.save()
            entity_num_statistic['dev'] += 1
            if single_sample.pos_label == True:
                dataset_statistic.dev_set_pos_num += 1
            else:
                dataset_statistic.dev_set_neg_num += 1
            continue
        else:
            single_sample.class_label = 'test'
            single_sample.save()
            entity_num_statistic['test'] += 1
            if single_sample.pos_label == True:
                dataset_statistic.test_set_pos_num += 1
            else:
                dataset_statistic.test_set_neg_num += 1
    dataset_statistic.entity_num_statistic = [entity_num_statistic]
    dataset_statistic.save()
    try:
        temp = TrainingRecord.objects.create(dataset = dataSetName, dataset_partition = dataset_partition,
        training_record_name = trainingRecordName)
    except:
        return JsonResponse({'error_code': 400, 'message': '训练模型名称已存在，请重命名', 'data': None})
    auto_increment_id = temp.auto_increment_id
    data = {'auto_increment_id': auto_increment_id}

    return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})

# 返回所有数据集的名称
def getDataset(request):
    try:
        data = []
        dataset_name_list = list(set(list(DatasetStatistic.objects.values_list('dataset_name', flat = True))))
        print(dataset_name_list, flush = True)
        for i in dataset_name_list:
            temp = {'dataset_name': None}
            temp['dataset_name'] = i
            # temp['size'] = TrainingSet.objects.filter(training_set_name = i).count()
            # dataset_filter = TrainingSet.objects.filter(training_set_name = i)
            # max_auto_increment_id = dataset_filter.aggregate(Max('auto_increment_id'))
            # min_auto_increment_id = dataset_filter.aggregate(Min('auto_increment_id')) 
            # print(max_auto_increment_id, flush = True) 
            # temp['size'] = int(max_auto_increment_id['auto_increment_id__max']) - int(min_auto_increment_id['auto_increment_id__min']) + 1
            data.append(temp)
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

def deleteDataset(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        dataset_to_delete = requestData['dataset_name']
        try:
            dataset = DatasetStatistic.objects.get(dataset_name = dataset_to_delete)
        except:
            return JsonResponse({'error_code': 201, 'message': 'dataset not exists'})
        temp = OriginDatasetData.objects.filter(dataset_name = dataset_to_delete)
        neg_samples = DatasetData.objects.filter(dataset_name = dataset_to_delete)
        if temp is not None:
            temp.delete()
        if neg_samples is not None:
            neg_samples.delete()
        dataset.delete()
        return JsonResponse({'error_code': 200, 'message': 'successfully deleted'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

def getTrainingSetting(request):
    requestData = json.loads(request.body.decode('utf-8'))
    training_record_name = requestData['trainingRecordName']
    temp = TrainingRecord.objects.get(training_record_name = training_record_name)
    if temp is None:
        return JsonResponse({'error_code': 300, 'message': 'not found', 'data': None})
    data = {'knowledge_base': None, 'dataset': None, 'dataset_partition': None,
        "model": None, "hyperparameters": None}
    data['knowledge_base'] = temp.knowleage_base
    data['dataset'] = temp.dataset
    data['dataset_partition'] = temp.dataset_partition
    data['model'] = temp.model
    data['hyperparameters'] = temp.hyperparameters
    return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})

def searchKnowledgeBaseByAlias(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        user_input = requestData['user_input']
        knowledge_base_name = requestData['knowledgeBaseName']
        data = []
        test = KnowledgeBaseData.objects.filter(knowledge_base = knowledge_base_name)
        print(len(test), flush = True)
        for i in test.values('alias', 'auto_increment_id'):
            temp = {}
            flag = 0
            for j in i['alias']:
                if user_input in j:
                    entity = KnowledgeBaseData.objects.get(pk = i['auto_increment_id'])
                    temp['entity'] = entity.subject
                    temp['entity_id'] = entity.subject_id
                    temp['type'] = entity.type
                    temp['data'] = entity.data
                    data.append(temp)
                    flag = 1
                    break
                if flag == 1:
                    break
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

def getAnnotationData(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        model_name = requestData['model_name']

        test_data = [
            {
                "auto_increment_id": 1,
                "raw_text": "小明拉肚子",
                "entity_to_annotate": "拉肚子",
            },
            {
                "auto_increment_id": 2,
                "raw_text": "比特币吸粉无数,但央行的心另有所属",
                "entity_to_annotate": "比特币"
            }
        ]
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': test_data})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

def dataAnnotation(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        model_name = requestData['model_name']
        test_data = requestData['data']
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

# 数据集中加入负例
def addNegativeSample(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        dataset_name = request_data['datasetName']
        negative_proportion = request_data['negativeProportion']
        knowledge_base_name = request_data['knowledgeBaseName']
        neg_per_sample = int(negative_proportion / (1 - negative_proportion))
        dataset_statistic = DatasetStatistic.objects.get(dataset_name = dataset_name)
        origin_dataset = OriginDatasetData.objects.filter(dataset_name = dataset_name)
        # max_auto_increment_id = dataset_filter.aggregate(Max('auto_increment_id'))
        max_auto_increment_id = KnowledgeBaseData.objects.filter(knowledge_base = knowledge_base_name).aggregate(Max('auto_increment_id'))
        min_auto_increment_id = KnowledgeBaseData.objects.filter(knowledge_base = knowledge_base_name).aggregate(Min('auto_increment_id'))
        print(min_auto_increment_id['auto_increment_id__min'], max_auto_increment_id['auto_increment_id__max'], flush = True)
        text_length_statistic = {'1-15': 0, '16-30': 0, '30+': 0}
        for row in origin_dataset:
            if len(row.text) > 30:
                text_length_statistic['30+'] += 1 + neg_per_sample
            elif len(row.text) > 15 and len(row.text) <= 30:
                text_length_statistic['16-30'] += 1 + neg_per_sample
            else:
                text_length_statistic['1-15'] += 1 + neg_per_sample
            # 正例
            DatasetData.objects.create(segment_id = row.segment_id, text = row.text,
            entity = row.entity, subject_id = row.subject_id, offset = row.offset,
            dataset_name = dataset_statistic, pos_label = True)
            # 负例
            for i in range(neg_per_sample):
                while True:
                    selected = random.randint(min_auto_increment_id['auto_increment_id__min'], max_auto_increment_id['auto_increment_id__max'])
                    if selected != row.auto_increment_id:
                        break
                neg_subject_id = KnowledgeBaseData.objects.filter(knowledge_base = knowledge_base_name).get(auto_increment_id = selected).subject_id
                DatasetData.objects.create(segment_id = row.segment_id, text = row.text,
                entity = row.entity, subject_id = neg_subject_id, offset = row.offset,
                dataset_name = dataset_statistic, pos_label = False)
        # 数据集统计
        dataset_size = len(DatasetData.objects.filter(dataset_name = dataset_name))
        dataset_statistic.text_length_statistic = [text_length_statistic]
        data = {'total_size': dataset_size, 'text_length_statistic': dataset_statistic.text_length_statistic}
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': traceback.format_exc()})




# 查询单个知识库的统计信息
def getKnowledgeBaseDetails(request):
    try:
        data = {}
        request_data = json.loads(request.body.decode('utf-8'))
        knowledge_base_name = request_data['knowledgeBaseName']
        try:
            kb = KnowledgeBaseStatistic.objects.get(knowledge_base_name = knowledge_base_name)
        except:
            return JsonResponse({'error_code': 300, 'message': 'not found', 'data': data})
        # if kb is None:
        #     return JsonResponse({'error_code': 300, 'message': 'not found', 'data': data})
        data['num_entity'] = kb.num_entity
        data['similar_entity_statistic'] = kb.similar_entity_statistic
        data['num_entity_attribute_statistic'] = kb.num_entity_attribute_statistic
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})

# 查询所有知识库
def getAllKnowledgeBases(request):
    data = {'name_list': []}
    try:
        kb_list = KnowledgeBaseStatistic.objects.all().values_list('knowledge_base_name')
        for i in kb_list:
            data['name_list'].append(i)
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error', 'data': data})

# 数据集统计
def getDatasetDetails(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        dataset_name = request_data['datasetName']
        dataset = DatasetStatistic.objects.get(dataset_name = dataset_name)
        data = {'training_set_num': dataset.training_set_num, 
                'training_set_pos_num': dataset.training_set_pos_num,
                'training_set_neg_num': dataset.training_set_neg_num,
                
                'dev_set_num': dataset.dev_set_num, 
                'dev_set_pos_num': dataset.dev_set_pos_num,
                'dev_set_neg_num': dataset.dev_set_neg_num,
                
                'test_set_num': dataset.test_set_num, 
                'test_set_pos_num': dataset.test_set_pos_num,
                'test_set_neg_num': dataset.test_set_neg_num,
                'entity_num_statistic': dataset.entity_num_statistic,
                'text_length_statistic': dataset.text_length_statistic}
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
        return JsonResponse({'error_code': 400, 'message': traceback.format_exc(), 'data': {}})
    # data['']

def configCandidateEntityGenerationModel(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        training_record_name = request_data['modelName']
        approach = request_data['approach']
        top = int(request_data['top'])
        training_record = TrainingRecord.objects.get(training_record_name = training_record_name)
        candidate_entity_generation_model = {'candidate_entity_generation_model': {'approach': approach, 
                                                                       'top': top}}
        temp_list = list(training_record.hyperparameters)
        temp_list.append(candidate_entity_generation_model)
        training_record.hyperparameters = temp_list
        training_record.save()
        return JsonResponse({'error_code': 200, 'message': 'success', 'data':  training_record.hyperparameters})

    except:
        return JsonResponse({'error_code': 400, 'message': traceback.format_exc(), 'data': {}})

def configDisambiguationModel(request):
    try:
        request_data = json.loads(request.body.decode('utf-8'))
        training_record_name = request_data['modelName']
        approach = request_data['approach']
        batch_size = request_data['batchSize']
        epoch = request_data['epoch']
        loss = request_data['loss']
        dropout = request_data['dropout']
        max_char_length = request_data['maxCharLength']
        learning_rate = request_data['learningRate']
        training_record = TrainingRecord.objects.get(training_record_name = training_record_name)
        disambiguation_model = {'disambiguation_model': {'approach': approach, 
                                                         'batch_size': batch_size,
                                                         'epoch': epoch,
                                                         'loss': loss,
                                                         'dropout': dropout,
                                                         'max_char_length': max_char_length,
                                                         'learning_rate': learning_rate}}
        temp_list = list(training_record.hyperparameters)
        temp_list.append(disambiguation_model)
        training_record.hyperparameters = temp_list
        training_record.save()
        return JsonResponse({'error_code': 200, 'message': 'success', 'data':  training_record.hyperparameters})        
    except:
        return JsonResponse({'error_code': 400, 'message': traceback.format_exc(), 'data': {}})
