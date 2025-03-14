FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files
COPY customer_service/customer_service_pb2.py .
COPY customer_service/customer_service_pb2_grpc.py .
COPY customer_service/customer_service.py .

EXPOSE 50054

CMD ["python", "customer_service.py"]