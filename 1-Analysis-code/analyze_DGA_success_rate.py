from collections import defaultdict
import numpy as np
import json
from utils import is_clean_domain
import os
from tqdm import tqdm
import pandas as pd


if __name__ == '__main__':
    malicious_domains = set()
    sample_ids = []

    with open('./statistical_result/DGA1.json', 'r', encoding='utf-8') as f:
        DGA_json = json.loads(f.read())

    for sample_id, lst in DGA_json.items():
        sample_ids.append(sample_id)
        for domain_name in lst:
            if is_clean_domain(domain_name):
                continue
            malicious_domains.add(domain_name)

    query_cnt = 0
    query_success_cnt = 0

    for sample_id in sample_ids:
        df = pd.read_csv(f'./data/ransomware_filtered/{sample_id}.csv', index_col=0)
        df = df[df['protocol'] == "DNS"]
        for _, row in df.iterrows():
            if row['info'].startswith('Standard query response'):
                target = None
                real_addr = None
                t = None
                # 1. Standard query response 0xdddd Refused A address
                if 'Refused' in row['info']:
                    target = row['info'].split(' ')[-1]
                    t = 'Refused'
                # 2. Standard query response 0xdddd No such name
                elif 'No such name' in row['info']:
                    target = row['info'].split(' ')[8]
                    t = 'No such name'
                # 3. Standard query response 0xdddd Server failure
                elif 'Server failure' in row['info']:
                    target = row['info'].split(' ')[-1]
                    t = 'Server failure'
                # 3. Standard query
                else:
                    target = row['info'].split(' ')[5]
                    real_addr = row['info'].split(' ')[-1]
                    t = 'success'

                if target in malicious_domains and t == 'success':
                    query_success_cnt += 1
            else:
                target = row['info'].split(' ')[-1]
                if target in malicious_domains:
                    query_cnt += 1

    print(query_success_cnt, query_cnt, query_success_cnt / query_cnt)

