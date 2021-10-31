from datetime import datetime

from flask import jsonify, request

from models.user import User
from permissions import authorization_required
from services.coupon import create_new_coupon, get_coupon_by_id, get_all_coupons, get_visible_coupons, delete_coupon, \
    apply_coupon
from settings import app


@app.route('/coupons', methods=['GET'])
@authorization_required()
def get_all_coupons_api(current_user: User):
    if not current_user.store_id:
        return jsonify({"message": "only vendors can have coupons."}), 400

    coupons = get_all_coupons(current_user)
    return jsonify([coupon.__dict__ for coupon in coupons])


@app.route('/coupons/visible/<store_id>', methods=['GET'])
def get_all_visible_coupons_api(store_id):
    coupons = get_visible_coupons(store_id)
    return jsonify(coupons)


@app.route('/coupons/<coupon_id>', methods=['GET'])
@authorization_required()
def get_coupon_by_id_api(coupon_id, current_user: User):
    coupon, message = get_coupon_by_id(coupon_id)
    if not coupon:
        return jsonify({"message": message}), 404
    return coupon.__dict__, 200


@app.route('/coupons/apply', methods=['POST'])
def apply_coupon_api():
    payload = request.get_json()
    # check if coupon and products in payload
    # if {'coupon', 'products'} <= payload.keys():
    #     return jsonify({"message": "missing params"}), 400

    coupon, msg = get_coupon_by_id(payload.get("coupon"))
    if coupon is None:
        return jsonify({"message": "Coupon does not exist."}), 404

    # if coupon.expiry_date > datetime.now(tz=None):
    #     return jsonify({"message": "Coupon expired"}), 400

    result = apply_coupon(coupon, payload['products'])

    return jsonify(result), 200


@app.route('/coupons', methods=['POST'])
@authorization_required()
def create_new_coupon_api(current_user: User):
    # check if user has a store
    if current_user.store_id is None:
        return jsonify({"message": "cannot create coupon without creating a store first."}), 400

    payload = request.get_json()
    # coupon, msg = get_coupon_by_id(payload.get("name"))
    # if coupon:
    #     return jsonify({"message": "Coupon already exists."}), 400

    success, message = create_new_coupon(current_user, **payload)
    if not success:
        return jsonify({"message": message}), 400

    return jsonify({"message": message}), 201


@app.route('/coupons/<coupon_id>', methods=['DELETE'])
def delete_coupon_api(coupon_id):
    coupon, msg = get_coupon_by_id(coupon_id)
    if not coupon:
        return jsonify({"message": "Coupon does not exist."}), 404
    # TODO : add check for delete owner only
    delete_coupon(coupon_id)
    return dict(message="coupon deleted successfully "), 200
