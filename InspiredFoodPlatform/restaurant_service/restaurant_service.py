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
        self.payments = {}
    
    def _initialize_restaurants(self):
        # Initialize with sample restaurant data
        restaurants = {}
        
        # Sample restaurant
        restaurant_id = "restaurant456"
        restaurants[restaurant_id] = {
            'restaurant_id': restaurant_id,
            'name': 'Tasty Pizza',
            'address': '123 Restaurant St, Foodville',
            'is_open': True,
            'menu_items': [
                {
                    'item_id': 'pizza1',
                    'name': 'Pepperoni Pizza',
                    'description': 'Classic pepperoni pizza with mozzarella cheese',
                    'price': 12.99,
                    'available': True
                },
                {
                    'item_id': 'salad1',
                    'name': 'Caesar Salad',
                    'description': 'Fresh romaine lettuce with Caesar dressing',
                    'price': 7.99,
                    'available': True
                }
            ]
        }
        
        return restaurants
    
    def GetRestaurant(self, request, context):
        restaurant_id = request.restaurant_id
        
        # Check if restaurant exists
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.RestaurantResponse()
        
        # Get restaurant data
        restaurant = self.restaurants[restaurant_id]
        
        logging.info(f"Retrieved restaurant {restaurant_id}")
        
        # Build menu items
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
        
        # Build response
        return restaurant_service_pb2.RestaurantResponse(
            restaurant_id=restaurant['restaurant_id'],
            name=restaurant['name'],
            address=restaurant['address'],
            menu_items=menu_items,
            is_open=restaurant['is_open']
        )
    
    def GetRestaurantPayments(self, request, context):
        restaurant_id = request.restaurant_id
        
        # Check if restaurant exists
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.GetRestaurantPaymentsResponse()
        
        # In a real implementation, you would fetch payments from a database
        # For now, use mock data
        mock_payments = []
        
        # Generate some mock payments data based on orders for this restaurant
        # In a real implementation, this would come from a database
        for i in range(3):  # Just creating 3 mock payments
            payment = restaurant_service_pb2.Payment(
                payment_id=f"payment_{i}_{restaurant_id}",
                order_id=f"order_{i}_{restaurant_id}",
                amount=15.99 + i * 5.0,
                status="completed",
                timestamp=datetime.now().isoformat()
            )
            mock_payments.append(payment)
        
        return restaurant_service_pb2.GetRestaurantPaymentsResponse(payments=mock_payments)
    
    def UpdateMenu(self, request, context):
        restaurant_id = request.restaurant_id
        
        # Check if restaurant exists
        if restaurant_id not in self.restaurants:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Restaurant {restaurant_id} not found")
            return restaurant_service_pb2.MenuResponse()
        
        # Get restaurant
        restaurant = self.restaurants[restaurant_id]
        
        # Update menu items
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
        
        # Build response
        return restaurant_service_pb2.MenuResponse(
            restaurant_id=restaurant_id,
            menu_items=request.menu_items,
            updated_at=now
        )


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