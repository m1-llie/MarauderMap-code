import json
import os
from tqdm import tqdm
from collections import defaultdict


process_download_data = defaultdict(lambda: defaultdict(list))
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for process_data in dct['behavior']['processes']:
            process_id = process_data['process_id']
            process_name = process_data['process_name']
            for call in process_data['calls']:
                if call['category'] == 'network':
                    process_download_data[sample_id][f"{process_id}-{process_name}"].append(call.copy())
    except Exception as e:
        print(f"{file} error: {e}")


with open('./statistical_result/powershell_download.json', 'w') as f:
    f.write(json.dumps(process_download_data, ensure_ascii=False, indent=4))
