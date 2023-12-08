import os
from tqdm import tqdm
import pandas as pd
from config import ransomware1888_id


cnt = 0

for file in tqdm(os.listdir("./data/ransomware_filtered")):
    sample_id = int(file.split('.')[0])
    if sample_id not in ransomware1888_id:
        continue
    df = pd.read_csv(f'./data/ransomware_filtered/{file}', index_col=0)
    df = df[(df['protocol'] != 'DNS') & (df['protocol'] != 'NBNS')]
    if df.shape[0] != 0:
        cnt += 1
        print(file)
print(cnt)
