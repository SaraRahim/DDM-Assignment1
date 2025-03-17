FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files
COPY delivery_service/delivery_service_pb2.py .
COPY delivery_service/delivery_service_pb2_grpc.py .
COPY delivery_service/delivery_service.py .

# Also need order service protos for cross-service communication
COPY order_service/order_service_pb2.py order_service/
COPY order_service/order_service_pb2_grpc.py order_service/

RUN sed -i 's/import order_service_pb2/from order_service import order_service_pb2/g' order_service/order_service_pb2_grpc.py


EXPOSE 50052

CMD ["python", "delivery_service.py"]