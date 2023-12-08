import json
import os
from tqdm import tqdm
from collections import defaultdict


process_network_activity = defaultdict(lambda: defaultdict(lambda: ["", "", []]))
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        flag = False
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for process_data in dct['behavior']['processes']:
            pid = process_data['process_id']
            process_name = process_data['process_name']
            first_seen_time = process_data['first_seen']
            for call in process_data['calls']:
                if call['category'] == 'network':
                    process_network_activity[sample_id][pid][0] = process_name
                    process_network_activity[sample_id][pid][1] = first_seen_time
                    process_network_activity[sample_id][pid][2].append(call)
                    flag = True
        if flag:
            with open(f'./statistical_result/network_activity/{sample_id}.json', 'w') as f:
                f.write(json.dumps(process_network_activity[sample_id], ensure_ascii=False, indent=4))
    except Exception as e:
        print(f'{file} error: {e}')

with open('./statistical_result/network_activity.json', 'w') as f:
    f.write(json.dumps(process_network_activity, ensure_ascii=False, indent=4))
