import whisper
import os
import subprocess

try:
    subprocess.run(["ffmpeg", "-version"], check=True)
except subprocess.CalledProcessError as e:
    print("ffmpeg is not installed or not accessible in the PATH.")
    raise e

model_name = "large"
cache_dir = os.path.join(os.getenv("HOME", os.getenv("USERPROFILE")), ".cache", "whisper")
model_path = os.path.join(cache_dir, f"{model_name}.pt")

model = whisper.load_model(model_name)

audio_path = os.path.abspath("./source_data/source.mp3")
print(f"Transcribing audio file at: {audio_path}")
try:
    result = model.transcribe(audio_path)
    transcription = result["text"]
    print(transcription)
except subprocess.CalledProcessError as e:
    print(f"Failed to process audio file with ffmpeg: {e}")
    raise e
except RuntimeError as e:
    print(f"Runtime error during transcription: {e}")
    raise e
