import os
import uuid
import logging
from datetime import datetime
from concurrent import futures

import grpc
import order_service_pb2
import order_service_pb2_grpc


class OrderServicer(order_service_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}  # In-memory storage
    
    def CreateOrder(self, request, context):
        order_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # Calculate total amount
        total_amount = sum(item.price * item.quantity for item in request.items)
        
        # Store order data
        self.orders[order_id] = {
            'order_id': order_id,
            'customer_id': request.customer_id,
            'restaurant_id': request.restaurant_id,
            'items': list(request.items),
            'delivery_address': request.delivery_address,
            'special_instructions': request.special_instructions,
            'status': order_service_pb2.ORDER_PENDING,
            'total_amount': total_amount,
            'created_at': now,
            'updated_at': now,
            'estimated_delivery_time': str(datetime.now().timestamp() + 3600)  # 1 hour from now
        }
        
        logging.info(f"Created order {order_id} for customer {request.customer_id}")
        
        # Build response
        return order_service_pb2.OrderResponse(
            order_id=order_id,
            customer_id=request.customer_id,
            restaurant_id=request.restaurant_id,
            items=request.items,
            delivery_address=request.delivery_address,
            special_instructions=request.special_instructions,
            status=order_service_pb2.ORDER_PENDING,
            total_amount=total_amount,
            created_at=now,
            updated_at=now,
            estimated_delivery_time=str(datetime.now().timestamp() + 3600)
        )
    
    def GetOrder(self, request, context):
        order_id = request.order_id
        
        # Check if order exists
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {order_id} not found")
            return order_service_pb2.OrderResponse()
        
        # Get order data
        order = self.orders[order_id]
        
        logging.info(f"Retrieved order {order_id}")
        
        # Build response
        return order_service_pb2.OrderResponse(
            order_id=order['order_id'],
            customer_id=order['customer_id'],
            restaurant_id=order['restaurant_id'],
            items=order['items'],
            delivery_address=order['delivery_address'],
            special_instructions=order['special_instructions'],
            status=order['status'],
            total_amount=order['total_amount'],
            created_at=order['created_at'],
            updated_at=order['updated_at'],
            estimated_delivery_time=order['estimated_delivery_time']
        )
    
    def UpdateOrderStatus(self, request, context):
        order_id = request.order_id
        
        # Check if order exists
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {order_id} not found")
            return order_service_pb2.OrderResponse()
        
        # Update order
        order = self.orders[order_id]
        order['status'] = request.status
        order['updated_at'] = datetime.now().isoformat()
        
        logging.info(f"Updated order {order_id} status to {request.status}")
        
        # Build response
        return order_service_pb2.OrderResponse(
            order_id=order['order_id'],
            customer_id=order['customer_id'],
            restaurant_id=order['restaurant_id'],
            items=order['items'],
            delivery_address=order['delivery_address'],
            special_instructions=order['special_instructions'],
            status=order['status'],
            total_amount=order['total_amount'],
            created_at=order['created_at'],
            updated_at=order['updated_at'],
            estimated_delivery_time=order['estimated_delivery_time']
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_service_pb2_grpc.add_OrderServiceServicer_to_server(OrderServicer(), server)
    
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Order service started on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()