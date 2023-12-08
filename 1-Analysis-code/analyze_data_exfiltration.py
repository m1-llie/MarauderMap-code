import re

import pandas as pd
from tqdm import tqdm
import os
import json
from collections import defaultdict


def collect_sample_process():
    root_dir = "C:\\Users\\gary\\Desktop\\reportjson-all-in-all"
    sample_processes = defaultdict(list)
    for file in tqdm(os.listdir(root_dir)):
        try:
            sample_id = int(file.split('.')[0])
            with open(f'{root_dir}\\{file}', 'r', encoding='utf-8') as f:
                dct = json.loads(f.read())
            for process_data in dct['behavior']['processes']:
                process_name = process_data['process_name']
                process_path = process_data['module_path']
                sample_processes[sample_id].append(f"{process_name}-{process_path}")
            with open(f'./statistical_result/sample_process/{sample_id}.json', 'w', encoding='utf-8') as g:
                g.write(json.dumps(sample_processes[sample_id], ensure_ascii=False, indent=4))
        except Exception as e:
            print(f'{file} error: {e}')

    with open(f'./statistical_result/sample_process.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(sample_processes, ensure_ascii=False, indent=4))


def calculate_network_size():
    rec = defaultdict(int)
    for file in tqdm(os.listdir('G:\\empirical_data\\ransomware_network')):
        df = pd.read_csv(f'G:\\empirical_data\\ransomware_network\\{file}', index_col=0)
        local_ip = ''
        pat = re.compile('192.168.88.\d\d\d')
        for _, row in df.iterrows():
            if pat.match(row['src']):
                local_ip = row['src']
                break
            elif pat.match(row['dst']):
                local_ip = row['dst']
                break
        df = df[df['src'] == local_ip]
        total_size_out = sum(df['length'])
        rec[file] = total_size_out
    with open(f'./statistical_result/network_size.txt', 'w') as f:
        for k, v in sorted(rec.items(), key=lambda item: item[1], reverse=True):
            f.write(f'{k},{v}\n')


if __name__ == '__main__':
    calculate_network_size()
    