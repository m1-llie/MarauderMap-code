from config import ransomware_csv_dir, benign_csv_dir, result_dir
from utils import is_clean_domain
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
import os
import json
from tqdm import tqdm


samples = [
    529,
    264,
    289,
    595,
    298,
    616,
    418,
    666,
    459,
    3150,
    4496,
    3718,
    6613,
    6615,
    6756,
    6988,
    6989,
    6990,
    6991,
    6992,
    6993,
    6994,
    6995,
    6997,
    6998,
    6999,
    8175,
    9249,
    9252,
    9323,
    9403,
    8553,
    9438,
    8580,
    9440,
    9442,
    8745,
    8835,
    9821,
    9871
]


if __name__ == '__main__':
    # ping_address_count = defaultdict(int)
    # ping_of_each_file = defaultdict(list)
    # for file in tqdm(os.listdir(ransomware_csv_dir)):
    #     sample_id = int(file.split('.')[0])
    #     try:
    #         df = pd.read_csv(f'{ransomware_csv_dir}/{file}', index_col=0)
    #         existed_address = set()
    #         for idx, row in df.iterrows():
    #             if row['protocol'] == 'ICMP':
    #                 if row['dst'] not in existed_address:
    #                     existed_address.add(row['dst'])
    #                     ping_address_count[row['dst']] += 1
    #                 ping_of_each_file[sample_id].append([row['src'], row['dst'], row['info']])
    #     except:
    #         print(f"{sample_id} error!")
    #
    # with open(f'{result_dir}/ping_address_count.json', 'w') as f:
    #     f.write(json.dumps(ping_address_count, ensure_ascii=False, indent=4))
    #
    # with open(f"{result_dir}/ping_of_each_file.json", 'w') as f:
    #     f.write(json.dumps(ping_of_each_file, ensure_ascii=False, indent=4))
    for sample_id in sorted(samples):
        print(sample_id)
        df = pd.read_csv(f'{ransomware_csv_dir}/{sample_id}.csv', index_col=0)
        df = df[df['protocol'] == 'ICMP']
        req_num = 0
        reply_success_number = 0
        reply_fail_number = 0
        for _, row in df.iterrows():
            # print(row['src'], row['dst'], row['info'])
            if row['info'].startswith('Echo (ping) request'):
                req_num += 1
            elif row['info'].startswith('Echo (ping) reply'):
                reply_success_number += 1
            else:
                reply_fail_number += 1
        with open(f'./glh.csv', 'a') as f:
            f.write(f'{sample_id},{req_num+reply_success_number+reply_fail_number},{req_num},{reply_success_number},{reply_fail_number}\n')

