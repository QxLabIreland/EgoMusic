import csv
import os

# VISQOL analysis for the separated tracks

# Create a CSV file to list data for VISQOL analysis
path_to_csv_file_separated = './output/input_separated_files.csv'
csv_file_separated = open(path_to_csv_file_separated, 'w')
csv_file_separated_writer = csv.writer(csv_file_separated)

# Aria locations
aria_locs = ['clean', 'near', 'mid', 'far', 'static']

# Put headers on the CSV file.
header = ['reference', 'degraded']
csv_file_separated_writer.writerow(header)

# Path to the reference tracks
path_to_ref_tracks = './data/audio_for_separation/tracks/'

# Iterate over all the reference tracks
paths_to_wavfile = []
for root, dirs, files in os.walk(path_to_ref_tracks):
    for name in files:
        if not name.endswith('.wav'):
            continue
        path_to_wavfile = os.path.join(root, name)
        paths_to_wavfile.append(path_to_wavfile)

for path_to_wavfile in paths_to_wavfile:
    # This is the reference track for VISQOL
    abspath_ref_track = os.path.abspath(path_to_wavfile)
    session_song_number = path_to_wavfile.split('/')[-2]
    session_song = session_song_number[:-2]                     # Name of the song
    sample_number = int(session_song_number.split('-')[-1])     # Sample number
    temp_label = path_to_wavfile.split('/')[-1]                 # Name of the track

    # Change track labels to the demucs labels
    if temp_label == 'percussion.wav':
        label = 'drums.wav'
    elif temp_label == 'piano.wav' or temp_label == 'guitar.wav':
        label = 'other.wav'
    else:
        label = temp_label

    # Find the test track for each aria location
    for aria_loc in aria_locs:
        path_to_estimated_folder = f'./data/audio_for_separation/estimated_{aria_loc}/htdemucs/{session_song}-{aria_loc}-{sample_number}/'
        path_to_estimated_track = os.path.join(path_to_estimated_folder, label)
        abspath_estimated_track = os.path.abspath(path_to_estimated_track)
        
        # Write to csv file
        csv_file_separated_writer.writerow([abspath_ref_track] + [abspath_estimated_track])

# Close CSV file
csv_file_separated.close()

# # Aria locations
# aria_locs = ['clean', 'near', 'mid', 'far', 'static']
# path_to_egomusic = './data/EgoMusic/'
# sessions = ['session-1-instruments-2', 'session-2-instruments-3', 'session-3-instruments-4']
# songs = ['amazing-grace', 'black-is-the-colour', 'the-house-of-the-rising-sun', 'wayfaring-stranger', 'whiskey-in-the-jar']
# aria_locs = ['aria-near', 'aria-mid', 'aria-far', 'aria-static']
# groups = ['mono', 'beam3', 'beam5', 'beam7']

# for session in sessions:
#     # Songs included in the session
#     path_to_session = os.path.join(path_to_egomusic, session)
#     session_songs = [directory for directory in os.listdir(path_to_session) if directory.split('_')[0] in songs]
    
#     for session_song in session_songs:
#         # Five 10-second reference files
#         path_to_session_song = os.path.join(path_to_session, session_song)
#         path_to_refs = os.path.join(path_to_session_song, 'refs', 'visqol_data')
#         path_to_reference_audios = [fname for fname in os.listdir(path_to_refs) if fname.endswith('.wav')]
#         path_to_reference_audios.sort()

#         # for fname in os.listdir(path_to_refs):
#         #     if 'mix_reverb.wav' in fname:
#         #         reference_file = fname
#         # path_to_reference_audio = os.path.join(path_to_refs, reference_file)
#         # abspath_to_reference_audio = os.path.abspath(path_to_reference_audio)

#         for aria_loc in aria_locs:
#             path_to_aria_loc = os.path.join(path_to_session_song, aria_loc)
#             path_to_visqol_data = os.path.join(path_to_aria_loc, 'visqol_data')
            
#             # Groups are mono, beam3, beam5, beam7
#             for group in groups:
#                 path_to_group = os.path.join(path_to_visqol_data, group)
#                 for test_file in os.listdir(path_to_group):
#                     if test_file.endswith('.wav'):
#                         path_to_test_file = os.path.join(path_to_group, test_file)
#                         abspath_to_test_file = os.path.abspath(path_to_test_file)

#                         # Check sample number
#                         sample_number = test_file.split('-')[-1]
#                         sample_number = int(sample_number.split('.')[0]) - 1

#                         # Path to reference
#                         path_to_reference_audio = os.path.join(path_to_refs, path_to_reference_audios[sample_number])
#                         abspath_to_reference_audio = os.path.abspath(path_to_reference_audio)

#                         # Put absolute paths of reference and test files to CSV
#                         csv_row = [abspath_to_reference_audio] + [abspath_to_test_file]
#                         csv_file_audio_writer.writerow(csv_row)

# # Close CSV file
# csv_file_audio.close()

# # VISQOL analysis for the audio files