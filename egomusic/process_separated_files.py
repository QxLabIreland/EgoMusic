import os
import librosa
import subprocess
from scipy.io import wavfile
from egomusic.utils import *

# Convert stereo separated files to mono
# Resample from 44.1k to 48k for VISQOL analysis
# Normalise to -30 LUFS
# Create a no_vocals track

# Sampling rate
sr = 48000

# Resample all the reference tracks to 48k
path_to_ref_tracks = './data/audio_for_separation/tracks/'

# Iterate over all the reference tracks
for root, dirs, files in os.walk(path_to_ref_tracks):
    for name in files:
        if not name.endswith('.wav'):
            continue
        path_to_wavfile = os.path.join(root, name)
        ref_track_audio, _ = librosa.load(path_to_wavfile, sr=sr, mono=True)

        # Overwrite ref track
        wavfile.write(path_to_wavfile, sr, float32_to_int16(ref_track_audio))

        # Normalise to -30 LUFS
        subprocess.run(['ffmpeg-normalize', path_to_wavfile, '-o', path_to_wavfile, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
        print(f'Wrote successfully to {path_to_wavfile}.')


# Aria locations
aria_locs = ['clean', 'near', 'mid', 'far', 'static']

# Iterate over aria locations
for aria_loc in aria_locs:
    path_to_estimated_folder = f'./data/audio_for_separation/estimated_{aria_loc}/htdemucs/'

    # Iterate over every song
    for song in os.listdir(path_to_estimated_folder):
        path_to_song = os.path.join(path_to_estimated_folder, song)

        # Create accompaniment track from the mix of the track audios != vocals
        accompaniment_tracks = []

        # Iterate over every track in the song
        for track_name in os.listdir(path_to_song):
            path_to_track = os.path.join(path_to_song, track_name)

            # Read audio file as a mono track
            track_audio, _  = librosa.load(path_to_track, sr=sr, mono=True)

            if track_name != 'vocals.wav':
                accompaniment_tracks.append(track_audio)
            
            # Overwrite track audio
            wavfile.write(path_to_track, sr, float32_to_int16(track_audio))
            
            # Normalise to -30 LUFS
            subprocess.run(['ffmpeg-normalize', path_to_track, '-o', path_to_track, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
            print(f'Wrote successfully to {path_to_track}.')
        
        # Write the accompaniment track
        accompaniment_track = np.mean(np.array(accompaniment_tracks), axis=0)
        path_to_accompaniment = os.path.join(path_to_song, 'no_vocals.wav')
        wavfile.write(path_to_accompaniment, sr, float32_to_int16(accompaniment_track))

        # Normalise to -30 LUFS
        subprocess.run(['ffmpeg-normalize', path_to_accompaniment, '-o', path_to_accompaniment, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
        print(f'Wrote successfully to {path_to_accompaniment}.')