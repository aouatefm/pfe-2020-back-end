from firebase import fs, COLLECTIONS as COL
from models.product import Product


def get_all_products() -> [dict]:
    products = fs.collection(COL['products']).stream()
    result = [dict(id=c.id, **c.to_dict()) for c in products]
    return result


def get_products_by_store(store_id: str) -> [dict]:
    products = fs.collection(COL['products']).where('store_id', '==', store_id).stream()
    result = [dict(id=c.id, **c.to_dict()) for c in products]
    return result


def get_product_by_id(product_id: str) -> (Product, str) or (None, str):
    product = fs.collection(COL['products']).document(product_id).get()
    if not product.exists:
        return None, "product does not exist"
    else:
        product = Product(product_id=product.id, **product.to_dict())

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
