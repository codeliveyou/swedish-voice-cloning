import whisper
import os


model = whisper.load_model("large")

audio_directory = "./preparing_dataset/dataset"
output_directory = "./preparing_dataset/dataset/transcriptions"

os.makedirs(output_directory, exist_ok=True)

for i in range(0, 206):
    audio_file = os.path.join(audio_directory, f"segment_{i}.mp3")
    output_file = os.path.join(output_directory, f"transcription_{i}.txt")

    if os.path.isfile(audio_file):
        result = model.transcribe(audio_file, language="swedish")

        transcription = result["text"]

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(transcription)

        print(f"Transcription for segment_{i}.mp3 completed!")

print("All transcriptions completed!")
