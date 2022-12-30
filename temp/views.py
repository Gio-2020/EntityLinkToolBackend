from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse, FileResponse
from io import BytesIO
from django.forms import model_to_dict
from .models import KB, TrainingSet, TrainingRecord
import xlsxwriter
import json, os, pathlib, xlrd
import pandas as pd
from django.db.models import Max, Min
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
                'entity_kb', 'data']
    for col_num in range(len(columns)):
    	#表头写入
        ws.write(row_num, col_num, columns[col_num])
        #从数据库获取指定字段的数据
    rows = TrainingSet.objects.values_list('auto_increment_id',
    'segment_id','text', 'entity', 'entity_kb')
    for row in rows:
        row_num += 1
        #此时row是元组形式，需转换成列表的形式
        row = list(row)
        # print(row)
        for col_num in range(len(row)):
            # ws.write(row_num, col_num, row[col_num])
            pairs = ''
            temp = KB.objects.get(subject_id = row[4])
            data = temp.data
            for i in data:
                pairs += i['predicate']
                pairs += ':'
                pairs += i['object']
                pairs += '|'
            ws.write(row_num, 0, row[0])
            ws.write(row_num, 1, row[1])
            ws.write(row_num, 2, row[2])
            ws.write(row_num, 3, row[3])
            ws.write(row_num, 4, temp.subject)
            ws.write(row_num, 5, pairs)
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
        paper_file = request.FILES.get('trainingset')
        df = pd.read_excel(paper_file)
    except:
        return JsonResponse({'errorCode': 400,'data': None, 'message': 'file not found'})
    # print(type(paper_file))
    # df = pd.read_excel(paper_file)
    num_row, num_col = df.shape
    print(num_row, num_col)
    for row in range(num_row):
        temp = {'self_defining_id': str(df.iloc[row][0]), 
                'segment_id': str(df.iloc[row][1]),
                'text': df.iloc[row][2], 
                'entity': df.iloc[row][3],
                'entity_kb': df.iloc[row][4],
                'data': df.iloc[row][5]}
        if type(df.iloc[row][5]) == float:
            temp['data'] = None
        data.append(temp)
    the_response = {'errorCode': 200, 'message': 'success', 'data': data}
    return JsonResponse(the_response)

def saveSingleTrainingData(request):
    pass

def saveTrainingSet(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        trainingData = requestData['trainingData']
        trainingSetName = requestData['trainingSetName']
        # print(type(trainingData))
        min_index = -1
        max_index = -1
        for single in trainingData:
            # print(type(single))
            temp = TrainingSet.objects.create(segment_id = single['segment_id'],
            text = single['text'], entity = single['entity'],
            subject = single['entity_kb'], entity_description = single['data'],
            training_set_name = trainingSetName)
            if trainingData.index(single) == 0:
                min_index = temp.auto_increment_id
            if trainingData.index(single) == len(trainingData) - 1:
                max_index = temp.auto_increment_id            
            # break
        return JsonResponse({'error_code': 200, 'message': 'success',
        'data': {'min': min_index, 'max': max_index}})
    except:
        return JsonResponse({'error_code': 400, 'message': 'failure'})

def reviceSingleTrainingData(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        singleTrainingData = requestData['singleTrainingData']
        temp = TrainingSet.objects.get(auto_increment_id = singleTrainingData['auto_increment_id'])
        temp.segment_id = singleTrainingData['segment_id']
        temp.text = singleTrainingData['text']
        temp.entity = singleTrainingData['entity']
        temp.subject = singleTrainingData['entity_kb']
        temp.entity_description = singleTrainingData['data']
        temp.save()
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'failure'})

def deleteSingleTrainingData(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        # trainingSetName = requestData['trainingSetName']
        auto_increment_id = requestData['auto_increment_id']
        obj = TrainingSet.objects.get(auto_increment_id = auto_increment_id)
        obj.delete()
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'failure'})

def searchKnowledgeBaseByName(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        entityName = requestData['entityName']
        obj = KB.objects.filter(subject = entityName).values('subject', 'subject_id')
        data = []
        for i in obj:
            print(i, flush = True)
            entity = KB.objects.get(pk = i['subject_id'])
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

def getTrainingSet(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        trainingSetName = requestData['trainingSetName']
        trainingSet = TrainingSet.objects.filter(training_set_name = trainingSetName)
        # print(type(trainingSetName))
        data = []
        for i in trainingSet:
            temp = {'segment_id': None, 'text': None, 'entity': None,
            'subject': None, 'entity_description': None}
            temp['segment_id'] = i.segment_id
            temp['text'] = i.text
            temp['entity'] = i.entity
            temp['subject'] = i.subject
            temp['entity_description'] = i.entity_description
            data.append(temp) 
        return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    except:
         return JsonResponse({'error_code': 400, 'message': 'failure'})

def dataSetPartition(request):
    requestData = json.loads(request.body.decode('utf-8'))
    trainingRecordName = requestData['trainingRecordName']
    dataSetName = requestData['dataSetName']
    trainingSetPartition = requestData['trainingSetPartition']
    validationSetPartition = requestData['validationSetPartition']
    testSetPartition = requestData['testSetPartition']
    dataset_partition = [trainingSetPartition, validationSetPartition, testSetPartition]
    try:
        temp = TrainingRecord.objects.create(dataset = dataSetName, dataset_partition = dataset_partition,
        training_record_name = trainingRecordName)
    except:
        return JsonResponse({'error_code': 400, 'message': '训练模型名称已存在，请重命名', 'data': None})

    dataset = TrainingSet.objects.filter(training_set_name = dataSetName)
    print(len(dataset))    
    
    auto_increment_id = temp.auto_increment_id
    data = {'auto_increment_id': auto_increment_id}

    return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})

def getDataset(request):
    # try:
    data = []
    dataset_name_list = list(set(list(TrainingSet.objects.values_list('training_set_name', flat = True))))
    print(dataset_name_list, flush = True)
    for i in dataset_name_list:
        temp = {'dataset_name': None, 'size': None}
        temp['dataset_name'] = i
        # temp['size'] = TrainingSet.objects.filter(training_set_name = i).count()
        dataset_filter = TrainingSet.objects.filter(training_set_name = i)
        max_auto_increment_id = dataset_filter.aggregate(Max('auto_increment_id'))
        min_auto_increment_id = dataset_filter.aggregate(Min('auto_increment_id')) 
        print(max_auto_increment_id, flush = True) 
        temp['size'] = int(max_auto_increment_id['auto_increment_id__max']) - int(min_auto_increment_id['auto_increment_id__min']) + 1
        data.append(temp)
    return JsonResponse({'error_code': 200, 'message': 'success', 'data': data})
    # except:
    #     return JsonResponse({'error_code': 400, 'message': 'error'})

def deleteDataset(request):
    try:
        requestData = json.loads(request.body.decode('utf-8'))
        dataset_to_delete = requestData['dataset_name']
        temp = TrainingSet.objects.filter(training_set_name = dataset_to_delete)
        if temp is None:
            return JsonResponse({'error_code': 201, 'message': 'dataset not exists'})
        temp.delete()
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
        data = []
        for i in KB.objects.all().values('alias', 'subject_id'):
            temp = {}
            flag = 0
            for j in i['alias']:
                if user_input in j:
                    entity = KB.objects.get(pk = i['subject_id'])
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
        test_data = request['data']
        return JsonResponse({'error_code': 200, 'message': 'success'})
    except:
        return JsonResponse({'error_code': 400, 'message': 'error'})