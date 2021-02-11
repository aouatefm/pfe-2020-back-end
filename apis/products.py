from flask import request, jsonify

from models.user import User
from permissions import authorization_required
from services.product import get_all_products, create_new_product, get_product_by_id
from settings import app
from models import product as product_model


@app.route('/products', methods=['GET'])
def get_all_products_api():
    products = get_all_products()
    return jsonify(products)


@app.route('/products/<product_id>', methods=['GET'])
def get_product_by_id_api(product_id):
    product, message = get_product_by_id(product_id)
    if not product:
        return jsonify({"message": message}), 404
    return product.__dict__, 200


@app.route('/products', methods=['POST'])
@authorization_required()
def create_new_product_api(current_user: User):
    # check if user has a store
    if current_user.store_id is None:
        return jsonify({"message": "cannot create products without creating a store first."}), 400

    payload = request.get_json()
    success, message = create_new_product(creator_id=current_user.uid, store_id=current_user.store_id, **payload)
    if not success:
        return jsonify({"message": message}), 400

    return jsonify({"message": message}), 201
