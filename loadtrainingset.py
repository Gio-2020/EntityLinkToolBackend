import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
from temp.models import KB, TrainingSet
from django.db import transaction
def load_training_set():
    sid = transaction.savepoint()
    path = './ccks2019_el/train.json' 
    with open(path, 'r', encoding = 'utf-8') as trainingSet:
        while True:
            line = trainingSet.readline()
            if not line:
                break
            obj = json.loads(line)
            text_id = obj['text_id']
            text = obj['text']
            data = obj['mention_data']


            # if int(text_id) > 10:
            #     break
            # print(type(obj))
            for i in data:
                # entity_index = str(i['kb_id'])
                # print(entity_index)
                try:
                    entity_kb = KB.objects.get(subject_id = str(i['kb_id']))
                    TrainingSet.objects.create(segment_id = text_id, text = text,
                    entity = i['mention'], subject = entity_kb.subject,
                    entity_description = entity_kb.data)
                except:
                    TrainingSet.objects.create(segment_id = text_id, text = text,
                    entity = i['mention'], subject = 'NIL')
            # break
            if int(text_id) % 100 ==0:
                transaction.savepoint_commit(sid)
                transaction.commit()
        transaction.commit()

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