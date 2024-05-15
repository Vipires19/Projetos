## Utilizando Python para criar um chat bot utilizando a API da OpenAi e ChatGpt


import openai
import json

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

client = openai.Client()

## Criando o arquivo jsonl que será usado pelo modelo

with open('chatbot_respostas.json', encoding='utf8') as f:
    json_respostas = json.load(f)
    
with open('chatbot_respostas.jsonl', 'w', encoding='utf8') as f:
    for entrada in json_respostas:
        respostas = {
            'resposta' : entrada['resposta'],
            'categoria' : entrada['categoria'],
            'Fonte' : 'AsimoBot'
        }
        entrada_jsonl = {
            'messages' : [
            {'role': 'user', 'content':entrada['pergunta']},
            {'role': 'assistant', 'content': json.dumps(respostas, ensure_ascii= False, indent= 2)}
        ]
    }
    json.dump(entrada_jsonl, f, ensure_ascii= False)
    f.write('\n')

## Enviando o arquivo jsonl para o modelo

file = client.files.create(
    file = open('chatbot_respostas.jsonl', 'rb'),
    purpose = 'fine-tune'
)

client.fine_tuning.jobs.create(
    training_file= file.id,
    model = 'gpt-3.5-turbo-0125'
)


def gerar_texto(mensagens):
    respostas = client.chat.completions.create(
        messages = mensagens,
        model = 'ft:gpt-3.5-turbo-0125:personal::9PFqKR5i',  ## Após o Fine Tuning terminado na parte onde selecionamos o modelo é necessário passar o nome do modelo treinado
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