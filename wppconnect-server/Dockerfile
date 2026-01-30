# Usamos Node 18 (Debian Bullseye - Estável)
FROM node:18-bullseye-slim

# 1. Instalar dependências do sistema, Chromium E FONTES (A Correção)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    procps \
    chromium \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    fonts-freefont-ttf \
    git \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 2. Configurar Pasta de Trabalho
WORKDIR /usr/src/wpp-server

# 3. Copiar TUDO para garantir que o Yarn veja o projeto
COPY . .

# 4. Limpeza preventiva
RUN rm -rf node_modules .yarn/cache yarn.lock

# 5. Habilitar Corepack
RUN corepack enable

# 6. Instalar Dependências
RUN yarn install

# 7. Construir o projeto
RUN yarn build

# 8. Variáveis de Ambiente para o Chrome
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
ENV CHROME_BIN=/usr/bin/chromium

# 9. Expor Porta e Rodar
EXPOSE 21465
CMD ["node", "dist/server.js"]