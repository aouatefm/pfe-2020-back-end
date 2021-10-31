from firebase import fs, COLLECTIONS as COL
from models.store import Store
from services.user import get_user_by_id, update_user_profile


def check_store_exist(store_id: str) -> bool:
    store = fs.collection(COL['stores']).document(store_id).get()
    return store.exists


def get_store_by_id(store_id: str) -> (Store, str) or (None, str):
    store = fs.collection(COL['stores']).document(store_id).get()
    if store.exists:
        return Store(**store.to_dict()), "store found"
    else:
        return None, "store not found!"


def create_store(name: str, owner_id: str, **kwargs) -> (Store, str) or (None, str):
    store_id = name.replace(' ', '-').lower()
    if check_store_exist(store_id):
        return None, "store already exists"

    user, detail = get_user_by_id(owner_id)
    if user.store_id is not None:
        return None, "user already have a store!"
    cover_image = kwargs.get('cover_image')
    if not cover_image or len(cover_image) == 0:
        kwargs['cover_image'] = "http://wp.reactstorefronts.com/static/img/vendor/store/default-store-banner.png"
    store = Store(name, owner_id, **kwargs)
    # create new store for the user
    fs.collection(COL['stores']).document(store_id).set(store.__dict__)
    # update user  with the newly created store id
    fs.collection(COL['users']).document(owner_id).set(dict(store_id=store_id), merge=True)

    return store, "store created."


def update_store(store_id, **kwargs) -> (bool, str):
    if not check_store_exist(store_id):
        return None, "store doest not exist."
    forbidden_fields = ['store_id', 'owner_id']
    for k in forbidden_fields:
        try:
            kwargs.pop(k)
        except KeyError:
            pass
    fs.collection(COL['stores']).document(store_id).set(kwargs, merge=True)
    return True, "store updated."


def delete_store(store_id: str) -> (bool, str):
    store = fs.collection(COL['stores']).document(store_id).get()
    if not store.exists:
        return False, "store not found."
    else:
        store = store.to_dict()

    fs.collection(COL['users']).document(store.get('owner_id')).set(dict(store_id=None), merge=True)
    fs.collection(COL['stores']).document(store_id).delete()
    return True, "store deleted."


def get_stores_list() -> [dict]:
    stores = fs.collection(COL['stores']).stream()
    return [s.to_dict() for s in stores]


def get_stores_names() -> [dict]:
    stores = fs.collection(COL['stores']).stream()
    return [s.to_dict().get('store_id') for s in stores]


def get_store_customers(store_id) -> [dict]:
    customer_orders = {}
    customers_and_orders = []
    orders = fs.collection(COL['orders']).where('store_id', '==', store_id).stream()

    for o in orders:
        if o.exists:
            order = o.to_dict()
            if order.get('customer_id') not in customer_orders:
                customer_orders[order.get('customer_id')] = dict(orders=[], orders_total=0)
            customer_orders[order.get('customer_id')]['orders'].append(dict(order_id=o.id, **order))
            customer_orders[order.get('customer_id')]['orders_total'] += order.get('total_price')

    for customer_id in customer_orders.keys():
        customer, detail = get_user_by_id(customer_id)
        if customer:
            data = dict(orders=customer_orders[customer_id]['orders'],
                        orders_total=customer_orders[customer_id]['orders_total'],
                        **customer.__dict__)
            customers_and_orders.append(data)
    return customers_and_orders

