FROM python:3.11-slim

WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "server.py"]
FROM jrottenberg/ffmpeg:6.0-alpine

WORKDIR /app

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "server.py"]
