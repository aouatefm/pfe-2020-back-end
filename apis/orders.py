from flask import request, jsonify

from models.user import User
from permissions import authorization_required
from services.email import send_order_confirmation_email
from services.order import create_new_order, get_all_orders, get_order_by_id, update_order
from settings import app


@app.route('/orders', methods=['GET'])
@authorization_required()
def get_all_orders_api(current_user: User):
    user_filter = request.args.get('user_filter', 'customer')
    status_filter = request.args.get('status_filter', None)
    orders = get_all_orders(user_filter, status_filter, current_user)
    return jsonify(orders)


@app.route('/orders', methods=['POST'])
@authorization_required()
def create_new_order_api(current_user: User):
    payload = request.get_json()
    try:
        products = payload.pop('products')
    except ValueError:
        return jsonify({"message": "products field required"}), 400
    if len(products) == 0:
        return jsonify({"message": "no products in this order"}), 400

    success, message = create_new_order(current_user=current_user, products=products, **payload)
    if not success:
        return jsonify({"message": message}), 400

    return jsonify({"message": message}), 201


@app.route('/orders/<order_id>', methods=['GET'])
@authorization_required()
def get_order_by_id_api(order_id, current_user: User):
    order, message = get_order_by_id(order_id)
    if not order:
        return jsonify({"message": message}), 404
    return order.__dict__, 200


@app.route('/orders/<order_id>', methods=['PUT'])
@authorization_required()
def update_order_api(order_id, current_user: User):
    payload = request.get_json()
    order, message = get_order_by_id(order_id)
    if not order:
        return jsonify({"message": message}), 404

    if order.store_id != current_user.store_id:
        return jsonify({"message": message}), 403

    success, msg = update_order(order_id, **payload)
    if not success:
        return jsonify({"message": message}), 404

    return order.__dict__, 200
