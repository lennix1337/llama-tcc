# start server em um terminal separado com o venv ativado
# executar em um terminal ou powershell (não no CMD)
# .\venv\Scripts\activate
# python -m llama_cpp.server --host 0.0.0.0 --model .\model\Llama-3-8B-Instruct.Q6_K.gguf --n_ctx 2048 --n_gpu_layers 24

# ator em inglês
# {"role": "system", "content": "You are an intelligent actor agent. You only provide actions after receiving a BDI system from a director agent. Always provide at least 5 actions. Focus your answers on the theme that will be given to you. Do not generate text other than your actions."},

from openai import OpenAI

# Aponta para o servidor local
client = OpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

def diretor(tema):
    # diretor
    history = [
        # {"role": "system", "content": "You are an intelligent director. You will receive a theme from the user. Based on agents BDI system, generate only 1 belief, desire, intention, you will only answer with an belief, desire and intention based on the theme that will be given to the actor agent so that he can generate actions based on that information."},
        {"role": "system", "content": "Responda apenas em Português Brasileiro. Você é um diretor de histórias inteligente e criativo. Evite o uso de generalizações. Você receberá um tema do usuário. Baseado no sistema BDI de agentes, gere apenas 1 crença, desejo, intenção, você só responderá com uma crença, desejo e intenção baseada no tema. Essas informações precisam condizer com o tema e fazer com o que gere uma história coerente."},
        {"role": "user", "content": tema}, 
    ]
    print("\033[94;1m") # azul
    
    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.6,
        stream=True,
        stop="assistant"
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    return new_message["content"]

def narrador(acoesAtor):
    # narrador
    history = [
        # {"role": "system", "content": "You are an intelligent narrator. You will receive actions from an actor. Talk about the story in third person. Turn them into a story. If your story has characters, you can give them names and describe their actions."},
        {"role": "system", "content": "Você é um narrador de histórias inteligente. Dite a história da mesma forma que um livro é escrito. Utilize palavras voltadas para um publico na faixa etaria entre 18 a 40 anos. Você receberá ações de um ator. Fale sobre a história em terceira pessoa. Transforme-os em uma história. Se sua história tiver personagens, você pode dar nomes a eles e descrever suas ações."},
        {"role": "user", "content": acoesAtor},
    ]
    print("\033[91;1m") # vermelho
    
    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.6,
        stream=True,
        stop="assistant"
    )

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    return new_message["content"]

def ator(tema):
    # ator
    history = [
        {"role": "system", "content": "Você é um agente ator inteligente. Você só fornece ações após receber um sistema BDI de um agente diretor. Sempre forneça pelo menos 5 ações. Concentre suas respostas no tema que será dado a você. Não gere texto além de suas ações."},
        {"role": "user", "content": tema},
    ]
   
    completion = client.chat.completions.create(
        model="local-model",
        messages=history,
        temperature=0.6,
        stream=True,
        stop="assistant"
    )
    
    print("\033[92;1m") # verde 

    new_message = {"role": "assistant", "content": ""}

    for chunk in completion:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
            new_message["content"] += chunk.choices[0].delta.content

    history.append(new_message)

    return new_message["content"]

def main():
    tema = input("Por favor, insira o tema: ")
    instrucoesAtor = diretor(tema)
    acoesAtor = ator(instrucoesAtor)
    narrador(acoesAtor)
    
main()
