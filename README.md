🤖 Norte Tech Bot - Sistema de Atendimento via WhatsApp
Este projeto é um sistema de Chatbot para triagem e atendimento automático via WhatsApp, orquestrado via Docker. Ele utiliza o WPPConnect para a interface com o WhatsApp e Django (Python) como o cérebro lógico (Máquina de Estados).

🏗 Arquitetura do Sistema
O sistema é composto por 4 containers Docker que se comunicam através de uma rede interna (norte-network):

wppconnect (Node.js 18):

Servidor responsável por rodar o navegador (Chromium/Puppeteer) headless.

Gerencia a sessão do WhatsApp e o QR Code.

Envia eventos (Webhooks) para o Django quando mensagens chegam.

Expõe uma API REST para o Django enviar mensagens.

backend (Django 5 + Python 3.12):

Recebe os Webhooks.

Processa a lógica de atendimento (Menu -> Seleção -> Encaminhamento).

Salva o histórico e estado do atendimento no Banco de Dados.

postgres (PostgreSQL 15):

Banco de dados relacional para persistência de colaboradores e atendimentos.

redis (Redis 7):

Broker de mensagens e cache (utilizado pelo Django/Celery se necessário futuramente).

🚀 Como Rodar o Projeto
Pré-requisitos
Docker & Docker Compose instalados.

Poetry (opcional, para rodar scripts locais de teste).

Passos para Inicialização
Clone o repositório e configure as variáveis de ambiente: Certifique-se de ter o arquivo .env na raiz (baseado no .env.example).

Construção e Subida dos Containers: Utilizamos um build forçado para garantir que as dependências do Node e Python estejam frescas.

Bash
docker-compose up -d --build
Aplicar Migrações do Banco de Dados: Necessário na primeira execução para criar as tabelas Colaborador e Atendimento.

Bash
docker exec -it norte_tech_django python manage.py migrate
Conectar o WhatsApp:

Visualize os logs para saber quando o servidor está pronto:

Bash
docker logs -f norte_tech_wpp
Gere o QR Code (via script auxiliar ou acessando a API) e escaneie com o celular.

🛠 Detalhes Técnicos Importantes (Para Desenvolvedores)
1. O Webhook "Camaleão" (views.py)
O WPPConnect pode enviar o payload JSON de duas formas dependendo da versão ou evento: aninhado em data: {} ou plano na raiz. Implementamos uma estratégia de busca robusta no WebhookView para evitar erros de NoneType:

Python
# Trecho da lógica em backend/bot/views.py
payload = data.get('data') if 'data' in data and isinstance(data['data'], dict) else data
sender = payload.get('from')
body = payload.get('body')
Filtros: Ignoramos eventos onack (confirmação de leitura), onparticipantschanged e mensagens enviadas pelo próprio bot (fromMe: true).

2. Correção de Docker e WPPConnect
Enfrentamos problemas de compatibilidade entre Node 20, Yarn Moderno e Docker. A solução estável implementada no Dockerfile do diretório wppconnect-server:

Base Image: node:18-bullseye-slim (Debian é mais estável que Alpine para Chrome).

Fontes: Instalação manual de fonts-liberation, fonts-freefont-ttf e libgbm1. Sem isso, o Chrome abre mas não consegue renderizar o texto do QR Code, causando crash.

Dependências:

Dockerfile
# Ordem crítica para funcionar o Yarn Berry
COPY . .
RUN rm -rf node_modules yarn.lock # Limpa lixo do Windows
RUN corepack enable
RUN yarn install
RUN yarn build
3. Argumentos do Puppeteer (config.ts)
Para evitar o crash do Chrome dentro do Docker (erro de memória compartilhada), injetamos as seguintes flags no src/config.ts:

--disable-dev-shm-usage: Usa /tmp em vez de /dev/shm.

--no-sandbox: Necessário para rodar como root no container.

--single-process: Evita zumbis de processos.

4. Networking
Os containers se comunicam via http://backend:8000 e http://wppconnect:21465.

Erro Comum: ENOTFOUND backend.

Solução: Foi definida a rede norte-network no docker-compose.yml e atribuída a todos os serviços.

📂 Estrutura de Arquivos
Plaintext
norte-tech-bot/
├── backend/                 # Aplicação Django
│   ├── bot/                 # App principal (Models, Views, Services)
│   │   ├── services.py      # Lógica de envio p/ API do WPP
│   │   └── views.py         # Webhook Receiver
│   ├── config/              # Settings do Django
│   └── Dockerfile           # Receita da imagem Django
├── wppconnect-server/       # Servidor Node.js (Clonado/Modificado)
│   ├── src/config.ts        # Configurações do Puppeteer injetadas
│   └── Dockerfile           # Receita Node 18 + Chrome + Fontes
├── docker-compose.yml       # Orquestrador
├── conectar_wpp.py          # Script Python para gerar Token/QR Code
└── teste_final.py           # Script para testar envio de mensagens
🐛 Troubleshooting (Solução de Problemas)
1. O Bot parou de responder.

Verifique se a sessão caiu. Apague a pasta wpp_sessions e reinicie o container wppconnect para escanear novamente.

2. Erro "Connection Refused" no Django.

O container do Postgres pode não ter subido a tempo. O depends_on no docker-compose ajuda, mas verifique os logs: docker logs norte_tech_postgres.

3. Loop de mensagens.

Verifique no views.py se a verificação if from_me: está ativa. Se não estiver, o bot responderá às próprias mensagens infinitamente.

Desenvolvido por: Luiz Guedes, Aron Pimentel & Nexus (AI Assistant). Data: Janeiro/2026.