import openai
import pyaudio
from playsound import playsound
from pathlib import Path
import speech_recognition as sr
from io import BytesIO
from dotenv import load_dotenv, find_dotenv

_=load_dotenv(find_dotenv())

client = openai.Client()
recognizer = sr.Recognizer()
mp3_data = r'C:\Users\user\Downloads\Data science\Python\AI\Open AI\audios\fala_assistant.mp3'

def grava_audio():
    with sr.Microphone() as source:
        print('Ouvindo...')
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source)
        return audio
    
def transcricao_audio(audio):
    wav_data = BytesIO(audio.get_wav_data())
    wav_data.name = 'audio.wav'
    transcricao = client.audio.transcriptions.create(
        model = 'whisper-1',
        file = wav_data,
        response_format = 'text',
        language = 'pt'
        )
    return transcricao

def resposta_chat(mensagens):
    respostas = client.chat.completions.create(
        messages = mensagens,
        model = 'gpt-3.5-turbo-0125',
        max_tokens = 1000,
        temperature = 0,
        stream = True,
    )
    
    print('Assistant:', end = '')
    texto_completo = ''
    for stream_respostas in respostas:
        texto = stream_respostas.choices[0].delta.content
        if texto:
            texto_completo += texto
            print(texto, end = '')
    print()
    mensagens.append({'role': 'assistant', 'content': texto_completo})
    return mensagens

def cria_audio(texto):
    if Path(mp3_data).exists():
        Path(mp3_data).unlink()
    resposta = client.audio.speech.create(
        model = 'tts-1',
        voice = 'nova',
        input = texto
    )
    resposta.write_to_file(mp3_data)

def play_audio():
    playsound(mp3_data)

if __name__ == '__main__':
    print('Bem vindo ao ChatBot')
    mensagens = []
    while True:
        audio = grava_audio()
        transcricao = transcricao_audio(audio)
        input_user = f'User: {transcricao}'
        mensagens.append({'role':'user','content':input_user})
        mensagens = resposta_chat(mensagens)
        cria_audio(mensagens[-1]['content'])
        play_audio()