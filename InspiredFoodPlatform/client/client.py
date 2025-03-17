import requests
import json
import time
import sys
import traceback

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

def create_order(customer_name, customer_email, customer_phone, restaurant_id, items, delivery_address, special_instructions=None):
    print(f"\n=== Creating Order ===")
    
    # Prepare the payload exactly as per the service requirements
    payload = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_phone": customer_phone,
        "restaurant_id": restaurant_id,
        "items": items,
        "delivery_address": delivery_address
    }
    
    # Add special instructions if provided
    if special_instructions:
        payload["special_instructions"] = special_instructions
    
    # For debugging: add customer ID if needed
    if not any(payload.get(key) for key in ['customer_id', 'customer_name', 'customer_email', 'customer_phone']):
        payload['customer_name'] = 'Unknown Customer'
    
    try:
        # Enable very verbose logging
        print("Full Request Payload:")
        print(json.dumps(payload, indent=2))
        
        # Add headers to help with debugging
        headers = {
            'Content-Type': 'application/json',
            'X-Debug-Mode': 'true'
        }
        
        # Perform the request with detailed error handling
        response = requests.post(
            f"{API_BASE_URL}/orders", 
            json=payload, 
            headers=headers
        )
        
        # Log full response details
        print("\n=== Full Response Details ===")
        print(f"Status Code: {response.status_code}")
        print("Response Headers:")
        for key, value in response.headers.items():
            print(f"{key}: {value}")
        
        # Try to parse response content
        try:
            response_content = response.json()
            print("\nResponse Content:")
            print(json.dumps(response_content, indent=2))
        except ValueError:
            print("\nResponse Content (non-JSON):")
            print(response.text)
        
        # Detailed error handling
        if response.status_code >= 400:
            print("\n=== Error Details ===")
            print(f"Status Code: {response.status_code}")
            print("Response Body:", response.text)
            return None
        
        # Parse successful response
        data = response.json()
        
        print(f"\n=== Order Created Successfully! ===")
        print("Returned Data Keys:", list(data.keys()))
        
        # Safely extract order details
        print(f"Order ID: {data.get('order_id', 'N/A')}")
        print(f"Status: {data.get('status', 'N/A')}")
        print(f"Total Amount: ${data.get('total_amount', 'N/A')}")
        
        return data
    
    except requests.exceptions.RequestException as e:
        print(f"\n=== Request Error ===")
        print(f"Error details: {e}")
        traceback.print_exc()
        return None
    except Exception as e:
        print(f"\n=== Unexpected Error ===")
        print(f"Error details: {e}")
        traceback.print_exc()
        return None

def get_order(order_id):
    print(f"\n=== Retrieving Order ===")
    try:
        response = requests.get(f"{API_BASE_URL}/orders/{order_id}")
        data = response.json()

        print(f"Order ID: {data['order_id']}")
        print(f"Customer Name: {data['customer_name']}")
        print(f"Customer Email: {data['customer_email']}")
        print(f"Customer Phone: {data['customer_phone']}")
        print(f"Restaurant ID: {data['restaurant_id']}")
        print(f"Delivery Address: {data['delivery_address']}")
        print(f"Status: {data['status']}")
        print(f"Total Amount: ${data['total_amount']}")
        print("Items:")
        
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
    
    # First, check API Gateway availability
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Connected to API Gateway: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API Gateway: {e}")
        sys.exit(1)
    
    # Retrieve restaurant details
    restaurant = get_restaurant("restaurant456")
    if not restaurant:
        sys.exit(1)
    
    # Prepare order items based on the restaurant's menu
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
    
    # Create an order
    order = create_order(
        customer_name="John Doe",
        customer_email="john.doe@example.com",
        customer_phone="555-123-4567",
        restaurant_id=restaurant['restaurant_id'],
        items=order_items,
        delivery_address="123 Customer Lane, Foodville",
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