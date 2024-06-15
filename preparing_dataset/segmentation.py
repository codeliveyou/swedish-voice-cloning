import os
import json
import numpy as np
import librosa
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load the full audio
audio_file_path = './source_data/source.mp3'
audio = AudioSegment.from_mp3(audio_file_path)

# Parameters for splitting the audio on silence
min_silence_len = 500  # in milliseconds
silence_thresh = audio.dBFS - 14  # adjust this threshold as needed

# Split the audio where silence is detected
audio_chunks = split_on_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)

# Directory to save the segments
segments_dir = "./preparing_dataset/dataset"
os.makedirs(segments_dir, exist_ok=True)

# Create the dataset
dataset = []
i = 0
for chunk in audio_chunks:
    segment_filename = os.path.join(segments_dir, f"segment_{i+1}.mp3")
    chunk.export(segment_filename, format="mp3")
    i += 1

print("Dataset creation completed!")
