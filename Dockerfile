FROM python:3.12.8-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libcurl4-openssl-dev \
    libgeos-dev \
    && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["shiny", "run", "--host", "0.0.0.0", "app.py"]