import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'order_service'))
sys.path.insert(0, os.path.join(project_root, 'restaurant_service'))
sys.path.insert(0, os.path.join(project_root, 'delivery_service'))
import logging
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
import grpc
from order_service import order_service_pb2
from order_service import order_service_pb2_grpc
from restaurant_service import restaurant_service_pb2
from restaurant_service import restaurant_service_pb2_grpc
from delivery_service import delivery_service_pb2
from delivery_service import delivery_service_pb2_grpc

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Inspired Food API Gateway")

ORDER_SERVICE_ADDR = os.environ.get('ORDER_SERVICE_ADDR', 'order_service:50051')
DELIVERY_SERVICE_ADDR = os.environ.get('DELIVERY_SERVICE_ADDR', 'delivery_service:50052')
RESTAURANT_SERVICE_ADDR = os.environ.get('RESTAURANT_SERVICE_ADDR', 'restaurant_service:50053')

order_channel = grpc.insecure_channel(ORDER_SERVICE_ADDR)
order_stub = order_service_pb2_grpc.OrderServiceStub(order_channel)

delivery_channel = grpc.insecure_channel(DELIVERY_SERVICE_ADDR)
delivery_stub = delivery_service_pb2_grpc.DeliveryServiceStub(delivery_channel)

restaurant_channel = grpc.insecure_channel(RESTAURANT_SERVICE_ADDR)
restaurant_stub = restaurant_service_pb2_grpc.RestaurantServiceStub(restaurant_channel)

class OrderItemModel(BaseModel):
    item_id: str
    quantity: int
    name: str
    price: float
    customizations: List[str] = []

class CreateOrderModel(BaseModel):
    customer_name: str          
    customer_email: str        
    customer_phone: Optional[str] = None  
    restaurant_id: str
    items: List[OrderItemModel]
    delivery_address: str
    special_instructions: Optional[str] = None

class MenuItemModel(BaseModel):
    item_id: str
    name: str
    description: str
    price: float
    available: bool = True

class UpdateMenuModel(BaseModel):
    restaurant_id: str
    menu_items: List[MenuItemModel]

@app.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: str):
    request = restaurant_service_pb2.GetRestaurantRequest(restaurant_id=restaurant_id)
    try:
        response = restaurant_stub.GetRestaurant(request)
        
        menu_items = []
        for item in response.menu_items:
            menu_items.append({
                "item_id": item.item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "available": item.available
            })
            
        return {
            "restaurant_id": response.restaurant_id,
            "name": response.name,
            "address": response.address,
            "is_open": response.is_open,
            "menu_items": menu_items
        }
    except grpc.RpcError as e:
        logging.error(f"Restaurant Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/restaurants/{restaurant_id}/orders/{order_id}/response")
async def restaurant_order_response(
    restaurant_id: str, 
    order_id: str, 
    response_data: dict = Body(...)
):

    accepted = response_data.get("accepted", False)
    rejection_reason = response_data.get("rejection_reason", "") if not accepted else ""
    
    request = order_service_pb2.RestaurantOrderResponseRequest(
        restaurant_id=restaurant_id,
        order_id=order_id,
        accepted=accepted,
        rejection_reason=rejection_reason
    )
    
    try:
        response = order_stub.RestaurantOrderResponse(request)
        
        result = {
            "order_id": response.order_id,
            "status": order_service_pb2.OrderStatus.Name(response.status),
            "updated_at": response.updated_at
        }
        
        if not accepted:
            result["rejection_reason"] = response.rejection_reason
            
        return result
    except grpc.RpcError as e:
        status_code = e.code()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=str(e.details()))
        elif status_code == grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(status_code=403, detail=str(e.details()))
        elif status_code == grpc.StatusCode.FAILED_PRECONDITION:
            raise HTTPException(status_code=400, detail=str(e.details()))
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.put("/restaurants/{restaurant_id}/menu")
async def update_menu(restaurant_id: str, menu_data: UpdateMenuModel):
    menu_items = []
    for item in menu_data.menu_items:
        menu_item = restaurant_service_pb2.MenuItem(
            item_id=item.item_id,
            name=item.name,
            description=item.description,
            price=item.price,
            available=item.available
        )
        menu_items.append(menu_item)
    
    request = restaurant_service_pb2.UpdateMenuRequest(
        restaurant_id=restaurant_id,
        menu_items=menu_items
    )
    
    try:
        response = restaurant_stub.UpdateMenu(request)
        
        result_items = []
        for item in response.menu_items:
            result_items.append({
                "item_id": item.item_id,
                "name": item.name,
                "price": item.price
            })
            
        return {
            "restaurant_id": response.restaurant_id,
            "updated_at": response.updated_at,
            "menu_items": result_items
        }
    except grpc.RpcError as e:
        logging.error(f"Restaurant Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/restaurants/{restaurant_id}/payments")
