## Utilizando Python para criar um chat bot utilizando a API da OpenAi e ChatGpt com adições de funções

import json
import openai
import yfinance as yf

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

client = openai.Client()

# Criar a função que pode ser usada pelo Bot.
## Utilizado a api do yahoo finance para obter dados sobre ações

def cotacao_hist(ticker, periodo):
    ticker_obj = yf.Ticker(f'{ticker}.SA')
    hist = ticker_obj.history(period = periodo, auto_adjust = False)
    if len(hist) > 30:
        slice_size = int(len(hist) / 30)
        hist = hist.iloc[:: - slice_size] [:: - 1]
    hist.index = hist.index.strftime('%m-%d-%y')
    return hist['Close'].to_json()

## Proxímo passo é passar para o bot as ferramentas que ele tem disponível caso ele julgue necessário utilizar

tools = [
    {
        'type' : 'function',
        'function': {
            'name': 'cotacao_hist',
            'description': 'Retorna a cotação histórica de uma ação da bovespa',
            'parameters': {
                'type':'object',
                'properties' : {
                    'ticker' : {
                        'type' : 'string',
                        'description' : 'O ticker da ação. Ex: "ABEV3" para ambev, "PETR4" para petrobras, etc',
                    },
                    'periodo' : {
                        'type' : 'string',
                        'description':'O período que será retornado pelos dados, \
                                        sendo "1mo" equivalente a um mês de dados, \
                                        "1d" a um dia e "1y" a um ano',                                        
                        'enum': ['1d','5d','1mo','6mo','1y','5y','10y','ytd','max']
                    },
                },
                'required' : ['ticker', 'periodo'],    
            },
        }
    }
    ]

funcoes_disponiveis = {
    'cotacao_hist' : cotacao_hist,
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