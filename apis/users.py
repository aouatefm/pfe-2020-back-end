from flask import jsonify, request

from models.user import User
from permissions import authorization_required
from services.user import get_user_by_id, get_all_users, delete_user, create_user, update_user_profile, \
    update_user_password, update_user_email
from settings import app


# ======= CRUD APIS ======= #
# ========================= #
@app.route('/users', methods=['GET'])
@authorization_required(admin_required=True)
def get_all_users_api(current_user: User):

    users = get_all_users()
    return jsonify(users)


@app.route('/users/<uid>', methods=['GET'])
def get_user_by_id_api(uid):
    user, detail = get_user_by_id(uid)
    if not user:
        return jsonify({"message": "user not found"}), 404

    return jsonify(user.__dict__), 200


@app.route('/users', methods=['POST'])
def create_user_api():
    try:
        user, detail = create_user(**request.get_json())
    except TypeError as e:
        return jsonify({"message": str(e)}), 400

    if not user:
        return jsonify({"message": detail}), 400
    else:
        return jsonify({"message": detail}), 201


@app.route('/users/<uid>', methods=['PUT'])
@authorization_required()
def edit_user_api(uid, current_user: User):
    # TODO: is owner required
    if current_user.uid != uid and current_user.role != 'admin':
        return jsonify({"message": "Not authorized!"}), 400

    success, detail = update_user_profile(uid, **request.get_json())
    if success:
        return jsonify({"message": detail}), 200
    else:
        return jsonify({"message": detail}), 400


@app.route('/users/<uid>', methods=['DELETE'])
def delete_user_api(uid):
    is_deleted, detail = delete_user(uid)
    if is_deleted:
        return jsonify({"message": detail}), 200
    else:
        return jsonify({"message": detail}), 404


# ======= CONTROLLERS ======= #
# =========================== #
@authorization_required(admin_required=True)
@app.route('/users/<uid>/change_password', methods=['PUT'])
def edit_user_password_api(uid):
    payload = request.get_json()

    if 'password' not in payload:
        return jsonify({"message": "password field required!"}), 400

    success, detail = update_user_password(uid=uid, password=payload['password'])

    if success:
        return jsonify({"message": detail}), 200
    else:
        return jsonify({"message": detail}), 400


@app.route('/users/<uid>/change_email', methods=['PUT'])
def edit_user_email_api(uid):
    payload = request.get_json()

    if 'email' not in payload:
        return jsonify({"message": "email field required!"}), 400

    success, detail = update_user_email(uid=uid, email=payload['email'].lower())

    if success:
        return jsonify({"message": detail}), 200
    else:
        return jsonify({"message": detail}), 400
