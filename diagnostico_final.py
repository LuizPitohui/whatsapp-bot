import requests
import json

# Configurações iguais ao Docker
API_URL = "http://localhost:21465"
SESSION_NAME = "norte-tech"
SECRET_KEY = "123456"

def diagnostico():
    print("🕵️‍♂️ INICIANDO DIAGNÓSTICO DETALHADO...")
    print(f"🎯 Alvo: {API_URL}")
    
    # 1. Teste Básico de Vida (O mesmo do navegador)
    try:
        print("\n1️⃣ Testando acesso à Home/Docs...")
        resp_home = requests.get(f"{API_URL}/api-docs")
        print(f"   Status: {resp_home.status_code}")
        if resp_home.status_code == 200:
            print("   ✅ Servidor acessível via Python!")
        else:
            print("   ❌ Servidor respondeu com erro na Home.")
    except Exception as e:
        print(f"   ❌ ERRO FATAL DE CONEXÃO: {e}")
        print("   ⚠️ Verifique se o Docker está rodando e se não há VPN/Firewall.")
        return

    # 2. Tentativa de Gerar Token (Onde estava falhando)
    print(f"\n2️⃣ Tentando gerar Token para sessão '{SESSION_NAME}'...")
    url_token = f"{API_URL}/api/{SESSION_NAME}/{SECRET_KEY}/generate-token"
    
    try:
        resp = requests.post(url_token)
        print(f"   📡 URL Usada: {url_token}")
        print(f"   🔢 Status Code: {resp.status_code}")
        print(f"   📄 Resposta Bruta: {resp.text}")
        
        if resp.status_code == 200:
            data = resp.json()
            token = data.get('token') or data.get('session') # Tenta achar onde está o token
            if token:
                print(f"   ✅ TOKEN GERADO: {token[:15]}...")
                iniciar_sessao(token)
            else:
                print("   ⚠️ Status 200, mas não achei o campo 'token' no JSON.")
        else:
            print("   ❌ O servidor recusou a geração do token.")

    except Exception as e:
        print(f"   ❌ Erro na requisição: {e}")

def iniciar_sessao(token):
    print("\n3️⃣ Tentando Iniciar Sessão e Pegar QR Code...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Payload para iniciar
    payload = {
        "webhook": "http://backend:8000/api/webhook/",
        "waitQrCode": True
    }
    
    try:
        # Iniciar Sessão
        resp_start = requests.post(
            f"{API_URL}/api/{SESSION_NAME}/start-session",
            json=payload,
            headers=headers
        )
        print(f"   Status Start: {resp_start.status_code}")
        print(f"   Resp Start: {resp_start.text}")
        
        # Buscar QR Code
        resp_qr = requests.get(
            f"{API_URL}/api/{SESSION_NAME}/auth/qr-code",
            headers=headers
        )
        
        if resp_qr.status_code == 200:
            print("\n   ✅✅ SUCESSO! QR CODE ENCONTRADO!")
            with open("diagnostico_qrcode.png", "wb") as f:
                f.write(resp_qr.content)
            print("   🖼️ Imagem salva como 'diagnostico_qrcode.png'")
            import os
            os.startfile("diagnostico_qrcode.png")
        else:
            print(f"   ❌ Não consegui baixar o QR Code. Status: {resp_qr.status_code}")
            
    except Exception as e:
        print(f"   ❌ Erro ao iniciar sessão: {e}")

if __name__ == "__main__":
    diagnostico()