import requests
import json
import time
import sys

API_BASE_URL = "http://api_gateway:50050"

def get_restaurant(restaurant_id):
    print(f"\n=== Retrieving Restaurant ===")
    try:
        response = requests.get(f"{API_BASE_URL}/restaurants/{restaurant_id}")
        data = response.json()
        
        print(f"Restaurant ID: {data['restaurant_id']}")
        print(f"Name: {data['name']}")
        print(f"Address: {data['address']}")
        print(f"Is Open: {data['is_open']}")
        print("\nMenu Items:")
        
        for item in data['menu_items']:
            print(f"  - {item['name']} (${item['price']})")
            print(f"    {item['description']}")
            print(f"    Available: {item['available']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving restaurant: {e}")
        return None

def create_order(customer_id, restaurant_id, items, delivery_address, special_instructions=None):
    print(f"\n=== Creating Order ===")
    
    payload = {
        "customer_id": customer_id,
        "restaurant_id": restaurant_id,
        "items": items,
        "delivery_address": delivery_address
    }
    
    if special_instructions:
        payload["special_instructions"] = special_instructions
    
    try:
        response = requests.post(f"{API_BASE_URL}/orders", json=payload)
        data = response.json()
        
        print(f"Order created successfully!")
        print(f"Order ID: {data['order_id']}")
        print(f"Status: {data['status']}")
        print(f"Total Amount: ${data['total_amount']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error creating order: {e}")
        return None

def get_order(order_id):
    print(f"\n=== Retrieving Order ===")
    try:
        response = requests.get(f"{API_BASE_URL}/orders/{order_id}")
        data = response.json()
        
        print(f"Order ID: {data['order_id']}")
        print(f"Customer ID: {data['customer_id']}")
        print(f"Restaurant ID: {data['restaurant_id']}")
        print(f"Status: {data['status']}")
        print(f"Total Amount: ${data['total_amount']}")
        print(f"Items:")
        
        for item in data['items']:
            print(f"  - {item['quantity']}x {item['name']} (${item['price']})")
            if 'customizations' in item and item['customizations']:
                print(f"    Customizations: {', '.join(item['customizations'])}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving order: {e}")
        return None

def update_order_status(order_id, status):
    print(f"\n=== Updating Order Status ===")
    try:
        response = requests.put(f"{API_BASE_URL}/orders/{order_id}/status", json={"status": status})
        data = response.json()
        
        print(f"Order status updated!")
        print(f"Order ID: {data['order_id']}")
        print(f"New Status: {data['status']}")
        print(f"Updated at: {data['updated_at']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error updating order status: {e}")
        return None

def assign_driver(order_id, driver_id):
    print(f"\n=== Assigning Driver ===")
    try:
        response = requests.post(f"{API_BASE_URL}/deliveries", json={
            "order_id": order_id,
            "driver_id": driver_id
        })
        data = response.json()
        
        print(f"Driver assigned successfully!")
        print(f"Delivery ID: {data['delivery_id']}")
        print(f"Order ID: {data['order_id']}")
        print(f"Driver ID: {data['driver_id']}")
        print(f"Status: {data['status']}")
        print(f"Current Location: {data['current_location']}")
        print(f"Estimated Delivery Time: {data['estimated_delivery_time']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error assigning driver: {e}")
        return None

def get_delivery(delivery_id):
    print(f"\n=== Retrieving Delivery ===")
    try:
        response = requests.get(f"{API_BASE_URL}/deliveries/{delivery_id}")
        data = response.json()
        
        print(f"Delivery ID: {data['delivery_id']}")
        print(f"Order ID: {data['order_id']}")
        print(f"Driver ID: {data['driver_id']}")
        print(f"Status: {data['status']}")
        print(f"Current Location: {data['current_location']}")
        print(f"Restaurant Address: {data['restaurant_address']}")
        print(f"Customer Address: {data['customer_address']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving delivery: {e}")
        return None

def update_delivery_status(delivery_id, status, current_location):
    print(f"\n=== Updating Delivery Status ===")
    try:
        response = requests.put(f"{API_BASE_URL}/deliveries/{delivery_id}/status", json={
            "status": status,
            "current_location": current_location
        })
        data = response.json()
        
        print(f"Delivery status updated!")
        print(f"Delivery ID: {data['delivery_id']}")
        print(f"New Status: {data['status']}")
        print(f"Current Location: {data['current_location']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error updating delivery status: {e}")
        return None

