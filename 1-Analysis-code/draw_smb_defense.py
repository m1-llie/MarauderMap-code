import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from brokenaxes import brokenaxes
from matplotlib.gridspec import GridSpec
import pandas as pd
plt.rcParams['font.sans-serif'] = ['Tahoma']
# plt.rcParams['font.size'] = 12


def make_label(value, pos):
    return f'{int(value)}s'


color1 = '#FFA500'
color2 = '#1E90FF'
x_label_font_size = 34
y_label_font_size = 18
xtick_font_size = 22
ytick_font_size = 16
legend_font_size = 22
figsize = (10, 6)

fig = plt.figure(figsize=figsize)

bax = brokenaxes(xlims=((0, 2), (172, 200), (416, 420)), wspace=0.1, despine=False)

df = pd.read_csv(f'./data/ransomware_filtered/1224.csv', index_col=0)
df = df[(df['protocol'] == 'SMB2') & (df['dst'] == '192.168.88.1') & (df['time'] < 210)]

cnt = 0
xs = [0]
ys = [0]
for _, row in df.iterrows():
    xs.append(row['time'])
    cnt += 1
    ys.append(cnt)

xs.append(420)
ys.append(ys[-1])

bax.plot(xs, ys, color=color1, label='SMB2 on 445', linewidth=3)
bax.plot([min(xs), max(xs)], [0, 0], color=color2, label='SMB2 on 65511', linewidth=3)
for i in range(3):
    bax.axs[i].xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    bax.axs[i].tick_params(axis='x', labelsize=xtick_font_size)
    bax.axs[i].tick_params(axis='y', labelsize=ytick_font_size)
bax.legend(loc=[0.01, 0.74], fontsize=legend_font_size)
bax.set_xlabel('sample id: 1224', fontsize=x_label_font_size, labelpad=35)
bax.set_ylabel('Cumulative Request to SMB2 Service', fontsize=y_label_font_size, labelpad=34)
plt.subplots_adjust()
plt.savefig('./figure/smb_defense(1224).pdf', bbox_inches='tight')
# plt.show()
plt.close()


fig = plt.figure(figsize=figsize)

bax = brokenaxes(xlims=((0, 2), (150, 190), (416, 420)), wspace=0.1, despine=False)

df = pd.read_csv(f'./data/ransomware_filtered/6998.csv', index_col=0)
df = df[(df['protocol'] == 'SMB2') & (df['dst'] == '192.168.88.1') & (df['time'] < 210)]

cnt = 0
xs = [0]
ys = [0]
for _, row in df.iterrows():
    xs.append(row['time'])
    cnt += 1
    ys.append(cnt)

xs.append(420)
ys.append(ys[-1])


bax.plot(xs, ys, color=color1, label='SMB2 on 445', linewidth=3)
bax.plot([min(xs), max(xs)], [0, 0], color=color2, label='SMB2 on 65511', linewidth=3)
for i in range(3):
    bax.axs[i].xaxis.set_major_formatter(ticker.FuncFormatter(make_label))
    bax.axs[i].tick_params(axis='x', labelsize=xtick_font_size)
    bax.axs[i].tick_params(axis='y', labelsize=ytick_font_size)
bax.legend(loc=[0.01, 0.74], fontsize=legend_font_size)
bax.set_xlabel('sample id: 6998', fontsize=x_label_font_size, labelpad=35)
bax.set_ylabel('Cumulative Request to SMB2 Service', fontsize=y_label_font_size, labelpad=40)
plt.subplots_adjust()
plt.savefig('./figure/smb_defense(6998).pdf', bbox_inches='tight')
# plt.show()
plt.close()
