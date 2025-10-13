import os
import numpy as np
import librosa
import csv
from fast_bss_eval import si_bss_eval_sources

# Sampling rate
sr = 44100

# Evaluation for the MUSDB data set

# Track list of the MUSDB data set
track_list_musdb = ['bass', 'drums', 'other', 'vocals']

# Load reference tracks from MUSDB
path_to_reference_musdb = './data/audio_for_separation/full_musdb_tracks/'
ref_tracks_musdb = []
ref_labels_musdb = []
ref_songs_musdb = []
for song_name in os.listdir(path_to_reference_musdb):
    # Folder containing the tracks of the song
    path_to_song = os.path.join(path_to_reference_musdb, song_name)
    if not os.path.isdir(path_to_song):
        continue
    temp_tracks = []
    temp_labels = []
    for fname in os.listdir(path_to_song):
        # It should be a wavfile
        if not fname.endswith('.wav'):
            continue
        label = fname.split('.')[0]
        path_to_track = os.path.join(path_to_song, fname)
        track_audio, _ = librosa.load(path_to_track, sr=sr)
        temp_tracks.append(track_audio)
        temp_labels.append(label)
    
    # Sort tracks in alphabetical order
    temp_tracks = np.array(temp_tracks)
    temp_labels = np.array(temp_labels)
    track_order = np.argsort(temp_labels)
    temp_tracks = temp_tracks[track_order]
    temp_labels = temp_labels[track_order]

    ref_tracks_musdb.append(temp_tracks)
    ref_labels_musdb.append(temp_labels)
    ref_songs_musdb.append(song_name)

# Load estimated tracks from MUSDB
path_to_estimates_musdb = './data/audio_for_separation/estimated_full_musdb/htdemucs/'
est_tracks_musdb = []
est_labels_musdb = []
est_songs_musdb = []
for song_name in os.listdir(path_to_estimates_musdb):
    song_index = [idx for idx, item in enumerate(ref_songs_musdb) if item == song_name]
    # Continue if the song does not exists
    if len(song_index) == 0:
        continue
    song_index = song_index[0]
    temp_tracks = []
    temp_labels = []

    # Folder containing the estimated tracks of the song
    path_to_song = os.path.join(path_to_estimates_musdb, song_name)
    for fname in os.listdir(path_to_song):
        if not fname.endswith('.wav'):
            continue
        label = fname.split('.')[0]
        if label in track_list_musdb:
            path_to_track = os.path.join(path_to_song, fname)
            track_audio, _ = librosa.load(path_to_track, sr=sr)
            temp_tracks.append(track_audio)
            temp_labels.append(label)
    
    # Sort tracks in alphabetical order
    temp_tracks = np.array(temp_tracks)
    temp_labels = np.array(temp_labels)
    track_order = np.argsort(temp_labels)
    temp_tracks = temp_tracks[track_order]
    temp_labels = temp_labels[track_order]

    est_tracks_musdb.append(temp_tracks)
    est_labels_musdb.append(temp_labels)
    est_songs_musdb.append(song_name)

# SDR evaluation
path_to_csv = './output/evaluation_results_musdb.csv'
results_csv = open(path_to_csv, 'w')
csv_writer = csv.writer(results_csv)

# Write the header on the CSV file
header = ['song_name'] + [f'sdr_{track}' for track in track_list_musdb]
csv_writer.writerow(header)

# Iterate over every reference song
for ref_index, ref_song in enumerate(ref_songs_musdb):
    # Match the index of the estimated tracks
    est_index = [idx for idx, item in enumerate(est_songs_musdb) if item == ref_song]
    est_index = est_index[0]

    # Scale-invariant SDR
    sdr, _, _, _ = si_bss_eval_sources(ref_tracks_musdb[ref_index], est_tracks_musdb[est_index])

    # SDR values for each track in the song
    sdr_values = [sdr[src_index] for src_index, _ in enumerate(ref_labels_musdb[ref_index])]
    csv_row = np.concatenate(([ref_song], sdr_values))
    csv_writer.writerow(csv_row)

results_csv.close()

# Evaluation for the EgoMusic data set

# Track list of EgoMusic
track_list_demucs = ['bass', 'drums', 'other', 'vocals']
track_list_egomusic = ['bass', 'guitar', 'percussion', 'piano', 'vocals']

