import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import json
from collections import defaultdict
from datetime import datetime

plt.rcParams['font.sans-serif'] = ['Tahoma']
color = '#AFB0B2'
xlabel_size = 16
x_tick_size = 14
y_tick_size = 14
figsize = (10, 3)
#
# sample_ids = [
#     418,
#     616,
#     666,
#     6613,
#     6615,
#     8553,
#     8835,
#     9249,
#     9252,
#     9323,
#     9403,
#     9438,
#     9442,
#     9821
# ]


def make_label(value, pos):
    return f'{value:.1f}s'


sample_ids = [
    616,
    8553,
    8835,
    9442
]

# for sample_id in sample_ids:
#     with open(f'./statistical_result/network_activity/{sample_id}.json', 'r') as f:
#         dct = json.loads(f.read())
#     record = defaultdict(int)
#     for pid in dct:
#         start_time = datetime.strptime(dct[pid][1], '%Y-%m-%d %H:%M:%S,%f')
#         for calls in dct[pid][2]:
#             if calls['api'] == 'WNetUseConnectionW':
#                 call_time = datetime.strptime(calls['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
#                 execution_time = call_time - start_time
#                 execution_microseconds = int(execution_time.seconds * 1000 + execution_time.microseconds / 1000)
#                 record[execution_microseconds] += 1
#                 # print(start_time, call_time, execution_time)
#                 # t = int(execution_time.microseconds / 500)
#                 # record[t] += 1
#     xs = []
#     ys = []
#     for k, v in record.items():
#         xs.append(k / 1000)
#         ys.append(v)
#     fig = plt.figure()
#     plt.bar(x=xs, height=ys, width=0.01, color='grey')
#     # plt.hist(xs)
#     plt.title(f'{sample_id}')
#     plt.show()


fig = plt.figure(figsize=figsize)

ax = plt.subplot(121)
with open(f'./statistical_result/network_activity/616.json', 'r') as f:
    dct = json.loads(f.read())
record = defaultdict(int)
for pid in dct:
    start_time = datetime.strptime(dct[pid][1], '%Y-%m-%d %H:%M:%S,%f')
    for calls in dct[pid][2]:
        if calls['api'] == 'WNetUseConnectionW':
            call_time = datetime.strptime(calls['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
            execution_time = call_time - start_time
            execution_microseconds = int(execution_time.seconds * 1000 + execution_time.microseconds / 1000)
            record[execution_microseconds] += 1
xs = []
ys = []
for k, v in record.items():
    xs.append(k / 1000)
    ys.append(v)
plt.bar(x=xs, height=ys, width=0.01, color=color)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
ax.tick_params(axis='x', labelsize=x_tick_size)
ax.tick_params(axis='y', labelsize=y_tick_size)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('sample id: 616', fontsize=xlabel_size)

ax = plt.subplot(122)

with open(f'./statistical_result/network_activity/8553.json', 'r') as f:
    dct = json.loads(f.read())
record = defaultdict(int)
for pid in dct:
    start_time = datetime.strptime(dct[pid][1], '%Y-%m-%d %H:%M:%S,%f')
    for calls in dct[pid][2]:
        if calls['api'] == 'WNetUseConnectionW':
            call_time = datetime.strptime(calls['timestamp'], '%Y-%m-%d %H:%M:%S,%f')
            execution_time = call_time - start_time
            execution_microseconds = int(execution_time.seconds * 1000 + execution_time.microseconds / 1000)
            record[execution_microseconds] += 1
xs = []
ys = []
for k, v in record.items():
    xs.append(k / 1000)
    ys.append(v)
plt.bar(x=xs, height=ys, width=0.01, color=color)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
ax.tick_params(axis='x', labelsize=x_tick_size)
ax.tick_params(axis='y', labelsize=y_tick_size)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xlabel('sample id: 8553', fontsize=xlabel_size)

fig.supylabel('API invoke num', fontsize=18)
fig.tight_layout()

plt.savefig('./figure/WNetUseConnectionW.pdf', dpi=300, bbox_inches='tight')
