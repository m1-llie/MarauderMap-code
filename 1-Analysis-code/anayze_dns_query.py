import os
from tqdm import tqdm
import pandas as pd
from collections import defaultdict


# query_total_cnt = defaultdict(int)
# query_file_cnt = defaultdict(int)
# for file in tqdm(os.listdir("./data/ransomware_filtered")):
#     try:
#         df = pd.read_csv(f"./data/ransomware_filtered/{file}", index_col=0)
#         df = df[df['protocol'] == 'DNS']
#         existed = set()
#         for _, row in df.iterrows():
#             info = row['info']
#             if 'Standard query response' in info:
#                 continue
#             target = info.split(' ')[-1]
#             query_total_cnt[target] += 1
#             if target not in existed:
#                 existed.add(target)
#                 query_file_cnt[target] += 1
#     except Exception as e:
#         print(f'{file} error: {e}')
#
# with open(f'./statistical_result/dns_query_stat.txt', 'w') as f:
#     for k, v in sorted(query_file_cnt.items(), key=lambda item: (item[1], item[0][::-1]), reverse=True):
#         f.write(f'{k},{v},{query_total_cnt[k]}\n')
#
# lst = []
# with open(f'./statistical_result/dns_query_stat_malicious.txt', 'r') as f:
#     for line in f.readlines():
#         line = line.strip()
#         if len(line) != 0:
#             lst.append(line.split(',')[0])
# with open(f'./statistical_result/dns_query_malicious_domain_set.txt', 'w') as f:
#     for d in sorted(lst, key=lambda item: item[::-1]):
#         f.write(f'{d}\n')

# malicious_domain_set = set()
# with open('./statistical_result/dns_query_malicious_domain_set.txt', 'r') as f:
#     for line in f.readlines():
#         line = line.strip()
#         if line != '':
#             malicious_domain_set.add(line)
#
#
# def filter_func(s):
#     if 'Standard query response' in s:
#         return False
#     target = s.split(' ')[-1]
#     return target in malicious_domain_set
#
#
# for file in tqdm(os.listdir('./data/ransomware_filtered')):
#     df = pd.read_csv(f'./data/ransomware_filtered/{file}', index_col=0)
#     df = df[df['protocol'] == 'DNS']
#     df = df[df['info'].map(filter_func)]
#     if df.shape[0] != 0:
#         df.to_csv(f'./data/ransomware_malicious_dns/{file}')

record = defaultdict(list)
for file in tqdm(os.listdir('./data/ransomware_malicious_dns')):
    query_set = set()
    df = pd.read_csv(f'./data/ransomware_malicious_dns/{file}', index_col=0)
    is_rdns = False
    for _, row in df.iterrows():
        target = row['info'].split(' ')[-1]
        if 'in-addr' in target:
            is_rdns = True
            break
        query_set.add(target)
    if is_rdns:
        continue
    record[len(query_set)].append(file)
    print(file, len(query_set))

for k, v in sorted(record.items(), key=lambda item: item[0]):
    print(k, len(v), ' '.join(record[k]))
