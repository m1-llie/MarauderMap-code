import os
import json
from tqdm import tqdm
from collections import defaultdict


# process_multiple_agents = defaultdict(list)
# for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
#     try:
#         sample_id = int(file.split('.')[0])
#         with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
#             dct = json.loads(f.read())
#         for sig in dct['signatures']:
#             if sig['name'] == 'multiple_useragents':
#                 process_multiple_agents[sample_id].append(sig)
#     except Exception as e:
#         print(f"{file} error: {e}")
#
# with open('./statistical_result/multiple_agents.json', 'w') as f:
#     f.write(json.dumps(process_multiple_agents, ensure_ascii=False, indent=4))

agents_combination = defaultdict(int)
with open('./statistical_result/multiple_agents.json', 'r') as f:
    dct = json.loads(f.read())
    for pid in dct.keys():
        lst = []
        for d in dct[pid][0]['data']:
            if 'user-agent' in d:
                lst.append(d['user-agent'])
        agents_combination['|'.join(lst)] += 1

for k, v in agents_combination.items():
    print(k.split('|'))
    print(v)
    print()