# Load reference tracks from EgoMusic
path_to_reference_egomusic = './data/audio_for_separation/full_egomusic_tracks/'
ref_tracks_egomusic = []
ref_labels_egomusic = []
ref_songs_egomusic = []
for song_name in os.listdir(path_to_reference_egomusic):
    # Folder containing the tracks of the song
    path_to_song = os.path.join(path_to_reference_egomusic, song_name)
    if not os.path.isdir(path_to_song):
        continue
    temp_tracks = []
    temp_labels = []
    for fname in os.listdir(path_to_song):
        # It should be a wavfile
        if not fname.endswith('.wav'):
            continue
        label = fname.split('.')[0]
        if label not in track_list_egomusic:
            continue

        # Change track labels according to htdemucs output
        if label == 'percussion':
            label = 'drums'
        elif label in ['guitar', 'piano']:
            label = 'other'
        
        # Load track audio
        path_to_track = os.path.join(path_to_song, fname)
        track_audio, _ = librosa.load(path_to_track, sr=sr)
        temp_tracks.append(track_audio)
        temp_labels.append(label)
    
    # Sort tracks in alphabetical order
    temp_tracks = np.array(temp_tracks)
    temp_labels = np.array(temp_labels)
    track_order = np.argsort(temp_labels)
    temp_tracks = temp_tracks[track_order]
    temp_labels = temp_labels[track_order]

    ref_tracks_egomusic.append(temp_tracks)
    ref_labels_egomusic.append(temp_labels)
    ref_songs_egomusic.append(song_name)

# Load estimated tracks from MUSDB
path_to_estimates_egomusic = './data/audio_for_separation/estimated_full_egomusic/htdemucs/'
est_tracks_egomusic = []
est_labels_egomusic = []
est_songs_egomusic = []
for song_name in os.listdir(path_to_estimates_egomusic):
    song_index = [idx for idx, item in enumerate(ref_songs_egomusic) if item == song_name]
    # Continue if the song does not exists
    if len(song_index) == 0:
        continue
    song_index = song_index[0]
    temp_tracks = []
    temp_labels = []

    # Folder containing the estimated tracks of the song
    path_to_song = os.path.join(path_to_estimates_egomusic, song_name)
    for fname in os.listdir(path_to_song):
        if not fname.endswith('.wav'):
            continue
        label = fname.split('.')[0]
        if label in track_list_demucs:
            path_to_track = os.path.join(path_to_song, fname)
            track_audio, _ = librosa.load(path_to_track, sr=sr)
            temp_tracks.append(track_audio)
            temp_labels.append(label)
    
    # Sort tracks in alphabetical order
    temp_tracks = np.array(temp_tracks)
    temp_labels = np.array(temp_labels)
    track_order = np.argsort(temp_labels)
    temp_tracks = temp_tracks[track_order]
    temp_labels = temp_labels[track_order]

    est_tracks_egomusic.append(temp_tracks)
    est_labels_egomusic.append(temp_labels)
    est_songs_egomusic.append(song_name)

# SDR evaluation
path_to_csv = './output/evaluation_results_egomusic.csv'
results_csv = open(path_to_csv, 'w')
csv_writer = csv.writer(results_csv)

# Write the header on the CSV file
header = ['song_name'] + [f'sdr_{track}' for track in track_list_demucs]
csv_writer.writerow(header)

# Iterate over every reference song
for ref_index, ref_song in enumerate(ref_songs_egomusic):
    # Match the index of the estimated tracks
    est_index = [idx for idx, item in enumerate(est_songs_egomusic) if item == ref_song]
    est_index = est_index[0]

    # Scale-invariant SDR
    sdr, _, _, _ = si_bss_eval_sources(ref_tracks_egomusic[ref_index], est_tracks_egomusic[est_index])

    sdr_values_row = np.full(len(track_list_demucs), None)
    # SDR values for each track in the song
    for src_index, source in enumerate(ref_labels_egomusic[ref_index]):
        index = [idx for idx, item in enumerate(track_list_demucs) if item == source]
        index = index[0]

        sdr_values_row[index] = sdr[src_index]

    csv_row = np.concatenate(([ref_song], sdr_values_row))
    csv_writer.writerow(csv_row)

results_csv.close()