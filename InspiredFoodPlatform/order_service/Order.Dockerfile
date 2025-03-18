FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY order_service/order_service_pb2.py .
COPY order_service/order_service_pb2_grpc.py .
COPY order_service/order_service.py .
EXPOSE 50051
CMD ["python", "order_service.py"]