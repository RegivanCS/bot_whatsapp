import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime
from openai import OpenAI  # ✅ Import correto

app = Flask(__name__)

# ✅ Configuração CORRETA do OpenAI
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

@app.route('/')
def home():
    return "Bot WhatsApp está rodando! ✅"

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').lower()
    sender = request.form.get('From', '')

    # LOG
    print("\n" + "="*50)
    print(f"📱 DE: {sender} | MENSAGEM: {msg}")
    
    # RESPOSTAS FIXAS (funciona SEM OpenAI)
    if 'oi' in msg or 'olá' in msg or 'ola' in msg:
        resposta = "E aí amigo! Tudo na paz? Deus abençoe! 🙏"
    
    elif 'tudo bem' in msg or 'como vai' in msg:
        resposta = "Tudo ótimo, graças a Deus! E você? 😊"
    
    elif 'horas' in msg:
        hora = datetime.now().strftime("%H:%M")
        resposta = f"Agora são {hora} ⏰"
    
    elif 'nome' in msg:
        resposta = "Sou o Dev_An, assistente do Regivan! Prazer! 😄"
    
    elif 'deus' in msg:
        resposta = "Deus é bom o tempo todo! Tudo no tempo d'Ele! 🙌"
    
    elif msg.startswith('!'):  # Comandos especiais
        if msg == '!ajuda':
            resposta = "Comandos: !hora, !data, !nome"
        elif msg == '!hora':
            hora = datetime.now().strftime("%H:%M")
            resposta = f"⏰ {hora}"
        elif msg == '!data':
            data = datetime.now().strftime("%d/%m/%Y")
            resposta = f"📅 {data}"
    
    else:
        # Tenta OpenAI, mas tem fallback
        try:
            resposta = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é Regivan, brasileiro, 44 anos, desenvolvedor. Fala casual como um amigo, usa 'Deus abençoe', 'misericórdia'. Respostas curtas com emojis."},
                    {"role": "user", "content": msg}
                ],
                max_tokens=100,
                temperature=0.7
            ).choices[0].message.content
            
        except Exception as e:
            print(f"⚠️ OpenAI offline: {e}")
            # Fallback inteligente
            if '?' in msg:
                resposta = "Boa pergunta! No momento estou sem conexão com a IA. Que tal perguntar a hora ou data? ⏰"
            else:
                resposta = f"Entendi '{msg}'! No momento respondo apenas comandos específicos. Digite '!ajuda' para ver opções. 😊"
    
    print(f"🤖 RESPOSTA: {resposta}")
    print("="*50)
    
    resp = MessagingResponse()
    resp.message(resposta)
    return str(resp)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)