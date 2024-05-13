## Utilizando Python para criar um chat bot utilizando a API da OpenAi e ChatGpt com adições de funções

import json
import openai

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

client = openai.Client()

# Criar a função que pode ser usada pelo Bot.
## No caso foi passado uma função em que ele obtem temperatura em cidades ja programadas, mas é possível utilizar outra api para obtenção de temperatura em tempo real.

def obter_temperatura_atual(local, unidade = 'celsius'):
    if 'são paulo' in local.lower():
        return json.dumps(
            {'local' : 'São Paulo', 'temperatura' : '32','unidade' : 'celsius'}, ensure_ascii=False
            )
    elif 'porto alegre' in local.lower():
        return json.dumps(
            {'local' : 'Porto Alegre', 'temperatura' : '25', 'unidade' : 'celsius'}, ensure_ascii=False
            )
    elif 'rio de janeiro' in local.lower():
        return json.dumps(
            {'local' : 'Rio de Janeiro', 'temperatura' : '38', 'unidade' : 'celsius'}, ensure_ascii=False
        )
    else:
        return json.dumps(
            {'local' : local, 'temperatura' : 'Unknow'}, ensure_ascii=False
        )
    

## Proxímo passo é passar para o bot as ferramentas que ele tem disponível caso ele julgue necessário utilizar

tools = [
    {
        'type' : 'function',
        'function': {
            'name': 'obter_temperatura_atual',
            'description': 'Obtém a temperatura atual em uma dada cidade',
            'parameters': {
                'type':'object',
                'properties' : {
                    'local' : {
                        'type' : 'string',
                        'description' : 'O nome da cidade. Ex: São Paulo',
                    },
                    'unidade' : {
                        'type' : 'string',
                        'enum': ['celsius', 'fahrenheit']
                    },
                },
                'required' : ['local'],    
            },
        }
    }
    ]

funcoes_disponiveis = {
    'obter_temperatura_atual' : obter_temperatura_atual,
    }

## Adicionando a função ao modelo

def gerar_texto(mensagens):

    respostas = client.chat.completions.create(
        messages = mensagens,
        model = 'gpt-3.5-turbo-0125',
        max_tokens = 1000,
        temperature = 0,
        tools=tools,
        tool_choice= 'auto'
    )

    mensagem_resp = respostas.choices[0].message
    tool_calls = mensagem_resp.tool_calls

    if tool_calls:
        mensagens.append(mensagem_resp)
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = funcoes_disponiveis[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(** function_args)
            mensagens.append(
                {'tool_call_id':tool_call.id,
                 'role' : 'tool',
                 'name' : function_name,
                 'content' : function_response,
                }
        )

        segunda_resposta =  client.chat.completions.create(
            messages = mensagens,
            model = 'gpt-3.5-turbo-0125',
            max_tokens = 1000,
            temperature = 0,
            stream = True,
        )
    
    print('Assistant:', end = '')
    texto_completo = ''
    for stream_respostas in segunda_resposta:
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