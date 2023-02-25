# bulk_create
import os
import json
import time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "entityLinkTool.settings")  
django.setup()
# from temp.models import KB
from temp.models import KnowledgeBaseData, KnowledgeBaseStatistic

def load_kb():
    knowledge_base_name = 'script_ccks2019_kb'
    # knowledge_base_name = 'script_ccks2020_kb'
    temp_knowledge_base = KnowledgeBaseStatistic.objects.create(knowledge_base_name = knowledge_base_name)
    path = 'test_data/ccks2019_el/kb_data'
    # path = 'test_data/ccks2020_el/kb'
    kb = []
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
            # knowledge_base = temp_knowledge_base
            single = KnowledgeBaseData(alias = alias, subject_id = subject_id,
            subject = subject, type = entityType, data = data, knowledge_base = temp_knowledge_base)
            kb.append(single)
    KnowledgeBaseData.objects.bulk_create(kb, batch_size = 5000)

def statistic():
    knowledge_base_name = 'script_ccks2019_kb'
    # knowledge_base_name = 'script_ccks2020_kb'
    kb = KnowledgeBaseStatistic.objects.get(knowledge_base_name = knowledge_base_name)
    data = KnowledgeBaseData.objects.filter(knowledge_base = kb)
    kb.num_entity = len(data)
    similar_entity_statistic = {'1-2':0, '3-4':0, '5+':0}
    num_entity_attribute_statistic = {'1-2':0, '3-4':0, '5+':0}
    for i in data:
        if len(i.alias) <= 2:
            similar_entity_statistic['1-2'] += 1
            continue
        elif len(i.alias) <= 4:
            similar_entity_statistic['3-4'] += 1
            continue
        else:
            similar_entity_statistic['5+'] += 1
    for i in data:
        if len(i.data) <= 2:
            num_entity_attribute_statistic['1-2'] += 1
            continue
        elif len(i.data) <= 4:
            num_entity_attribute_statistic['3-4'] += 1
            continue
        else:
            num_entity_attribute_statistic['5+'] += 1
    temp_list = []
    temp_list.append(similar_entity_statistic)
    kb.similar_entity_statistic = temp_list
    temp_list = []
    temp_list.append(num_entity_attribute_statistic)
    kb.num_entity_attribute_statistic = temp_list
    kb.save()
    print(kb)

def test():
    data = KnowledgeBaseData.objects.all()
    for i in data:
        print(type(i.knowledge_base))
        break


if __name__ == "__main__":
    start = time.time()
    load_kb()
    statistic()
    # test()
    print('Done!')
    end = time.time()
    print('Running time: %s Seconds'%(end-start))
