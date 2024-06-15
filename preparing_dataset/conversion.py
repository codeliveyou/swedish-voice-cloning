import os
from pydub import AudioSegment
import json

audio_directory = "./preparing_dataset/dataset"
output_directory = "./preparing_dataset/converted_dataset"
os.makedirs(output_directory, exist_ok=True)

desired_sample_rate = 22050

dataset = []

for i in range(1, 206):
    audio_file = os.path.join(audio_directory, f"segment_{i}.mp3")
    transcription_file = os.path.join(audio_directory, f"transcription_{i}.txt")

    if os.path.isfile(audio_file) and os.path.isfile(transcription_file):
        audio = AudioSegment.from_mp3(audio_file)
        audio = audio.set_frame_rate(desired_sample_rate)
        wav_file = os.path.join(output_directory, f"segment_{i}.wav")
        audio.export(wav_file, format="wav")

        with open(transcription_file, "r", encoding="utf-8") as file:
            transcription = file.read().strip()

        dataset.append({
            "audio": wav_file,
            "text": transcription
        })

output_file = os.path.join(output_directory, "dataset.json")
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(dataset, file, ensure_ascii=False, indent=4)

print(f"Dataset saved to {output_file}")
