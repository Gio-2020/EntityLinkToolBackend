# bulk_create
import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
from temp.models import KB, TrainingSet
from django.db import transaction

# @transaction.commit_manually
# @transaction.atomic
def load_training_set():
    path = 'test_data/ccks2019_el/train.json' 
    # transaction.set_autocommit(False)
    temp = []
    # count = 0
    with open(path, 'r', encoding = 'utf-8') as trainingSet:
        while True:
            # count += 1
            line = trainingSet.readline()
            if not line:
                break
            obj = json.loads(line)
            text_id = obj['text_id']
            text = obj['text']
            data = obj['mention_data']
            for i in data:
                try:
                    entity_kb = KB.objects.get(subject_id = str(i['kb_id']))
                    # TrainingSet.objects.create(segment_id = text_id, text = text,
                    # entity = i['mention'], subject = entity_kb.subject,
                    # entity_description = entity_kb.data,
                    # training_set_name = 'mtx_test')
                    single_record = TrainingSet(segment_id = text_id, text = text,
                    entity = i['mention'], subject = entity_kb.subject,
                    entity_description = entity_kb.data,
                    training_set_name = 'mtx_test')
                    temp.append(single_record)
                except:
                    single_record = TrainingSet(segment_id = text_id, text = text,
                    entity = i['mention'], subject = 'NIL',
                    training_set_name = 'mtx_test')
                    temp.append(single_record)
            # if count % 5000 == 0:
            #     TrainingSet.objects.bulk_create(temp, batch_size = 5000)
            #     temp = []
    TrainingSet.objects.bulk_create(temp, batch_size = 5000)

def test():
    temp = TrainingSet.objects.filter(segment_id = '90000')
    print(temp[0].entity_kb.data)            

if __name__ == "__main__":
    start = time.time()
    load_training_set()
    # test()
    print('Done!')
    end = time.time()
    print('Running time: %s Seconds'%(end-start))