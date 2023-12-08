import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import os


df = pd.read_csv('data/animagus.csv', index_col=0)
t0 = None
for _, row in df.iterrows():
    t0 = row['time']
    break
df['time'] = (df['time'] - t0) / 1e12

all_files = set()
for root, dirs, files in os.walk('../../Animgaus/ransomware_ochestration/target/release/files'):
    for name in files:
        all_files.add(name)

read_set = set()
write_set = set()
read_x = []
read_y = []
write_x = []
write_y = []
for _, row in df.iterrows():
    fname = row['file_name'].split('\\')[-1]
    if fname not in all_files:
        continue

    if row['major_opr'] == 'IRP_MJ_READ':
        read_set.add(fname)
        read_x.append(row['time'])
        read_y.append(len(read_set) / len(all_files) * 100)
    elif row['major_opr'] == 'IRP_MJ_WRITE':
        write_set.add(fname)
        write_x.append(row['time'])
        write_y.append(len(write_set) / len(all_files) * 100)

plt.figure()
plt.plot(read_x, read_y)
plt.plot(write_x, write_y)
plt.legend(['read', 'write'])
plt.show()