async def get_restaurant_payments(restaurant_id: str):
    try:
        request = restaurant_service_pb2.GetRestaurantPaymentsRequest(restaurant_id=restaurant_id)
        response = restaurant_stub.GetRestaurantPayments(request)
        
        payments = []
        for payment in response.payments:
            payments.append({
                "payment_id": payment.payment_id,
                "order_id": payment.order_id,
                "amount": payment.amount,
                "status": payment.status,
                "timestamp": payment.timestamp
            })
        
        return payments
    except grpc.RpcError as e:
        status_code = e.code()
        if status_code == grpc.StatusCode.NOT_FOUND:
            raise HTTPException(status_code=404, detail=str(e.details()))
        else:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/orders")
async def create_order(order_data: CreateOrderModel):
    items = []
    for item in order_data.items:
        order_item = order_service_pb2.OrderItem(
            item_id=item.item_id,
            quantity=item.quantity,
            name=item.name,
            price=item.price,
            customizations=item.customizations
        )
        items.append(order_item)
    
    request = order_service_pb2.CreateOrderRequest(
        customer_name=order_data.customer_name,       
        customer_email=order_data.customer_email,    
        customer_phone=order_data.customer_phone or "",
        restaurant_id=order_data.restaurant_id,
        items=items,
        delivery_address=order_data.delivery_address,
        special_instructions=order_data.special_instructions or ""
    )
    
    try:
        response = order_stub.CreateOrder(request)
        
        result_items = []
        for item in response.items:
            item_dict = {
                "item_id": item.item_id,
                "quantity": item.quantity,
                "name": item.name,
                "price": item.price
            }
            if item.customizations:
                item_dict["customizations"] = list(item.customizations)
            result_items.append(item_dict)
            
        return {
            "order_id": response.order_id,
            "customer_name": response.customer_name,  
            "customer_email": response.customer_email, 
            "customer_phone": response.customer_phone,  
            "restaurant_id": response.restaurant_id,
            "items": result_items,
            "delivery_address": response.delivery_address,
            "special_instructions": response.special_instructions,
            "status": order_service_pb2.OrderStatus.Name(response.status),
            "total_amount": response.total_amount,
            "created_at": response.created_at,
            "updated_at": response.updated_at,
            "estimated_delivery_time": response.estimated_delivery_time
        }
    except grpc.RpcError as e:
        logging.error(f"Order Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders/{order_id}")
