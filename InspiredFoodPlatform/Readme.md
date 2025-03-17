# Inspired Food Platform

A microservice-based food ordering and delivery platform that connects customers, restaurants, and delivery drivers through a seamless and integrated experience.

## System Architecture

This platform implements a microservice architecture with the following components:

1. **API Gateway**: Entry point for client applications, providing a RESTful API interface
2. **Restaurant Service**: Manages restaurant information, menus, and payments
3. **Order Service**: Handles order creation, processing, and tracking
4. **Delivery Service**: Coordinates delivery assignments and driver tracking
5. **Client Demo**: Simulates a customer application for testing

### Communication Layer
- **Inter-service communication**: gRPC for efficient service-to-service communication
- **External API**: RESTful API exposed through the Gateway for clients
- **Data serialization**: Protocol Buffers for structured data exchange

## Bounded Contexts & Business Capabilities

The system is designed around distinct bounded contexts that align with key business capabilities:

### Restaurant Domain
- **Capabilities**: Menu management, restaurant profile management, payment processing
- **Service**: Restaurant Service
- **Key Entities**: Restaurant, MenuItem, Payment
- **Business Rules**: Restaurants can update menus, view order payments, manage availability

### Order Domain  
- **Capabilities**: Order creation, status management, pricing calculations
- **Service**: Order Service
- **Key Entities**: Order, OrderItem, OrderStatus
- **Business Rules**: Orders track status changes, calculate total prices, maintain customer information

### Delivery Domain
- **Capabilities**: Driver assignment, delivery tracking, status updates
- **Service**: Delivery Service
- **Key Entities**: Delivery, Driver, DeliveryStatus
- **Business Rules**: Track delivery progress, manage driver locations, update order statuses

### Integration Domain
- **Capabilities**: API unification, protocol translation, client communication
- **Service**: API Gateway
- **Key Entities**: Requests/Responses, API Endpoints
- **Business Rules**: Translate REST to gRPC, provide unified client access point

## Data Flow & Dependencies
![Communication Diagram](communicationdiagram.png "Inspired Food Platform Communication Diagram")

### Key Dependencies:
- **Order Service** depends on **Restaurant Service** for menu validation
- **Delivery Service** depends on **Order Service** for order information
- **API Gateway** depends on all services to route client requests

### Data Flow Examples:
1. **Order Creation:**
   - Client sends order request to Gateway
   - Gateway forwards to Order Service
   - Order Service creates order and returns confirmation
   - Gateway returns REST response to client

2. **Delivery Process:**
   - Client requests driver assignment for order
   - Gateway forwards to Delivery Service
   - Delivery Service checks order with Order Service
   - Delivery Service assigns driver and updates order status
   - Gateway returns confirmation to client

## Bonus Challenge Implementation: Customer Information Management

The implemented bonus challenge is **Customer Information Integration**, where instead of creating a separate Customer Service, customer information was integrated directly into the Order domain.

### Implementation Approach:
- Added customer information fields (`customer_name`, `customer_email`, `customer_phone`) to the Order entity
- Updated Protocol Buffer definitions to include these fields in the CreateOrderRequest
- Modified the API Gateway to accept and validate customer details with orders
- Ensured proper propagation of customer details throughout the delivery process

### Benefits of this approach:
1. **Reduced complexity**: Eliminated need for an additional microservice
2. **Improved performance**: No additional network calls to fetch customer information
3. **Simplified data flow**: Order contains all necessary information for processing
4. **Enhanced reliability**: No dependencies on external customer service availability

### Tradeoffs:
1. Potential data duplication if customer information needs to be stored separately
2. More complex order service responsibilities
3. Limited customer profile management capabilities

## Running the Application

### Prerequisites
- Docker and Docker Compose
- Git

### Setup Instructions
1. Clone the repository
   ```
   git clone https://github.com/yourusername/inspiredfoodplatform.git
   cd inspiredfoodplatform
   ```

2. Build and run the services
   ```
   docker-compose up --build
   ```

3. The API will be available at:
   - API Gateway: http://localhost:50050
   - The demo client will automatically run to demonstrate the system

### Available Endpoints

#### Restaurant Endpoints
- `GET /restaurants/{restaurant_id}` - Get restaurant information
- `PUT /restaurants/{restaurant_id}/menu` - Update restaurant menu
- `GET /restaurants/{restaurant_id}/payments` - Get restaurant payments

#### Order Endpoints
- `POST /orders` - Create a new order
- `GET /orders/{order_id}` - Get order information
- `PUT /orders/{order_id}/status` - Update order status

#### Delivery Endpoints
- `POST /deliveries` - Assign driver to order
- `GET /deliveries/{delivery_id}` - Get delivery information
- `PUT /deliveries/{delivery_id}/status` - Update delivery status

## Testing

The application includes a demo client that tests all major functionality:
1. Restaurant information retrieval
2. Order creation with customer details
3. Order status updates
4. Driver assignment and tracking
5. Delivery status updates
6. Payment verification

To run just the tests:
```
docker-compose run client
```

## Architecture Decisions

### Why Microservices?
- **Scalability**: Each service can scale independently based on demand
- **Team organization**: Separate teams can own different services
- **Technology flexibility**: Different services can use different technologies if needed
- **Resilience**: Failure in one service doesn't bring down the entire system
- **Deployment independence**: Services can be deployed independently

### Why gRPC for Service Communication?
- **Performance**: Efficient binary serialization with Protocol Buffers
- **Strong typing**: Contract-first approach with clear interfaces
- **Bi-directional streaming**: Supports advanced communication patterns
- **Language agnostic**: Services can be implemented in different languages

### Why REST for Client API?
- **Widespread adoption**: Easy integration with various client platforms
- **Developer familiarity**: Most frontend developers are familiar with REST
- **Debugging**: Easier to test and debug using standard HTTP tools