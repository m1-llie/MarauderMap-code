import pandas as pd
import os
import matplotlib.pyplot as plt
from config import ransomware_csv_dir
from collections import defaultdict
import seaborn as sns
import pyshark
from utils import is_clean_domain
import numpy as np


if __name__ == '__main__':
    for file in os.listdir(ransomware_csv_dir):
        sample_id = int(file.split('.')[0])
        if not (6984 <= sample_id <= 7001):
            continue
        print(f"processing {file}")
        protocols = defaultdict(list)
        try:
            df = pd.read_csv(f"{ransomware_csv_dir}/{file}")
            for idx, row in df.iterrows():
                if is_clean_domain(row['src']) or is_clean_domain(row['dst']) or (row['protocol'] == 'DNS' and is_clean_domain(row['info'].split(' ')[-1])):
                    continue

                protocols[row['protocol']].append(row['time'])
            plt.figure()
            draw_values = []
            draw_labels = []
            for k, v in sorted(protocols.items(), key=lambda x : len(x[1]), reverse=True)[::]:
                draw_values.append(v)
                draw_labels.append(k)

            plt.hist(draw_values, np.linspace(0, 420, 21), label=draw_labels)
            plt.legend()
            plt.show()
        except:
            pass
        