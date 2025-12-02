"""
backend.api

A small Flask blueprint exposing a subset of the JSON API.
This blueprint is provided for future refactoring and is not required
for the current app (app.py contains the primary endpoints).

To use this blueprint, import and register it from `app.py`:

    from backend.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

"""
from flask import Blueprint, jsonify, request
from .models import add_reading, get_readings, add_food, get_foods, init_db

api_bp = Blueprint('api_bp', __name__)

@api_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

@api_bp.route('/readings', methods=['GET', 'POST'])
def readings_route():
    if request.method == 'GET':
        user_id = int(request.args.get('user_id', 1))
        limit = int(request.args.get('limit', 50))
        readings = get_readings(user_id=user_id, limit=limit)
        return jsonify({'ok': True, 'readings': readings})
    else:
        data = request.get_json() or {}
        reading = add_reading(data.get('user_id', 1), data['glucose'], data.get('context', 'general'), data.get('meal', ''), data.get('note', ''))
        return jsonify({'ok': True, 'reading': reading}), 201

@api_bp.route('/foods', methods=['GET', 'POST'])
def foods_route():
    if request.method == 'GET':
        foods = get_foods()
        return jsonify({'ok': True, 'foods': foods})
    else:
        data = request.get_json() or {}
        f = add_food(data.get('date'), data.get('time'), data.get('food'))
        return jsonify({'ok': True, 'food': f}), 201

@api_bp.route('/init', methods=['POST'])
def init_route():
    init_db()
    return jsonify({'ok': True})
