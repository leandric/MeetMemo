from pathlib import Path
from datetime import datetime
import time
import queue
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import pydub
import streamlit as st
import openai
from dotenv import load_dotenv, find_dotenv

AUDIO_FILES = Path(__file__).parent / 'audios'
AUDIO_FILES.mkdir(exist_ok=True)

PROMPT = '''
faça o resumo do texto delimitado por ####
O texto é a transcrição de uma reunião.
O resumo deve contar com os principais pontos abordados.
O resumo deve ter no máximo 300 caracteres.
O Resumo deve estar em texto corrido.
No final, devem ser apresentados todos acordos e combinados feitos na reunião em formato de bullet points.

O formato final que eu desejo é:
Resumo reunião:
- escreva aqui o resumo da reunião
Acordos da Reunião:
- acordo 1
- acordo 2
- acordo n

texto: ####{}####
'''


_ = load_dotenv(find_dotenv())

def save_text(path_file, content):
    with open(path_file, 'w') as f:
        f.write(content)

def read_file(path_file):
    if path_file.exists():
        with open(path_file) as f:
            return f.read()
    else:
        return ''

def listen_audio(path_meet):
    if path_meet.exists():
        with open(path_meet / 'audio.mp3', 'rb') as f:
            return f.read()


def list_meets():
    list_meet = list(AUDIO_FILES.glob('*'))
    list_meet.sort(reverse=True)
    meet_dict={}
    for dir_meet in list_meet:
        date_meet = dir_meet.stem
        yer, month, day, hour, minute, second = date_meet.split('_')
        meet_dict[date_meet] = f'{yer}/{month}/{day} {hour}:{minute}:{second}'
        title = read_file(dir_meet / 'titulo.txt')
        if title != '':
            meet_dict[date_meet] += f' - {title}'
    return meet_dict

client = openai.OpenAI()

#================================== Componentes OpenAI ================================
def transcribe_audio(path_audio, language='pt', response_format='text'):
    with open(path_audio, 'rb') as file_audio:
        transcribe = client.audio.transcriptions.create(
            model ='whisper-1',
            language = language,
            response_format = response_format,
            file = file_audio
        )
    return transcribe

def chat_openai(message, model='gpt-3.5-turbo-1106'):
    messages = [{'role':'user', 'content': message}]
    response = client.chat.completions.create(model = model, messages = messages)
    return response.choices[0].message.content


# ================================ Componentes Stremalit =========================

def add_chunck_audio(frames_audio, audio_chunck):
    for frame in frames_audio:
        sound = pydub.AudioSegment(
            data = frame.to_ndarray().tobytes(),
            sample_width = frame.format.bytes,
            frame_rate = frame.sample_rate,
            channels = len(frame.layout.channels)
        )
        audio_chunck += sound
    return audio_chunck

def tab_record_view():
    webrtc_ctx = webrtc_streamer(
        key='record',
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={'video':False, 'audio':True}
        )
    if not webrtc_ctx.state.playing:
        return
    
    container = st.empty()
    container.markdown('Gravando...')
    dir_meet = AUDIO_FILES / datetime.now().strftime('%Y_%m_%d_%H_%M_%s')
    dir_meet.mkdir()

    last_transcription = time.time()
    audio_completed = pydub.AudioSegment.empty()
    audio_chunck = pydub.AudioSegment.empty()
    transcription = ''
    
    while True:
        if webrtc_ctx.audio_receiver:
            try:
                frames_audio = webrtc_ctx.audio_receiver.get_frames(timeout=1)
            except queue.Empty:
                time.sleep(0.1)
                continue
            audio_completed = add_chunck_audio(frames_audio, audio_chunck)
            audio_chunck = add_chunck_audio(frames_audio, audio_chunck)
            if len(audio_chunck) > 0:
                audio_completed.export(dir_meet / 'audio.mp3')
                now = time.time()
                if now - last_transcription > 5:
                    last_transcription = now
                    audio_chunck.export(dir_meet / 'audio_temp.mp3')
                    
                    audio_transcription = transcribe_audio(dir_meet / 'audio_temp.mp3')
                    transcription += audio_transcription
                    container.markdown(transcription)
                    save_text(dir_meet / 'transcription.txt', transcription)
                    audio_chunck = pydub.AudioSegment.empty()
        else:
            break


def tab_selection_meet_view():
    meet_dict = list_meets()
    if len(meet_dict) >0:
        meet_selected = st.selectbox('Selecione uma Reunião', list(meet_dict.values()))
    st.divider()
    meet_date = [k for k, v in meet_dict.items() if v == meet_selected][0]
    dir_meet = AUDIO_FILES / meet_date
    if not (dir_meet / 'titulo.txt').exists():
        st.warning('Adicione um titulo')
        title_meet = st.text_input('Título da Reunião')
        st.button('Salvar',
                  on_click=save_title,
                  args=(dir_meet, title_meet))
    else:
        title = read_file(dir_meet / 'titulo.txt')
        transcription = read_file(dir_meet / 'transcription.txt')
        resume = read_file(dir_meet / 'resume.txt')
        if resume == '':
            create_resume(dir_meet)
            resume = read_file(dir_meet / 'resume.txt')
        st.markdown(f'## {title}')
        st.audio(listen_audio(dir_meet), format='audio/mp3')
        st.markdown(f'{resume}')
        st.markdown(f'Transcrição: {transcription}')

def save_title(dir_meet, title):
    save_text(dir_meet / 'titulo.txt' , title)
    
def create_resume(path_meet):
    transcription = read_file(path_meet / 'transcription.txt')
    resume = chat_openai(message=PROMPT.format(transcription))
    save_text(path_meet / 'resume.txt', resume)


def main():
    st.header('MeetMEMO 💬', divider=True)
    tab_record, tab_selection = st.tabs(['Gravar Reunião', 'Ver Gravações Salvas'])

    with tab_record:
        tab_record_view()
    with tab_selection:
        tab_selection_meet_view()
    
if __name__ == '__main__':
    main()