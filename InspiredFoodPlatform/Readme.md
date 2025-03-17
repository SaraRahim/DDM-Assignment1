# Inspired Food Platform

This assignment requires me to analyse a business problem, design a microservice-based solution, implement core functionalities, and deploy the system using Docker Compose.

## Project Information

**Author:** Sara Anegelina Rahim  
**Student ID:** R00211761

## System Architecture

The system is composed of several microservices:
- **API Gateway**: Single entry point for external REST API calls, converting them to gRPC calls for internal communication.
- **Restaurant Service**: Oversees restaurant profiles by managing details such as menus and processing payments. This service allows restaurants to update their menus and accept or reject incoming orders while keeping track of payments.
- **Order Service**: Manages the order lifecycle by creating orders and updating their status. It embeds customer information directly within each order so that customers can place orders and later track their delivery status.
- **Delivery Service**: Handles all aspects of delivery by assigning drivers to orders and tracking the progress of deliveries. This service ensures that delivery drivers can view their assigned orders, update their status as they move along the route and mark orders as delivered.
- **Client Demo**: Simulates an end-to-end workflow for system testing.

## Prerequisites

Ensure the following are installed:
- Docker and Docker Compose
- Git
- Python 3.9

## Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inspiredfoodplatform.git
   cd inspiredfoodplatform
   ```

2. Create a virtual environment:

   On macOS/Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   On Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install project requirements:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running the Application and Integration Tests

When running `docker-compose up --build`, the system performs an end-to-end integration test through the `client.py` script. This test simulates a complete food ordering workflow:

1. **API Gateway Availability**: Checks if the API Gateway is operational
2. **Restaurant Discovery**: Retrieves restaurant details and menu information
3. **Order Creation**:
   - Sends customer details (name, email, phone)
   - Selects a restaurant and menu items
   - Creates an order marked as pending
4. **Restaurant Order Processing**:
   - Restaurant reviews the order
   - Decides to accept or reject the order
5. **Delivery Assignment**:
   - Delivery Service assigns a driver
   - Tracks delivery status
6. **Order Finalization**:
   - Retrieves updated order details
   - Processes restaurant payment information

The `client.py` script serves as an integration test, ensuring that:
- All microservices communicate correctly
- REST to gRPC translation works seamlessly
- The entire business process flows without interruption

To run the full test suite:
```bash
docker-compose up --build
```

If everything runs successfully, you'll see a message indicating that the demo completed successfully, verifying the entire system's integration and functionality.

## Bonus Challenge: API Gateway Implementation

### Bonus Challenge Details

The API Gateway was implemented as a key component of the microservice architecture, addressing several critical design considerations:

#### Implementation Approach
- **Technology**: Implemented using FastAPI
- **Primary Objectives**:
  - Create a single entry point for all client requests
  - Convert REST calls to gRPC messages for internal communication
  - Provide a centralized and controlled interface to microservices

#### Key Features
- **Protocol Translation**: 
  - Converts external REST API calls to internal gRPC communication
  - Enables clients to interact with a simple REST interface
  - Maintains high-performance internal communication via gRPC

- **Architecture Benefits**:
  - Centralized access management
  - Simplified client integration
  - Enhanced security through a controlled interface
  - Abstraction of internal service complexities

### Why This Approach Matters
The API Gateway solution demonstrates:
- Understanding of microservice architectural patterns
- Advanced communication protocol handling
- System design considerations for scalability and maintainability

## Troubleshooting

### Issues I Encountered
- Container problems: I Used `docker ps` to verify running containers
- Network errors: I had to ensure required ports are free
- Detailed logs:
  ```bash
  docker-compose logs [service_name]
  ```

## API Gateway Features

The API Gateway provides:
- Centralized access point
- REST to gRPC protocol translation
- Enhanced security
- Simplified client integration

## Testing Approach

The integration tests (client demo) cover the entire workflow, ensuring:
- Correct API Gateway REST to gRPC translation
- Proper microservice interactions
- End-to-end system functionality

## Final Notes

Running `docker-compose up --build` will:
- Build all services
- Start all containers
- Run the comprehensive integration test
- Verify the complete system functionality
