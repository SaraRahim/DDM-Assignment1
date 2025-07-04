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
        self.orders = {} # in memory storage for orders
    
    # create a new order
    def CreateOrder(self, request, context):
        order_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        # calculating the total amount for the order
        total_amount = sum(item.price * item.quantity for item in request.items)
        
        customer_id = str(uuid.uuid4()) # generating a customer id
        
        self.orders[order_id] = {
            'order_id': order_id,
            'customer_id': customer_id,
            'customer_name': request.customer_name,
            'customer_email': request.customer_email,
            'customer_phone': request.customer_phone,
            'restaurant_id': request.restaurant_id,
            'items': list(request.items),
            'delivery_address': request.delivery_address,
            'special_instructions': request.special_instructions or '',
            'status': order_service_pb2.ORDER_PENDING,
            'total_amount': total_amount,
            'created_at': now,
            'updated_at': now,
        }
        
        logging.info(f"Created order {order_id} for customer {customer_id}")
        
        return order_service_pb2.OrderResponse(
            order_id=order_id,
            customer_name=request.customer_name,
            customer_email=request.customer_email,
            customer_phone=request.customer_phone,
            restaurant_id=request.restaurant_id,
            items=request.items,
            delivery_address=request.delivery_address,
            special_instructions=request.special_instructions or '',
            status=order_service_pb2.ORDER_PENDING,
            total_amount=total_amount,
            created_at=now,
            updated_at=now,
        )
    
    # handling restaurant response based on accepted or rejected 
    def RestaurantOrderResponse(self, request, context):
        order_id = request.order_id
        restaurant_id = request.restaurant_id
        accepted = request.accepted
        rejection_reason = request.rejection_reason
    
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {order_id} not found")
            return order_service_pb2.RestaurantOrderResponseResponse()
    
        order = self.orders[order_id]
        if order["restaurant_id"] != restaurant_id:
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details(f"Order {order_id} does not belong to restaurant {restaurant_id}")
            return order_service_pb2.RestaurantOrderResponseResponse()
    
        if order["status"] != order_service_pb2.ORDER_PENDING:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details(f"Order {order_id} is not in PENDING state")
            return order_service_pb2.RestaurantOrderResponseResponse()
    
        now = datetime.now().isoformat()
        new_status = order_service_pb2.ORDER_CONFIRMED if accepted else order_service_pb2.ORDER_REJECTED
    
        order["status"] = new_status
        order["updated_at"] = now
    
        if not accepted:
            order["rejection_reason"] = rejection_reason
        logging.info(f"Restaurant {restaurant_id} {'accepted' if accepted else 'rejected'} order {order_id}")
    
        response = order_service_pb2.RestaurantOrderResponseResponse(
            order_id=order_id,
            status=new_status,
            updated_at=now
        )
    
        if not accepted:
            response.rejection_reason = rejection_reason
        
        return response
    
    # get order
    def GetOrder(self, request, context):
        order_id = request.order_id
        
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {order_id} not found")
            return order_service_pb2.OrderResponse()
        
        order = self.orders[order_id]        
        logging.info(f"Retrieved order {order_id}")
        
        return order_service_pb2.OrderResponse(
            order_id=order['order_id'],
            customer_name=order['customer_name'],
            customer_email=order['customer_email'],
            customer_phone=order['customer_phone'],
            restaurant_id=order['restaurant_id'],
            items=order['items'],
            delivery_address=order['delivery_address'],
            special_instructions=order['special_instructions'],
            status=order['status'],
            total_amount=order['total_amount'],
            created_at=order['created_at'],
            updated_at=order['updated_at'],
        )
    
    # update the status of the order
    def UpdateOrderStatus(self, request, context):
        order_id = request.order_id
        
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Order {order_id} not found")
            return order_service_pb2.OrderResponse()
        
        order = self.orders[order_id]
        order['status'] = request.status
        order['updated_at'] = datetime.now().isoformat()
        
        logging.info(f"Updated order {order_id} status to {request.status}")
        
        return order_service_pb2.OrderResponse(
            order_id=order['order_id'],
            customer_name=order['customer_name'],
            customer_email=order['customer_email'],
            customer_phone=order['customer_phone'],
            restaurant_id=order['restaurant_id'],
            items=order['items'],
            delivery_address=order['delivery_address'],
            special_instructions=order['special_instructions'],
            status=order['status'],
            total_amount=order['total_amount'],
            created_at=order['created_at'],
            updated_at=order['updated_at'],
        )

# starting the gRPC server
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