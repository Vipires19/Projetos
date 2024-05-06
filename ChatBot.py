## Utilizando Python para criar um chat bot utilizando a API da OpenAi e ChatGpt


import openai

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

client = openai.Client()

def gerar_texto(mensagens):
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

    

if __name__ == '__main__':
    print('Bem vindo ao ChatBot')
    mensagens=[]
    while True:
        input_user = input('User:')
        mensagens.append({'role':'user','content':input_user})
        mensagens = gerar_texto(mensagens)