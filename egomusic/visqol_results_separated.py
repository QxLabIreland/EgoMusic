import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Get VISQOL results
path_to_visqol_results = './output/results_separated_files.csv'
df = pd.read_csv(path_to_visqol_results)
test_fnames = df['degraded'].to_numpy()
test_mos = df['moslqo'].to_numpy()

song_names = [fname.split('/')[-2].split('_')[0] for fname in test_fnames]
aria_locs = [fname.split('/')[-4].split('_')[-1] for fname in test_fnames]
track_names = [fname.split('/')[-1].split('.')[0] for fname in test_fnames]

# VISQOL results in long format
df_long = pd.DataFrame({
    'song': song_names,
    'location': aria_locs,
    'track': track_names,
    'mos': test_mos
})

# Calculate average MOS across locations and groups
locations = ['clean', 'near', 'mid', 'far', 'static']
tracks = ['vocals', 'drums', 'bass', 'other', 'no_vocals']
n_locs = len(locations)
n_tracks = len(tracks)
average_moslqo = np.empty((n_locs, n_tracks))
mos_values_arr = []
for i, location in enumerate(locations):
    for j, track in enumerate(tracks):
        mos_values = df_long[(df_long['location'] == location) & (df_long['track'] == track)]['mos'].to_numpy()
        mos_values_arr.append(mos_values)
        average_moslqo[i, j] = np.mean(mos_values)

print('Average MOS across locations (rows) and tracks (columns)')
print(average_moslqo)

for j, track in enumerate(tracks):
    # Exclude the clean tracks
    stat, pvalue = f_oneway(mos_values_arr[(n_locs * 1) + j], mos_values_arr[(n_locs * 2) + j], mos_values_arr[(n_locs * 3) + j], mos_values_arr[(n_locs * 4) + j])
    print(f'One-way ANOVA for track {track} across aria locations: p-value = {pvalue}')