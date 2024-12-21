FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python download.py

EXPOSE 8080

CMD ["shiny", "run", "app.py"]