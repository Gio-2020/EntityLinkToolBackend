import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
from temp.models import KB, TrainingSet

def load_training_set():
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
            # print(type(obj))
            for i in data:
                # entity_index = str(i['kb_id'])
                # print(entity_index)
                try:
                    entity_kb = KB.objects.get(subject_id = str(i['kb_id']))
                    TrainingSet.objects.create(segment_id = text_id, text = text,
                    entity = i['mention'], entity_kb = entity_kb)
                except:
                    continue

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