from flask import jsonify

from models.user import User
from permissions import authorization_required
from services.dashboard import get_general_stats
from settings import app


@app.route('/dashboards/stats', methods=['GET'])
def get_general_stats_api():
    return jsonify(get_general_stats())


@app.route('/dashboards/vendor_stats', methods=['GET'])
@authorization_required()
def get_vendor_general_stats_api(current_user: User):
    return jsonify(get_general_stats(store_id=current_user.store_id))
