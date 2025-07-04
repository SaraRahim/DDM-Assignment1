# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: order_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'order_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13order_service.proto\x12\x05order\"\xcb\x01\n\x12\x43reateOrderRequest\x12\x15\n\rcustomer_name\x18\x01 \x01(\t\x12\x16\n\x0e\x63ustomer_email\x18\x02 \x01(\t\x12\x16\n\x0e\x63ustomer_phone\x18\x03 \x01(\t\x12\x15\n\rrestaurant_id\x18\x04 \x01(\t\x12\x1f\n\x05items\x18\x05 \x03(\x0b\x32\x10.order.OrderItem\x12\x18\n\x10\x64\x65livery_address\x18\x06 \x01(\t\x12\x1c\n\x14special_instructions\x18\x07 \x01(\t\"#\n\x0fGetOrderRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\"P\n\x18UpdateOrderStatusRequest\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\"\n\x06status\x18\x02 \x01(\x0e\x32\x12.order.OrderStatus\"c\n\tOrderItem\x12\x0f\n\x07item_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\r\n\x05price\x18\x03 \x01(\x01\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x12\x16\n\x0e\x63ustomizations\x18\x05 \x03(\t\"u\n\x1eRestaurantOrderResponseRequest\x12\x15\n\rrestaurant_id\x18\x01 \x01(\t\x12\x10\n\x08order_id\x18\x02 \x01(\t\x12\x10\n\x08\x61\x63\x63\x65pted\x18\x03 \x01(\x08\x12\x18\n\x10rejection_reason\x18\x04 \x01(\t\"\x85\x01\n\x1fRestaurantOrderResponseResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\"\n\x06status\x18\x02 \x01(\x0e\x32\x12.order.OrderStatus\x12\x12\n\nupdated_at\x18\x03 \x01(\t\x12\x18\n\x10rejection_reason\x18\x04 \x01(\t\"\xdb\x02\n\rOrderResponse\x12\x10\n\x08order_id\x18\x01 \x01(\t\x12\x15\n\rcustomer_name\x18\x02 \x01(\t\x12\x16\n\x0e\x63ustomer_email\x18\x03 \x01(\t\x12\x16\n\x0e\x63ustomer_phone\x18\x04 \x01(\t\x12\x18\n\x10\x64\x65livery_address\x18\x05 \x01(\t\x12\x15\n\rrestaurant_id\x18\x06 \x01(\t\x12\x1f\n\x05items\x18\x07 \x03(\x0b\x32\x10.order.OrderItem\x12\x1c\n\x14special_instructions\x18\x08 \x01(\t\x12\"\n\x06status\x18\t \x01(\x0e\x32\x12.order.OrderStatus\x12\x14\n\x0ctotal_amount\x18\n \x01(\x01\x12\x12\n\ncreated_at\x18\x0b \x01(\t\x12\x12\n\nupdated_at\x18\x0c \x01(\t\x12\x1f\n\x17\x65stimated_delivery_time\x18\r \x01(\t*\xc8\x01\n\x0bOrderStatus\x12\x11\n\rORDER_UNKNOWN\x10\x00\x12\x11\n\rORDER_PENDING\x10\x01\x12\x13\n\x0fORDER_CONFIRMED\x10\x02\x12\x12\n\x0eORDER_REJECTED\x10\x03\x12\x13\n\x0fORDER_PREPARING\x10\x04\x12\x0f\n\x0bORDER_READY\x10\x05\x12\x1a\n\x16ORDER_OUT_FOR_DELIVERY\x10\x06\x12\x13\n\x0fORDER_DELIVERED\x10\x07\x12\x13\n\x0fORDER_CANCELLED\x10\x08\x32\xbe\x02\n\x0cOrderService\x12>\n\x0b\x43reateOrder\x12\x19.order.CreateOrderRequest\x1a\x14.order.OrderResponse\x12\x38\n\x08GetOrder\x12\x16.order.GetOrderRequest\x1a\x14.order.OrderResponse\x12J\n\x11UpdateOrderStatus\x12\x1f.order.UpdateOrderStatusRequest\x1a\x14.order.OrderResponse\x12h\n\x17RestaurantOrderResponse\x12%.order.RestaurantOrderResponseRequest\x1a&.order.RestaurantOrderResponseResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'order_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ORDERSTATUS']._serialized_start=1062
  _globals['_ORDERSTATUS']._serialized_end=1262
  _globals['_CREATEORDERREQUEST']._serialized_start=31
  _globals['_CREATEORDERREQUEST']._serialized_end=234
  _globals['_GETORDERREQUEST']._serialized_start=236
  _globals['_GETORDERREQUEST']._serialized_end=271
  _globals['_UPDATEORDERSTATUSREQUEST']._serialized_start=273
  _globals['_UPDATEORDERSTATUSREQUEST']._serialized_end=353
  _globals['_ORDERITEM']._serialized_start=355
  _globals['_ORDERITEM']._serialized_end=454
  _globals['_RESTAURANTORDERRESPONSEREQUEST']._serialized_start=456
  _globals['_RESTAURANTORDERRESPONSEREQUEST']._serialized_end=573
  _globals['_RESTAURANTORDERRESPONSERESPONSE']._serialized_start=576
  _globals['_RESTAURANTORDERRESPONSERESPONSE']._serialized_end=709
  _globals['_ORDERRESPONSE']._serialized_start=712
  _globals['_ORDERRESPONSE']._serialized_end=1059
  _globals['_ORDERSERVICE']._serialized_start=1265
  _globals['_ORDERSERVICE']._serialized_end=1583
# @@protoc_insertion_point(module_scope)
