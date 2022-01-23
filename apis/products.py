from flask import request, jsonify

from models.user import User
from permissions import authorization_required
from services.product import get_all_products, create_new_product, get_product_by_id, get_products_by_store, can_i_rate
from services.recommended_products import recommended_products, data_prep
from settings import app
import pickle


@app.route('/products', methods=['GET'])
def get_all_products_api():
    products = get_all_products()
    return jsonify(products)


@app.route('/products/store/<store_id>', methods=['GET'])
def get_store_products_api(store_id):
    products = get_products_by_store(store_id)
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


@app.route('/products/<product_id>/recommendations', methods=['GET'])
def product_recommendations(product_id):
    product, msg = get_product_by_id(product_id)
    if not product:
        return jsonify(dict(message=msg)), 404

    # Extract product title
    title = product.name

    # get products data
    data = get_all_products()

    # generate new model
    data_prep(data)

    # Load model
    rec_model = pickle.load(open('rec_model.pickle', 'rb'))

    # Call recommendation engine
    recommendations = recommended_products(title, data, rec_model)[0]

    # return recommended products
    return jsonify(recommendations)


@app.route('/products/<product_id>/can_i_rate', methods=['GET'])
@authorization_required()
def can_i_rate_api(current_user: User, product_id):
    return dict(res=can_i_rate(current_user.uid, product_id))
