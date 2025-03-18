import requests
import time
import sys
import traceback

API_BASE_URL = "http://api_gateway:50050"

def get_restaurant(restaurant_id):
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱🍲🍕🍱🍲 \n"
          "Retrieving Restaurant \n"
           "🍕🍱🍲🍕🍱🍲🍕🍱🍲🍕🍱🍲 \n")
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
    print(f"\n🍕🍱🍲🍕🍱🍲🍕 \n"
          "Creating Order \n"
           "🍕🍱🍲🍕🍱🍲🍕 \n")
    
    payload = {
        "customer_name": customer_name,
        "customer_email": customer_email,
        "customer_phone": customer_phone,
        "restaurant_id": restaurant_id,
        "items": items,
        "delivery_address": delivery_address
    }
    
    if special_instructions:
        payload["special_instructions"] = special_instructions
     
    try:
        
        headers = {
            'Content-Type': 'application/json',
            'X-Debug-Mode': 'true'
        }
        
        response = requests.post(
            f"{API_BASE_URL}/orders", 
            json=payload, 
            headers=headers
        )
        
        if response.status_code >= 400:
            print("\n=== Error Details ===")
            print(f"Status Code: {response.status_code}")
            print("Response Body:", response.text)
            return None
        
        data = response.json()
        
        print(f"\n✅✅✅ Order Created! ✅✅✅")
        #print("Returned Data Keys:", list(data.keys()))
        
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
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲 \n"
          "Retrieving Order \n"
           "🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲 \n")
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
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲🍱🍕🍲 \n"
          "Updating Order Status \n"
            "🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲🍱🍕🍲 \n")
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
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱 \n"
          "Assigning Driver \n"
           "🍕🍱🍲🍕🍱🍲🍕🍱 \n")
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
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error assigning driver: {e}")
        return None

def get_delivery(delivery_id):
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲 \n"
          " Retrieving Delivery \n"
          "🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲 \n")
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
    print(f"\n🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲🍱🍕 \n"
          "Updating Delivery Status \n"
          "🍕🍱🍲🍕🍱🍲🍕🍱🍕🍲🍱🍕 \n")
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
    
def restaurant_respond_to_order(restaurant_id, order_id, accepted, rejection_reason=None):
    print(
        f"\n 🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲 \n"
        f" Restaurant {'Accepting' if accepted else 'Rejecting'} Order \n"
        f"🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲🍱🍕🍲 \n"
    )
    payload = {
        "accepted": accepted
    }
    if not accepted and rejection_reason:
        payload["rejection_reason"] = rejection_reason
        
    try:
        response = requests.post(
            f"{API_BASE_URL}/restaurants/{restaurant_id}/orders/{order_id}/response", 
            json=payload
        )
        
        if response.status_code >= 400:
            print(f"Error: {response.status_code} - {response.text}")
            return None
            
        data = response.json()
        
        if accepted:
            print(f"✅✅✅ Order accepted by restaurant! ✅✅✅")
        else:
            print(f"❌❌❌ Order rejected by restaurant. ❌❌❌ Reason: {data.get('rejection_reason', 'No reason provided')}")
            
        print(f"Order ID: {data['order_id']}")
        print(f"New Status: {data['status']}")
        print(f"Updated at: {data['updated_at']}")
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error responding to order: {e}")
        return None

def get_restaurant_payments(restaurant_id):
    print(f"\n💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸 \n"
          "Retrieving Payments for Restaurant \n"
          "💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸💸 \n")
    try:
        response = requests.get(f"{API_BASE_URL}/restaurants/{restaurant_id}/payments")
        data = response.json()
        
        print(f"Payments retrieved for restaurant {restaurant_id}:")
        
        if not data:  
            print(" ❌ No payments found ❌")
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
    print("🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕 \n"
    "Inspired Food Platform Client Demo \n"
    "🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕\n")
    
    try:
        response = requests.get(f"{API_BASE_URL}/")
        print(f"Connected to API Gateway: {response.json()['message']}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API Gateway: {e}")
        sys.exit(1)
    
    restaurant = get_restaurant("restaurant456")
    if not restaurant:
        sys.exit(1)
    
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
        customer_name="Sara Rahim",
        customer_email="sara.rahim@mycit.ie",
        customer_phone="R00-211-761",
        restaurant_id=restaurant['restaurant_id'],
        items=order_items,
        delivery_address="Rossa Ave, Bishopstown, Cork, T12 P928",
        special_instructions="Please leave the food outside."
    )
    
    if not order:
        sys.exit(1)
    
    response = restaurant_respond_to_order(
        restaurant_id=restaurant['restaurant_id'],
        order_id=order['order_id'],
        accepted=True  
    )
    
    if not response:
        sys.exit(1)
        
    if response['status'] == "ORDER_CONFIRMED":
        time.sleep(1)
        update_order_status(order['order_id'], 4)  # ORDER_PREPARING
        
        delivery = assign_driver(order['order_id'], "driver789")
        if not delivery:
            sys.exit(1)
        
        time.sleep(1)
        get_delivery(delivery['delivery_id'])
        
        time.sleep(1)
        update_delivery_status(
            delivery_id=delivery['delivery_id'],
            status=2,  # DELIVERY_PICKED_UP
            current_location="At restaurant"
        )
            
        time.sleep(1)
        update_delivery_status(
            delivery_id=delivery['delivery_id'],
            status=3,  # DELIVERY_IN_PROGRESS
            current_location="Halfway to customer's address"
        )
        
        time.sleep(1)
        update_delivery_status(
            delivery_id=delivery['delivery_id'],
            status=4,  # DELIVERY_DELIVERED
            current_location="At customer's address"
        )
        
        time.sleep(1)
        get_order(order['order_id'])
        
        time.sleep(1)
        get_restaurant_payments("restaurant456")
        
        print("\n🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕 \n"
        " Demo completed successfully! \n"
        "🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕⭐🍕")
    else:
        print("Order was rejected by restaurant. Ending demo.")
        sys.exit(0)

if __name__ == "__main__":
    time.sleep(5)
    run()