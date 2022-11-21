# excel生成脚本
import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
from temp.models import KB, TrainingSet
import pathlib, xlsxwriter
def makeexcel():
    dest_filename = './static/result.xlsx'
    if pathlib.Path(dest_filename).exists():
        print('done')
        return
    else:
        print('todo')
    wb = xlsxwriter.Workbook(dest_filename)
    ws = wb.add_worksheet('trainingset')
    row_num = 0
    # 设置表头
    columns = ['auto_increment_id', 'segment_id', 'text', 'entity',
                'entity_kb','data']
    for col_num in range(len(columns)):
    	#表头写入第一行
        ws.write(row_num, col_num, columns[col_num])
        #从数据库获取指定字段的数据
    rows = TrainingSet.objects.values_list('auto_increment_id',
    'segment_id','text', 'entity', 'subject', 'entity_description')
    for row in rows:
        row_num += 1
        #此时row是元组形式，需转换成列表的形式
        row = list(row)
        # print(row)
        for col_num in range(len(row)):
            # ws.write(row_num, col_num, row[col_num])
            pairs = ''
            for i in row[5]:
                pairs += i['predicate']
                pairs += ':'
                pairs += i['object']
                pairs += '|'
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
            ws.write(row_num, 5, pairs)
        # break
    wb.close()
    return
if __name__ == "__main__":
    start = time.time()
    makeexcel()
    # test()
    print('Done!')
    end = time.time()
    print('Running time: %s Seconds'%(end-start))