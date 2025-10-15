import librosa
import os
import subprocess
from egomusic.utils import *
from scipy.io import wavfile

# Process EgoMusic data for VISQOL analysis

# Sampling rate
sr = 48000

# Get the directory of EgoMusic songs
path_to_egomusic = './data/EgoMusic/'
sessions = ['session-1-instruments-2', 'session-2-instruments-3', 'session-3-instruments-4']
songs = ['amazing-grace', 'black-is-the-colour', 'the-house-of-the-rising-sun', 'wayfaring-stranger', 'whiskey-in-the-jar']
aria_locs = ['aria-near', 'aria-mid', 'aria-far', 'aria-static']
groups = ['mono', 'beam3', 'beam5', 'beam7']

for session in sessions:
    # Songs included in the session
    path_to_session = os.path.join(path_to_egomusic, session)
    session_songs = [directory for directory in os.listdir(path_to_session) if directory.split('_')[0] in songs]

    for session_song in session_songs:
        # Obtain the reverberated reference file of the song
        path_to_session_song = os.path.join(path_to_session, session_song)
        path_to_refs = os.path.join(path_to_session_song, 'refs')
        for fname in os.listdir(path_to_refs):
            if 'mix_reverb.wav' in fname:
                reference_file = fname
        path_to_reference_audio = os.path.join(path_to_refs, reference_file)
        reference_audio, _ = librosa.load(path_to_reference_audio, sr=sr)

        # Apply peak normalisation
        normalised_ref = normalise_audio(reference_audio)

        # Acquire five 10-second samples from this song
        duration = 10.0     # in seconds
        offset_min = 1.0    # start at 1-second mark
        offset_max = len(normalised_ref) / sr - duration - 1.0     # end point excluding 1-second from the end
        offset_values = np.linspace(offset_min, offset_max, 5)     # 10-second segments from start to finish

        for sample_number, offset in enumerate(offset_values):
            reference_snippet = extract_snippet(reference_audio, sr, duration, offset, silence_dur=0.5, normalise=True)
            path_to_reference_output = os.path.join(path_to_session_song, 'refs', 'visqol_data')
            reference_output_fname = f'{session_song}-clean-{sample_number+1}.wav'

            # Create directory if it does not exists
            if not os.path.exists(path_to_reference_output):
                os.makedirs(path_to_reference_output)

            # Save wav file
            path_to_reference_output_fname = os.path.join(path_to_reference_output, reference_output_fname)
            wavfile.write(path_to_reference_output_fname, sr, float32_to_int16(reference_snippet))

            # Normalise to -30 LUFS using ffmpeg-normalize
            subprocess.run(['ffmpeg-normalize', path_to_reference_output_fname, '-o', path_to_reference_output_fname, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
            print(f'Wrote successfully to {path_to_reference_output_fname}.')

            # Obtain test segments from Aria glasses
            for aria_loc in aria_locs:
                loc = aria_loc.split('-')[-1]
                path_to_aria_loc = os.path.join(path_to_session_song, aria_loc, 'audio')

                # Get all wav files and put in a mic_array
                aria_audio_fnames = [fname for fname in os.listdir(path_to_aria_loc) if fname.endswith('.wav')]
                aria_audio_fnames.sort()

                # Get the aria id, session id, and song id from the filename
                aria_session_song_id = aria_audio_fnames[0].rsplit('_', 1)[0]
                
                mic_array = []
                for fname in aria_audio_fnames:
                    path_to_aria_audio = os.path.join(path_to_aria_loc, fname)
                    mic_audio, _ = librosa.load(path_to_aria_audio, sr=sr)
                    mic_audio_snippet = extract_snippet(mic_audio, sr, duration, offset, silence_dur=0.0, normalise=False)
                    mic_array.append(mic_audio_snippet)
                mic_array = np.array(mic_array)

                mono_audio = mic_array[1]   # Select mic1 from the Aria Glasses
                mono_audio = add_silence(mono_audio, sr, silence_dur=0.5)
                beam3_audio = delay_sum(mic_array[np.array([1, 5, 6]), :], 
                                        sr, n_fft=1200, normalise=True, silence_dur=0.5)    # Beamforming with 3 mics
                beam5_audio = delay_sum(mic_array[np.array([1, 3, 4, 5, 6]), :], 
                                        sr, n_fft=1200, normalise=True, silence_dur=0.5)    # Beamforming with 5 mics
                beam7_audio = delay_sum(mic_array, 
                                        sr, n_fft=1200, normalise=True, silence_dur=0.5)    # Beamforming with 7 mics
                
                path_to_visqol_data = os.path.join(path_to_session_song, aria_loc, 'visqol_data')
                
                # Save mono audio
                path_to_mono_audio = os.path.join(path_to_visqol_data, 'mono', f'{aria_session_song_id}_mono-{sample_number+1}.wav')
                wavfile.write(path_to_mono_audio, sr, float32_to_int16(mono_audio))
                subprocess.run(['ffmpeg-normalize', path_to_mono_audio, '-o', path_to_mono_audio, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
                print(f'Wrote successfully to {path_to_mono_audio}.')

                # Save mono audio
                path_to_beam3_audio = os.path.join(path_to_visqol_data, 'beam3', f'{aria_session_song_id}_beam3-{sample_number+1}.wav')
                wavfile.write(path_to_beam3_audio, sr, float32_to_int16(beam3_audio))
                subprocess.run(['ffmpeg-normalize', path_to_beam3_audio, '-o', path_to_beam3_audio, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
                print(f'Wrote successfully to {path_to_beam3_audio}.')

                # Save beam5 audio
                path_to_beam5_audio = os.path.join(path_to_visqol_data, 'beam5', f'{aria_session_song_id}_beam5-{sample_number+1}.wav')
                wavfile.write(path_to_beam5_audio, sr, float32_to_int16(beam5_audio))
                subprocess.run(['ffmpeg-normalize', path_to_beam5_audio, '-o', path_to_beam5_audio, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
                print(f'Wrote successfully to {path_to_beam5_audio}.')

                # Save beam7 audio
                path_to_beam7_audio = os.path.join(path_to_visqol_data, 'beam7', f'{aria_session_song_id}_beam7-{sample_number+1}.wav')
                wavfile.write(path_to_beam7_audio, sr, float32_to_int16(beam7_audio))
                subprocess.run(['ffmpeg-normalize', path_to_beam7_audio, '-o', path_to_beam7_audio, '-f', '--keep-loudness-range-target', '-t', '-30.0'])
                print(f'Wrote successfully to {path_to_beam7_audio}.')


