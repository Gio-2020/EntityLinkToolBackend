from django.shortcuts import render
from django.http import HttpResponse, request, JsonResponse, FileResponse
from io import BytesIO
from django.forms import model_to_dict
from .models import KB, TrainingSet
import xlsxwriter
import json, os, pathlib
# Create your views here.
def send(request):
    test = KB.objects.filter(subject_id = '200000')
    data = list(map(lambda x: model_to_dict(x, exclude=["avatr"]), test))
    # print(data)

    x_io = BytesIO()
    work_book = xlsxwriter.Workbook(x_io)
    work_sheet = work_book.add_worksheet("excel-1")
    
    # data = [{"a":1, "b": 2}, {"a":22, "b":11}, {"a":54, "b":99}]
    # print(data[0].keys)
    keys = data[0].keys()

    # keys = dict(data[0].keys())

    # keys.sort()
    row, col = 0, 0
    # 写头
    for k in keys:
        # 意思是：在row行，col列，写了一个k
        work_sheet.write(row, col, k)
        col += 1
    # 写内容
    row, col = 1, 0
    for temp in data:
        for k in keys:
            work_sheet.write(row, col, temp[k])
            col += 1
        row += 1
        col = 0

    work_book.close()
    res = HttpResponse()
    res["Content-Type"] = "application/octet-stream"
    res["Content-Disposition"] = 'filename="userinfos.xlsx"'
    res.write(x_io.getvalue())
    print(res)
    return res


def getTable(request):
    requestData = json.loads(request.body.decode('utf-8'))
    segment_id = requestData['segment_id']
    print(segment_id)
    test = TrainingSet.objects.filter(segment_id = segment_id)
    # sample = {'text': test[0].text, 'auto_increment_id': }
    data = []
    # sample.text = test[0].text
    # sample.segment_id = test[0].segment_id
    # print(test[0].text)
    for i in test:
        temp = {'text': i.text, 'auto_increment_id': i.auto_increment_id,
        'segment_id': i.segment_id, 'entity': i.entity, 
        'entity_kb': i.entity_kb.subject, 'entity_property': i.entity_kb.data
        }
        data.append(temp)
    the_response = {'errorCode': 200,'data': data}
    return JsonResponse(the_response)

def getExcel(request):
    test = KB.objects.filter(subject_id = '200000')
    data = list(map(lambda x: model_to_dict(x, exclude=["avatr"]), test))
    # print(data)

    x_io = BytesIO()
    work_book = xlsxwriter.Workbook(x_io)
    work_sheet = work_book.add_worksheet("excel-1")
    
    data = [{"a":1, "b": 2}, {"a":22, "b":11}, {"a":54, "b":99}]
    keys = data[0].keys()

    # keys = dict(data[0].keys())

    # keys.sort()
    row, col = 0, 0
    # 写头
    for k in keys:
        # 意思是：在row行，col列，写了一个k
        work_sheet.write(row, col, k)
        col += 1
    # 写内容
    row, col = 1, 0
    for temp in data:
        for k in keys:
            work_sheet.write(row, col, temp[k])
            col += 1
        row += 1
        col = 0

    work_book.close()
    res = HttpResponse()
    res["Content-Type"] = "application/octet-stream"
    res["Content-Disposition"] = 'filename="userinfos.xlsx"'
    res.write(x_io.getvalue())
    print(res)
    return res

def exportdata(request):

    file_name = 'for_download.xlsx'
    dest_filename = './static/result.xlsx'
    if pathlib.Path(dest_filename).exists():
        excel = open(dest_filename,"rb")
        response = FileResponse(excel)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response
	# return response
    # 定义时间，在下载附件的时候以时间为文件名
    # time_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # file_name = 'Rule_list' + '_' + time_str + 'result.xlsx'
    
    # 项目路径
    # document_root = settings.BASE_DIR
    # dest_filename = document_root + '\\BM\\query_tmp\\' + file_name
    wb = xlsxwriter.Workbook(dest_filename)
    ws = wb.add_worksheet('Menu')
	# 定义写入excel文件的时间格式
    # format2 = wb.add_format({'num_format': 'yyyy/mm/dd hh:mm:ss'})
    # format3 = wb.add_format({'align':    'center'})
    # fomat4 = wb.add_format({'border': 1})
    row_num = 0
    # 设置表头
    columns = ['auto_increment_id', 'segment_id', 'text', 'entity',
                'entity_kb', 'data']
    for col_num in range(len(columns)):
    	#表头写入第一行
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
            temp = KB.objects.get(subject_id = row[4])
            ws.write(row_num, 0, row[0])
            ws.write(row_num, 1, row[1])
            ws.write(row_num, 2, row[2])
            ws.write(row_num, 3, row[3])
            ws.write(row_num, 4, temp.subject)
            # ws.write(row_num, 5, temp.data)

    wb.close()
    # 数据库的数据写入excel表格之后，需要在浏览器以附件的形式下载，所以可以用二进制的形式进行读取
    excel = open(dest_filename,"rb")
    # FileResponse 该类可以将文件下载到浏览器
    response = FileResponse(excel)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

