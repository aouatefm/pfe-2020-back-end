from datetime import datetime

from flask import request
from firebase import fs


class Product:
    def __init__(self, name: str, price: float, description, images, creator_id, store_id, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.name = name
        self.price = price
        self.description = description
        self.category = kwargs.get('category')
        self.sub_category = kwargs.get('sub_category')
        self.images = images
        self.shipping_price = kwargs.get('shipping_price')
        self.product_type = kwargs.get('product_type')
        self.stock = kwargs.get('stock')
        self.video = kwargs.get('video')
        self.store_id = store_id
        self.creator_id = creator_id
        self.created_at = kwargs.get('created_at', datetime.now())
        self.updated_at = kwargs.get('updated_at')

    product_id: str
    name: str
    price: float
    description: str
    category: str
    sub_category: str
    images: [str]
    shipping_price: float
    product_type: str
    stock: int
    video: str
    store_id: str
    creator_id: str
    created_at: datetime
    updated_at: datetime
