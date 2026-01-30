import requests
import base64
import os
import time
from datetime import datetime

# --- CONFIGURAÇÕES ---
API_URL = "http://localhost:8080" 
API_KEY = "123456"
INSTANCE_NAME = "norte-tech"

def log(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def busca_infinita():
    print("="*50)
    print(f"🚀 INICIANDO BUSCA INFINITA POR QR CODE")
    print(f"📡 Alvo: {API_URL} (Instância: {INSTANCE_NAME})")
    print("   Pressione CTRL + C para parar quando quiser.")
    print("="*50)

    # 1. Tenta garantir que a instância existe (uma única vez no início)
    try:
        url_create = f"{API_URL}/instance/create"
        payload = {
            "instanceName": INSTANCE_NAME,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        headers = {"apikey": API_KEY, "Content-Type": "application/json"}
        requests.post(f"{url_create}?apikey={API_KEY}", json=payload, headers=headers, timeout=5)
    except:
        pass # Se der erro aqui, o loop abaixo vai pegar

    tentativa = 1
    inicio = time.time()

    # 2. LOOP INFINITO
    while True:
        try:
            url_connect = f"{API_URL}/instance/connect/{INSTANCE_NAME}?apikey={API_KEY}"
            headers = {"apikey": API_KEY}
            
            # Timeout curto para não travar o script se o servidor estiver lento
            resp = requests.get(url_connect, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                
                # A. Checa se já conectou
                state = data.get('instance', {}).get('state')
                if state == 'open':
                    print("\n" + "="*50)
                    log("✅ SUCESSO! O WhatsApp JÁ ESTÁ CONECTADO!")
                    print("="*50)
                    break

                # B. Checa se tem QR Code
                base64_code = data.get('base64') or data.get('qrcode', {}).get('base64')
                
                if base64_code:
                    # Limpa e salva
                    img_data = base64.b64decode(base64_code.replace("data:image/png;base64,", ""))
                    with open("qrcode.png", "wb") as f:
                        f.write(img_data)
                    
                    print("\n" + "="*50)
                    log(f"✅ QR CODE CAPTURADO NA TENTATIVA {tentativa}!")
                    print("="*50)
                    
                    # Abre a imagem
                    try:
                        os.startfile("qrcode.png")
                    except:
                        log("⚠️ Imagem salva como 'qrcode.png'. Abra manualmente!")
                    break
                
                # Se respondeu 200 mas não tem QR nem Conexão (ainda carregando)
                tempo_decorrido = int(time.time() - inicio)
                print(f"\r⏳ Tentativa {tentativa} ({tempo_decorrido}s): Aguardando geração do QR Code...", end="")
            
            else:
                # Erro 404, 403, 500
                print(f"\r⚠️ Tentativa {tentativa}: API respondeu status {resp.status_code}...", end="")

        except requests.exceptions.ConnectionError:
            print(f"\r❌ Tentativa {tentativa}: Servidor indisponível (Tentando reconectar...)", end="")
        except Exception as e:
            print(f"\r⚠️ Tentativa {tentativa}: Erro genérico ({str(e)})", end="")

        tentativa += 1
        time.sleep(5) # Espera 5 segundos entre tentativas

if __name__ == "__main__":
    busca_infinita()