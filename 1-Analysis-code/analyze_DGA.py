"""
分析DGA情况
"""
from config import ransomware_csv_dir, benign_csv_dir, result_dir
from utils import is_clean_domain
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json
from tqdm import tqdm
import re


samples = [
    2962,
    2993,
    3155,
    3836,
    4517,
    5391,
    7900,
    7916,
    9255,
    9739,
    9925
]


if __name__ == '__main__':
    # 统计信息
    sample_dns_address = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for sample_id in samples:
        df = pd.read_csv(f'{ransomware_csv_dir}/{sample_id}.csv', index_col=0)
        for _, row in df.iterrows():
            if row['protocol'] == 'DNS':
                if row['info'].startswith('Standard query response'):
                    # DNS结果:
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
                    if is_clean_domain(target):
                        continue

                    if t == 'Refused' or t == 'No such name' or t == 'Server failure':
                        sample_dns_address[sample_id]['response'][t].append(f'{target}')
                    else:
                        sample_dns_address[sample_id]['response'][t].append(f'{target},{real_addr}')
                else:
                    # DNS请求
                    target = row['info'].split(' ')[-1]
                    if is_clean_domain(target):
                        continue
                    sample_dns_address[sample_id]['request']['req'].append(target)
    with open(f'./statistical_result/DGA.json', 'w') as f:
        f.write(json.dumps(sample_dns_address, ensure_ascii=False, indent=4))
