import os
import json
from tqdm import tqdm
from collections import defaultdict

sample_ids = [
    1224,
    2266,
    3718,
    4403,
    6984,
    7000,
    9333,
    9583,
    9924
]


record = defaultdict(list)
for sample_id in tqdm(sample_ids):
    try:
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for sig in dct['signatures']:
            if sig['name'] == 'infostealer_browser':
                record[sample_id].append(sig)
    except Exception as e:
        print(f"{sample_id} error {e}")

with open('./statistical_result/steal_browser_information.json', 'w') as f:
    f.write(json.dumps(record, ensure_ascii=False, indent=4))