async def get_order(order_id: str):
    request = order_service_pb2.GetOrderRequest(order_id=order_id)
    try:
        response = order_stub.GetOrder(request)
        
        result_items = []
        for item in response.items:
            item_dict = {
                "item_id": item.item_id,
                "quantity": item.quantity,
                "name": item.name,
                "price": item.price
            }
            if item.customizations:
                item_dict["customizations"] = list(item.customizations)
            result_items.append(item_dict)
            
        return {
            "order_id": response.order_id,
            "customer_name": response.customer_name, 
            "customer_email": response.customer_email,  
            "customer_phone": response.customer_phone,  
            "restaurant_id": response.restaurant_id,
            "items": result_items,
            "delivery_address": response.delivery_address,
            "special_instructions": response.special_instructions,
            "status": order_service_pb2.OrderStatus.Name(response.status),
            "total_amount": response.total_amount,
            "created_at": response.created_at,
            "updated_at": response.updated_at,
            "estimated_delivery_time": response.estimated_delivery_time
        }
    except grpc.RpcError as e:
        logging.error(f"Order Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: int = Body(..., embed=True)):
    request = order_service_pb2.UpdateOrderStatusRequest(
        order_id=order_id,
        status=status
    )
    
    try:
        response = order_stub.UpdateOrderStatus(request)
        
        return {
            "order_id": response.order_id,
            "status": order_service_pb2.OrderStatus.Name(response.status),
            "updated_at": response.updated_at
        }
    except grpc.RpcError as e:
        logging.error(f"Order Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deliveries")
async def assign_driver(order_id: str = Body(...), driver_id: str = Body(...)):
    request = delivery_service_pb2.AssignDriverRequest(
        order_id=order_id,
        driver_id=driver_id
    )
    
    try:
        response = delivery_stub.AssignDriver(request)
        
        result = {
            "delivery_id": response.delivery_id,
            "order_id": response.order_id,
            "driver_id": response.driver_id,
            "restaurant_address": response.restaurant_address,
            "customer_address": response.customer_address,
            "status": delivery_service_pb2.DeliveryStatus.Name(response.status),
            "current_location": response.current_location,
            "assigned_at": response.assigned_at,
            "estimated_delivery_time": response.estimated_delivery_time
        }
        
        if hasattr(response, 'picked_up_at') and response.picked_up_at:
            result["picked_up_at"] = response.picked_up_at
            
        if hasattr(response, 'delivered_at') and response.delivered_at:
            result["delivered_at"] = response.delivered_at
            
        return result
    except grpc.RpcError as e:
        logging.error(f"Delivery Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/deliveries/{delivery_id}")
async def get_delivery(delivery_id: str):
    request = delivery_service_pb2.GetDeliveryRequest(delivery_id=delivery_id)
    
    try:
        response = delivery_stub.GetDelivery(request)
        
        result = {
            "delivery_id": response.delivery_id,
            "order_id": response.order_id,
            "driver_id": response.driver_id,
            "restaurant_address": response.restaurant_address,
            "customer_address": response.customer_address,
            "status": delivery_service_pb2.DeliveryStatus.Name(response.status),
            "current_location": response.current_location,
            "assigned_at": response.assigned_at,
            "estimated_delivery_time": response.estimated_delivery_time
        }
        
        if hasattr(response, 'picked_up_at') and response.picked_up_at:
            result["picked_up_at"] = response.picked_up_at
            
        if hasattr(response, 'delivered_at') and response.delivered_at:
            result["delivered_at"] = response.delivered_at
            
        return result
    except grpc.RpcError as e:
        logging.error(f"Delivery Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/deliveries/{delivery_id}/status")
async def update_delivery_status(
    delivery_id: str, 
    status: int = Body(..., embed=True),
    current_location: str = Body(..., embed=True)
):
    request = delivery_service_pb2.UpdateDeliveryStatusRequest(
        delivery_id=delivery_id,
        status=status,
        current_location=current_location
    )
    
    try:
        response = delivery_stub.UpdateDeliveryStatus(request)
        
        result = {
            "delivery_id": response.delivery_id,
            "status": delivery_service_pb2.DeliveryStatus.Name(response.status),
            "current_location": response.current_location
        }
        
        return result
    except grpc.RpcError as e:
        logging.error(f"Delivery Service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {
        "message": "Inspired Food Platform API Gateway",
        "services": {
            "order_service": ORDER_SERVICE_ADDR,
            "delivery_service": DELIVERY_SERVICE_ADDR,
            "restaurant_service": RESTAURANT_SERVICE_ADDR
        }
    }

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get("PORT", "50050"))
    uvicorn.run(app, host="0.0.0.0", port=port)