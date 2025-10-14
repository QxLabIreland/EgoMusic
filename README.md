# EgoMusic
This project contains the Python code for reproducing the results in the paper:

Alessandro Ragano, Carl Timothy Tolentino, Kata Szita, Dan Barry, Davoud Shariat Panah, Niall Murray, and Andrew Hines. 2025. **EgoMusic: An Egocentric Augmented Reality Glasses Dataset for Music**. In Proceedings of
the 33rd ACM International Conference on Multimedia (MM ’25), October 27–31, 2025, Dublin, Ireland. ACM, New York, NY, USA, 8 pages. https://doi.org/10.1145/3746027.3758262

## Setup

1. Install a recent version of [ffmpeg](https://ffmpeg.org/download.html).
2. Install the required packages by running `pip install -r requirements.txt`.
3. Install [VISQOL](https://github.com/google/visqol) by following the instructions on its GitHub page.
4. Download the EgoMusic data set by running `python -m egomusic.download_egomusic`. You need at least 70 GB of disk space. Alternatively, you can download the data set on [Zenodo](https://zenodo.org/records/16753794) and place the files on `./data/EgoMusic/`.

## Audio Quality Objective Tests

1. Prepare the audio files to employ VISQOL by running `python -m egomusic.prepare_visqol_files.
2. Generate the CSV file for batch processing of VISQOL by running `python -m csv_for_visqol`. The CSV file should be saved in `./output/input_audio_files.csv`.
3. Run VISQOL by invoking the following command: `path/to/visqol/bazel-bin/visqol --batch_input_csv "./output/input_audio_files.csv" --results_csv "./output/results_audio_files.csv"`.
4. Obtain the objective test results by running `python -m egomusic.visqol_results`.

## Music Source Separation

1. Download the MUSDB18-HQ data set [here](https://zenodo.org/records/3338373) and save it to `./data/musdb18/`. We only need the test set (50 songs) so you can delete the train folder if you want.
2. Prepare the files for separation by running `python -m egomusic.process_musdb_egomusic` and `python -m egomusic.separation_files`.
3. Employ music source separation using `demucs` by uploading the files in your Google Drive and running `./egomusic/source_separation.ipynb` on Google Colab.
4. Download the separated files and place them on `./data/audio_for_separation/`.
5. To evaluate the SDR on MUSDB and EgoMusic, run `python -m egomusic.evaluate_separation
6. To run audio quality objective tests on the stems, prepare the audio files for VISQOL analysis by running `python -m egomusic.process_separated_files.
7. Generate the CSV file for batch processing by running `python -m csv_for_visqol_separated`. The CSV file will be saved in `./output/input_separated_files.csv`.
8. Run VISQOL by invoking the command `path/to/visqol/bazel-bin/visqol --batch_input_csv "./output/input_separated_files.csv" --results_csv "./output/results_separated_files.csv"`.
9. Obtain the objective test results by running `python -m egomusic.visqol_results_separated`.
