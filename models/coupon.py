from datetime import timedelta, datetime
from typing import Any


class Coupon:
    def __init__(self, name: str, discount_type: str, description, products, store_id: str,
                 discount_amount, visible: bool = False, expiry_date=(datetime.now() + timedelta(days=3)), **kwargs):
        self.id = name
        self.name = name
        self.description = description
        self.discount_type = discount_type
        self.discount_amount = discount_amount
        self.expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d') if type(expiry_date) is str else expiry_date
        self.is_expired = True if self.expiry_date.replace(tzinfo=None) < datetime.now() else False
        self.products = products
        self.visible = visible
        self.store_id = store_id
        self.created_at = kwargs.get('created_at', datetime.now())

    id: str
    name: str
    description: str
    discount_type: str
    discount_amount: int
    expiry_date: datetime
    is_expired: bool
    products: Any
    visible: bool
    store_id: str
    created_at: datetime
