from pprint import pprint

from firebase import fs, COLLECTIONS as COL
from models.order import Order
from models.user import User
from services.email import send_order_confirmation_email


def get_all_orders(user_filter, status_filter, current_user: User) -> [dict]:
    if user_filter == 'store':
        if status_filter:
            orders = fs.collection(COL['orders']).where('store_id', '==', current_user.store_id) \
                .where('status', '==', status_filter).stream()
        else:
            orders = fs.collection(COL['orders']).where('store_id', '==', current_user.store_id).stream()

    elif user_filter == 'customer':
        if status_filter:
            orders = fs.collection(COL['orders']).where('customer_id', '==', current_user.uid) \
                .where('status', '==', status_filter).stream()
        else:
            orders = fs.collection(COL['orders']).where('customer_id', '==', current_user.uid).stream()
    else:
        orders = []
    result = [dict(id=c.id, **c.to_dict()) for c in orders]
    return result


def create_new_order(current_user: User, products: [dict], **kwargs) -> (bool, str):
    print(kwargs)
    products_per_store = {}
    pprint(products)
    for p in products:
        if not products_per_store.get(p.get('store_id')):
            products_per_store[p.get('store_id')] = []
        products_per_store[p.get('store_id')].append(p)
    orders_created = []
    for store_id, products in products_per_store.items():
        total_price = 0
        for p in products:
            if p.get('discounted_price', 0) == 0:
                total_price += float(p['price']) * int(p['quantity'])
            else:
                total_price += float(p['discounted_price']) * int(p['quantity'])
        try:
            order = Order(order_id=kwargs.get('order_id'),
                          store_id=store_id,
                          customer_id=current_user.uid,
                          products=products,
                          billing_adr=kwargs.get('billing_adr'),
                          shipping_adr=kwargs.get('shipping_adr'),
                          contact_number=kwargs.get('contact_number'),
                          total_price=total_price,
                          delivery=kwargs.get('delivery'),
                          payment=kwargs.get('payment'),
                          notes=kwargs.get('notes'),
                          second_contact_number=kwargs.get('SecondPhone'),
                          )

            order_dict = order.__dict__
            order_dict.pop('order_id')
            res = fs.collection(COL['orders']).add(order_dict)
            order.order_id = res[1].id
            orders_created.append(order.order_id)

            # Send email confirmation after order creation
            try:
                send_order_confirmation_email(current_user, order)
            except Exception as e:
                print(e)

        except KeyError as e:
            return False, f"missing params ({str(e)})"
    return True, f"orders created. ({orders_created})"


def get_order_by_id(order_id: str) -> (Order, str) or (None, str):
    order = fs.collection(COL['orders']).document(order_id).get()
    if not order.exists:
        return None, "order does not exist"
    else:
        product = Order(order_id=order.id, **order.to_dict())

    return product, "order found."


def update_order(order_id, **kwargs) -> (bool, str):
    if "status" in kwargs:
        if kwargs["status"] not in ["pending", "canceled", "processing", "completed"]:
            return False, "wrong order status value."

    fs.collection(COL['orders']).document(order_id).set(kwargs, merge=True)
    return True, "order updated."
