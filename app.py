import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# Configuração segura do OpenAI (não quebra se não tiver)
openai_available = False

try:
    # NOVA SINTAXE OpenAI v1.x
    from openai import OpenAI
    
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key and api_key.startswith('sk-'):
        client = OpenAI(api_key=api_key)
        openai_available = True
        print("✅ OpenAI configurado (v1.x)")
    else:
        print("⚠️ OPENAI_API_KEY inválida ou não encontrada")
        openai_available = False
except Exception as e:
    print(f"⚠️ OpenAI não disponível: {e}")
    openai_available = False

@app.route('/')
def home():
    return "Bot WhatsApp está rodando! ✅"

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    msg = request.form.get('Body', '').strip()
    sender = request.form.get('From', '')

    # LOG
    print("\n" + "="*50)
    print(f"📱 DE: {sender[:20]}... | MENSAGEM: {msg}")
    
    # Converte para minúsculas para comparação
    msg_lower = msg.lower()
    
    # RESPOSTAS FIXAS (100% funcional SEM OpenAI)
    if not msg:
        resposta = "Ops, não recebi nenhuma mensagem! 🤔"
    
    elif any(palavra in msg_lower for palavra in ['oi', 'olá', 'ola', 'eae', 'salve']):
        resposta = "E aí amigo! Tudo na paz? Deus abençoe! 🙏"
    
    elif any(palavra in msg_lower for palavra in ['tudo bem', 'como vai', 'tudo bom']):
        resposta = "Tudo ótimo, graças a Deus! E você? 😊"
    
    elif any(palavra in msg_lower for palavra in ['horas', 'hora', 'que horas']):
        hora = datetime.now().strftime("%H:%M")
        resposta = f"Agora são {hora} ⏰"
    
    elif any(palavra in msg_lower for palavra in ['nome', 'quem é', 'quem é você']):
        resposta = "Sou o Dev_An, assistente do Regivan! Prazer! 😄"
    
    elif any(palavra in msg_lower for palavra in ['deus', 'jesus', 'abençoe']):
        resposta = "Deus é bom o tempo todo! Tudo no tempo d'Ele! 🙌"
    
    elif 'misericórdia' in msg_lower:
        resposta = "Misericórdia, Senhor! Que Deus nos abençoe sempre! ✨"
    
    elif any(palavra in msg_lower for palavra in ['obrigado', 'valeu', 'obrigada']):
        resposta = "Por nada! Que Deus continue te abençoando! 😊"
    
    elif msg_lower.startswith('!ajuda') or msg_lower == '!comandos':
        resposta = """📋 *Comandos disponíveis:*
• *!hora* - Mostra a hora atual
• *!data* - Mostra a data atual  
• *!status* - Verifica se o bot está online
• *!nome* - Descobre quem sou eu

Ou apenas converse normalmente! 😊"""
    
    elif msg_lower == '!hora':
        hora = datetime.now().strftime("%H:%M")
        resposta = f"⏰ *Hora atual:* {hora}"
    
    elif msg_lower == '!data':
        data = datetime.now().strftime("%d/%m/%Y")
        resposta = f"📅 *Data atual:* {data}"
    
    elif msg_lower == '!status':
        resposta = f"✅ *Status:* Bot online!\n🕒 {datetime.now().strftime('%H:%M')}\n🤖 OpenAI: {'Disponível' if openai_available else 'Modo básico'}"
    
    elif msg_lower == '!nome':
        resposta = "Me chamo *Dev_An*! Fui criado pelo Regivan para ajudar no WhatsApp! 😄"
    
    # PERGUNTAS ESPECÍFICAS
    elif 'idade' in msg_lower:
        resposta = "Meu criador tem 44 anos! Mas eu sou eternamente jovem! 😄"
    
    elif any(palavra in msg_lower for palavra in ['trabalho', 'faz', 'profissão']):
        resposta = "Sou desenvolvedor de software! Ajudo a automatizar tarefas no WhatsApp! 💻"
    
    elif any(palavra in msg_lower for palavra in ['criador', 'fez', 'criou']):
        resposta = "Fui criado pelo Regivan usando Python + Flask! Muito café envolvido! ☕"
    
    # SE NÃO FOR NENHUM DOS ACIMA
    else:
        if openai_available:
            try:
                # Usa OpenAI se disponível
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Você é Regivan, 44 anos, desenvolvedor brasileiro. Fala como amigo casual. Use: 'Deus abençoe', 'misericórdia', 'tudo no tempo de Deus'. Respostas curtas (1-2 linhas) com emojis. Nunca diga que é uma IA."},
                        {"role": "user", "content": msg}
                    ],
                    max_tokens=80,
                    temperature=0.8
                )
                resposta = response.choices[0].message.content
                print(f"🤖 Resposta da IA para: '{msg[:30]}...'")
                
            except Exception as e:
                print(f"⚠️ Erro OpenAI: {e}")
                resposta = f"Entendi '{msg}'! No momento estou no modo básico. Tente !ajuda para comandos! 😊"
        else:
            # Fallback inteligente SEM OpenAI
            if '?' in msg:
                resposta = "Boa pergunta! No momento respondo melhor a comandos específicos. Digite *!ajuda* para ver opções! 😊"
            elif len(msg) < 3:
                resposta = "Mensagem muito curta! Pode digitar algo mais? 😅"
            else:
                # Resposta personalizada baseada em palavras-chave
                if any(palavra in msg_lower for palavra in ['amor', 'namorar', 'casamento']):
                    resposta = "O amor é lindo! Que Deus abençoe relacionamentos sinceros! ❤️"
                elif any(palavra in msg_lower for palavra in ['dinheiro', 'emprego', 'trabalho']):
                    resposta = "Deus proverá! Tudo no tempo d'Ele! Trabalhe com fé! 💼"
                elif any(palavra in msg_lower for palavra in ['saúde', 'doente', 'hospital']):
                    resposta = "Que Deus restaure a saúde! Misericórdia e cura! 🏥✨"
                elif any(palavra in msg_lower for palavra in ['família', 'filhos', 'parentes']):
                    resposta = "Família é bênção! Que Deus proteja seus entes queridos! 👨‍👩‍👧‍👦"
                else:
                    resposta = f"Entendi '{msg}'! Eu respondo sobre horários, datas, ou podemos conversar! Digite *!ajuda* para ver comandos! 😄"
    
    print(f"🤖 RESPOSTA: {resposta[:50]}...")
    print("="*50)
    
    resp = MessagingResponse()
    resp.message(resposta)
    return str(resp)

# Configuração de porta
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    print(f"🚀 Servidor iniciando na porta {port}")
    print(f"🔧 OpenAI disponível: {openai_available}")
    app.run(host='0.0.0.0', port=port, debug=True)