# Imagem base com Python
FROM python:3.11

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos
COPY . .

# Garante que o sitecustomize seja detectado
ENV PYTHONPATH=/app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    xvfb \
    && apt-get clean

# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Instala os navegadores do Playwright
RUN playwright install --with-deps

# Comando padrão: roda os testes
CMD ["pytest", "tests/"]
