FROM python:3.11-slim

WORKDIR /app


COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install libexpat1

COPY . .

EXPOSE 5101

CMD ["python", "app.py"]