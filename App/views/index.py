from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from flask_jwt_extended import jwt_required
from App.controllers import create_user, initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@jwt_required(optional=True)
def index_page():
    user = current_user if current_user else None
    is_authenticated = user is not None
    recipes = get_all_recipes()
    recipes_json = [r.get_json() for r in recipes]
    return render_template(
        'index.html',
        current_user=user,
        is_authenticated=is_authenticated,
        recipes=recipes,
        recipes_json = recipes_json
    )

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})