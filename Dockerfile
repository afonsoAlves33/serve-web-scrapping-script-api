FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add python3 python3-dev g++ unixodbc-dev \
    && python3 -m ensurepip \
    && pip3 install --user pyodbc \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
