import requests
import base64
import os
import time

API_URL = "http://localhost:21465"
SECRET_KEY = "123456"
SESSION_NAME = "norte-tech"

def conectar():
    print("🚀 Iniciando Conexão V2 (Tagarela)...")
    
    # 1. Gera Token
    try:
        url_token = f"{API_URL}/api/{SESSION_NAME}/{SECRET_KEY}/generate-token"
        resp = requests.post(url_token)
        if resp.status_code in [200, 201]:
            token = resp.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Token OK.")
        else:
            print(f"❌ Erro Token: {resp.text}")
            return
    except Exception as e:
        print(f"❌ Servidor Offline? {e}")
        return

    # 2. Inicia Sessão (Se já não estiver rodando)
    print("📡 Solicitando início de sessão...")
    try:
        requests.post(f"{API_URL}/api/{SESSION_NAME}/start-session", 
                     json={"webhook": "http://backend:8000/api/webhook/", "waitQrCode": True}, 
                     headers=headers)
    except:
        pass

    # 3. Monitoramento de Estado (O Segredo)
    print("🕵️ Monitorando Status do Servidor...")
    
    for i in range(60): # Tenta por 2 minutos (browser pode demorar)
        try:
            # Pede o status atual para o servidor
            resp_status = requests.get(f"{API_URL}/api/{SESSION_NAME}/status-session", headers=headers)
            
            if resp_status.status_code == 200:
                dados = resp_status.json()
                status = dados.get('status') or dados.get('qrCode') # Varia conforme versao
                
                print(f"\r⏳ Tentativa {i}/60 - Status Atual: {status}   ", end="")
                
                # Se o status indicar que tem QR Code...
                if status == 'qrRead' or status == 'inChat':
                     print("\n✅ JÁ CONECTADO! Pare de tentar.")
                     return
                
                # Tenta baixar a imagem independente do status
                resp_qr = requests.get(f"{API_URL}/api/{SESSION_NAME}/auth/qr-code", headers=headers)
                if resp_qr.status_code == 200 and 'image/png' in resp_qr.headers.get('Content-Type', ''):
                    print("\n\n📸 QR CODE RECEBIDO!!!")
                    with open("qrcode_final.png", "wb") as f:
                        f.write(resp_qr.content)
                    os.startfile("qrcode_final.png")
                    print("✅ Imagem aberta. Escaneie rápido!")
                    return

            else:
                print(f"\r⚠️ Erro ao checar status: {resp_status.status_code}", end="")

            time.sleep(2)
            
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            time.sleep(2)

if __name__ == "__main__":
    conectar()