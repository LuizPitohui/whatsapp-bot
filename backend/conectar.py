import requests
import base64
import os
import time

# CONFIGURAÇÕES
API_URL = "http://localhost:8080" 
API_KEY = "123456"
INSTANCE_NAME = "norte-tech"

def conectar():
    print(f"🔄 Conectando a: {API_URL}")
    headers = {"apikey": API_KEY, "Content-Type": "application/json"}

    # 1. TENTA CRIAR
    print(f"1. Verificando instância '{INSTANCE_NAME}'...")
    try:
        url_create = f"{API_URL}/instance/create"
        payload = {
            "instanceName": INSTANCE_NAME,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        resp = requests.post(f"{url_create}?apikey={API_KEY}", json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 403:
            print("   ℹ️ Instância já existe. Avançando para o QR Code...")
        elif resp.status_code == 201:
            print("   ✅ Instância criada agora!")
    except Exception as e:
        print(f"   ❌ Erro de conexão inicial: {e}")
        return

    # 2. BUSCA O QR CODE (LOOP LONGO)
    print("-" * 40)
    print("2. Buscando QR Code (Isso pode levar até 60 segundos)...")
    
    url_connect = f"{API_URL}/instance/connect/{INSTANCE_NAME}?apikey={API_KEY}"

    # AUMENTEI PARA 60 TENTATIVAS (2 MINUTOS)
    for i in range(60):
        try:
            resp = requests.get(url_connect, headers=headers, timeout=5)
            
            if resp.status_code != 200:
                print(f"   ⚠️ API retornou status {resp.status_code}...")
                time.sleep(2)
                continue

            data = resp.json()
            
            # Checa se já conectou
            if data.get('instance', {}).get('state') == 'open':
                print("\n✅ SUCESSO! O WhatsApp JÁ ESTÁ CONECTADO!")
                print("   O Bot está pronto para responder.")
                return

            # Busca o base64
            base64_code = data.get('base64') or data.get('qrcode', {}).get('base64')
            
            if base64_code:
                # Salva a imagem
                img_data = base64.b64decode(base64_code.replace("data:image/png;base64,", ""))
                with open("qrcode.png", "wb") as f:
                    f.write(img_data)
                
                print(f"\n✅ QR CODE GERADO na tentativa {i+1}!")
                print("   Abrindo imagem automaticamente...")
                
                try:
                    os.startfile("qrcode.png")
                except:
                    print("   Abra o arquivo 'qrcode.png' na pasta para escanear.")
                return

            print(f"   ⏳ Tentativa {i+1}/60: Motor do WhatsApp iniciando...")
            time.sleep(2)
            
        except Exception as e:
            print(f"   ⚠️ Falha na conexão ({e}). Tentando novamente...")
            time.sleep(2)
    
    print("\n❌ Tempo esgotado. Verifique os logs do docker: docker logs norte_tech_whatsapp")

if __name__ == "__main__":
    conectar()