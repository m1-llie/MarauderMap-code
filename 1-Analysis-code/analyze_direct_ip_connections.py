import os
import json
from tqdm import tqdm
from collections import defaultdict


process_direct_ip_connections = defaultdict(list)
for file in tqdm(os.listdir("D:\\reportjson-all-in-all")):
    try:
        sample_id = int(file.split('.')[0])
        with open(f"D:\\reportjson-all-in-all\\{sample_id}.json", 'r', encoding='utf-8') as f:
            dct = json.loads(f.read())
        for sig in dct['signatures']:
            if sig['name'] == 'network_multiple_direct_ip_connections':
                process_direct_ip_connections[sample_id].append(sig)
    except Exception as e:
        print(f"{file} error: {e}")

with open('./statistical_result/direct_ip_connections.json', 'w') as f:
    f.write(json.dumps(process_direct_ip_connections, ensure_ascii=False, indent=4))
