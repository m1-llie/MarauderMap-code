import json

from utils import is_clean_domain
from tqdm import tqdm
import pandas as pd
import os
from collections import defaultdict


malicious_samples = {
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
    9925,
    124,
    128,
    264,
    289,
    298,
    418,
    459,
    529,
    595,
    616,
    666,
    681,
    798,
    877,
    900,
    922,
    925,
    949,
    1009,
    1073,
    1147,
    1319,
    1382,
    1401,
    1492,
    1513,
    1515,
    1524,
    1540,
    1563,
    1572,
    1693,
    1697,
    1712,
    1768,
    1903,
    2036,
    2113,
    2156,
    2230,
    2233,
    2694,
    2820,
    3117,
    3670,
    4039,
    4512,
    6402,
    6585,
    6613,
    6615,
    6998,
    7044,
    7074,
    7080,
    7103,
    7127,
    7132,
    7196,
    7210,
    7267,
    7320,
    7390,
    7403,
    7527,
    7530,
    7590,
    7710,
    7742,
    8055,
    8175,
    8399,
    8553,
    8580,
    8745,
    8835,
    9249,
    9252,
    9323,
    9403,
    9438,
    9442,
    9821,
    9913
}


def get_malicious_domain_names():
    s = set()
    with open(f'./statistical_result/malicious_domains.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            s.add(line)
    return s


if __name__ == '__main__':
    # malicious_domain_names = get_malicious_domain_names()
    # for sample_id in malicious_samples:
    #     records = []
    #     with open(f'./data/ransomware_filtered/{sample_id}.csv', 'r', encoding='utf-8') as f:
    #         for line in f.readlines():
    #             line = line.strip()
    #             lst = line.split(',')
    #             if lst[2] in malicious_domain_names or lst[4] in malicious_domain_names:
    #                 records.append(line)
    #                 continue
    #             if lst[5] == 'DNS':
    #                 info = lst[7]
    #                 if info.find('in-addr') != -1:
    #                     records.append(line)
    #                     if info.count('PTR') == 2:
    #                         add_domain = info.split(' ')[-1]
    #                         if not is_clean_domain(add_domain):
    #                             print(add_domain)
    #                             malicious_domain_names.add(info.split(' ')[-1])
    #                     continue
    #                 for s in info.split(' '):
    #                     if s in malicious_domain_names:
    #                         records.append(line)
    #                         break
    #     if len(records) != 0:
    #         with open(f'./statistical_result/malicious_network/{sample_id}.csv', 'w', encoding='utf-8') as f:
    #             for r in records:
    #                 f.write(f'{r}\n')

    # protocol_count = defaultdict(int)
    # for file in tqdm(os.listdir('./statistical_result/malicious_network')):
    #     df = pd.read_csv(f'./statistical_result/malicious_network/{file}', index_col=0, names=[
    #         'idx',
    #         'time',
    #         'src',
    #         'dir',
    #         'dst',
    #         'protocol',
    #         'port',
    #         'info'
    #     ])
    #     for _, row in df.iterrows():
    #         if row['protocol'] == 'TCP':
    #             s = str(row['info'])
    #             s = s.lower()
    #             if s.find('https') != -1:
    #                 protocol_count['https'] += 1
    #             elif s.find('http') != -1:
    #                 protocol_count['http'] += 1
    #             else:
    #                 protocol_count['TCP'] += 1
    #         else:
    #             protocol_count[row['protocol']] += 1
    # print(protocol_count)

    network_api = defaultdict(int)
    for file in tqdm(os.listdir('./statistical_result/network_activity')):
        with open(f'./statistical_result/network_activity/{file}', 'r') as f:
            dct = json.loads((f.read()))
        existed = set()
        for pid in dct:
            for network_activity in dct[pid][2]:
                api = network_activity['api']
                if api not in existed:
                    network_api[network_activity['api']] += 1
                    existed.add(api)
    for k, v in network_api.items():
        print(k, v)
