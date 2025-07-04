# Inspired Food Platform

This assignment required me to analyse a business problem, design a micro service based solution, implement core functionalities and deploy the system using Docker Compose.

## Project Information

**Author:** Sara Anegelina Rahim  
**Student ID:** R00211761

## System Architecture

The system is made up of 5 micro services:
- **API Gateway**: Single entry point for external REST API calls, converting them to gRPC calls for internal communication.
- **Restaurant Service**: Oversees restaurant profiles by managing details such as menus and processing payments. This service allows restaurants to update their menus and accept or reject incoming orders while keeping track of payments.
- **Order Service**: Manages the order lifecycle by creating orders and updating their status. It embeds customer information directly within each order so that customers can place orders and later track their delivery status.
- **Delivery Service**: Handles all aspects of delivery by assigning drivers to orders and tracking the progress of deliveries. This service ensures that delivery drivers can view their assigned orders, update their status as they move along the route and mark orders as delivered.
- **Client Demo**: Simulates an end to end workflow for system testing.

## Prerequisites

Ensure the following are installed:
- Docker and Docker Compose
- Git
- Python 

## Local Development Setup

1. Download the ZIP file:
   - Download the Inspired Food Platform ZIP file.
   - Extract the contents to a folder on your computer.
   - Open your terminal and navigate to the extracted folder:
     ```
     cd InspiredFoodPlatform
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
   pip install -r requirements.txt
   ```

## Running the Application and Integration Tests

When running `docker compose up --build`, the system performs an end to end integration test through the `client.py` script. This test simulates a complete food ordering workflow:

1. **API Gateway Availability**: Checks if the API Gateway is working
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
- REST to gRPC translation works 
- The entire business process flows without errors

To run the full test suite:
```bash
docker-compose up --build
```

If everything runs successfully, a message will come up indicating that the demo completed successfully, verifying the entire system's integration and functionality.

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
  - Maintains high performance internal communication via gRPC

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
