FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all proto implementations needed by the gateway
COPY order_service/order_service_pb2.py .
COPY order_service/order_service_pb2_grpc.py .
COPY delivery_service/delivery_service_pb2.py .
COPY delivery_service/delivery_service_pb2_grpc.py .
COPY restaurant_service/restaurant_service_pb2.py .
COPY restaurant_service/restaurant_service_pb2_grpc.py .
COPY customer_service/customer_service_pb2.py .
COPY customer_service/customer_service_pb2_grpc.py .

# Copy the gateway implementation
COPY gateway/gateway.py .

EXPOSE 50050

CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "50050"]