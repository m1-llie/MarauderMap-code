import json
import os
from tqdm import tqdm
from collections import defaultdict


record = defaultdict(list)
for file in tqdm(os.listdir("C:\\Users\\gary\\Desktop\\reportjson-all-in-all")):
    try:
        with open(f'C:\\Users\\gary\\Desktop\\reportjson-all-in-all\\{file}', 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for process in dct['behavior']['processes']:
            record[file].append(process['process_name'])
    except Exception as e:
        print(f'{file} error: {e}')

with open(f'./statistical_result/process_names.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(record, ensure_ascii=False, indent=4))
