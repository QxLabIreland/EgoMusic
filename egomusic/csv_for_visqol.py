import csv
import os

# VISQOL analysis for the audio files

# Create a CSV file to list data for VISQOL analysis
path_to_csv_file_audio = './output/input_audio_files.csv'
csv_file_audio = open(path_to_csv_file_audio, 'w')
csv_file_audio_writer = csv.writer(csv_file_audio)

# Put headers on the CSV file.
header = ['reference', 'degraded']
csv_file_audio_writer.writerow(header)

# Analyse EgoMusic data
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
        # Five 10-second reference files
        path_to_session_song = os.path.join(path_to_session, session_song)
        path_to_refs = os.path.join(path_to_session_song, 'refs', 'visqol_data')
        path_to_reference_audios = [fname for fname in os.listdir(path_to_refs) if fname.endswith('.wav')]
        path_to_reference_audios.sort()

        # for fname in os.listdir(path_to_refs):
        #     if 'mix_reverb.wav' in fname:
        #         reference_file = fname
        # path_to_reference_audio = os.path.join(path_to_refs, reference_file)
        # abspath_to_reference_audio = os.path.abspath(path_to_reference_audio)

        for aria_loc in aria_locs:
            path_to_aria_loc = os.path.join(path_to_session_song, aria_loc)
            path_to_visqol_data = os.path.join(path_to_aria_loc, 'visqol_data')
            
            # Groups are mono, beam3, beam5, beam7
            for group in groups:
                path_to_group = os.path.join(path_to_visqol_data, group)
                for test_file in os.listdir(path_to_group):
                    if test_file.endswith('.wav'):
                        path_to_test_file = os.path.join(path_to_group, test_file)
                        abspath_to_test_file = os.path.abspath(path_to_test_file)

                        # Check sample number
                        sample_number = test_file.split('-')[-1]
                        sample_number = int(sample_number.split('.')[0]) - 1

                        # Path to reference
                        path_to_reference_audio = os.path.join(path_to_refs, path_to_reference_audios[sample_number])
                        abspath_to_reference_audio = os.path.abspath(path_to_reference_audio)

                        # Put absolute paths of reference and test files to CSV
                        csv_row = [abspath_to_reference_audio] + [abspath_to_test_file]
                        csv_file_audio_writer.writerow(csv_row)

# Close CSV file
csv_file_audio.close()

# VISQOL analysis for the audio files

# path_to_tracks = "normalized/audio_for_separation/tracks/"
# path_to_estimated_master = "normalized/audio_for_separation/estimated_master/htdemucs"
# path_to_estimated_near = "normalized/audio_for_separation/estimated_near/htdemucs"
# path_to_estimated_mid = "normalized/audio_for_separation/estimated_mid/htdemucs"
# path_to_estimated_far = "normalized/audio_for_separation/estimated_far/htdemucs"
# path_to_estimated_static = "normalized/audio_for_separation/estimated_static/htdemucs"

# path_to_csv_file_master = "/Users/carltimothytolentino/visqol-master/input_separated_master.csv"
# csv_file_master = open(path_to_csv_file_master, 'w')
# writer_master = csv.writer(csv_file_master)

# path_to_csv_file_near = "/Users/carltimothytolentino/visqol-master/input_separated_near.csv"
# csv_file_near = open(path_to_csv_file_near, 'w')
# writer_near = csv.writer(csv_file_near)

# path_to_csv_file_mid = "/Users/carltimothytolentino/visqol-master/input_separated_mid.csv"
# csv_file_mid = open(path_to_csv_file_mid, 'w')
# writer_mid = csv.writer(csv_file_mid)

# path_to_csv_file_far = "/Users/carltimothytolentino/visqol-master/input_separated_far.csv"
# csv_file_far = open(path_to_csv_file_far, 'w')
# writer_far = csv.writer(csv_file_far)

# path_to_csv_file_static = "/Users/carltimothytolentino/visqol-master/input_separated_static.csv"
# csv_file_static = open(path_to_csv_file_static, 'w')
# writer_static = csv.writer(csv_file_static)

# header = ["reference", "degraded"]
# writer_master.writerow(header)
# writer_near.writerow(header)
# writer_mid.writerow(header)
# writer_far.writerow(header)
# writer_static.writerow(header)

# paths_to_wavfiles = []
# for root, dirs, files in os.walk(path_to_tracks):
#     for name in files:
#         if not name.endswith('.wav'):
#             continue
#         path_to_wavfile = os.path.join(root, name)
#         paths_to_wavfiles.append(path_to_wavfile)

# paths_to_wavfiles.sort()
# for path_to_wavfile in paths_to_wavfiles:
#     abspath_track = os.path.abspath(path_to_wavfile)
#     temp_src = path_to_wavfile.split('/')[-1]
#     if temp_src == "percussion.wav":
#         src = "drums.wav"
#     elif temp_src == "piano.wav" or temp_src == "guitar.wav":
#         src = "other.wav"
#     else:
#         src = path_to_wavfile.split('/')[-1]
#     song_src = path_to_wavfile.split('/')[-2] + '/' + src
    
