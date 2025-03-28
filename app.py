from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Variáveis de configuração
TOKEN = 'SEU_TOKEN'  # Substitua pelo seu token
PHONE_NUMBER_ID = 'SEU_PHONE_NUMBER_ID'  # Substitua pelo seu ID de número de telefone
VERIFY_TOKEN = 'TOKEN_DE_VERIFICACAO'  # Token de verificação do webhook
WEBHOOK_URL = 'http://localhost:5000/webhook'  # URL para onde o WhatsApp vai enviar mensagens

# Endpoint para verificar se a URL do Webhook é válida
@app.route('/webhook', methods=['GET'])
def verify_webhook():
    # O WhatsApp verifica a URL do webhook com o token de verificação
    if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
        if request.args.get('hub.verify_token') == VERIFY_TOKEN:
            return request.args['hub.challenge'], 200
        return 'Token de verificação inválido', 403
    return 'Erro', 400

# Endpoint para receber mensagens
@app.route('/webhook', methods=['POST'])
def handle_message():
    data = request.get_json()

    # Extrai a mensagem recebida
    message = data['entry'][0]['changes'][0]['value']['messages'][0]
    from_number = message['from']
    text_message = message['text']['body']

    # Processa a mensagem - Exemplo simples de resposta
    response_text = process_message(text_message)

    # Envia a resposta de volta para o WhatsApp
    send_message(from_number, response_text)

    return jsonify({"status": "ok"}), 200

# Função que processa a mensagem recebida
def process_message(text):
    if 'gasto' in text.lower():
        return "Envie sua despesa no formato: Produto + Valor (ex: Camisa 99)"
    else:
        return f"Você disse: {text}"

# Função para enviar mensagens ao WhatsApp
def send_message(to, message):
    url = f'https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages'
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'messaging_product': 'whatsapp',
        'to': to,
        'text': {'body': message}
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.json())

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
