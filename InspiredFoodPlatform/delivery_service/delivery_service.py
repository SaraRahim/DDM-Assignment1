import os
import uuid
import logging
from datetime import datetime
from concurrent import futures
import sys
import grpc
import delivery_service_pb2
import delivery_service_pb2_grpc
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'order_service'))
from order_service import order_service_pb2
from order_service import order_service_pb2_grpc


class DeliveryServicer(delivery_service_pb2_grpc.DeliveryServiceServicer):
    def __init__(self):
        self.deliveries = {}  
        
        order_service_addr = os.environ.get('ORDER_SERVICE_ADDR', 'order_service:50051')
        try:
            self.order_channel = grpc.insecure_channel(order_service_addr)
            self.order_stub = order_service_pb2_grpc.OrderServiceStub(self.order_channel)
            logging.info(f"Connected to Order Service at {order_service_addr}")
        except Exception as e:
            logging.error(f"Failed to connect to Order Service: {e}")
    
    def AssignDriver(self, request, context):
        order_id = request.order_id
        driver_id = request.driver_id
        
        try:
            order_request = order_service_pb2.GetOrderRequest(order_id=order_id)
            order_response = self.order_stub.GetOrder(order_request)
            
            if not order_response or not order_response.order_id:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f"Order {order_id} not found")
                return delivery_service_pb2.DeliveryResponse()
                
            delivery_id = str(uuid.uuid4())
            now = datetime.now().isoformat()
            
            self.deliveries[delivery_id] = {
                'delivery_id': delivery_id,
                'order_id': order_id,
                'driver_id': driver_id,
                'restaurant_address': '123 Restaurant St', 
                'customer_address': order_response.delivery_address,
                'status': delivery_service_pb2.DELIVERY_ASSIGNED,
                'current_location': 'Driver starting location',
                'assigned_at': now,
                'picked_up_at': None,
                'delivered_at': None,
                'estimated_delivery_time': str(datetime.now().timestamp() + 1800) 
            }
            
            logging.info(f"Assigned driver {driver_id} to order {order_id}, delivery {delivery_id}")
            
            update_request = order_service_pb2.UpdateOrderStatusRequest(
                order_id=order_id,
                status=order_service_pb2.ORDER_CONFIRMED
            )
            self.order_stub.UpdateOrderStatus(update_request)
            
            return delivery_service_pb2.DeliveryResponse(
                delivery_id=delivery_id,
                order_id=order_id,
                driver_id=driver_id,
                restaurant_address='123 Restaurant St',
                customer_address=order_response.delivery_address,
                status=delivery_service_pb2.DELIVERY_ASSIGNED,
                current_location='Driver starting location',
                assigned_at=now,
                estimated_delivery_time=str(datetime.now().timestamp() + 1800)
            )
            
        except grpc.RpcError as e:
            logging.error(f"Error communicating with Order service: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error communicating with Order service: {e.details() if hasattr(e, 'details') else str(e)}")
            return delivery_service_pb2.DeliveryResponse()
    
    def GetDelivery(self, request, context):
        delivery_id = request.delivery_id
        
        if delivery_id not in self.deliveries:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Delivery {delivery_id} not found")
            return delivery_service_pb2.DeliveryResponse()
        
        delivery = self.deliveries[delivery_id]
        logging.info(f"Retrieved delivery {delivery_id}")
        
        response = delivery_service_pb2.DeliveryResponse(
            delivery_id=delivery['delivery_id'],
            order_id=delivery['order_id'],
            driver_id=delivery['driver_id'],
            restaurant_address=delivery['restaurant_address'],
            customer_address=delivery['customer_address'],
            status=delivery['status'],
            current_location=delivery['current_location'],
            assigned_at=delivery['assigned_at'],
            estimated_delivery_time=delivery['estimated_delivery_time']
        )
        
        if delivery['picked_up_at']:
            response.picked_up_at = delivery['picked_up_at']
        if delivery['delivered_at']:
            response.delivered_at = delivery['delivered_at']
        
        return response
    
    def UpdateDeliveryStatus(self, request, context):
        delivery_id = request.delivery_id
        
        if delivery_id not in self.deliveries:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Delivery {delivery_id} not found")
            return delivery_service_pb2.DeliveryResponse()
        
        delivery = self.deliveries[delivery_id]
        delivery['status'] = request.status
        delivery['current_location'] = request.current_location
        
        now = datetime.now().isoformat()
        if request.status == delivery_service_pb2.DELIVERY_PICKED_UP:
            delivery['picked_up_at'] = now
            
            try:
                update_request = order_service_pb2.UpdateOrderStatusRequest(
                    order_id=delivery['order_id'],
                    status=order_service_pb2.ORDER_OUT_FOR_DELIVERY
                )
                self.order_stub.UpdateOrderStatus(update_request)
            except Exception as e:
                logging.error(f"Failed to update order status: {e}")
                
        elif request.status == delivery_service_pb2.DELIVERY_DELIVERED:
            delivery['delivered_at'] = now
            
            try:
                update_request = order_service_pb2.UpdateOrderStatusRequest(
                    order_id=delivery['order_id'],
                    status=order_service_pb2.ORDER_DELIVERED
                )
                self.order_stub.UpdateOrderStatus(update_request)
            except Exception as e:
                logging.error(f"Failed to update order status: {e}")
        
        logging.info(f"Updated delivery {delivery_id} status to {request.status}")
        
        response = delivery_service_pb2.DeliveryResponse(
            delivery_id=delivery['delivery_id'],
            order_id=delivery['order_id'],
            driver_id=delivery['driver_id'],
            restaurant_address=delivery['restaurant_address'],
            customer_address=delivery['customer_address'],
            status=delivery['status'],
            current_location=delivery['current_location'],
            assigned_at=delivery['assigned_at'],
            estimated_delivery_time=delivery['estimated_delivery_time']
        )
        
        if delivery['picked_up_at']:
            response.picked_up_at = delivery['picked_up_at']
        if delivery['delivered_at']:
            response.delivered_at = delivery['delivered_at']
        
        return response
    
    def TrackDelivery(self, request, context):
        delivery_id = request.delivery_id
        
        if delivery_id not in self.deliveries:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Delivery {delivery_id} not found")
            return
        
        delivery = self.deliveries[delivery_id]
        
        response = delivery_service_pb2.TrackDeliveryResponse(
            delivery_id=delivery['delivery_id'],
            driver_id=delivery['driver_id'],
            current_location=delivery['current_location'],
            status=delivery['status'],
            estimated_arrival_time=delivery['estimated_delivery_time']
        )
        
        yield response
        
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    delivery_service_pb2_grpc.add_DeliveryServiceServicer_to_server(DeliveryServicer(), server)
    
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Delivery service started on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()