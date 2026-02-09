import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import openai
from datetime import datetime  # ✅ Import correto

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot WhatsApp está rodando! ✅"

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Prompt personalizado
SEU_PERFIL = """
Você é Regivan, brasileiro, 44 anos, desenvolvedor de software.
Fala de forma casual, usa "amigo(a)", "valeu", "beleza","Deus abençoe", 
"Misericórdia", "tudo no tempo de Deus".
Respostas curtas, diretas, às vezes com emojis.
Nunca diga "como um modelo de IA".
"""

# ✅ CORREÇÃO: Definir client OpenAI corretamente
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').lower()
    sender = request.form.get('From', '')  # Número de quem enviou

    # LOG DETALHADO - aparece no Render
    print("\n" + "="*50)
    print(f"📱 NOVA MENSAGEM RECEBIDA")
    print(f"⏰ Hora: {datetime.now()}")  # ✅ Agora funciona
    print(f"👤 De: {sender}")
    print(f"💬 Texto: {msg}")
    print("="*50 + "\n")
    
    # SUAS REGRAS PERSONALIZADAS
    if 'oi' in msg or 'olá' in msg or 'ola' in msg:
        resposta = "E aí! Tudo bem? Como posso ajudar? 😊"
    
    elif 'tudo bem' in msg or 'como vai' in msg:
        resposta = "Tudo ótimo por aqui! Graças a Deus! E com você? 🙏"
    
    elif 'horas' in msg or 'hora' in msg:
        hora = datetime.now().strftime("%H:%M")  # ✅ Funciona
        resposta = f"Agora são {hora} ⏰"
    
    elif 'nome' in msg or 'quem é você' in msg:
        resposta = "Sou seu assistente pessoal! Pode me chamar de Dev_An 😄"
    
    elif 'ajuda' in msg or 'comandos' in msg:
        resposta = "Posso responder sobre: horas, data, ou conversar normalmente!"
    
    elif 'deus' in msg:
        resposta = "Deus é bom o tempo todo! Tudo no tempo d'Ele! 🙌"
    
    else:
        # Se não cair nas regras, usa IA (OpenAI)
        try:
            # Use o SEU_PERFIL completo
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SEU_PERFIL},
                    {"role": "user", "content": msg}
                ],
                max_tokens=150,
                temperature=0.8
            )
            resposta = response.choices[0].message.content
            
        except Exception as e:
            print(f"Erro OpenAI: {e}")
            resposta = "Estou aprendendo ainda! Pode reformular a pergunta? 😅"
    
    # LOG da resposta
    print(f"🤖 RESPOSTA: {resposta}")
    
    # Envia resposta
    resp = MessagingResponse()
    resp.message(resposta)
    return str(resp)

# Render usa PORT automático
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)