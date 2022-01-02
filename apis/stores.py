from flask import jsonify, request

# ======= CRUD APIS ======= #
# ========================= #

from models.user import User
from permissions import authorization_required
from services.store import create_store, get_stores_list, get_store_by_id, delete_store, update_store, get_stores_names, \
    get_store_customers
from settings import app
from utilities import bool_eval


@app.route('/stores', methods=['GET'])
def get_all_stores_api():
    is_active = request.args.get('is_active', default=None, type=bool_eval)
    return jsonify(get_stores_list(is_active))


@app.route('/stores/names', methods=['GET'])
def get_all_stores_name_api():
    return jsonify(get_stores_names())


@app.route('/stores/<store_id>', methods=['GET'])
def get_store_by_id_api(store_id):
    store, detail = get_store_by_id(store_id)
    if store:
        return jsonify(store.__dict__), 200
    else:
        return jsonify({"message": detail}), 404


@app.route('/stores/<store_id>/customers', methods=['GET'])
@authorization_required()
def get_store_customers_api(store_id, current_user: User):
    store, detail = get_store_by_id(store_id)
    if not store:
        return jsonify({"message": detail}), 404

    if current_user.store_id != store_id:
        return jsonify({"message": "Unauthorized access!"}), 403

    result_data = get_store_customers(store_id)
    return jsonify(result_data), 200


@app.route('/stores', methods=['POST'])
@authorization_required()
def create_store_api(current_user: User):
    payload = request.get_json()
    if 'name' not in payload:
        return jsonify({"message": "store name required"}), 422
    store, detail = create_store(owner_id=current_user.uid, name=payload.pop('name'), **payload)
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
