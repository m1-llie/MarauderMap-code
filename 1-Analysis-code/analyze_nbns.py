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
    for file in os.listdir(ransomware_csv_dir):
        sample_id = int(file.split('.')[0])
        df = pd.read_csv(f'{ransomware_csv_dir}/{file}', index_col=0)

        cnt = 0
        for idx, row in df.iterrows():
            if not row['protocol'] == 'NBNS':
                continue
            cnt += 1
        print(sample_id, cnt)
