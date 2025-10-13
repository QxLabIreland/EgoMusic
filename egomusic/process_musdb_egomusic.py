import librosa
from egomusic.utils import *
from scipy.io import wavfile

# Sampling rate
sr = 44100

# Save separation files here
path_to_output_audio = './data/audio_for_separation/'

# Process full EgoMusic data set for separation
path_to_egomusic = './data/EgoMusic'
sessions = ['session-1-instruments-2', 'session-2-instruments-3', 'session-3-instruments-4']
songs = ['amazing-grace', 'black-is-the-colour', 'the-house-of-the-rising-sun', 'wayfaring-stranger', 'whiskey-in-the-jar']
aria_locs = ['aria-near', 'aria-mid', 'aria-far', 'aria-static']
track_names = ['vocals', 'percussion', 'bass', 'guitar', 'piano']
for session in sessions:
    # Songs included in the session
    path_to_session = os.path.join(path_to_egomusic, session)
    session_songs = [directory for directory in os.listdir(path_to_session) if directory.split('_')[0] in songs]

    for session_song in session_songs:
        # Obtain the mixture and the tracks for this song
        path_to_session_song = os.path.join(path_to_session, session_song)
        path_to_refs = os.path.join(path_to_session_song, 'refs')

        accompaniment_tracks = []       # These are the tracks without the vocals
        for fname in os.listdir(path_to_refs):
            track_label = fname.split('_')[-1].split('.')[0]
            # Obtain the dry mix as the reference file
            if 'mix_dry.wav' in fname:
                path_to_reference_audio = os.path.join(path_to_refs, fname)

                # Resample to 44.1k and convert stereo to mono
                reference_audio, _ = librosa.load(path_to_reference_audio, sr=sr, mono=True)
    
                # Save wav file
                path_to_reference_output = os.path.join(path_to_output_audio, 'full_egomusic')
                reference_output_fname = f'{session_song}.wav'

                # Create directory if it does not exists
                os.makedirs(path_to_reference_output, exist_ok=True)

                path_to_reference_output_fname = os.path.join(path_to_reference_output, reference_output_fname)
                wavfile.write(path_to_reference_output_fname, sr, float32_to_int16(reference_audio))
                print(f'Wrote successfully to {path_to_reference_output_fname}.')
            # Obtain the tracks
            elif track_label in track_names:
                path_to_track_audio = os.path.join(path_to_refs, fname)
                track_audio, _ = librosa.load(path_to_track_audio, sr=sr, mono=True)
                if track_label != 'vocals':
                    accompaniment_tracks.append(track_audio)

                # Create directory if it does not exists
                path_to_reference_tracks = os.path.join(path_to_output_audio, 'full_egomusic_tracks', session_song)
                os.makedirs(path_to_reference_tracks, exist_ok=True)

                # Save wav file
                path_to_reference_track = os.path.join(path_to_reference_tracks, f'{track_label}.wav')
                wavfile.write(path_to_reference_track, sr, float32_to_int16(track_audio))
                print(f'Wrote successfully to {path_to_reference_track}.')
            else:
                continue
        
        # Save the accompaniment track
        path_to_reference_tracks = os.path.join(path_to_output_audio, 'full_egomusic_tracks', session_song)
        accompaniment_track = np.sum(np.array(accompaniment_tracks), axis=0)
        path_to_accompaniment_track = os.path.join(path_to_reference_tracks, 'no_vocals.wav')
        wavfile.write(path_to_accompaniment_track, sr, float32_to_int16(accompaniment_track))
        print(f'Wrote successfully to {path_to_accompaniment_track}.')
