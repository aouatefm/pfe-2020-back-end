from flask import jsonify, request

# ======= CRUD APIS ======= #
# ========================= #

from models.user import User
from permissions import authorization_required
from services.store import create_store, get_stores_list, get_store_by_id, delete_store, update_store
from settings import app


@app.route('/stores', methods=['GET'])
def get_all_stores_api():
    return jsonify(get_stores_list())


@app.route('/stores/<store_id>', methods=['GET'])
def get_store_by_id_api(store_id):
    store, detail = get_store_by_id(store_id)
    if store:
        return jsonify(store.__dict__), 200
    else:
        return jsonify({"message": detail}), 404


@app.route('/stores', methods=['POST'])
@authorization_required()
def create_store_api(current_user: User):
    payload = request.get_json()
    if 'name' not in payload:
        return jsonify({"message": "store name required"}), 422

    store, detail = create_store(owner_id=current_user.uid, name=payload['name'])
    if store:
        return jsonify({"message": detail}), 201
    else:
        return jsonify({"message": detail}), 400


@app.route('/stores/<store_id>', methods=['PUT'])
@authorization_required()
def edit_store_api(store_id, current_user: User):
    if current_user.store_id != store_id and current_user.role != "admin":
        return jsonify({"message": "unauthorised action!"}), 403
    payload = request.get_json()
    success, message = update_store(store_id=store_id, **payload)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 400


@app.route('/stores/<store_id>', methods=['DELETE'])
@authorization_required()
def delete_store_api(store_id, current_user: User):
    if current_user.store_id != store_id and current_user.role != "admin":
        return jsonify({"message": "unauthorised action!"}), 403

    success, message = delete_store(store_id)
    if success:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"message": message}), 404
