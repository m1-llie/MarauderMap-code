import json
import os
from tqdm import tqdm
from collections import defaultdict


record = defaultdict(list)
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for sig in dct['signatures']:
            if sig['name'] == 'recon_checkip':
                for d in sig['data']:
                    record[sample_id].append(d['domain'])
    except Exception as e:
        print(f"{sample_id} error: {e}")

with open(f'./statistical_result/checkip.json', 'w') as f:
    f.write(json.dumps(record, ensure_ascii=False, indent=4))
