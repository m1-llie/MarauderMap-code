import pandas as pd
import pyshark
from collections import defaultdict
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
import numpy as np
import pandas
from collections import defaultdict
import json
from utils import is_clean_domain


def filter_ransomware_csv():
    root_dir = 'data/ransomware'

    for csv_file in os.listdir(root_dir):
        file_id = int(csv_file.split('.')[0])
        print(file_id)
        df = pd.read_csv(f'{root_dir}/{csv_file}', delimiter='\t', names=['idx', 'time', 'src', 'dir', 'dst', 'protocol', 'port', 'info'])
        df = df[(~df['src'].apply(is_clean_domain)) & (~df['dst'].apply(is_clean_domain))]
        fname = csv_file.replace('tsv', 'csv')
        df.to_csv(f'data/ransomware_filtered/{fname}', index=0)


if __name__ == '__main__':
    root_dir = './data/ransomware_filtered'
    protocol_count = defaultdict(int)

    

    total = 0
    for file in os.listdir(root_dir):
        sample_id = int(file.split('.')[0])
        df = pd.read_csv(f'{root_dir}/{file}', index_col=0)
        for protocol, count in df['protocol'].value_counts().items():
            protocol_count[protocol] += count
            total += count
        
        # DNS_domains = defaultdict(int)
        # for idx, row in df.iterrows():
        #     if row['protocol'] == 'DNS':
        #         query_domain = row['info'].split(' ')[-1]
        #         # print(idx, query_domain)
        #         if is_clean_domain(query_domain):
        #             continue
        #         DNS_domains[query_domain] += 1
        # print('=====================================')
        # print(sample_id)
        # for k, v in DNS_domains.items():
        #     print(k, v)
        # print('=====================================\n')

        # SMB2_files = set()
        # for idx, row in df.iterrows():
        #     if row['protocol'] == 'SMB2':
        #         file_name = row['info'].replace('Create Request File: ', '')
        #         SMB2_files.add(file_name)
        # print('=====================================')
        # print(sample_id, len(SMB2_files))
        # for file in SMB2_files:
        #     print(file)
        # print('=====================================\n')

        # TCP_reset_count = 0
        # for idx, row in df.iterrows():
        #     if row['protocol'] == 'TCP':
        #         if '[RST, ACK]' in row['info']:
        #             TCP_reset_count += 1
        # print('=====================================')
        # print(sample_id, TCP_reset_count)
        # print('=====================================\n')

        Protocol_Port_count = defaultdict(int)
        for idx, row in df.iterrows():
            Protocol_Port_count[f"{row['protocol']}:{row['port']}"] += 1
        print('=====================================')
        print(sample_id)
        for k, v in sorted(Protocol_Port_count.items(), key=lambda x : (x[1], x[0]), reverse=True):
            print(k, v)
        print('=====================================\n')
    # with open(f'./statistical_result/ransomware_protocol_distribution.json', 'w') as f:
    #     f.write(json.dumps(protocol_count, indent=4, ensure_ascii=False))

    # draw_dct = defaultdict(int)
    # for k, v in protocol_count.items():
    #     if v < total * 0.05:
    #         draw_dct['other'] += v
    #     else:
    #         draw_dct[k] = v
    # plt.figure()
    # plt.pie(x=draw_dct.values(), labels=draw_dct.keys(), autopct='%.2f%%')
    # plt.title('72+24 ransowmare samples')
    # plt.savefig('./statistical_result/72+24 ransomware samples.png')
    # plt.show()
