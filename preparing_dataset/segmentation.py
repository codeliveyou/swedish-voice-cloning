from pydub import AudioSegment
import json
import os

audio = AudioSegment.from_mp3("./source_data/source.mp3")

with open("./preparing_dataset/transcription1.txt", "r", encoding="utf-8") as file:
    transcription = file.read().strip().split('. ')

transcription = [sentence.strip() for sentence in transcription if sentence.strip()]

segments_dir = "./preparing_dataset/segments"
os.makedirs(segments_dir, exist_ok=True)

total_duration_ms = len(audio)
segment_duration_ms = total_duration_ms / len(transcription)

dataset = []

for i, sentence in enumerate(transcription):
    start_time = int(i * segment_duration_ms)
    end_time = int(start_time + segment_duration_ms)
    segment = audio[start_time:end_time]
    
    segment_filename = f"{segments_dir}/segment_{i+1}.mp3"
    segment.export(segment_filename, format="mp3")
    
    dataset.append({"audio": segment_filename, "text": sentence + '.'})

dataset_path = f"{segments_dir}/dataset.json"
with open(dataset_path, "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("Dataset creation completed!")
