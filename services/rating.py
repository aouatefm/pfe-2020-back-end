from math import ceil

from firebase import fs, COLLECTIONS as COL
from models.rating import Rating
from models.user import User


def create_rating(rating_value: float, rating_date, product_id, user: User) -> (bool, str):
    # TODO : check if the user bought the product
    # TODO : check if the user already rated the product
    try:
        rate = dict(rating_value=rating_value,
                    user_id=user.uid,
                    rating_date=rating_date,
                    product_id=product_id,
                    user_name=user.display_name,
                    avatar=user.avatar)

        res = fs.collection(COL['ratings']).add(rate)
        return True, f"ratings created. (rate_id: {res[1].id})"
    except KeyError as e:
        return False, f"missing params ({str(e)})"


def get_ratings_by_product(product_id: str) -> (dict, str) or (None, str):
    rating_stats = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0}
    # check if product id is found
    product = fs.collection(COL['products']).document(product_id).get()
    if not product.exists:
        return None, "not exist"

    # get all ratings of the product
    ratings = fs.collection(COL['ratings']).where('product_id', '==', product_id).stream()
    ratings = [dict(id=c.id, **c.to_dict()) for c in ratings]

    avg = get_product_ratings_avg(product_id, ratings=ratings)
    for r in ratings:
        rating_stats[f'{r.get("rating_value")}'] += 1
    result = dict(ratings=ratings, avg=avg, count=len(ratings), rating_stats=rating_stats)
    return result, f"{len(ratings)} ratings found"


def get_product_ratings_avg(product_id: str, ratings=None) -> float:
    if ratings is None:  # for db calls optimisation
        ratings = fs.collection(COL['ratings']).where('product_id', '==', product_id).stream()
        ratings = [dict(id=c.id, **c.to_dict()) for c in ratings]

    if len(ratings) > 0:
        avg = sum(r['rating_value'] for r in ratings) / len(ratings)
    else:
        avg = 0
    return round(avg * 2) / 2
