import numpy as np
import torch
from speechbrain.processing.features import STFT, ISTFT
from speechbrain.processing.multi_mic import Covariance, GccPhat, DelaySum

def normalise_audio(data):
    data = data - np.mean(data)
    data = data / np.max(np.abs(data))
    return data

def add_silence(data, sr, silence_dur=0.5):
    # Include silence at the start and end
    silence = np.zeros(int(silence_dur * sr))
    data = np.concatenate((silence, data, silence))
    return data

def extract_snippet(data, sr, duration=10.0, offset=0.0, silence_dur=0.5, normalise=True):
    
    # Normalize
    if normalise:
        data = normalise_audio(data)
    
    # Extract at offset
    start_n = int(offset * sr)
    end_n = start_n + int(duration * sr)
    audio = data[start_n:end_n]

    if silence_dur > 0.0:
        audio = add_silence(audio, sr, silence_dur)

    return audio

def float32_to_int16(data):
    output_data = (data * 32767).astype(np.int16)
    return output_data

def delay_sum(mic_array, samplerate, n_fft=1200, normalize=True, silence_dur=0.5):

    mic_array = mic_array.T     # [time, channels]
    mic_array = torch.tensor(mic_array)
    mic_array = mic_array.unsqueeze(0)  # [batch, time, channels]

    stft = STFT(sample_rate=samplerate, n_fft=n_fft)
    cov = Covariance()
    gccphat = GccPhat()
    delaysum = DelaySum()
    istft = ISTFT(sample_rate=samplerate)

    Xs = stft(mic_array)
    XXs = cov(Xs)
    tdoas = gccphat(XXs)

    Ys_ds = delaysum(Xs, tdoas)
    beamformed = istft(Ys_ds)

    beamformed = beamformed.squeeze()
    beamformed = beamformed.numpy()

    if normalize:
        beamformed = normalise_audio(beamformed)
    
    if silence_dur > 0.0:
        beamformed = add_silence(beamformed, samplerate, silence_dur)

    return beamformed