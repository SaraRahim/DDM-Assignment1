import os
import logging
from datetime import datetime
from concurrent import futures
import grpc
import restaurant_service_pb2
import restaurant_service_pb2_grpc

class RestaurantServicer(restaurant_service_pb2_grpc.RestaurantServiceServicer):
    def __init__(self):
        self.restaurants = self._initialize_restaurants()
        self.payments = {} # in memory storage for payments
    
    def _initialize_restaurants(self):
        restaurants = {}
        restaurant_id = "restaurant456"
        restaurants[restaurant_id] = {
            'restaurant_id': restaurant_id,
            'name': 'Eskimo Pizza Bandon',
            'address': '1st Patricks quay, Gully, Bandon, Co. Cork, P72 TN93',
            'is_open': True,
            'menu_items': [
                {
                    'item_id': 'pizza1',
                    'name': 'Eskimo Classic Pizza',
                    'description': 'Pepperoni, ham, onions, peppers, pineapple and sweetcorn.',
                    'price': 12.99,
                    'available': True
                },
                {
                    'item_id': 'pizza2',
                    'name': 'Mighty Meaty Pizza',
                    'description': 'Pepperoni, ham, crispy bacon and tender chicken.',
                    'price': 14.99,
                    'available': True
                }
            ]
        }
        
        return restaurants
    
    # get restaurants
    def GetRestaurant(self, request, context):
        restaurant_id = request.restaurant_id
        
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.RestaurantResponse()
        
        restaurant = self.restaurants[restaurant_id]
        
        logging.info(f"Retrieved restaurant {restaurant_id}")
        
        # convert items -> protobuf messages
        menu_items = []
        for item in restaurant['menu_items']:
            menu_item = restaurant_service_pb2.MenuItem(
                item_id=item['item_id'],
                name=item['name'],
                description=item['description'],
                price=item['price'],
                available=item['available']
            )
            menu_items.append(menu_item)
        
        return restaurant_service_pb2.RestaurantResponse(
            restaurant_id=restaurant['restaurant_id'],
            name=restaurant['name'],
            address=restaurant['address'],
            menu_items=menu_items,
            is_open=restaurant['is_open']
        )
    
    # get restaurant payments
    def GetRestaurantPayments(self, request, context):
        restaurant_id = request.restaurant_id
        
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.GetRestaurantPaymentsResponse()

        mock_payments = []
        
        for i in range(3): 
            payment = restaurant_service_pb2.Payment(
                payment_id=f"payment_{i}_{restaurant_id}",
                order_id=f"order_{i}_{restaurant_id}",
                amount=round(14.99 + i * 5.0, 2),
                status="completed",
                timestamp=datetime.now().isoformat()
            )
            mock_payments.append(payment)
        
        return restaurant_service_pb2.GetRestaurantPaymentsResponse(payments=mock_payments)
    
    # update menu
    def UpdateMenu(self, request, context):
        restaurant_id = request.restaurant_id
        
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.MenuResponse()
        
        restaurant = self.restaurants[restaurant_id]
        
        restaurant['menu_items'] = []
        for item in request.menu_items:
            menu_item = {
                'item_id': item.item_id,
                'name': item.name,
                'description': item.description,
                'price': item.price,
                'available': item.available
            }
            restaurant['menu_items'].append(menu_item)
        
        now = datetime.now().isoformat()
        
        logging.info(f"Updated menu for restaurant {restaurant_id}")
        
        return restaurant_service_pb2.MenuResponse(
            restaurant_id=restaurant_id,
            menu_items=request.menu_items,
            updated_at=now
        )

# starting the gRPC server
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_service_pb2_grpc.add_RestaurantServiceServicer_to_server(RestaurantServicer(), server)
    
    server.add_insecure_port('[::]:50053')
    server.start()
    logging.info("Restaurant service started on port 50053")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()