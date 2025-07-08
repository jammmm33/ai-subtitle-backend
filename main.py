from fastapi import FastAPI, UploadFile
import os
import whisper
from datetime import datetime, timedelta

## 디렉토리 설정 =====================
## 동영상이 저장되는 폴더: uploads
## SRT 파일이 저장되는 폴더 output

UPLOAD_DIR = './uploads'
OUTPUT_DIR = './output'

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

## Whisper 모델 로드 =================

model = whisper.load_model('small')

## FastAPI 실행
app = FastAPI()

@app.get('/')
def index():
    return '환영합니다.'

## 요청 URL: /create_subtitled_video
## 요청 method: post
## 요청 return: 요청 처리됨

@app.post('/create_subtitled_video')
async def create_subtitled_video(file: UploadFile):
    print('\n=== 비디오 처리 시작 ===')

    ## video 파일명 지정
    ## /upload/temp_video_20250707_1720.mp4
    tempstamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    temp_video_path = os.path.join(UPLOAD_DIR, f'temp_video_{tempstamp}.mp4')

    ## 업로드 영상 저장
    contents = await file.read()
    ## with 문 사용하여 쓰기 작업: wb
    ## 파일 경로 및 파일명 : temp_video_path
    with open(temp_video_path, 'wb') as file:
        file.write(contents)


    print('Whisper로 자막 추출 중')
    result = model.transcribe(temp_video_path)

    segments = result['segments']
    
    ## srt 파일 : 파일 명 지정
    srt_filename = f'subtitle_{tempstamp}.srt'
    srt_path = os.path.join(OUTPUT_DIR, srt_filename)

    ## srt 파일 생성
    ## with 문 사용: 쓰기 작업
    with open(srt_path, 'w', encoding='utf-8') as file:
        for i, seg in enumerate(segments, 1):
            start = format_time(seg['start'])
            end = format_time(seg['end'])
            text = seg['text'].strip()

            file.write(f'{i}\n')
            file.write(f'{start} --> {end}\n')
            file.write(f'{text}\n\n')


    return '요청 처리됨'



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