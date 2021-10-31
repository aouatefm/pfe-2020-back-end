from firebase import fs
from datetime import datetime


class Rating:
    def __init__(self, rating_value: float, user_id: str, rating_date, id_product):
        self.user_id = user_id
        self.rating_value = rating_value
        self.rating_date = rating_date
        self.id_product = id_product

    user_id: str
    rating_value: float
    rating_date: datetime
    id_product: str
