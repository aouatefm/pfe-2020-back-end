from models.user import User
from permissions import authorization_required
from services.rating import create_rating, get_ratings_by_product
from flask import request, jsonify
from settings import app


@app.route('/ratings', methods=['POST'])
@authorization_required()
def create_ratings_api(current_user: User):
    payload = request.get_json()
    success, message = create_rating(user=current_user, **payload)
    if not success:
        return jsonify({"message": message}), 400

    return jsonify({"message": message}), 201


@app.route('/ratings/<product_id>', methods=['GET'])
def get_ratings_api(product_id: str):
    result, message = get_ratings_by_product(product_id)
    if not result:
        return jsonify({"message": message}), 400

    return jsonify(result), 200
    # return jsonify({"data": result}), 200
