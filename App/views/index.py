from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify
from flask_jwt_extended import jwt_required, current_user
from App.controllers import *

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

@index_views.route('/addRecipe', methods=['POST'])
@jwt_required()
def add_recipe():
    title = request.form.get('title')
    instructions = request.form.get('instructions')
    image = request.form.get('image') or ""
    user_id = current_user.id

    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", default='', type=str)
    sort_by = request.args.get("sort_by", default='title_asc')

    if not title or not instructions:
        flash("Missing required fields", "error")
        return redirect(url_for('index_views.index_page', page=page, q=q, sort_by = sort_by))

    recipe = create_recipe(title, instructions, user_id, image)

    
    num_ingredients = int(request.form.get('num-ingredients') or 1)

    for i in range(num_ingredients):
        name = request.form.get(f'ingredient_name_{i}') or "none"
        quantity = request.form.get(f'ingredient_quantity_{i}') or "0"
        unit = request.form.get(f'ingredient_unit_{i}') or "none"
        img = request.form.get(f'ingredient_image_{i}') or "none"
        if name and quantity:
            add_ingredient_to_recipe(recipe.id, name, quantity, img, unit)
    
    flash("Recipe added", "success")
    return redirect(url_for('index_views.index_page', page=page, q=q, sort_by = sort_by))