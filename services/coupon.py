from firebase import fs, COLLECTIONS as COL
from models.coupon import Coupon
from models.user import User


def get_all_coupons(current_user: User) -> [dict]:
    coupons = fs.collection(COL['coupons']).where('store_id', '==', current_user.store_id).stream()
    result = [Coupon(**c.to_dict()) for c in coupons]
    return result


def get_visible_coupons(store_id) -> [dict]:
    coupons = fs.collection(COL['coupons']).where('store_id', '==', store_id).where('visible', '==', True).stream()
    result = [dict(id=c.id, **c.to_dict()) for c in coupons]
    return result


def get_coupon_by_id(coupon_id: str) -> (Coupon, str) or (None, str):
    coupon = fs.collection(COL['coupons']).document(coupon_id).get()
    if not coupon.exists:
        return None, "coupon does not exist"
    else:
        coupon = Coupon(**coupon.to_dict())
    return coupon, "coupon found."


def apply_coupon(coupon: Coupon, products: [dict]) -> [dict]:
    eligible_products = [ep.get("value") for ep in coupon.products]

    for p in products:
        p['eligible'] = False
        p['discounted_price'] = 0

        if p.get("product_id") in eligible_products:
            p['eligible'] = True
            if coupon.discount_type == 'fixed':
                p['discounted_price'] = max(0.0, float(p['price']) - int(coupon.discount_amount))

            else:
                p['discounted_price'] = float(p['price']) * ((100 - int(coupon.discount_amount)) / 100)
    return products


def create_new_coupon(current_user: User, **kwargs):
    print("coupon data:")
    print(kwargs)
    try:
        coupon = Coupon(name=kwargs.pop('name'),
                        description=kwargs.pop('description'),
                        discount_type=kwargs.pop('discount_type'),
                        discount_amount=kwargs.pop('discount_amount'),
                        expiry_date=kwargs.pop('expiry_date'),
                        products=kwargs.pop('products'),
                        visible=kwargs.pop('visible'),
                        store_id=current_user.store_id,
                        **kwargs
                        )

        coupon_dict = coupon.__dict__
        res = fs.collection(COL['coupons']).document(coupon.name).set(coupon_dict, merge=True)
        return True, f"coupon created. (coupon_id: {coupon.name})"
    except KeyError as e:
        return False, f"missing params ({str(e)})"


def delete_coupon(coupon_id):
    fs.collection(COL['coupons']).document(coupon_id).delete()
