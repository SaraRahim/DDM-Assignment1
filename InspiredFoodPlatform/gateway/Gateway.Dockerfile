# dockerfile for gateway microservice
FROM python:3.9-slim
WORKDIR /app
COPY . .
ENV PYTHONPATH=/app:$PYTHONPATH
RUN pip install --no-cache-dir -r requirements.txt
COPY order_service/order_service_pb2.py order_service/
COPY order_service/order_service_pb2_grpc.py order_service/
COPY restaurant_service/restaurant_service_pb2.py restaurant_service/
COPY restaurant_service/restaurant_service_pb2_grpc.py restaurant_service/
COPY delivery_service/delivery_service_pb2.py delivery_service/
COPY delivery_service/delivery_service_pb2_grpc.py delivery_service/

COPY gateway/gateway.py .
COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
CMD ["./wait-for-it.sh", "order_service:50051", "--", \
     "./wait-for-it.sh", "delivery_service:50052", "--", \
     "./wait-for-it.sh", "restaurant_service:50053", "--", \
     "uvicorn", "gateway.gateway:app", "--host", "0.0.0.0", "--port", "50050"]