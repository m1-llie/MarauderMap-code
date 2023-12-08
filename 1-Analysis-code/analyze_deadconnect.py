import json
import os
from collections import defaultdict
from tqdm import tqdm


process_connect_data = defaultdict(lambda: defaultdict(list))
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for process_data in dct['behavior']['processes']:
            process_id = process_data['process_id']
            process_name = process_data['process_name']
            for call in process_data['calls']:
                if call['category'] == 'network' and call['api'] == 'connect':
                    process_connect_data[f"{sample_id}"][f"{process_id}-{process_name}"].append([call['timestamp'], call['arguments'][1]['value'] + ':' + call['arguments'][2]['value'], call['status']])
    except Exception as e:
        print(f"{sample_id} error: {e}")

with open(f'./statistical_result/deadconnect.json', 'w') as f:
    f.write(json.dumps(process_connect_data, ensure_ascii=False, indent=4))
