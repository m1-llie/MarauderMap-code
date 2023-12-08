import os
import pandas as pd
from tqdm import tqdm
import re


# query_cnt = 0
# query_success_cnt = 0
# sample_count = 0
# for file in tqdm(os.listdir('./data/ransomware_filtered')):
#     try:
#         flag = False
#         df = pd.read_csv(f'./data/ransomware_filtered/{file}', index_col=0)
#         df = df[df['protocol'] == 'DNS']
#         for _, row in df.iterrows():
#             if row['info'].find('in-addr') == -1:
#                 continue
#             if not flag:
#                 sample_count += 1
#                 flag = True
#             if not row['info'].startswith('Standard query response'):
#                 # DNS request
#                 query_cnt += 1
#             else:
#                 if row['info'].count('PTR') == 2:
#                     query_success_cnt += 1
#     except Exception as e:
#         print(f'{file} error: {e}')
#
# print(query_success_cnt, query_cnt, query_success_cnt / query_cnt)


sample_count = 0
for file in tqdm(os.listdir('./data/ransomware_filtered')):
    try:
        df = pd.read_csv(f'./data/ransomware_filtered/{file}', index_col=0)
        df = df[(df['protocol'] == 'DNS') | (df['protocol'] == 'ICMP')]
        find = False
        for idx, row in df.iterrows():
            if row['info'].find('in-addr') == -1:
                continue
            if row['info'].startswith('Standard query response') and row['info'].count('PTR') == 2:
                for i in range(1, 5):
                    if df.loc[idx+i]['protocol'] == 'ICMP':
                        sample_count += 1
                        find = True
                        break
            if find:
                break
    except Exception as e:
        print(f'{file} error: {e}')

print(sample_count)

