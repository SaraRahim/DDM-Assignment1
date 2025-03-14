# InspiredFoodPlatform

InspiredFoodPlatform is a microservices-based online order and delivery platform for small restaurants. The system leverages gRPC for fast and efficient internal communication and a RESTful API Gateway (built with FastAPI) for external client interactions.

## Table of Contents

- [Introduction](#introduction)
- [Architecture Overview](#architecture-overview)
- [gRPC Interfaces & Protobuf](#grpc-interfaces--protobuf)
- [Microservices Implementation](#microservices-implementation)
  - [OrderService](#orderservice)
  - [DeliveryService](#deliveryservice)
  - [RestaurantService](#restaurantservice)
  - [CustomerService](#customerservice)
  - [API Gateway](#api-gateway)
- [Docker & Deployment](#docker--deployment)
- [Testing](#testing)
- [Design Choices & Challenges](#design-choices--challenges)
- [Possible Improvements](#possible-improvements)
- [Conclusion](#conclusion)

## Introduction

InspiredFoodPlatform allows customers to:
- **Browse menus:** View restaurant menus.
- **Place orders:** Create orders that get routed through the system.
- **Track deliveries:** Receive real-time updates on delivery status.

Restaurants can:
- Update their menus.
- Accept or reject orders.
- Track payments.

Delivery drivers can:
- View assigned deliveries.
- Update their delivery status.
- Mark orders as delivered.

## Architecture Overview

### Microservices
The system is decomposed into several microservices, each responsible for a distinct domain:

- **OrderService:** Handles order creation, retrieval, and status updates.
- **DeliveryService:** Manages driver assignment, delivery status updates, and real-time tracking.
- **RestaurantService:** Provides restaurant details and supports menu updates.
- **CustomerService:** Manages customer profiles and data.
- **API Gateway:** Acts as a centralized entry point that receives HTTP/REST requests and routes them to the appropriate gRPC microservice.

### Communication
- **Internal:** gRPC is used between microservices to ensure strongly-typed and efficient communication.
- **External:** A FastAPI-based API Gateway exposes REST endpoints for client applications.

### Diagram

```
          [Client]
             │
             ▼
     [API Gateway (FastAPI)]
             │

┌──────────────┼──────────────┐
▼              ▼              ▼
[Order]      [Delivery]     [Restaurant]
│              │
└──────────────┘
[Customer]
```

## gRPC Interfaces & Protobuf

The `food_service.proto` file defines:

- **Messages** for orders, delivery, restaurant details, and customer data (e.g., `OrderItem`, `CreateOrderRequest`, `RestaurantResponse`, etc.).
- **Services**:
  - **OrderService:** Methods like `CreateOrder`, `GetOrder`, and `UpdateOrderStatus`.
  - **DeliveryService:** Methods like `AssignDriver`, `UpdateDeliveryStatus`, `GetDelivery`, and `TrackDelivery`.
  - **RestaurantService:** Methods like `GetRestaurant` and `UpdateMenu`.
  - **CustomerService:** Methods like `GetCustomer` and `UpdateCustomer`.

gRPC provides a contract-first approach with Protobuf, ensuring efficient binary messaging and support for streaming (e.g., `TrackDelivery`).

## Microservices Implementation

### OrderService

- **File:** `order_service.py`
- **Description:** Handles creation, retrieval, and status updates for orders. It calculates the total amount for an order and assigns a unique order ID using UUIDs. Data is stored in an in-memory dictionary.

### DeliveryService

- **File:** `delivery_service.py`
- **Description:** Manages the assignment of drivers, updates delivery status, and supports real-time tracking via streaming. It calls the OrderService (via gRPC) to validate order existence and update order status when necessary.

### RestaurantService

- **File:** `restaurant_service.py`
- **Description:** Maintains restaurant details and menus in memory. Offers methods to retrieve restaurant details and update menus.

### CustomerService

- **File:** `customer_service.py`
- **Description:** Manages customer profiles using an in-memory database. Provides endpoints to retrieve and update customer information.

### API Gateway

- **File:** `gateway.py`
- **Description:** Built with FastAPI, the API Gateway provides a centralized HTTP interface for clients. It translates HTTP requests into gRPC calls to the underlying microservices.
- **Example Endpoints:**
  - `GET /restaurants/{restaurant_id}` calls `RestaurantService.GetRestaurant`
  - `POST /orders` calls `OrderService.CreateOrder`
  - `GET /deliveries/{delivery_id}` calls `DeliveryService.GetDelivery`

## Docker & Deployment

- **Docker Compose:**  
  The `docker-compose.yml` file orchestrates the containers for each microservice, the API Gateway, and the client.
  
  **Key Points:**
  - Each microservice is built from its own Dockerfile.
  - Ports are exposed to enable internal and external communication.
  - All services share a common Docker network (`food-network`).

**How to Run:**

1. **Generate gRPC Code:**  
   ```bash
   python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. food_service.proto
   ```

2. **Build and Run Containers:**
   ```bash
   docker compose up --build
   ```

3. **Access the API Gateway:**
   Once running, the API Gateway will be available at http://localhost:50050.

## Testing

### Manual Testing
- **Using cURL/HTTP Clients:**

  ```bash
  curl http://localhost:50050/restaurants/restaurant456
  ```

  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"customer_id":"customer123","restaurant_id":"restaurant456","items":[]}' http://localhost:50050/orders
  ```

### Automated Testing
- **Integration Test:**
  The provided client.py script demonstrates a full workflow (browsing menus, placing orders, tracking delivery, etc.).

## Design Choices & Challenges

### Design Choices
- **Microservice Decomposition:**
  Each service is responsible for a single bounded context (orders, delivery, restaurant, customer) which improves cohesion and minimizes coupling.
- **gRPC Communication:**
  gRPC offers a high-performance, strongly typed, and efficient communication protocol between services.
- **API Gateway:**
  Centralizes the external API and abstracts the underlying microservices from the client.

### Challenges
- **Service Discovery:**
  Ensuring Docker containers correctly resolve each other by service name on the shared network.
- **Port Management:**
  Avoiding conflicts when exposing multiple service ports.
- **Partial Failures:**
  Handling situations where one service may be temporarily down without crashing the entire system.

## Possible Improvements

- **Persistence:**
  Move from in-memory storage to dedicated databases (SQLite, PostgreSQL, etc.) for each service.
- **Event-Driven Communication:**
  Introduce an event bus (RabbitMQ or Redis Pub/Sub) for decoupling and asynchronous processing (e.g., order events triggering delivery processing).
- **Enhanced Security:**
  Implement authentication, authorization, and secure communications (SSL/TLS).
- **Scalability:**
  Scale the API Gateway and microservices independently using container orchestration platforms like Kubernetes.

## Conclusion

InspiredFoodPlatform is a robust microservices-based solution that meets the core requirements for an online order and delivery platform. The system leverages:
- gRPC for efficient inter-service communication,
- Docker Compose for orchestration, and
- FastAPI as an API Gateway for client interactions.

This design supports scalability, modularity, and easy maintenance, and offers a solid foundation for future enhancements such as persistent storage and event-driven communication.

---

Thank you for reviewing the InspiredFoodPlatform project!