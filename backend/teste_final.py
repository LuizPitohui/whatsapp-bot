import requests
import time

# Configurações
API_URL = "http://localhost:21465"
SESSION = "norte-tech"
SECRET = "123456"

# 🎯 NÚMERO DO AMIGO (Com o sufixo mágico @c.us)
# @c.us = Contact User (Para pessoas)
# @g.us = Group User (Para grupos)
NUMERO_DESTINO = "559284529951@c.us" 

def teste_completo():
    print(f"🚀 Iniciando Teste de Envio para {NUMERO_DESTINO}...\n")

    # 1. Gerar Token
    print("1️⃣ Gerando Token de Acesso...")
    try:
        resp = requests.post(f"{API_URL}/api/{SESSION}/{SECRET}/generate-token")
        if resp.status_code in [200, 201]:
            data = resp.json()
            token = data.get('token') or data.get('session')
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Token OK.")
        else:
            print(f"❌ Erro Token: {resp.text}")
            return
    except Exception as e:
        print(f"❌ Erro Conexão (Token): {e}")
        return

    # 2. Enviar Mensagem (Com persistência)
    print(f"\n2️⃣ Enviando mensagem...")
    payload_msg = {
        "phone": NUMERO_DESTINO,
        "message": "🤖 *Olá! Eu sou o Bot da Norte Tech.*\n\nSe chegou, o sistema está 100% ONLINE! 🚀✅",
        "isGroup": False
    }
    
    # Tenta enviar 3 vezes caso o servidor esteja ocupado sincronizando
    for tentativa in range(1, 4):
        try:
            print(f"   Tentativa {tentativa}...")
            resp_msg = requests.post(f"{API_URL}/api/{SESSION}/send-message", json=payload_msg, headers=headers)
            
            if resp_msg.status_code == 201:
                print("\n🎉🎉 SUCESSO! MENSAGEM ENVIADA!")
                print("✅ O servidor aceitou o pedido.")
                print("📲 Peça para seu amigo confirmar no WhatsApp dele!")
                return
            else:
                print(f"   ⚠️ Falha (Status {resp_msg.status_code}): {resp_msg.text}")
                time.sleep(2) # Espera um pouco

        except Exception as e:
            print(f"   ⚠️ Erro de conexão: {e}")
            print("   (O servidor deve estar sincronizando mensagens antigas, tentando de novo...)")
            time.sleep(3)

    print("\n❌ Todas as tentativas falharam. O servidor ainda está ocupado.")

if __name__ == "__main__":
    teste_completo()