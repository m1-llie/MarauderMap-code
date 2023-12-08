import os
from tqdm import tqdm
import pandas as pd
import shutil
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import json
from config import benign_csv_dir
import numpy as np


record = defaultdict(int)
for file in tqdm(os.listdir("G:\\empirical_data\\ransomware_network_filtered")):
    df = pd.read_csv(f'G:\\empirical_data\\ransomware_network_filtered\\{file}', index_col=0)
    for _, row in df.iterrows():
        if row['protocol'] == 'TCP':
            s = row['info']
            idx1 = s.find('[')
            idx2 = s.find(']')
            tcp_info = s[idx1+1:idx2]
            if tcp_info.startswith('TCP Dup ACK'):
                tcp_info = 'TCP Dup ACK'
            record[tcp_info] += 1

# new_dict = defaultdict(int)
s = sum(record.values())
# for k, v in record.items():
#     if v / s * 100 < 1:
#         new_dict['others'] += v
#     else:
#         new_dict[k] = v

for k, v in sorted(record.items(), key=lambda item: item[1], reverse=True):
    print(k, v, v / s * 100)

