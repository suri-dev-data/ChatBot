import spacy
import random
from flask import Flask, request
import requests

app = Flask(__name__)

# Solicite o token no facebook business suite.
ACCESS_TOKEN = "SEU_TOKEN_DO_FACEBOOK"
PHONE_NUMBER_ID = "SEU_PHONE_NUMBER_ID"
URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if "messages" in data["entry"][0]["changes"][0]["value"]:
        mensagem = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        numero = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        
        resposta = chatbot(mensagem)
        enviar_mensagem(numero, resposta)

    return "OK", 200

def enviar_mensagem(numero, mensagem):
    data = {
        "messaging_product": "whatsapp",
        "to": numero,
        "text": {"body": mensagem}
    }
    requests.post(URL, json=data, headers=HEADERS)

def chatbot(message):
    nlp = spacy.load("pt_core_news_sm")
    
    respostas = {
    "tempo": [
        "Quer saber sobre o clima? Dá uma olhada no site de previsão do tempo! ⛅",
        "O tempo pode mudar rápido! Melhor conferir a previsão antes de sair. 🌦️"
    ],
    "nome": [
        "Sou um chatbot feito com spaCy para te ajudar! 🤖",
        "Olá! Meu nome é Chatbot e estou aqui para auxiliar você. 😊"
    ],
    "ajudar": [
        "Me conta! Como posso te ajudar? 😊",
        "Estou aqui para ajudar. O que você precisa? 👀"
    ],
    "desenvolvimento": [
        "O desenvolvimento de software é fascinante! Você tem interesse em frontend ou backend? 💻",
        "Já ouviu falar sobre Clean Code? Manter o código organizado faz toda a diferença! 📖"
    ],
    "python": [
        "Python é uma linguagem incrível! Precisa de dicas sobre bibliotecas ou frameworks? 🐍",
        "Você já trabalhou com Django ou Flask? Se precisar de ajuda, me avise! 🚀"
    ],
    "debug": [
        "Depurar código pode ser desafiador! Já tentou usar print() ou um debugger como o PDB? 🧐",
        "Dividir o código em partes menores pode ajudar a encontrar o erro mais rápido. 🔍"
    ],
    "git": [
        "Git é essencial para controle de versão! Você precisa de ajuda com commits, branches ou merges? 🛠️",
        "Commits organizados fazem toda a diferença! Evite mensagens como 'update final v2'. 😅"
    ],
    "desconhecido": [
        "Desculpe, não entendi. Você pode reformular sua pergunta? 🤔",
        "Não tenho certeza sobre isso. Pode me explicar melhor? 😊"
    ],
    "saudação": [
        "Olá! Como posso te ajudar hoje? 😊",
        "Oi! Tudo bem? Me conta como posso te auxiliar! 👋"
    ],
    "despedida": [
        "Até logo! Se precisar, estarei por aqui. 👋",
        "Tchau! Qualquer coisa, é só chamar. 😊"
    ],
    "pedido": [
        "Gostaria de fazer um pedido? Me informe os detalhes. 🛒",
        "Qual produto você deseja comprar? Estou pronto para ajudar! 📦"
    ],
    "pagamento": [
        "Aceitamos pagamentos via Pix, cartão e boleto. Qual método você prefere? 💳",
        "O pagamento pode ser feito por Pix, cartão ou boleto. Como deseja proceder? 🏦"
    ],
    "entrega": [
        "As entregas são feitas em até 3 dias úteis. Você pode acompanhar pelo código de rastreamento. 📦",
        "Para qual endereço devemos enviar o pedido? 🚚"
    ],
    "suporte": [
        "Nosso suporte está disponível 24/7. Como posso te ajudar? 🛠️",
        "Se precisar de assistência, estou aqui para ajudar! 😊"
    ],
    "horário": [
        "Normalmente estou disponível a partir das 17h. ⏳",
        "Nosso horário de atendimento é das 8h às 18h. Como posso te ajudar? 🕒"
    ],
    "contato": [
        "Você pode entrar em contato pelo e-mail: viniciussurianolopesdasilva@gmail.com 📩",
        "Se precisar, meu e-mail é viniciussurianolopesdasilva@gmail.com. Estou à disposição! ✉️"
    ]
}
    
    user_input = message
    if user_input.lower() in ["sair", "tchau", "adeus"]:
        print("Chatbot: Até logo! Foi um prazer conversar com você.")
        return None
    
    doc = nlp(user_input)
    resposta = "desconhecido"
    
    for token in doc:
        # print(token.lemma_)
        if token.lemma_ in respostas:
            resposta = token.lemma_
            break
    
    return random.choice(respostas[resposta])

if __name__ == "__main__":
    app.run(port=5000)