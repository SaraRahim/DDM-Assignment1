from concurrent import futures
import logging
from datetime import datetime
import os

import grpc
import customer_service_pb2
import customer_service_pb2_grpc


class CustomerServicer(customer_service_pb2_grpc.CustomerServiceServicer):

    """Customer service implementation"""

    def __init__(self):
        # In-memory customer database
        self.customers = self._initialize_customers()

    def _initialize_customers(self):
        """Initialize with sample customer data"""
        customers = {}
        
        # Sample customer
        customer_id = "customer123"
        customers[customer_id] = {
            'customer_id': customer_id,
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '555-123-4567',
            'delivery_addresses': [
                '123 Main St, Anytown, USA',
                '456 Work Ave, Anytown, USA'
            ]
        }
        
        return customers

    def GetCustomer(self, request, context):
        """Gets customer details."""
        customer_id = request.customer_id
        
        # Check if customer exists
        if customer_id not in self.customers:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Customer {customer_id} not found")
            return customer_service_pb2.CustomerResponse()
        
        # Get customer
        customer = self.customers[customer_id]
        
        # Log info
        logging.info(f"Retrieved customer {customer_id}")
        
        # Return response
        return customer_service_pb2.CustomerResponse(
            customer_id=customer['customer_id'],
            name=customer['name'],
            email=customer['email'],
            phone=customer['phone'],
            delivery_addresses=customer['delivery_addresses']
        )

    def UpdateCustomer(self, request, context):
        """Updates customer details."""
        customer_id = request.customer_id
        
        # Check if customer exists
        if customer_id not in self.customers:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Customer {customer_id} not found")
            return customer_service_pb2.CustomerResponse()
        
        # Get customer
        customer = self.customers[customer_id]
        
        # Update customer info
        if request.name:
            customer['name'] = request.name
        if request.email:
            customer['email'] = request.email
        if request.phone:
            customer['phone'] = request.phone
        if request.delivery_addresses:
            customer['delivery_addresses'] = list(request.delivery_addresses)
        
        # Log info
        logging.info(f"Updated customer {customer_id}")
        
        # Return response
        return customer_service_pb2.CustomerResponse(
            customer_id=customer['customer_id'],
            name=customer['name'],
            email=customer['email'],
            phone=customer['phone'],
            delivery_addresses=customer['delivery_addresses']
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    customer_service_pb2_grpc.add_CustomerServiceServicer_to_server(CustomerServicer(), server)
    
    server.add_insecure_port('[::]:50054')
    server.start()
    logging.info("Customer service started on port 50054")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()