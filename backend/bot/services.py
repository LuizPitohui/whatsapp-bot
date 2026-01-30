import requests
import logging

# Configurações Hardcoded (para facilitar agora, depois podemos mover para settings)
# O host é 'wppconnect' porque é o nome do serviço no docker-compose
API_URL = "http://wppconnect:21465" 
SESSION_NAME = "norte-tech"
SECRET_KEY = "123456"

logger = logging.getLogger(__name__)

class WppConnectService:
    def __init__(self):
        self.base_url = API_URL
        self.session = SESSION_NAME
        self.secret = SECRET_KEY
        self.token = self._get_token()

    def _get_token(self):
        """Gera um token novo para autenticação usando a SecretKey"""
        try:
            url = f"{self.base_url}/api/{self.session}/{self.secret}/generate-token"
            # Timeout curto para não travar o Django se o WPP estiver fora
            response = requests.post(url, timeout=5)
            
            if response.status_code in [200, 201]:
                data = response.json()
                # Tenta pegar o token de várias formas possíveis que a API retorna
                token = data.get('token') or data.get('session')
                return token
            
            logger.error(f"Falha ao gerar token WPPConnect: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Erro de conexão ao gerar token WPPConnect: {e}")
            return None

    def _get_headers(self):
        """Monta o cabeçalho com o Token Bearer"""
        if not self.token:
            # Tenta gerar novamente se estiver sem token
            self.token = self._get_token()
            
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def enviar_texto(self, numero, mensagem):
        """
        Envia mensagem de texto para um número (@c.us) ou grupo (@g.us).
        """
        url = f"{self.base_url}/api/{self.session}/send-message"
        
        payload = {
            "phone": numero,
            "message": mensagem,
            "isGroup": "@g.us" in numero
        }

        try:
            logger.info(f"Enviando msg WPP para {numero}...")
            response = requests.post(
                url, 
                json=payload, 
                headers=self._get_headers(), 
                timeout=10
            )
            
            if response.status_code == 201:
                logger.info(f"Mensagem enviada com sucesso para {numero}")
                return True
            else:
                logger.error(f"Erro WPP ({response.status_code}): {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exceção ao enviar mensagem WPP: {e}")
            return False

    def enviar_para_grupo(self, grupo_id, mensagem):
        """
        Alias para enviar especificamente para grupos.
        Garante que o ID tenha o sufixo correto.
        """
        if "@" not in grupo_id:
            grupo_id = f"{grupo_id}@g.us"
            
        return self.enviar_texto(grupo_id, mensagem)