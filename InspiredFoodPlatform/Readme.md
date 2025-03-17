# Inspired Food Platform

Inspired Food Platform is a microservice-based food ordering and delivery application that connects customers, restaurants, and delivery drivers through a streamlined process.

## Project Information

**Author:** Sara Anegelina Rahim  
**Student ID:** R00211761

## System Architecture

The system is composed of several microservices:
- **API Gateway**: Single entry point for external REST API calls, converting them to gRPC calls for internal communication
- **Restaurant Service**: Manages restaurant details, menus, and payment tracking
- **Order Service**: Handles order creation, status updates, and customer information
- **Delivery Service**: Coordinates driver assignments and tracks delivery status
- **Client Demo**: Simulates an end-to-end workflow for system testing

## Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Compose
- Git
- Python 3.9 (for local development)

## Setup Instructions

### Option 1: Using Docker Compose

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inspiredfoodplatform.git
   cd inspiredfoodplatform
   ```

2. Build and run the services:
   ```bash
   docker-compose up --build
   ```

### Option 2: Running Locally

1. Create and activate a virtual environment:

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

2. Install requirements:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Run individual services:
   ```bash
   python order_service.py
   python restaurant_service.py
   # Run other services similarly
   ```

## Running the Application

The client demo script simulates a complete workflow:
1. API Gateway availability check
2. Restaurant information retrieval
3. Order creation
4. Restaurant order acceptance
5. Delivery process
6. Order and payment updates

### Running the Client Demo

With Docker Compose:
```bash
docker-compose up --build
```

## Workflow Details

The application demonstrates a full food ordering process:
- Fetch restaurant and menu details
- Create an order with customer information
- Restaurant reviews and accepts the order
- Assign a delivery driver
- Track delivery status
- Update order and payment information

## Troubleshooting

### Common Issues
- Container problems: Use `docker ps` to verify running containers
- Network errors: Ensure required ports are free
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

Follow the provided setup instructions to build, run, and test the Inspired Food Platform. Whether using Docker Compose or running services locally, the system provides a comprehensive food ordering solution.

Happy testing!