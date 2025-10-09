import librosa
import os
import matplotlib.pyplot as plt
from egomusic.utils import *
from librosa.feature import rms
from scipy.io import wavfile

# Sampling rate
sr = 44100

# Save audio files to path
path_to_output_audio = './data/audio_for_separation/'

# Get the directory of EgoMusic songs
path_to_egomusic = './data/EgoMusic/'
sessions = ['session-1-instruments-2', 'session-2-instruments-3', 'session-3-instruments-4']
songs = ['amazing-grace', 'black-is-the-colour', 'the-house-of-the-rising-sun', 'wayfaring-stranger', 'whiskey-in-the-jar']
aria_locs = ['aria-near', 'aria-mid', 'aria-far', 'aria-static']

for session in sessions:
    # Songs included in the session
    path_to_session = os.path.join(path_to_egomusic, session)
    session_songs = [directory for directory in os.listdir(path_to_session) if directory.split('_')[0] in songs]

    for session_song in session_songs:
        # Obtain the dry reference file of the song
        path_to_session_song = os.path.join(path_to_session, session_song)
        path_to_refs = os.path.join(path_to_session_song, 'refs')
        for fname in os.listdir(path_to_refs):
            if 'mix_dry.wav' in fname:
                reference_file = fname
        path_to_reference_audio = os.path.join(path_to_refs, reference_file)
        reference_audio, _ = librosa.load(path_to_reference_audio, sr=sr)

        # Apply peak normalisation
        normalised_ref = normalise_audio(reference_audio)

        # Acquire five 10-second samples from this song
        duration = 10.0     # in seconds
        offset_min = 1.0    # start at 1-second mark
        offset_max = len(normalised_ref) / sr - duration - 1.0     # end point excluding 1-second from the end
        offset_values = np.arange(offset_min, offset_max, duration)     # 10-second segments from start to finish

        sample_number = 0
        for offset in offset_values:
            temp_track_labels = []
            temp_track_audios = []
            temp_track_rms_arr = []
            for fname in os.listdir(path_to_refs):
                # Get reference tracks
                track_label = fname.split('_')[-1]
                track_label = track_label.split('.')[0]
                if track_label not in ['vocals', 'percussion', 'bass', 'guitar', 'piano']:
                    continue
                path_to_track_audio = os.path.join(path_to_refs, fname)
                track_audio, _ = librosa.load(path_to_track_audio, sr=sr)

                # Extract 10-second snippet from the source
                track_segment = extract_snippet(track_audio, sr=sr, duration=duration, offset=offset, silence_dur=0.5)
                
                # Compute for the RMS per frame of the track segment
                track_segment_rms = rms(y=track_segment, frame_length=2048, hop_length=512).squeeze()
                track_segment_rms_db = 10 * np.log10(track_segment_rms)
                temp_track_labels.append(track_label)
                temp_track_audios.append(track_segment)
                if track_label in ['vocals', 'bass', 'guitar', 'piano']: 
                    temp_track_rms_arr.append(track_segment_rms_db)

            # Convert python lists to numpy arrays
            temp_track_labels = np.array(temp_track_labels)
            temp_track_audios = np.array(temp_track_audios)
            temp_track_rms_arr = np.array(temp_track_rms_arr)

            # Check if all tracks have 50% activity
            threshold = -15
            percentage = 0.5
            activity = np.zeros(np.shape(temp_track_rms_arr))
            activity[temp_track_rms_arr > threshold] = 1
            percentages = np.sum(activity, axis=1) / np.shape(activity)[1]

            if not (all(percentages > percentage)):
                print('The segment does not contain activity in some of the tracks. Checking the next segment')
                continue

            # Sort according to track labels
            track_order = np.argsort(temp_track_labels)
            temp_track_labels = temp_track_labels[track_order]
            temp_track_audios = temp_track_audios[track_order]

            # Obtain reference segment
            reference_snippet = extract_snippet(reference_audio, sr, duration, offset, silence_dur=0.5, normalise=True)
            path_to_reference_output = os.path.join(path_to_output_audio, 'clean')
            reference_output_fname = f'{session_song}-clean-{sample_number+1}.wav'

            # Create directory if it does not exists
            if not os.path.exists(path_to_reference_output):
                os.makedirs(path_to_reference_output)

            # Save wav file
            path_to_reference_output_fname = os.path.join(path_to_reference_output, reference_output_fname)
            wavfile.write(path_to_reference_output_fname, sr, float32_to_int16(reference_snippet))
            print(f'Wrote successfully to {path_to_reference_output_fname}.')

            # Obtain test segments from Aria glasses
            for aria_loc in aria_locs:
                loc = aria_loc.split('-')[-1]
                path_to_aria_loc = os.path.join(path_to_session_song, aria_loc, 'audio')

                # Get data from the second microphone (at the nose bridge) of Aria glasses
                for fname in os.listdir(path_to_aria_loc):
                    if 'mic2.wav' in fname:
                        aria_audio_fname = fname
                
                path_to_aria_audio = os.path.join(path_to_aria_loc, aria_audio_fname)
                aria_audio, _ = librosa.load(path_to_aria_audio, sr=sr)

                # Extract snippet from aria audio based on the offset value
                aria_audio_snippet = extract_snippet(aria_audio, sr, duration, offset, silence_dur=0.5, normalise=True)
                path_to_aria_audio_output = os.path.join(path_to_output_audio, loc)
                aria_audio_output_fname = f'{session_song}-{loc}-{sample_number+1}.wav'

                # Create directory if it does not exists
                if not os.path.exists(path_to_aria_audio_output):
                    os.makedirs(path_to_aria_audio_output)
                
                # Save wav file
                path_to_aria_audio_output_fname = os.path.join(path_to_aria_audio_output, aria_audio_output_fname)
                wavfile.write(path_to_aria_audio_output_fname, sr, float32_to_int16(aria_audio_snippet))
                print(f'Wrote successfully to {path_to_aria_audio_output_fname}.')

            # Obtain the tracks
            path_to_reference_tracks = os.path.join(path_to_output_audio, 'tracks', f'{session_song}-{sample_number+1}')

            # Create directory if it does not exists
            if not os.path.exists(path_to_reference_tracks):
                os.makedirs(path_to_reference_tracks)

            # Iterate over the tracks
            accompaniment_tracks = []   # These are the tracks without the vocals
            for index, label in enumerate(temp_track_labels):
                reference_track = temp_track_audios[index]
                path_to_reference_track =os.path.join(path_to_reference_tracks, label + '.wav')
                wavfile.write(path_to_reference_track, sr, float32_to_int16(reference_track))
                print(f'Wrote sueccessfully to {path_to_reference_track}.')
                if label != 'vocals':
                    accompaniment_tracks.append(reference_track)
            
            accompaniment_track = np.mean(np.array(accompaniment_tracks), axis=0)    # Track without vocals
            path_to_accompaniment_track = os.path.join(path_to_reference_tracks, 'no_vocals.wav')
            wavfile.write(path_to_accompaniment_track, sr, float32_to_int16(accompaniment_track))
            print(f'Wrote sueccessfully to {path_to_accompaniment_track}.')

            # Proceed to next sample. Stop if it reaches 5 samples
            sample_number += 1
            if sample_number >= 5:
                break