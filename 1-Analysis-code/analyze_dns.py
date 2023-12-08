from config import ransomware_csv_dir, benign_csv_dir, result_dir
from utils import is_clean_domain
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json
from tqdm import tqdm
import re


if __name__ == '__main__':
    if os.path.exists(f'./statistical_result/dns_success.txt'):
        with open(f'./statistical_result/dns_success.txt', 'w'):
            pass

    for file in os.listdir(ransomware_csv_dir):
        sample_id = int(file.split('.')[0])
        df = pd.read_csv(f'{ransomware_csv_dir}/{file}', index_col=0)

        query_domain_count = defaultdict(int)

        out_flow = defaultdict(int)
        in_flow = defaultdict(int)

        success_count = 0
        lst = []
        for idx, row in df.iterrows():
            if not row['protocol'] == 'DNS':
                continue
            if re.match('192.168.88.1\d\d', row['src']):
                direction = 'out'
            else:
                direction = 'in'
            if direction == 'out':
                query_domain = row['info'].split(' ')[-1]
                if is_clean_domain(query_domain):
                    continue
                query_domain_count[query_domain] += 1
                out_flow[int(row['time']) // 10] += 1
            elif direction == 'in':
                if re.match('^\d+.\d+.\d+.\d+$', row['info'].split(' ')[-1]):
                    success_count += 1
                    lst.append(row['info'])
                in_flow[int(row['time']) // 10] += 1

        # with open(f'{result_dir}/dns_query/{sample_id}.json', 'w') as f:
        #     f.write(json.dumps(query_domain_count, indent=4, ensure_ascii=False))

        if len(query_domain_count) > 20:
            assert success_count == len(lst)
            with open(f'./statistical_result/dns_success.txt', 'a') as f:
                f.write(f'{sample_id},{len(query_domain_count)},{success_count}\n')
                s = '\n'.join(lst)
                f.write(f"{s}\n")
            print(sample_id, len(query_domain_count), success_count)
        