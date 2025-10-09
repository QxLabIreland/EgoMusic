import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Get VISQOL results
path_to_visqol_results = './output/results_audio_files.csv'
df = pd.read_csv(path_to_visqol_results)
test_fnames = df['degraded'].to_numpy()
test_mos = df['moslqo'].to_numpy()

song_names = [fname.split('/')[-5].split('_')[0] for fname in test_fnames]
aria_locs = [fname.split('/')[-4].split('-')[-1] for fname in test_fnames]
beam_groups = [fname.split('/')[-2] for fname in test_fnames]

# VISQOL results in long format
df_long = pd.DataFrame({
    'song': song_names,
    'location': aria_locs,
    'group': beam_groups,
    'mos': test_mos
})

# Box plots
ax = sns.boxplot(data=df_long, x = 'group', y = 'mos', hue = 'location')
ax.set_ylim(1.0, 5.0)
ax.legend(loc = 'upper center', ncol=4)
plt.savefig('./output/visqol_results.jpg', bbox_inches='tight', dpi=300)
plt.show()

# Calculate average MOS across locations and groups
locations = ['near', 'mid', 'far', 'static']
groups = ['mono', 'beam3', 'beam5', 'beam7']
n_locs = len(locations)
n_groups = len(groups)
average_moslqo = np.empty((n_locs, n_groups))
mos_values_arr = []
for i, location in enumerate(locations):
    for j, group in enumerate(groups):
        mos_values = df_long[(df_long['location'] == location) & (df_long['group'] == group)]['mos'].to_numpy()
        mos_values_arr.append(mos_values)
        average_moslqo[i, j] = np.mean(mos_values)

print('Average MOS across locations (rows) and beamforming groups (columns)')
print(average_moslqo)

# Compute statistical significance across locations and groups
for i, location in enumerate(locations):
    stat, pvalue = f_oneway(mos_values_arr[n_locs * i], mos_values_arr[(n_locs * i) + 1], mos_values_arr[(n_locs * i) + 2], mos_values_arr[(n_locs * i) + 3])
    print(f'One-way ANOVA for location {location} across beamforming groups: p-value = {pvalue}')

for j, group in enumerate(groups):
    stat, pvalue = f_oneway(mos_values_arr[j], mos_values_arr[(n_locs * 1) + j], mos_values_arr[(n_locs * 2) + j], mos_values_arr[(n_locs * 3) + j])
    print(f'One-way ANOVA for beamforming group {group} across aria locations: p-value = {pvalue}')