#     path_to_track_master = os.path.join(path_to_estimated_master, song_src)
#     abspath_master = os.path.abspath(path_to_track_master)

#     path_to_track_near = os.path.join(path_to_estimated_near, song_src)
#     abspath_near = os.path.abspath(path_to_track_near)

#     path_to_track_mid = os.path.join(path_to_estimated_mid, song_src)
#     abspath_mid = os.path.abspath(path_to_track_mid)

#     path_to_track_far = os.path.join(path_to_estimated_far, song_src)
#     abspath_far = os.path.abspath(path_to_track_far)

#     path_to_track_static = os.path.join(path_to_estimated_static, song_src)
#     abspath_static = os.path.abspath(path_to_track_static)

#     writer_master.writerow([abspath_track] + [abspath_master])
#     writer_near.writerow([abspath_track] + [abspath_near])
#     writer_mid.writerow([abspath_track] + [abspath_mid])
#     writer_far.writerow([abspath_track] + [abspath_far])
#     writer_static.writerow([abspath_track] + [abspath_static])

# csv_file_master.close()
# csv_file_near.close()
# csv_file_mid.close()
# csv_file_far.close()
# csv_file_static.close()

# # SEPARATED AUDIO 2 STEMS
# path_to_tracks = "normalized/audio_for_separation/tracks/"
# path_to_estimated_master = "normalized/audio_for_separation/estimated_master/htdemucs"
# path_to_estimated_near = "normalized/audio_for_separation/estimated_near/htdemucs"
# path_to_estimated_mid = "normalized/audio_for_separation/estimated_mid/htdemucs"
# path_to_estimated_far = "normalized/audio_for_separation/estimated_far/htdemucs"
# path_to_estimated_static = "normalized/audio_for_separation/estimated_static/htdemucs"

# path_to_csv_file_master = "/Users/carltimothytolentino/visqol-master/input_separated_no_vocals_master.csv"
# csv_file_master = open(path_to_csv_file_master, 'w')
# writer_master = csv.writer(csv_file_master)

# path_to_csv_file_near = "/Users/carltimothytolentino/visqol-master/input_separated_no_vocals_near.csv"
# csv_file_near = open(path_to_csv_file_near, 'w')
# writer_near = csv.writer(csv_file_near)

# path_to_csv_file_mid = "/Users/carltimothytolentino/visqol-master/input_separated_no_vocals_mid.csv"
# csv_file_mid = open(path_to_csv_file_mid, 'w')
# writer_mid = csv.writer(csv_file_mid)

# path_to_csv_file_far = "/Users/carltimothytolentino/visqol-master/input_separated_no_vocals_far.csv"
# csv_file_far = open(path_to_csv_file_far, 'w')
# writer_far = csv.writer(csv_file_far)

# path_to_csv_file_static = "/Users/carltimothytolentino/visqol-master/input_separated_no_vocals_static.csv"
# csv_file_static = open(path_to_csv_file_static, 'w')
# writer_static = csv.writer(csv_file_static)

# header = ["reference", "degraded"]
# writer_master.writerow(header)
# writer_near.writerow(header)
# writer_mid.writerow(header)
# writer_far.writerow(header)
# writer_static.writerow(header)

# paths_to_wavfiles = []
# for root, dirs, files in os.walk(path_to_tracks):
#     for name in files:
#         if name == 'no_vocals.wav':
#             path_to_wavfile = os.path.join(root, name)
#             paths_to_wavfiles.append(path_to_wavfile)

# paths_to_wavfiles.sort()
# for path_to_wavfile in paths_to_wavfiles:
#     abspath_track = os.path.abspath(path_to_wavfile)
#     temp_src = path_to_wavfile.split('/')[-1]
#     src = path_to_wavfile.split('/')[-1]
#     song_src = path_to_wavfile.split('/')[-2] + '/' + src
    
#     path_to_track_master = os.path.join(path_to_estimated_master, song_src)
#     abspath_master = os.path.abspath(path_to_track_master)

#     path_to_track_near = os.path.join(path_to_estimated_near, song_src)
#     abspath_near = os.path.abspath(path_to_track_near)

#     path_to_track_mid = os.path.join(path_to_estimated_mid, song_src)
#     abspath_mid = os.path.abspath(path_to_track_mid)

#     path_to_track_far = os.path.join(path_to_estimated_far, song_src)
#     abspath_far = os.path.abspath(path_to_track_far)

#     path_to_track_static = os.path.join(path_to_estimated_static, song_src)
#     abspath_static = os.path.abspath(path_to_track_static)

#     writer_master.writerow([abspath_track] + [abspath_master])
#     writer_near.writerow([abspath_track] + [abspath_near])
#     writer_mid.writerow([abspath_track] + [abspath_mid])
#     writer_far.writerow([abspath_track] + [abspath_far])
#     writer_static.writerow([abspath_track] + [abspath_static])

# csv_file_master.close()
# csv_file_near.close()
# csv_file_mid.close()
# csv_file_far.close()
# csv_file_static.close()

