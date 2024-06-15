import whisper

model = whisper.load_model("large")

result = model.transcribe("./source_data/source.mp3", language="swedish")

transcription = result["text"]

with open("./preparing_dataset/transcription2.txt", "w", encoding="utf-8") as file:
    file.write(transcription)

print("Transcription completed!")
