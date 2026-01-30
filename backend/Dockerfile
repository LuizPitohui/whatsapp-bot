# ESTADO DA ARTE 2026: Python 3.14 Slim
FROM python:3.14-slim

# Otimizações para Python em container
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Instalação de dependências do sistema
# Nota: libpq-dev é necessário para compilar drivers de banco, se necessário
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalação do Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# 1. Copia dependências
COPY pyproject.toml poetry.lock ./

# 2. Instala dependências (Ignorando o projeto raiz para evitar erro de README)
RUN poetry install --no-interaction --no-ansi --no-root

# 3. Copia o código fonte
COPY . .

EXPOSE 8000

# Script de entrada padrão (dev)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]