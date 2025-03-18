FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY restaurant_service/restaurant_service_pb2.py .
COPY restaurant_service/restaurant_service_pb2_grpc.py .
COPY restaurant_service/restaurant_service.py .
EXPOSE 50053
CMD ["python", "restaurant_service.py"]