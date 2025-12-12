FROM python:3.11-slim

WORKDIR /app

# install psutil build deps (if needed)
RUN apt-get update && apt-get install -y gcc libffi-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
CMD ["python", "monitor.py"]
