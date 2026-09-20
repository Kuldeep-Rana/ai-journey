orders = {
 "ORD-101": {

    "status": "SHIPPED",
    "item": "Laptop",
    "amount": 85000,
    "payment": "PAID",
    "estimated_delivery": "2026-09-18"
  },
 
 "ORD-102":
  {
    "status": "PROCESSING",
    "item": "Headphones",
    "amount": 5000,
    "payment": "PAID",
    "estimated_delivery": "2026-09-20"
  }
}

def get_order_status(order_id):
    """Returns the status of the order, defaulting to 'UNKNOWN' if not found."""
    return orders.get(order_id, {}).get("status", "UNKNOWN")


def get_order_details(order_id):
    return orders.get(order_id)


def get_payment_status(order_id):
    return orders.get(order_id, {}).get("payment", "UNPAID")


def get_shipping_estimate(order_id):
    return orders.get(order_id, {}).get("estimated_delivery")

order_tool_registry = {
    "get_order_status" : get_order_status,
    "get_order_details" : get_order_details,
    "get_payment_status" : get_payment_status,
    "get_shipping_estimate" : get_shipping_estimate
}