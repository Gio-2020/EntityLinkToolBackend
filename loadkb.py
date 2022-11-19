import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
from temp.models import KB
  
def load_kb():
    path = './ccks2019_el/kb_data'
    with open(path, 'r', encoding = 'utf-8') as kbFile:
        while True:
            line = kbFile.readline()
            if not line:
                break
            obj = json.loads(line)
            alias = obj['alias']
            subject_id = obj['subject_id']
            subject = obj['subject']
            entityType = obj['type']
            data = obj['data']
            KB.objects.create(alias = alias, subject_id = subject_id,
            subject = subject, type = entityType, data = data)
  
if __name__ == "__main__":
    start = time.time()
    load_kb()
    print('Done!')
    end = time.time()
    print('Running time: %s Seconds'%(end-start))
