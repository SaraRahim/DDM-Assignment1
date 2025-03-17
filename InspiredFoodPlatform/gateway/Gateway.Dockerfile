FROM python:3.9-slim

WORKDIR /app

# Copy entire project
COPY . .

# Set PYTHONPATH to include the project root
ENV PYTHONPATH=/app:$PYTHONPATH

# Install requirements from root directory
RUN pip install --no-cache-dir -r requirements.txt

# Copy proto files
COPY order_service/order_service_pb2.py order_service/
COPY order_service/order_service_pb2_grpc.py order_service/
COPY restaurant_service/restaurant_service_pb2.py restaurant_service/
COPY restaurant_service/restaurant_service_pb2_grpc.py restaurant_service/
COPY delivery_service/delivery_service_pb2.py delivery_service/
COPY delivery_service/delivery_service_pb2_grpc.py delivery_service/

# Copy gateway script
COPY gateway/gateway.py .

CMD ["uvicorn", "gateway.gateway:app", "--host", "0.0.0.0", "--port", "50050"]