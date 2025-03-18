# dockerfile for delivery microservice

FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY delivery_service/delivery_service_pb2.py .
COPY delivery_service/delivery_service_pb2_grpc.py .
COPY delivery_service/delivery_service.py .
COPY order_service/order_service_pb2.py order_service/
COPY order_service/order_service_pb2_grpc.py order_service/
RUN sed -i 's/import order_service_pb2/from order_service import order_service_pb2/g' order_service/order_service_pb2_grpc.py
EXPOSE 50052
CMD ["python", "delivery_service.py"]