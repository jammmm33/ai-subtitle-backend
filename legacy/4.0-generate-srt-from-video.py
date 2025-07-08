from datetime import timedelta
from moviepy import VideoFileClip
import json
import whisper
import os
from config import SUBTITLE_JSON_FILE, SUBTITLE_SRT_FILE, SUBTITLE_DIR, AUDIO_FILE, SUBTITLE_FILE, VIDEO_FILE


def format_time(seconds):
    '''
    초 단위 시간을 STR 형식으로(HH:MM:SS,mm)으로 변환
    '''
    td = timedelta(seconds=seconds)
    hours = int(td.total_seconds() // 3600)
    minutes = int((td.total_seconds() % 3600) // 60)
    seconds = int(td.total_seconds() % 60)
    milliseconds = int((td.total_seconds()% 1) * 1000)
    
    return f'{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:3d}'


def extract_audio_movieby(input_video_path, output_audio_path):
	video = VideoFileClip(input_video_path)
	video.audio.write_audiofile(output_audio_path, fps=16000, nbytes=2, codec='pcm_s16le')
	video.close()
     

def transcribe_audio_to_text(audio_path):
    model = whisper.load_model('small')
    result = model.transcribe(audio_path)
    return result


def save_transcription(result):
    os.makedirs(SUBTITLE_DIR, exist_ok=True)

    with open(SUBTITLE_FILE, 'w', encoding='utf-8') as file:
        file.write(result['text'])

    with open(SUBTITLE_JSON_FILE, 'w', encoding='utf-8') as file:
        json.dump(result['segments'], file, indent=2, ensure_ascii=False)


def generate_srt_from_json(json_path, srt_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        segments = json.load(file)

    with open(srt_path, 'w', encoding='utf-8') as file:
        for i, seg in enumerate(segments, start=1):
            start = format_time(seg['start'])
            end = format_time(seg['end'])
            text = seg['text'].strip()

            file.write(f"{i}\n")
            file.write(f"{start} --> {end}\n")
            file.write(f"{text}\n\n")



def generate_srt_from_movie():
    extract_audio_movieby(VIDEO_FILE, AUDIO_FILE)
    result = transcribe_audio_to_text(AUDIO_FILE)
    save_transcription(result)
    generate_srt_from_json(SUBTITLE_JSON_FILE, SUBTITLE_SRT_FILE)



generate_srt_from_movie()
