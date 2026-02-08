import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt personalizado
SEU_PERFIL = """
Você é Regivan, brasileiro, 44 anos, desenvolvedor de software.
Fala de forma casual, usa "amigo(a)", "valeu", "beleza","Deus abençoe", "Misericórdia", "tudo no tempo de Deus".
Respostas curtas, diretas, às vezes com emojis.
Nunca diga "como um modelo de IA".
"""

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').lower()
    sender = request.form.get('From', '')  # Número de quem enviou
    
    # LOG IMPORTANTE (aparece no Render)
    print(f"📱 DE: {sender} | MENSAGEM: {msg}")
    
    # SUAS REGRAS PERSONALIZADAS
    if 'oi' in msg or 'olá' in msg or 'ola' in msg or 'Bom dia' in msg:
        resposta = "E aí! Tudo bem? Como posso ajudar? 😊"
    
    elif 'tudo bem' in msg:
        resposta = "Tudo ótimo por aqui! E com você?"
    else:
        # Usa IA
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SEU_PERFIL},
                    {"role": "user", "content": msg}
                ],
                max_tokens=150,
                temperature=0.7
            )
            resposta = completion.choices[0].message.content
        except:
            resposta = "Deu ruim aqui, tenta de novo mais tarde 😅"

    # Responde via Twilio
    resp = MessagingResponse()
    resp.message(resposta)
    return str(resp)

@app.route('/')
def home():
    return "Bot WhatsApp está rodando!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)