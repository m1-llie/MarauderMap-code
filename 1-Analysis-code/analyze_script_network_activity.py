import json
import os
from tqdm import tqdm
from collections import defaultdict


process_script_network = defaultdict(list)
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for sig in dct['signatures']:
            if sig['name'] == 'script_network_activity':
                for d in sig['data']:
                    if 'pid' not in d:
                        continue
                    pid = d['pid']
                    cid = d['cid']
                    for process_data in dct['behavior']['processes']:
                        if process_data['process_id'] == pid:
                            process_script_network[sample_id].append([process_data['first_seen'], process_data['calls'][cid].copy()])
    except Exception as e:
        print(f'{file} error: {e}')

with open('./statistical_result/script_network.json', 'w') as f:
    f.write(json.dumps(process_script_network, ensure_ascii=False, indent=4))
