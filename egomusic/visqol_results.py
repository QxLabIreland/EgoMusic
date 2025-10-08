import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# Get VISQOL results
path_to_visqol_results = './output/results_audio_files.csv'
df = pd.read_csv(path_to_visqol_results)
test_fnames = df['degraded'].to_numpy()
test_mos = df['moslqo'].to_numpy()

song_names = [fname.split('/')[-5] for fname in test_fnames]
aria_locs = [fname.split('/')[-4].split('-')[-1] for fname in test_fnames]
beam_groups = [fname.split('/')[-2] for fname in test_fnames]

# # VISQOL results in long format
df_long = pd.DataFrame(np.column_stack((song_names, aria_locs, beam_groups, test_mos)), 
                       columns = ['song', 'location', 'group', 'mos'])

print(df_long[['location', 'group', 'mos']])
# Box plots
ax = sns.boxplot(data=df_long[['location', 'group', 'mos']], x = 'group', y = 'mos', hue = 'location')
# ax.set_ylim(1.0, 5.0)
ax.legend(loc = 'upper center', ncol=4)
# plt.savefig('./output/visqol_results.jpg', bbox_inches='tight', dpi=300)
plt.show()