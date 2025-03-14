FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the client implementation
COPY client/client.py .

CMD ["python", "client.py"]