def get_customer(customer_id):
    print(f"\n=== Retrieving Customer ===")
    try:
        response = requests.get(f"{API_BASE_URL}/customers/{customer_id}")
        data = response.json()
        
        print(f"Customer ID: {data['customer_id']}")
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Phone: {data['phone']}")
        print(f"Delivery Addresses:")
        
        for address in data['delivery_addresses']:
            print(f"  - {address}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving customer: {e}")
        return None

def get_restaurant_payments(restaurant_id):
    print(f"\n=== Retrieving Payments for Restaurant ===")
    try:
        response = requests.get(f"{API_BASE_URL}/restaurants/{restaurant_id}/payments")
        data = response.json()
        
        print(f"Payments retrieved for restaurant {restaurant_id}:")
        
        if not data:  # If the list is empty
            print("  No payments found")
        else:
            for payment in data:
                print(f"  Payment ID: {payment['payment_id']}")
                print(f"  Order ID: {payment['order_id']}")
                print(f"  Amount: ${payment['amount']}")
                print(f"  Status: {payment['status']}")
                print(f"  Timestamp: {payment['timestamp']}")
                print()
                
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving payments: {response.status_code} - {response.text}")
        return None

def run():
    print("=== Inspired Food Platform Client Demo ===")
    
    # Check if API Gateway is available
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Connected to API Gateway: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API Gateway: {e}")
        sys.exit(1)
    
    # Get restaurant
    restaurant = get_restaurant("restaurant456")
    if not restaurant:
        sys.exit(1)
    
    # Get customer
    customer = get_customer("customer123")
    if not customer:
        sys.exit(1)
    
    # Create an order
    order_items = [
        {
            "item_id": restaurant['menu_items'][0]['item_id'],
            "name": restaurant['menu_items'][0]['name'],
            "price": restaurant['menu_items'][0]['price'],
            "quantity": 2,
            "customizations": ["Extra cheese", "Well done"]
        },
        {
            "item_id": restaurant['menu_items'][1]['item_id'],
            "name": restaurant['menu_items'][1]['name'],
            "price": restaurant['menu_items'][1]['price'],
            "quantity": 1,
            "customizations": []
        }
    ]
    
    order = create_order(
        customer_id=customer['customer_id'],
        restaurant_id=restaurant['restaurant_id'],
        items=order_items,
        delivery_address=customer['delivery_addresses'][0],
        special_instructions="Please ring doorbell twice"
    )
    
    if not order:
        sys.exit(1)
    
    # Simulate restaurant confirming order
    time.sleep(1)
    update_order_status(order['order_id'], 2)  # ORDER_CONFIRMED
    
    # Simulate restaurant preparing order
    time.sleep(1)
    update_order_status(order['order_id'], 3)  # ORDER_PREPARING
    
    # Assign a driver for delivery
    delivery = assign_driver(order['order_id'], "driver789")
    if not delivery:
        sys.exit(1)
    
    # Get delivery details
    time.sleep(1)
    get_delivery(delivery['delivery_id'])
    
    # Update delivery status - driver picked up the order
    time.sleep(1)
    update_delivery_status(
        delivery_id=delivery['delivery_id'],
        status=2,  # DELIVERY_PICKED_UP
        current_location="At restaurant"
    )
    
    # Get updated order status
    time.sleep(1)
    get_order(order['order_id'])
    
    # Update delivery status - driver is on the way
    time.sleep(1)
    update_delivery_status(
        delivery_id=delivery['delivery_id'],
        status=3,  # DELIVERY_IN_PROGRESS
        current_location="Halfway to customer's address"
    )
    
    # Update delivery status - order delivered
    time.sleep(1)
    update_delivery_status(
        delivery_id=delivery['delivery_id'],
        status=4,  # DELIVERY_DELIVERED
        current_location="At customer's address"
    )
    
    # Get final order status
    time.sleep(1)
    get_order(order['order_id'])
    
    # Get restaurant payments
    time.sleep(1)
    get_restaurant_payments("restaurant456")
    
    print("\n=== Demo completed successfully! ===")

if __name__ == "__main__":
    # Wait a moment for services to be ready
    time.sleep(5)
    run()