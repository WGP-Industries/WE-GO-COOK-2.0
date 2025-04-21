from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from App.controllers import create_user, initialize

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
@jwt_required(optional=True)
def index_page():
    user = current_user if current_user else None
    is_authenticated = user is not None

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if user:
        paginated_recipes = get_recipes_by_user(user.id, page, 5, q, sort_by)
        recipes_json = [r.get_json() for r in paginated_recipes.items]
    else:
        paginated_recipes = []
        recipes_json = [""]

    return render_template(
        'index.html',
        current_user=user,
        is_authenticated=is_authenticated,
        recipes=paginated_recipes,
        recipes_json=recipes_json,
        q=q, sort_by=sort_by,
        num_ingredients=1
    )

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})