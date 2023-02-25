# bulk_create
import os
import json
import time
import django
import django.db
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
# from temp.models import KB, TrainingSet
from temp.models import KnowledgeBaseData, KnowledgeBaseStatistic, DatasetData, DatasetStatistic, OriginDatasetData, TrainingRecord, AnnotatedData

def load_training_set():
    path = 'test_data/ccks2019_el/train.json' 
    # path = 'test_data/ccks2020_el/train.json' 
    # transaction.set_autocommit(False)
    temp = []
    count = 0
    with open(path, 'r', encoding = 'utf-8') as trainingSet:
        knowledge_base_name = 'script_ccks2019_kb'
        # knowledge_base_name = 'script_ccks2020_kb'
        kb = KnowledgeBaseStatistic.objects.get(knowledge_base_name = knowledge_base_name)
        dataset_name = 'script_ccks2019_dataset'
        # dataset_name = 'script_ccks2020_dataset'
        dataset = DatasetStatistic.objects.create(dataset_name = dataset_name, knowledge_base_name = kb)
        while True:
            count += 1
            if (count % 10000 == 0):
                print(count)
            line = trainingSet.readline()
            if not line:
                break
            obj = json.loads(line)
            text_id = obj['text_id']
            text = obj['text']
            data = obj['mention_data']
            for i in data:
                # try:
                    # 这里有个坑，多个知识库时subject_id不是unique的
                    # entity_kb = KnowledgeBaseData.objects.get(subject_id = str(i['kb_id']))
                single_record = OriginDatasetData(segment_id = text_id, text = text,
                entity = i['mention'], subject_id = i['kb_id'], offset = i['offset'],
                dataset_name = dataset)
                temp.append(single_record)
                # except:
                #     single_record = OriginDatasetData(segment_id = text_id, text = text,
                #     entity = i['mention'], subject = 'NIL', offset = i['offset'],
                #     dataset_name = dataset)
                #     temp.append(single_record)
    OriginDatasetData.objects.bulk_create(temp, batch_size = 5000)

def test():
    temp = OriginDatasetData.objects.filter(segment_id = '90000')
    print(temp[0].entity_kb.data)            

if __name__ == "__main__":
    django.db.close_old_connections()
    print('start')
    start = time.time()
    load_training_set()
    # test()
    print('Done!')
    end = time.time()
    print('Running time: %s Seconds'%(end-start))