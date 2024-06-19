import logging
import os
import json
import pysrt
from pydub import AudioSegment

def create_training_data(audio_path: str, transcription_path: str, output_data_path: str, target_sample_rate: int, min_combination: int, max_combination: int):
    def srt_time_to_ms(srt_time):
        return (srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds) * 1000 + srt_time.milliseconds

    logging.basicConfig(filename=os.path.join(output_data_path, 'audio_processing.log'), level=logging.ERROR)
    
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(target_sample_rate)

    transcription = pysrt.open(transcription_path)

    max_combination = min(max_combination, len(transcription))
    min_combination = min(min_combination, max_combination)

    for num_combination in range(min_combination, max_combination + 1):
        current_path = os.path.join(output_data_path, f'{num_combination:02d}_combination')
        os.makedirs(current_path, exist_ok=True)
        data = []
        for i in range(len(transcription) - num_combination + 1):
            start_time = srt_time_to_ms(transcription[i].start)
            end_time = srt_time_to_ms(transcription[i + num_combination - 1].end)
            text = ' '.join([transcription[j].text for j in range(i, i + num_combination)])
            audio_segment = audio[start_time:end_time]

            audio_segment.export(os.path.join(current_path, f'{i:03d}_({num_combination})_audio.wav'), format='wav')
            with open(os.path.join(current_path, f'{i:03d}_({num_combination})_transcription.txt'), 'w', encoding='utf-8') as text_file:
                text_file.write(text)
            
            data.append({"audio": f'training_data/{num_combination:02d}_combination/{i:03d}_({num_combination})_audio.wav', "text": text})

        with open(os.path.join(output_data_path, f'{num_combination:02d}_data.json'), 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        
        print(f"Audio segments and corresponding text files for {num_combination} combinations have been saved.")

    print("Processing complete.")

audio_path = './source_data/voice_recording.mp3'
transcription_path = './transcription_data/voice_recording_transcription.srt'
output_data_path = './training_data'

create_training_data(audio_path, transcription_path, output_data_path, 16000, 1, 10)
