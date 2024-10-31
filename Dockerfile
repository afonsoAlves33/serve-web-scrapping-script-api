FROM python:3.11-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de requisitos
COPY requirements.txt .

# Instala as dependências necessárias
RUN apk update && \
    apk add --no-cache \
        python3 \
        python3-dev \
        g++ \
        unixodbc-dev \
        curl \
        gnupg && \
    # Detecta a arquitetura
    case $(uname -m) in \
        x86_64) architecture="amd64" ;; \
        arm64) architecture="arm64" ;; \
        *) architecture="unsupported" ;; \
    esac && \
    if [[ "unsupported" == "$architecture" ]]; then \
        echo "Alpine architecture $(uname -m) is not currently supported."; \
        exit; \
    fi && \
    # Faz o download dos pacotes desejados
    curl -O https://download.microsoft.com/download/7/6/d/76de322a-d860-4894-9945-f0cc5d6a45f8/msodbcsql18_18.4.1.1-1_$architecture.apk && \
    curl -O https://download.microsoft.com/download/7/6/d/76de322a-d860-4894-9945-f0cc5d6a45f8/mssql-tools18_18.4.1.1-1_$architecture.apk && \
    # Faz o download das assinaturas
    curl -O https://download.microsoft.com/download/7/6/d/76de322a-d860-4894-9945-f0cc5d6a45f8/msodbcsql18_18.4.1.1-1_$architecture.sig && \
    curl -O https://download.microsoft.com/download/7/6/d/76de322a-d860-4894-9945-f0cc5d6a45f8/mssql-tools18_18.4.1.1-1_$architecture.sig && \
    # Importa a chave e verifica as assinaturas
    curl https://packages.microsoft.com/keys/microsoft.asc | gpg --import - && \
    gpg --verify msodbcsql18_18.4.1.1-1_$architecture.sig msodbcsql18_18.4.1.1-1_$architecture.apk && \
    gpg --verify mssql-tools18_18.4.1.1-1_$architecture.sig mssql-tools18_18.4.1.1-1_$architecture.apk && \
    # Instala os pacotes
    apk add --allow-untrusted msodbcsql18_18.4.1.1-1_$architecture.apk && \
    apk add --allow-untrusted mssql-tools18_18.4.1.1-1_$architecture.apk && \
    # Instala pyodbc
    python3 -m ensurepip && \
    pip3 install --user pyodbc && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante dos arquivos
COPY . .

# Expõe a porta
EXPOSE 4500

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4500", "--reload"]
