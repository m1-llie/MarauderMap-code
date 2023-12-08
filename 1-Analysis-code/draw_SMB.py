import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from collections import defaultdict


plt.rcParams['font.sans-serif'] = ['Tahoma']
color = '#AFB0B2'
xlabel_size = 16
x_tick_size = 14
y_tick_size = 16
sample_ids = [
    1224,
    6984,
    6993,
    6998,
    7001
]

# for sample_id in sample_ids:
#     df = pd.read_csv(f'./data/ransomware_filtered/{sample_id}.csv', index_col=0)
#     # df = df[df['time'] < 200]
#     df = df[df['protocol'].str.contains('SMB2')]
#     print(df.shape)
#
#     fig = plt.figure()
#     sns.histplot(df['time'])
#     plt.title(f'{sample_id}')
#     plt.show()


def make_label(value, pos):
    return f'{int(value)}s'


fig = plt.figure(figsize=(10, 3))

ax = plt.subplot(121)
df = pd.read_csv('./data/ransomware_filtered/1224.csv', index_col=0)
df = df[(df['protocol'].str.contains('SMB')) & (df['dst'] == '192.168.88.1')]
df = df[(150 < df['time']) & (df['time'] < 200)]
record = defaultdict(int)
for _, row in df.iterrows():
    record[int(row['time'])] += 1

ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
ax.tick_params(axis='x', labelsize=x_tick_size)
ax.tick_params(axis='y', labelsize=y_tick_size)
plt.bar(record.keys(), record.values(), width=0.6, color=color)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('sample id: 1224', fontsize=xlabel_size)

ax = plt.subplot(122)
df = pd.read_csv('./data/ransomware_filtered/6998.csv', index_col=0)
df = df[df['protocol'].str.contains('SMB') & (df['dst'] == '192.168.88.1')]
df = df[(150 < df['time']) & (df['time'] < 180)]
record = defaultdict(int)
for _, row in df.iterrows():
    record[int(row['time'])] += 1

ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
ax.tick_params(axis='x', labelsize=x_tick_size)
ax.tick_params(axis='y', labelsize=y_tick_size)
plt.bar(record.keys(), record.values(), width=0.6, color=color)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('sample id: 6998', fontsize=xlabel_size)

fig.supylabel('SMB2 packet num', fontsize=18)
fig.tight_layout()
plt.savefig('./figure/SMB_frequency.pdf', dpi=300, bbox_inches='tight')
# plt.show()
