FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY food_service.proto .
COPY food_service_pb2.py .
COPY food_service_pb2_grpc.py .
COPY server.py .

EXPOSE 50051

CMD ["python", "service.py"]