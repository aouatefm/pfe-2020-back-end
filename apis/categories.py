from flask import request

from settings import app
from firebase import fs
from models import category as category_model


@app.route('/categories', methods=['GET'])
def get_all_categories():
    return category_model.get_all_categories()


@app.route('/categories', methods=['POST'])
def create_new_category():
    data = request.get_json()
    try:
        fs.collection('categories').document(data.get('title')).set(dict(title=data['title'],
                                                                         description=data['description']))
        return dict(message='category created with success'), 201

    except KeyError as e:
        return dict(message=f"missing parameters ({str(e)})"), 400


@app.route('/categories/<category_id>', methods=['GET'])
def get_one_category(category_id):
    category = fs.collection('categories').document(category_id).get()

    if category.exists:
        return dict(data=category.to_dict())
    else:
        return dict(message="category not found"), 404


@app.route('/categories/<category_id>', methods=['DELETE'])
def delete_one_category(category_id):
    fs.collection('categories').document(category_id).delete()
    return dict(message="category deleted successfully "), 200


@app.route('/categories/<category_id>', methods=['PUT'])
def edit_one_category(category_id):
    data = request.get_json()
    category = fs.collection('categories').document(category_id).get()

    if not category.exists:
        return dict(message="category not found"), 404
    # TODO: add data validation
    fs.collection('categories').document(category_id).set(data, merge=True)
    return dict(message='category edited with success'), 201


