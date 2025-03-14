import os
import logging
import grpc
from concurrent import futures
from proto import food_service_pb2
from proto import food_service_pb2_grpc


class FoodServiceGateway(food_service_pb2_grpc.OrderServiceServicer):
    """Gateway service that routes requests to the appropriate microservice."""
    
    def __init__(self):
        # Connect to Order service
        order_service_addr = os.environ.get('ORDER_SERVICE_ADDR', 'order_service:50051')
        self.order_channel = grpc.insecure_channel(order_service_addr)
        self.order_stub = food_service_pb2_grpc.OrderServiceStub(self.order_channel)
        
        # Connect to Delivery service
        delivery_service_addr = os.environ.get('DELIVERY_SERVICE_ADDR', 'delivery_service:50052')
        self.delivery_channel = grpc.insecure_channel(delivery_service_addr)
        self.delivery_stub = food_service_pb2_grpc.DeliveryServiceStub(self.delivery_channel)
        
        # Connect to Restaurant service
        restaurant_service_addr = os.environ.get('RESTAURANT_SERVICE_ADDR', 'restaurant_service:50053')
        self.restaurant_channel = grpc.insecure_channel(restaurant_service_addr)
        self.restaurant_stub = food_service_pb2_grpc.RestaurantServiceStub(self.restaurant_channel)
        
        logging.info(f"Connected to Order Service at {order_service_addr}")
        logging.info(f"Connected to Delivery Service at {delivery_service_addr}")
        logging.info(f"Connected to Restaurant Service at {restaurant_service_addr}")
    
    # Order service methods
    def CreateOrder(self, request, context):
        try:
            return self.order_stub.CreateOrder(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Order service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.OrderResponse()
    
    def GetOrder(self, request, context):
        try:
            return self.order_stub.GetOrder(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Order service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.OrderResponse()
    
    def UpdateOrderStatus(self, request, context):
        try:
            return self.order_stub.UpdateOrderStatus(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Order service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.OrderResponse()
    
    # Delivery service methods
    def AssignDriver(self, request, context):
        try:
            return self.delivery_stub.AssignDriver(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Delivery service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.DeliveryResponse()
    
    def GetDelivery(self, request, context):
        try:
            return self.delivery_stub.GetDelivery(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Delivery service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.DeliveryResponse()
    
    def UpdateDeliveryStatus(self, request, context):
        try:
            return self.delivery_stub.UpdateDeliveryStatus(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Delivery service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.DeliveryResponse()
    
    def TrackDelivery(self, request, context):
        try:
            for response in self.delivery_stub.TrackDelivery(request):
                yield response
        except grpc.RpcError as e:
            logging.error(f"Error from Delivery service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return
    
    # Restaurant service methods
    def GetRestaurant(self, request, context):
        try:
            return self.restaurant_stub.GetRestaurant(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Restaurant service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.RestaurantResponse()
    
    def UpdateMenu(self, request, context):
        try:
            return self.restaurant_stub.UpdateMenu(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Restaurant service: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.MenuResponse()
        
        # Payment tracking methods
    def GetRestaurantPayments(self, request, context):
        """Gets payments for a restaurant."""
        try:
            return self.restaurant_stub.GetRestaurantPayments(request)
        except grpc.RpcError as e:
            logging.error(f"Error from Restaurant service when tracking payments: {e}")
            context.set_code(e.code())
            context.set_details(e.details())
            return food_service_pb2.GetRestaurantPaymentsResponse()


def serve():
    port = os.environ.get('PORT', '50050')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    food_service_pb2_grpc.add_OrderServiceServicer_to_server(
        FoodServiceGateway(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    logging.info(f"Food service gateway started, listening on port {port}")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()