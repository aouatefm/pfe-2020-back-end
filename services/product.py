from firebase import fs, COLLECTIONS as COL
from models.product import Product
from services.rating import get_product_ratings_avg


def get_all_products() -> [dict]:
    products = fs.collection(COL['products']).stream()
    result = [dict(id=c.id, ratings_avg=get_product_ratings_avg(c.id), **c.to_dict()) for c in products]
    return result


def get_products_by_store(store_id: str) -> [dict]:
    products = fs.collection(COL['products']).where('store_id', '==', store_id).stream()
    result = [dict(id=c.id,
                   ratings_avg=get_product_ratings_avg(c.id),
                   **c.to_dict()) for c in products
              ]
    return result


def get_product_by_id(product_id: str) -> (Product, str) or (None, str):
    product = fs.collection(COL['products']).document(product_id).get()
    if not product.exists:
        return None, "product does not exist"
    else:
        product = Product(product_id=product.id,
                          ratings_avg=get_product_ratings_avg(product.id),
                          **product.to_dict()
                          )

    return product, "product found."


def create_new_product(creator_id: str, store_id: str, **kwargs) -> (bool, str):
    print(kwargs)
    try:
        product = Product(store_id=store_id,
                          name=kwargs.pop('name'),
                          price=kwargs.pop('price'),
                          images=kwargs.pop('images'),
                          description=kwargs.pop('description'),
                          creator_id=creator_id,
                          **kwargs
                          )

        product_dict = product.__dict__
        product_dict.pop('product_id')
        res = fs.collection(COL['products']).add(product_dict)
        return True, f"product created. (product_id: {res[1].id})"
    except KeyError as e:
        return False, f"missing params ({str(e)})"


def edit_product(product_id, **kwargs):
    try:
        fs.collection(COL['products']).document(product_id).set(dict(name=kwargs.get('name'),
                                                                     price=kwargs.get('price'),
                                                                     images=kwargs.get('images'),
                                                                     description=kwargs.get('description'),
                                                                     shipping_price=kwargs.get('shipping_price'),
                                                                     category=kwargs.get('category'),
                                                                     stock=kwargs.get('stock'),
                                                                     video=kwargs.get('video'),
                                                                     product_type=kwargs.get('product_type')),
                                                                merge=True)
        return True, f"Product [{product_id}] updated successfully!"
    except Exception as e:
        return False, str(e)


def delete_product(product_id):
    try:
        fs.collection(COL['products']).document(product_id).delete()
        return True, f"Product [{product_id}] deleted successfully!"
    except Exception as e:
        return False, str(e)


def can_i_rate(user_id, product_id):
    customer_ratings = fs.collection(COL['ratings']) \
        .where('user_id', '==', user_id) \
        .where('product_id', '==', product_id) \
        .stream()

    if len(list(customer_ratings)) > 0:
        print('product Already rated!')
        return False

    customer_orders = fs.collection(COL['orders']) \
        .where('customer_id', '==', user_id) \
        .where('status', '==', 'completed') \
        .stream()
    customer_orders = [dict(order_id=o.id, products=o.to_dict().get('products')) for o in customer_orders]
    for o in customer_orders:
        for p in o.get('products'):
            if product_id == p.get('product_id'):
                return True

    return False
