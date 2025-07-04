from datetime import timedelta


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

def generate_srt_from_movie(params):
    pass
    ## 1. 영상 -> 오디오
    ## 2. 오디오 -> segments
    ## 3. segments -> srt 저장


generate_srt_from_movie()
