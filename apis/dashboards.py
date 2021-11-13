from flask import jsonify

from services.dashboard import get_general_stats
from settings import app


@app.route('/dashboards/stats', methods=['GET'])
def get_general_stats_api():
    return jsonify(get_general_stats())

